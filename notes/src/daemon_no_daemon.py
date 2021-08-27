"""Module contains an example of the distinction between no daemon/daemon in Python."""
import threading
import time
import logging


def long_task():
    """Long task."""
    logging.info("Staring long task.")
    time.sleep(2)
    logging.info("Ending long task")


def without_daemon():
    """Example with thread but without daemon."""
    logging.info("Starting program.")

    thread = threading.Thread(target=long_task, daemon=True)

    logging.info("Starting daemonized thread.")
    thread.start()
    # this will finish whatever is running on thread before executing rest.
    # thread.join()

    logging.info("Stopping program.")


def with_daemon():
    """Example function with thread and daemon."""
    logging.info("Starting program.")

    thread = threading.Thread(target=long_task, daemon=False)

    logging.info("Starting non-daemonized thread.")
    thread.start()
    # this will finish whatever is running on thread before executing rest.
    # thread.join()

    logging.info("Stopping program.")


def setup_logging():
    logging.basicConfig(format="%(asctime)s: %(message)s",
                        level=logging.INFO,
                        datefmt="%H:%M:%S")


def main():
    setup_logging()

    logging.info("With daemon...")
    with_daemon()

    time.sleep(4)
    print("")

    logging.info("Without daemon...")
    without_daemon()


if __name__ == "__main__":
    main()
