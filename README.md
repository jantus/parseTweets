# parseTweets
Tweet parser built on Celery, RabbitMQ with a Flask API as frontend.

## Program flow
main.py gives a task to a celery worker


## Running the script
1. Start a RabbitMQ server by runnig rabbitmq-server. If rabbitmq is not installed, go ahead and install it.
```
$ rabbitmq-server
```

2. Start a celery worker that can run the celeryapp.
```
$ celery -A celeryapp.celeryapp worker --loglevel=info
```

3. run the main.py script. Open the browser at localhost:5000 and amaze over the out put.
```
$ python main.py
```
