"""
Controller for routes
"""
from flask import jsonify, url_for, abort
from service import app
from service.common import status

COUNTER = {}


@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


@app.route("/")
def index():
    """Returns information abut the service"""
    app.logger.info("Request for Base URL")
    return jsonify(
        status=status.HTTP_200_OK,
        message="Hit Counter Service",
        version="1.0.0",
        url=url_for("list_counters", _external=True),
    )


@app.route("/counters", methods=["GET"])
def list_counters():
    """Lists all counters"""
    app.logger.info("Request to list all counters...")
    counters = [dict(name=k, counter=v) for k, v in COUNTER.items()]
    return jsonify(counters)


@app.route("/counters/<name>", methods=["POST"])
def create_counters(name):
    """Creates a new counter"""
    app.logger.info("Request to Create counter: %s...", name)

    if name in COUNTER:
        return abort(
            status.HTTP_409_CONFLICT,
            f"Counter {name} already exists"
        )

    COUNTER[name] = 0
    location_url = url_for("read_counters", name=name, _external=True)
    return (
        jsonify(name=name, counter=0),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


@app.route("/counters/<name>", methods=["GET"])
def read_counters(name):
    """Reads a single counter"""
    app.logger.info("Request to Read counter: %s...", name)

    if name not in COUNTER:
        return abort(
            status.HTTP_404_NOT_FOUND,
            f"Counter {name
