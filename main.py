from tasks import parse_tweets
from twitterparser import get_twitter_file_names
from twitterparser import create_pronoun_dictionary
from celery import group
import flaskapp 
import random
import worker_vm.server as worker


def get_worker_information():
	information = {}
	worker_results = []
	information["progress"] = "100%"
	information["worker_results"] = worker_results
	
	# calculate total
	total = create_pronoun_dictionary()
	total['file'] = ""
	total_sum = 0
	for key, value in result_dict.iteritems():
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

	'''
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
	'''
	

def main():
	
	tweet_files = get_twitter_file_names()

	result_dict = create_pronoun_dictionary()
	global result_dict
	
	n = 5
	chunks_list = [tweet_files[i:i+n] for i in range(0, len(tweet_files), n)]

	jobs_list = []
	for chunck in chunks_list:
		jobs = group(parse_tweets.s(filename) for filename in chunck)
		res = jobs.apply_async()
		jobs_list.append(res)

	print "Jobs added to the queue"

	worker_name = "joakim-lab3-worker-"
	# Start servers
	for i in range(0, len(jobs_list)):
		print "Starting worker named: ", worker_name+str(i)
		worker.initialize(worker_name+str(i))


	for jobs in jobs_list:
		print "waiting for", jobs, "..."
		result_list = jobs.get()
		for result in result_list:
			for key, value in result[1].iteritems():
				global result_dict
				result_dict[key] += value




	for i in range(0, len(jobs_list)):
		worker.terminate(worker_name+str(i))


	flaskapp.set_function(get_worker_information)
	flaskapp.run_app()

	
	print "Done"

if __name__ == '__main__':
	main()






