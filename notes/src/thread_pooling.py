"""Module contains an example of the distinction between no thread/thread in Python."""
from concurrent.futures import ThreadPoolExecutor
import time
import logging


def long_task(i: int) -> None:
    """Long task."""
    logging.info(f"Starting long task - thread: {i}.")
    time.sleep(2)
    logging.info(f"Ending long task - thread: {i}")


def setup_logging() -> None:
    """Sets up logging."""
    logging.basicConfig(format="%(asctime)s: %(message)s",
                        level=logging.INFO,
                        datefmt="%H:%M:%S")


def main() -> None:
    setup_logging()

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(long_task, range(3))


if __name__ == "__main__":
    main()
