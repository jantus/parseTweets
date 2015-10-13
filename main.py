from celeryapp import parse_tweets
import flaskapp 
import random


def get_worker_information():
	
	task = parse_tweets.AsyncResult(task_id)
	print task.id
	print task.state
	information = {}
	information['state'] = task.state
	information['tweet_file'] = 'None'
	information['progress'] = 'N/A'
	information['function'] = 'None'
	information['tweets'] = 0
	information['han'] = 0
	information['hon'] = 0
	information['det'] = 0
	information['denne'] = 0
	information['den'] = 0
	information['denna'] = 0
	information['hen'] = 0
	information['total'] = 0

	information['han%'] = 0
	information['hon%'] = 0
	information['det%'] = 0
	information['denne%'] = 0
	information['den%'] = 0
	information['denna%'] = 0
	information['hen%'] = 0
	

	if task.state == "WORKING":
		information['state'] = task.state
		information['tweet_file'] = task.info['file']
		information['progress'] = task.info['progress']
		information['function'] = task.info['function']
		if task.info['result']:
			information['tweets'] = task.info['result']['tweets']
			information['han'] = task.info['result']['han']
			information['hon'] = task.info['result']['hon']
			information['det'] = task.info['result']['det']
			information['denne'] = task.info['result']['denne']
			information['den'] = task.info['result']['den']
			information['denna'] = task.info['result']['denna']
			information['hen'] = task.info['result']['hen']
			information['total'] = float(information['han']+
										information['hon']+
										information['det']+
										information['denne']+
										information['den']+
										information['denna']+
										information['hen'])
			if information['total'] > 0:
				information['han%'] = round(information['han']/information['total']*100,2)
				information['hon%'] = round(information['hon']/information['total']*100,2)
				information['det%'] = round(information['det']/information['total']*100,2)
				information['denne%'] = round(information['denne']/information['total']*100,2)
				information['den%'] = round(information['den']/information['total']*100,2)
				information['denna%'] = round(information['denna']/information['total']*100,2)
				information['hen%'] = round(information['hen']/information['total']*100,2)

	elif task.state == "SUCCESS":
		information['state'] = task.state
		information['tweet_file'] = 'None'
		information['progress'] = '100'
		information['function'] = 'None'
		information['tweets'] = task.result['tweets']
		information['han'] = task.result['han']
		information['hon'] = task.result['hon']
		information['det'] = task.result['det']
		information['denne'] = task.result['denne']
		information['den'] = task.result['den']
		information['denna'] = task.result['denna']
		information['hen'] = task.result['hen']
		information['total'] = float(information['han']+
										information['hon']+
										information['det']+
										information['denne']+
										information['den']+
										information['denna']+
										information['hen'])
		if information['total'] > 0:
			information['han%'] = round(information['han']/information['total']*100,2)
			information['hon%'] = round(information['hon']/information['total']*100,2)
			information['det%'] = round(information['det']/information['total']*100,2)
			information['denne%'] = round(information['denne']/information['total']*100,2)
			information['den%'] = round(information['den']/information['total']*100,2)
			information['denna%'] = round(information['denna']/information['total']*100,2)
			information['hen%'] = round(information['hen']/information['total']*100,2)

	information['total'] = int(information['total'])

	return information

	

def main():
	print "Start worker"
	task = parse_tweets.apply_async()
	global task_id
	task_id = task.id

	print "Worker state"
	print task.state
	print task.info

	flaskapp.set_function(get_worker_information)

	flaskapp.run_app()

if __name__ == '__main__':
	main()