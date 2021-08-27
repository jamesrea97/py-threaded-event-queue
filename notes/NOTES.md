# Python Threading Notes

## Python and threads

In Computer Science, a thread is a separate flow of execution.

Although in several languages, thread concurrency exits (e.g. C, Java, Go), Python does not allow for this. 

Python's Global Interpreter Lock (GIL) prevents two threads from running at the same time (as Python's Interpreter only can interpret one flow of execution at a time).

Actual concurrency is achieved through the `multiprocessing` module.

### Running threads

```py
from threading import Thread

def main():
    thread = Thread(target=some_func)

    # Main thread code before
    thread.start() # runs some_func in sepeare thread

    # Main thread executes code

    thread.join()
    # All code here is executed after executioni of some_func in seperate thread
```
Full example: Run `python ./notes/thread_no_thread`.


### The `daemon` flag

In Computer Science, a daemon is a process that runs in the background.

In Python's `threading` module, the `daemon=True` flag means the thread will be killed when the program has terminated. This means that the program will run the thread to completion before terminating. On the other hand `daemon=False` implies that the program stops, letting the daemon thread to run after the program has ended.

For each non-daemonic threads (i.e. not killed when program finishes), Python's `threading.__shutdown()` calls `.join()` so to run the clean up process after the program has ended.

You can use `.join()` to let the thread complete its process at any point to let a thread complete it's task before completing any of the `__main__` process.

```py
from threading import Thread

def main():
    thread_daemon = Thread(target=some_func, daemon=True) # will be killed at the latest when main program terminates
    thread_non_daemon = Thread(target=some_func, daemon=False) # will be killed after main program terminates

    thread_daemon.start()
    thread_non_daemon.start()

    
    # End of main program start
    # kill thread_wihtout_daemon
    # End of program finishes

    # thread_daemon finishes
    # kill thread_daemon - this is not part of the __main__ program
```
Full example: Run `python ./notes/daemon_no_daemon.py`.


### Thread pooling

Often, you would like to run multiple threads at once. 

In Python `concurrent.futures` manages a thread pool through `ThreadPoolExecutor`. This handles the start and end of threads.

```py
import concurrent.futures

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(some_func, range(3))

```
Full example: Run `python ./notes/thread_pooling.py`.


### Race conditions and Locks

Suppose that two threads update state at the same time. Then each thread may update the state without taking into consideration the other thread's contribution. 
This is known as a Race Condition. 
In order to prevent Race Conditions, one can create a Mutual Exclusion (MutEx), which allows only one thread to update the state at any one time, preventing undesirable behaviour from occuring. A MutEx can be achieved through a Lock - similar to the GIL stated above.

Python provides the `threading.Lock` class allows for the creation of a Lock.

```py
from threading import Lock, Thread
import time

state = 0
lock = Lock()

def update(i: int) ->None:
    """
    Function contains a Race Condition as second thread A could run state=local while thread B sleeps, 
    prevent thread B from updating most recent state.
    """
    local = i
    time.slepp(0.1)
    state = local

def locked_updaet(i):
    with Lock():
        update(i)

```
Full example: Run `./notes/`



### Queues and threading

A classic example of threading usage in Computer Science is the Producer/Consumer: Suppose you have a set of Producers, producing some load and a set of Consumers consume from the load the Producers produced. How to allow mulitple Producers/Consumres (threads) to produce/consume wihtout causing a Race Condition?

In Python, the `queue.Queue` object is implemented with the thread-safe property.

The `threading.Event` mechanism provides an alternative to `threading.Lock`. `Event` allows threads to signal an event that other threads are waiting for. This can be used when signalling the end of a process for example.

The following sample is a multi-threaded example using `event` and  `Queue`:

```py
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import random
from threading import Event
import time

def producer(queue, event):
    while not event.is_set():
        message = random.randint(1, 101)
        queue.put(message)


def consumer(queue, event):
    while not (event.is_set() and queue.empty()):
        message = queue.get()

def main():

    pipeline = Queue(maxsize=10)
    event = Event()
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, event) # listens on changes of state of event
        executor.submit(consumer, pipeline, event) # listens on changes of state of event

        time.sleep(0.1) # simulating time messages produced/consumed.
        event.set() # no more messages to produce -> signal both producers and consumers.

```

### Additional Notes


```py
import concurrent.futures

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(some_func, *args, **kwargs)

```
`submit` allows you to pass arguemnts to `some_func`.