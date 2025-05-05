import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()
import snscrape.modules.twitter as sntwitter
from datetime import datetime
import re

query = 'url:substack.com since:2024-04-01 until:2024-04-30'
limit = 1000

tweets = []
substack_links = {}

for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    if len(tweets) >= limit:
        break

    # Extract all substack URLs in tweet
    urls = re.findall(r'https?://[\w./-]*substack\.com[\w./-]*', tweet.content)
    for url in urls:
        url = url.split('?')[0]  # Clean tracking params
        if url not in substack_links:
            substack_links[url] = {
                "count": 1,
                "likes": tweet.likeCount,
                "retweets": tweet.retweetCount,
                "text_samples": [tweet.content]
            }
        else:
            substack_links[url]["count"] += 1
            substack_links[url]["likes"] += tweet.likeCount
            substack_links[url]["retweets"] += tweet.retweetCount
            substack_links[url]["text_samples"].append(tweet.content)

    tweets.append(tweet)

# Preview top discussed Substack articles
top_links = sorted(substack_links.items(), key=lambda x: x[1]["count"], reverse=True)

for link, data in top_links[:10]:
    print(f"{link} mentioned {data['count']} times, {data['likes']} likes, {data['retweets']} RTs")