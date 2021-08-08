# A simple use case of threading in Python

Multi-threading allows for tasks to run in the background. This is particularly usefull when there are long tasks.

In this project, we simulated a long database call (taking several seconds). For each call, a thread is launched and handles the processing of the db call, storing the various events on a Queue. One can query for the status of a particular process using the UUID of the initial process, which is also returned to the client. The process disappears from the message queue as soon as the user has read it.

In this way, we ensure that the service can handle several expensive calls to the database whilst serving clients quickly.

## Deployment
Python=3.9
### Local
```
virtualenv venv --python=/path/to/python/3.9
source venv/bin/activate
pip install -r ./requirements/prod.txt
```

## Service API
Please refer to `./http` to get a full list of the routing for this service's API.

