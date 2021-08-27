"""Module contains service app logic"""
import os
import logging

from flask import Flask
from flask import request
from flask import jsonify
from werkzeug.exceptions import BadRequest

from db_handler import DBHandler
from dotenv import load_dotenv

app = Flask(__name__)
db_handler = DBHandler()


@app.route('/db',  methods=["GET", "POST"])
def db():
    """Retrieves data from DB (POST) or status of DB request(GET)."""
    if request.method == "POST":
        return jsonify(db_handler.get_data(request.json).to_json())

    event_id = request.args.get('event_id')
    if event_id is not None:
        return jsonify(db_handler.get_status(event_id).to_json())
    return 404, BadRequest


def setup_logging() -> None:
    """Sets up logging."""
    log_level = os.getenv("LOG_LEVEL", logging.INFO)
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s",
                        level=log_level,
                        datefmt="%H:%M:%S")


def start():
    app.run(host=os.getenv("HOST", "0.0.0.0"), port=os.getenv("PORT", 8080))


def main():
    """Main driver for service."""
    load_dotenv('.env')
    setup_logging()

    start()


if __name__ == "__main__":
    main()
