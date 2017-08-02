```sh
$ python make_jawikicorpus.py resources/jawiki-latest-pages-articles.xml.bz2 output/jawiki
```

- Create Japanese Wikipedia corpus
- Requirement: `jawiki-latest-pages-articles.xml.bz2` must be downloaded from [Index of /jawiki/latest/](https://dumps.wikimedia.org/jawiki/latest/) and placed under *resources/*

```sh
$ python lda.py output/jawiki 100
```

- Create LDA model (1st time)
- Load existing LDA model and display top-5 topic words (2nd time~)

