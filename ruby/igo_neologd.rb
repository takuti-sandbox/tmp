require 'igo-ruby'

tagger = Igo::Tagger.new('/Users/kitazawa/src/github.com/neologd/mecab-ipadic-neologd/build/mecab-ipadic-2.7.0-20070801-neologd-20170828/ipadic-neologd')

p tagger.wakati('人工知能')
p tagger.wakati('ニコニコ動画')
p tagger.wakati('10日放送の「中居正広のミになる図書館」（テレビ朝日系）で、SMAPの中居正広が、篠原信一の過去の勘違いを明かす一幕があった。')
