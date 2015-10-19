from tasks import parse_tweets
from twitterparser import get_twitter_file_names
from twitterparser import create_pronoun_dictionary
import flaskapp 
import random


def get_worker_information():
	information = {}
	worker_results = []
	information["progress"] = 0
	print result_array
	for result in result_array:
		print result.ready()
		if result.ready() == True:
			information["progress"] += 1
			filename, result_dict = result.get()
			result_dict['file'] = filename
			worker_results.append(result_dict)

	information["worker_results"] = worker_results
	information["progress"] = int(round(float(information["progress"]) / float(len(result_array)),2)*100)

	# calculate total
	total = create_pronoun_dictionary()
	total['file'] = ""
	total_sum = 0
	for result in information["worker_results"]:
		for key, value in result.iteritems():
			if key == "file":
				continue
			total[key] += value
			total_sum += value
	total['total'] = total_sum

	# calculate total in percent

	total_percent =  create_pronoun_dictionary()
	total_percent["file"] = ""
	total_percent["total"] = 0
	for key, value in total.iteritems():
		if key == "file":
				continue
		if total['total'] > 0:
			total_percent[key] += round(float(value)/float(total['total']), 2)*100
		else:
			total_percent[key] = 0
	information["total"] = total
	information["total_percent"] = total_percent


	print information
	return information

	

def main():
	
	tweet_files = get_twitter_file_names()

	global result_array
	result_array = []
	
	for filename in tweet_files:
		print "Create task for file", filename
		result = parse_tweets.delay(filename)
		global result_array
		result_array.append(result)

	flaskapp.set_function(get_worker_information)
	flaskapp.run_app()

	
	print "Done"

if __name__ == '__main__':
	main()






