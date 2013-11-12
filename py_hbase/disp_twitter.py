#!/usr/bin/python

import twitter


twitter_api = twitter.Twitter(domain='api.twitter.com', api_version='1')
#world_woe_id = 1
#world_trends = twitter_api.trends._(world_woe_id)
#twitter_api = twitter.api(consumer_key='consumer_key', consumer_secret='consumer_secret', access_token_key='access_token', access_token_secret='access_token_secret')
world_woe_id = 1
world_trends = twitter_api.trends._(world_woe_id)
print str([ trend['name'] for trend in world_trends()[0]['trends'] ])
#twitter_search = twitter.Twitter(domain='search.twitter.com')
#search_results = []
#for page in range(1,6):
#    search_results.append(twitter_search.search(q="FDA", rpp=100, page=page))


#for result in search_results:
#    print str(result)
#    break
