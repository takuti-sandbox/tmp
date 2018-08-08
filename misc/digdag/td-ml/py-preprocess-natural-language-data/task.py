import csv
import json
import os
import re
import time
import tdclient
from collections import OrderedDict


class TitleMappingGenerator(object):
    """Normalize contacts' titles so that they can be used as categorical variables.
    """

    def run(self):
        # load cluster definitions
        with open('resources/cluster_definitions.json') as f:
            self.cluster_definitions = json.loads(f.read(), object_pairs_hook=OrderedDict)

        database = 'takuti'

        td = tdclient.Client(apikey=os.environ['TD_API_KEY'], endpoint=os.environ['TD_API_SERVER'])

        # read original title data
        job = td.query(database, 'select title, words from title', type='presto')
        job.wait()

        titles = {}
        for row in job.result():
            title, words = row
            titles[title] = words

        # categorize & write to a mapping file
        with open('resources/title_mapping.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['time', 'title', 'role', 'job'])
            writer.writeheader()
            t = int(time.time())
            for raw_title, words in titles.items():
                row = self.__categorize(raw_title, words)
                row['time'] = t
                writer.writerow(row)

        table = 'title_mapping'
        try:
            td.table(database, table)
        except tdclient.errors.NotFoundError:
            pass
        else:
            td.delete_table(database, table)
        td.create_log_table(database, table)
        td.import_file(database, table, 'csv', 'resources/title_mapping.csv')

        os.remove('resources/title_mapping.csv')

        # Wait for a while until imported records are fully available on TD
        # console.
        while True:
            job = td.query(database, 'select count(title) from ' + table, type='presto')
            job.wait()
            if not job.error():
                break
            time.sleep(10)

    def __categorize(self, raw_title, words):
        # expand clipped words
        transforms = [
            ('sr', 'senior'),
            ('jr', 'junior'),
            ('ceo', 'chief,executive,officer'),
            ('coo', 'chief,operating,officer'),
            ('cto', 'chief,technology,officer'),
            ('cfo', 'chief,finance,officer'),
            ('cio', 'chief,information,officer'),
            ('cmo', 'chief,marketing,officer'),
            ('vp', 'vice,president'),
            ('assoc', 'associate'),
            ('mgr', 'manager')
        ]
        for src, dst in transforms:
            words = re.sub(src, dst, words)

        role = self.__find_category(words, self.cluster_definitions['role'], 'employee')
        job = self.__find_category(words, self.cluster_definitions['job'], 'others')

        return {'title': raw_title, 'role': role, 'job': job}

    def __find_category(self, words, cat2keywords, default):
        cat = default
        for cat_name, keywords in cat2keywords.items():
            found = [w for w in keywords if w in words]
            if len(found) != 0:
                cat = cat_name
                break
        return cat


if __name__ == '__main__':
    TitleMappingGenerator().run()
