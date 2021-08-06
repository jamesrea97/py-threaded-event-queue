"""Module contains service app logic"""
import os
import logging

from flask import Flask
from flask import request
from flask import jsonify
from werkzeug.exceptions import BadRequest

from db_handler import DBHandler

app = Flask(__name__)
db_handler = DBHandler()

# @app.route('/db', defaults={'event_id': None},  methods=["GET", "POST"])


@app.route('/db',  methods=["GET", "POST"])
def db():
    """Retrieves data/status of retrieval from DB."""
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


def main():
    setup_logging()

    app.run(host=os.getenv("HOST", "0.0.0.0"), port=os.getenv("PORT", 8080))


if __name__ == "__main__":
    main()
