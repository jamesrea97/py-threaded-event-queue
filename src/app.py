"""Module contains service app logic"""
import os

from flask import Flask
from flask import request

from db_handler import DatabaseHandler

app = Flask(__name__)
db_handler = DatabaseHandler()


@app.route("/db/<id>", methods=["GET", "POST"])
def db(id_):
    if request.method == "POST":
        return db_handler.get_data(request.json)

    if id_ is not None:
        return db_handler.get_status(id_)
    return db_handler.get_status()


def main():
    app.run(host=os.getenv("HOST", "0.0.0.0"), port=os.getenv("PORT", 8080))


if __name__ == "__name__":
    main()
