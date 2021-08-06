"""Module contains Database handler logic"""
from queue import Queue, Empty
import time
from threading import Thread
import logging
from copy import deepcopy
from uuid import uuid4, UUID
from typing import Optional

from domain_objects import DBRequest, Status, DbResponse
from data import COUNTRIES


class DBHandler:

    def __init__(self) -> None:
        self.__db = DB()

    def get_data(self, request: dict[str, str]) -> DbResponse:
        """Gets data from DB - simulation"""
        country = request.get('country')
        logging.info(f"Retrieving data from DB for {country}")

        event_id = uuid4()
        db_request = self.__db.lookup(event_id, country)

        if db_request.data is None:
            logging.info(f"Cache miss. Started retrieiving value "
                         f"for country {db_request.parameter} "
                         f"for event {str(db_request.event_id)}.")
        else:

            logging.info(f"Cache hit. Retrieved value {db_request.data} "
                         f"for country {db_request.parameter} "
                         f"for event {str(db_request.event_id)}.")

        return DbResponse(event_id=event_id,
                          request=db_request.parameter,
                          status=db_request.status,
                          data=db_request.data)

    def get_status(self, event_id: Optional[str]) -> DbResponse:

        db_request = self.__db.get_status(UUID(event_id))

        return DbResponse(event_id=event_id,
                          request=db_request.parameter,
                          status=db_request.status,
                          data=db_request.data)


class DB:

    def __init__(self) -> None:
        self.__event_queue = Queue()
        self.__workers = set()
        self.__current_processes = {}
        self.__cache = {}  # TODO implement.

    def lookup(self, event_id: uuid4, country: str) -> DBRequest:
        logging.debug(f"DB lookup for param {country} for event_id {event_id}.")
        self.__reduce_queue()

        # TODO add cache check here

        # Cache miss so dispatch
        return self.__dispatch_lookup_worker(event_id, country)

    def get_status(self, event_id: uuid4) -> Optional[DBRequest]:
        self.__reduce_queue()
        db_request = self.__current_processes.get(event_id)

        if db_request is None:
            return DBRequest(event_id=event_id,
                             parameter=None,
                             status=Status.NOT_FOUND,
                             data=None)

        if db_request.status == Status.FINISHED:
            self.__current_processes.pop(event_id)

        return db_request

    def __dispatch_lookup_worker(self, event_id: uuid4, country: str) -> DBRequest:

        db_request = DBRequest(event_id=event_id, parameter=country, status=Status.IN_PROGRESS)
        worker = Thread(target=self.__lookup_db, kwargs={'db_request': deepcopy(db_request)})
        worker.start()

        self.__workers.add(worker)

        return db_request

    def __lookup_db(self, **kwargs) -> None:
        db_request = kwargs.get('db_request')
        logging.debug(f"Thread looks up value "
                      f"for parameter {db_request.parameter} for event_id {db_request.event_id}.")

        self.__event_queue.put(db_request)

        time.sleep(10)

        value = COUNTRIES.get(db_request.parameter)
        self.__event_queue.put(DBRequest(event_id=db_request.event_id,
                                         parameter=db_request.parameter,
                                         status=Status.FINISHED,
                                         data=value))
        logging.debug(f"Thread found value {value} "
                      f"for paramter {db_request.parameter} for event_id {db_request.event_id}.")

    def __reduce_queue(self):
        logging.debug("Reducing queue.")
        try:
            event = self.__event_queue.get_nowait()
            while event is not None:
                self.__current_processes[event.event_id] = event
                event = self.__event_queue.get_nowait()
        except Empty:
            pass

        self.__workers = {w for w in self.__workers if w.is_alive()}
