import simplejson as json
import re
import urllib2
import unicodedata
import time


base_url = 'http://smog.uppmax.uu.se:8080/swift/v1/tweets/'


# returns dictionary of pronouns
def create_pronoun_dictionary():
	return {"tweets":0, "han":0, "hon":0, "den":0, "det":0, "denna":0, "denne":0, "hen":0}

# returns a list of all filenames containing tweets
def get_twitter_file_names():
	request = urllib2.Request(base_url)
	filename_list = urllib2.urlopen(request).read().split('\n')
	return filename_list

# returns a string of all tweets
def get_twitter_file(filename):
	base_url = 'http://smog.uppmax.uu.se:8080/swift/v1/tweets/'
	request = urllib2.Request(base_url+filename)
	twitter_file = urllib2.urlopen(request).read()
	return twitter_file


# Takes a String of tweets and a dictionary to store the values.
def parse_tweetfile(tweet_file, pronoun_dictionary):
	tweet_list = tweet_file.split('\r\n\n')
	pronoun_list = [("han", re.compile(ur"\b(han)\b")), 
					("hon", re.compile(ur"\b(hon)\b")), 
					("den", re.compile(ur"\b(den)\b")), 
					("det", re.compile(ur"\b(det)\b")), 
					("denna", re.compile(ur"\b(denna)\b")), 
					("denne", re.compile(ur"\b(denne)\b")), 
					("hen", re.compile(ur"\b(hen)\b"))]

	for tweet in tweet_list: 
		try:
			json_tweet = json.loads(tweet)
		except:
			print "tweet is not json"
			continue
		
		if json_tweet["retweeted"]:
			#print "tweet is a retweet"
			continue

		
		try:
			#Retweets can be distinguished from typical Tweets by the existence of a retweeted_status attribute.
			json_tweet["retweeted_status"]
			#print "tweet is a retweet"
			continue
		except:
			pass


		if not json_tweet["in_reply_to_status_id"] == None:
			#Nullable. If the represented Tweet is a reply, 
			#this field will contain the integer representation of the original Tweet's ID.
			#print "tweet is a reply"
			continue
		

		for pronoun, p in pronoun_list:
			pronoun_dictionary[pronoun] += len(re.findall(p, json_tweet["text"].lower()))

		pronoun_dictionary["tweets"] += 1

	return pronoun_dictionary		

