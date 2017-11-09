## Preparation

```
$ pip install scrapy wordcloud
```

## Get abstracts

```
$ scrapy runspider recsys_spider.py -a yy=17 -o csv/recsys17.csv
```

## Create wordcloud

```
$ wordcloud_cli.py --text csv/recsys17.csv --imagefile png/recsys17.png --stopwords stopwords.txt
```

## At once

```
$ echo 14 15 16 17 | xargs -n 1 -I{} scrapy runspider recsys_spider.py -a yy={} -o out/recsys{}.csv
$ echo 14 15 16 17 | xargs -n 1 -I{} wordcloud_cli.py --text csv/recsys{}.csv --imagefile png/recsys{}.png --stopwords stopwords.txt
```