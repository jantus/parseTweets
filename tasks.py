from celery import Celery
import twitterparser as twitter

app = Celery('tasks', backend='amqp', broker='amqp://antus:antusantus@130.238.29.29/vhost_antus')

@app.task(bind=True)
def parse_tweets(self, filename):
	print "Start parsing tweets"

	self.update_state(state='WORKING', meta={'file': None, 'function': "create_pronoun_dictionary()", 'result': None})
	pronoun_dictionary = twitter.create_pronoun_dictionary()

	
	# get twitter file
	self.update_state(state='WORKING', meta={	'file': filename, 'function': "get_twitter_file()", 'result': pronoun_dictionary})
	
	# downloading the file and save it as a string
	
	print "downloading ", filename
	tweet_file = twitter.get_twitter_file(filename)

	print "parsing tweetfile:", filename
	# add local dictionary of pronouns to large dictionary of pronouns
	self.update_state(state='WORKING', meta={	'file': filename, 'function': "parse_tweetfile()", 'result': pronoun_dictionary})
	pronoun_dictionary = twitter.parse_tweetfile(tweet_file, pronoun_dictionary)

	print "Worker done", filename, pronoun_dictionary
	return (filename, pronoun_dictionary)

