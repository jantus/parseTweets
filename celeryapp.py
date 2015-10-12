from celery import Celery
import twitterparser as twitter

celeryapp = Celery('tasks', backend='amqp', broker='amqp://')


def start_worker(): 
	print "Start worker"
	task = parse_tweets.apply_async()
	return task.id 

@celeryapp.task(bind=True)
def parse_tweets(self):
	print "Start parsing tweets"
	self.update_state(state='WORKING', meta={'file': None, 'function': None, 'progress': 0, 'result': None})

	self.update_state(state='WORKING', meta={'file': None, 'function': "get_twitter_file_names()", 'progress': 0, 'result': None})
	filename_list = twitter.get_twitter_file_names()

	
	self.update_state(state='WORKING', meta={'file': None, 'function': "create_pronoun_dictionary()", 'progress': 0, 'result': None})
	pronoun_dictionary = twitter.create_pronoun_dictionary()

	iterator = 0
	list_size = float(len(filename_list))
	for filename in filename_list:
		# get twitter file
		self.update_state(state='WORKING', meta={	'file': filename, 'function': "get_twitter_file()", 
													'progress': iterator/list_size, 'result': pronoun_dictionary})
		
		tweet_file = twitter.get_twitter_file(filename)

		# add local dictionary of pronouns to large dictionary of pronouns
		self.update_state(state='WORKING', meta={	'file': filename, 'function': "parse_tweetfile()", 
													'progress': iterator/list_size, 'result': pronoun_dictionary})
		pronoun_dictionary = twitter.parse_tweetfile(tweet_file, pronoun_dictionary)

		iterator += 1



	return pronoun_dictionary

