## Preparation

```
$ pip install scrapy wordcloud
```

## Get abstracts

```
$ scrapy runspider recsys_spider.py -a yy=17 -o recsys2017.csv
```

## Create wordcloud

```
$ wordcloud_cli.py --text recsys2017.csv --imagefile recsys2017.png --stopwords stopwords.txt
```