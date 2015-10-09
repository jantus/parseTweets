# parseTweets
Tweet parser built on Celery, RabbitMQ with a Flask API as frontend. Developed for the Applied Cloud Computing fall 2015 class at Uppsala University.

## Program flow
When running the main.py a parse_tweets task started to run asynchronously on the celery worker. 


## Running the script
1. Start a RabbitMQ server by runnig rabbitmq-server. If rabbitmq is not installed, go ahead and install it
```
$ rabbitmq-server
```

2. Start a celery worker that can run the celeryapp. If celery is not installed, go ahead and install it
```
$ celery -A celeryapp.celeryapp worker --loglevel=info
```

3. Run the main.py script. Open the browser at localhost:5000 and amaze over the out put
```
$ python main.py
```
	