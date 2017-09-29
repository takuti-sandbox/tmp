"""https://github.com/apache/incubator-hivemall/blob/master/core/src/main/java/hivemall/tools/text/SingularizeUDF.java
"""

import re

prepositions = set(['about', 'above', 'across', 'after',
                    'among', 'around', 'at', 'athwart', 'before', 'behind', 'below', 'beneath', 'beside',
                    'besides', 'between', 'betwixt', 'beyond', 'but', 'by', 'during', 'except', 'for',
                    'from', 'in', 'into', 'near', 'of', 'off', 'on', 'onto', 'out', 'over', 'since',
                    'till', 'to', 'under', 'until', 'unto', 'upon', 'with'])

unchanged = set(['advice', 'bison', 'bread', 'bream',
                 'breeches', 'britches', 'butter', 'carp', 'chassis', 'cheese', 'christmas', 'clippers',
                 'cod', 'contretemps', 'corps', 'debris', 'diabetes', 'djinn', 'eland', 'electricity',
                 'elk', 'equipment', 'flounder', 'fruit', 'furniture', 'gallows', 'garbage', 'georgia',
                 'graffiti', 'gravel', 'happiness', 'headquarters', 'herpes', 'high-jinks', 'homework',
                 'information', 'innings', 'jackanapes', 'ketchup', 'knowledge', 'love', 'luggage',
                 'mackerel', 'mathematics', 'mayonnaise', 'measles', 'meat', 'mews', 'mumps', 'mustard',
                 'news', 'news', 'pincers', 'pliers', 'proceedings', 'progress', 'rabies', 'research',
                 'rice', 'salmon', 'sand', 'scissors', 'series', 'shears', 'software', 'species',
                 'swine', 'swiss', 'trout', 'tuna', 'understanding', 'water', 'whiting', 'wildebeest'])

irregular = {
    'atlantes': 'atlas',
    'atlases': 'atlas',
    'axes': 'axe',
    'beeves': 'beef',
    'brethren': 'brother',
    'children': 'child',
    'corpora': 'corpus',
    'corpuses': 'corpus',
    'ephemerides': 'ephemeris',
    'feet': 'foot',
    'ganglia': 'ganglion',
    'geese': 'goose',
    'genera': 'genus',
    'genii': 'genie',
    'graffiti': 'graffito',
    'helves': 'helve',
    'kine': 'cow',
    'leaves': 'leaf',
    'loaves': 'loaf',
    'men': 'man',
    'mongooses': 'mongoose',
    'monies': 'money',
    'moves': 'move',
    'mythoi': 'mythos',
    'numena': 'numen',
    'occipita': 'occiput',
    'octopodes': 'octopus',
    'opera': 'opus',
    'opuses': 'opus',
    'our': 'my',
    'oxen': 'ox',
    'penes': 'penis',
    'penises': 'penis',
    'people': 'person',
    'sexes': 'sex',
    'soliloquies': 'soliloquy',
    'teeth': 'tooth',
    'testes': 'testis',
    'trilbys': 'trilby',
    'turves': 'turf',
    'zoa': 'zoon'
}

# regexp1, replacement1, regexp2, replacement2, ...
rules = [(re.compile('(quiz)zes$'), '$1'),
         (re.compile('(matr)ices$'), '$1ix'),
         (re.compile('(vert|ind)ices$'), '$1ex'),
         (re.compile('^(ox)en'), '$1'),
         (re.compile('(alias|status)$'), '$1'),
         (re.compile('(alias|status)es$'), '$1'),
         (re.compile('(octop|vir)us$'), '$1us'),
         (re.compile('(octop|vir)i$'), '$1us'),
         (re.compile('(cris|ax|test)es$'), '$1is'),
         (re.compile('(cris|ax|test)is$'), '$1is'),
         (re.compile('(shoe)s$'), '$1'),
         (re.compile('(o)es$'), '$1'),
         (re.compile('(bus)es$'), '$1'),
         (re.compile('([m|l])ice$'), '$1ouse'),
         (re.compile('(x|ch|ss|sh)es$'), '$1'),
         (re.compile('(m)ovies$'), '$1ovie'),
         (re.compile('(s)eries$'), '$1eries'),
         (re.compile('([^aeiouy]|qu)ies$'), '$1y'),
         (re.compile('([lr])ves$'), '$1f'),
         (re.compile('(tive)s$'), '$1'),
         (re.compile('(hive)s$'), '$1'),
         (re.compile('([^f])ves$'), '$1fe'),
         (re.compile('(^analy)sis$'), '$1sis'),
         (re.compile('(^analy)ses$'), '$1sis'),
         (re.compile('((a)naly|(b)a|(d)iagno|(p)arenthe|(p)rogno|(s)ynop|(t)he)ses$'), '$1$2sis'),
         (re.compile('([ti])a$'), '$1um'),
         (re.compile('(n)ews$'), '$1ews'),
         (re.compile('(s|si|u)s$'), '$1s'),
         (re.compile('s$'), '')]


def singularize(word):
    if word is None:
        return None

    if not word:  # empty
        return word

    if word in unchanged:
        return word

    if '-' in word:  # compound words (e.g., mothers-in-law)
        chunks = word.split('-')
        if len(chunks) > 1 and chunks[1] in prepositions:
            return singularize(chunks[0]) + '-' + '-'.join(chunks[1:])

    if word[-1] == "'":
        return singularize(word[:len(word) - 1]) + "'s"

    if word in irregular:
        return irregular[word]

    for suffix, inflection in range(0, len(rules), 2):
        m = suffix.search(word)
        g = m and m.groups() or []
        if m:
            for k in range(len(g)):
                if g[k] is None:
                    inflection = inflection.replace('\\' + str(k + 1), '')
            return suffix.sub(inflection, word)

    return word
