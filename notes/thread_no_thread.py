"""Module contains an example of the distinction between no thread/thread in Python."""
import threading
import time
import logging
import cProfile


def long_task() -> None:
    """Long task."""
    logging.info("Starting long task.")
    time.sleep(2)
    logging.info("Ending long task")


def without_thread() -> None:
    """Example function without threading."""

    logging.info("Starting program.")

    logging.info("No threading - run method directly.")

    long_task()

    logging.info("Stopping program.")


def with_thread() -> None:
    """Example function with threading."""

    logging.info("Starting program.")

    thread = threading.Thread(target=long_task)

    logging.info("Starting thread.")
    thread.start()

    logging.info("Waiting for thread to finish.")

    logging.info("Stopping program.")


def setup_logging() -> None:
    """Sets up logging."""
    logging.basicConfig(format="%(asctime)s: %(message)s",
                        level=logging.INFO,
                        datefmt="%H:%M:%S")


def main() -> None:
    setup_logging()

    logging.info("Without Threading...")
    without_thread()

    print("")
    time.sleep(4)

    logging.info("With Threading...")
    with_thread()


if __name__ == "__main__":
    main()
