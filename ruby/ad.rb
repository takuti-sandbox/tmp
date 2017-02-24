require 'ostruct'

# $model = read_model_from_mysql()
$model = {
  'i0' => 1.0,
  'i1' => 2.0,
  'c1#Ohio' => 3.0,
  'c3#xxx' => 4.0
}
def scoring(i, a)
  features = [
    # [feature, value]
    ['i0', i.user_generation],
    ['i1', i.user_age],
    ["c1##{i.user_address}", 1.0],
    ["c2##{i.user_browser}", 1.0],
    ["c3##{a.ad_id}", 1.0],
    ["c4##{i.publisher_id}", 1.0],
    ["c5##{a.advertiser_id}", 1.0],
    ["c6##{a.campaign_id}", 1.0],
    ["c7##{a.creative_id}", 1.0]
  ]

  # compute weighted sum
  features.inject(0) { |sum, f| sum += ($model[f.first] || 0) * f.last }
end

impression = { # target impression
  'user_generation' => 1,
  'user_age' => 40,
  'user_address' => 'Ohio',
  'user_browser' => 'Firefox',
  'publisher_id' => 'Foo'
}
ads = [ # list of possible ads
  {'ad_id' => 'xxx', 'advertiser_id' => 'aaa', 'campaign_id' => '123', 'creative_id' => '000'},
  {'ad_id' => 'yyy', 'advertiser_id' => 'bbb', 'campaign_id' => '456', 'creative_id' => '111'},
  {'ad_id' => 'zzz', 'advertiser_id' => 'ccc', 'campaign_id' => '789', 'creative_id' => '222'}
]
best_performing_ad = ads.map{|ad| [scoring(OpenStruct.new(impression), OpenStruct.new(ad)), ad['ad_id']]}.sort.last[1]

p best_performing_ad
