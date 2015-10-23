from tasks import parse_tweets
from twitterparser import get_twitter_file_names
from twitterparser import create_pronoun_dictionary
from celery import group
import flaskapp 
import random
import worker_vm.server as worker
import time


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
	result_array = []
	global result_array
	result_array = []


	###########################################################################
	#	Add tasks
	###########################################################################
	init_time = time.time()
	start_time = time.time()
	jobs_list = []
	for filename in tweet_files:
		print "Create task for  file", filename
		result = parse_tweets.delay(filename)
		global result_array
		result_array.append(result)
	end_time = time.time()
	print "Created "+str(len(tweet_files))+" tasks in "+str(end_time-start_time)+" seconds"
	

	###########################################################################
	#	Add workers
	###########################################################################
	num_workers = 2
	worker_name = "joakim-lab3-worker-"
	start_time = time.time()
	# Start servers
	for i in num_workers:
		print "Starting worker named: ", worker_name+str(i)
		worker.initialize(worker_name+str(i))
	end_time = time.time()
	print "Created "+str(num_workers)+" workers in "+str(end_time-start_time)+" seconds"

	###########################################################################
	#	waiting for result
	###########################################################################
	start_time = time.time()
	while true:
		time.sleep(10)
		all_done = 0
		for result in result_array:
			if result.ready() == True:
				all_done += 1
		print str(all_done) + " out of "+str(len(result_array))+" tasks are done"
		if all_done == len(result_array):
			break

	for result in result_array:
		data = result.get()
		for key, value in data.iteritems():
			result_dict[key] += value
	end_time = time.time()
	print "Waiting for "+str(len(result_array))+" results in "+str(end_time-start_time)+" seconds"

	###########################################################################
	#	Terminate workers
	###########################################################################
	start_time = time.time()
	for i in range(0, len(jobs_list)):
		worker.terminate(worker_name+str(i))
	end_time = time.time()
	print "Terminting  "+str(len(result_array))+" workers in "+str(end_time-start_time)+" seconds"

	###########################################################################
	#	Start Flask App
	###########################################################################

	print "total execution time: " + time.time()-init_time
	flaskapp.set_function(get_worker_information)
	flaskapp.run_app()

	
	print "Done"

if __name__ == '__main__':
	main()






