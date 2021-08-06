"""Module contains an example of thead locks in Python."""
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
import time

import logging


class DB:

    def __init__(self) -> None:
        self.__state = 0
        self.__lock = Lock()

    def reset(self) -> None:
        """Resets DB to initial state"""
        self.__state = 0

    def __update(self, value) -> None:
        """Race condition update - caused by sleep."""
        local = self.__state
        local += value
        time.sleep(1)
        self.__state = local

    def no_lock_update(self, value: int) -> None:
        """Updae state with Race Condition - i.e. not thread safe."""
        logging.info(f"Starting updating state from {self.__state} to {value + self.__state}.")

        self.__update(value)

        logging.info(f"Ending updating: current state = {self.__state}.")

    def lock_update(self, value: int) -> None:
        """Update state without Race Condition - i.e. thread safe."""

        with self.__lock:
            logging.info(f"Starting updating state from {self.__state} to {value + self.__state}.")

            self.__update(value)

            logging.info(f"Ending updating:: current state = {self.__state}.")


def setup_logging() -> None:
    """Sets up logging."""
    logging.basicConfig(format="%(asctime)s: %(message)s",
                        level=logging.INFO,
                        datefmt="%H:%M:%S")


def main() -> None:
    setup_logging()

    db = DB()

    logging.info("Updating DB state without lock.")
    with ThreadPoolExecutor(max_workers=3) as executor:
        for index in range(1, 3):
            executor.submit(db.no_lock_update, index)

    print("")
    time.sleep(0.5)

    db.reset()

    logging.info("Updating DB state with lock.")
    with ThreadPoolExecutor(max_workers=3) as executor:
        for index in range(1, 3):
            executor.submit(db.lock_update, index)


if __name__ == "__main__":
    main()
