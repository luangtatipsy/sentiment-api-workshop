from flask import Flask, jsonify, request
from http import HTTPStatus
from sentiment import get_sentiment_result
from exception import InvalidUsage

import logging

app = Flask(__name__)

@app.route('/hello')
def hello():
    response = {"message": "Hello Sentiment API"}

    return jsonify(response)


@app.route("/sentiment", methods=["POST"])
def get_sentiment():
    status_code = HTTPStatus.OK
    response = {"status_code": status_code, "results": dict(), "message": ""}
    try:
        text = request.get_json()["text"]
        results = dict()
        results["sentiment"], results["score"] = get_sentiment_result(text)

        response["message"] = text
        response["results"] = results

    except KeyError as error:
        # ex. invalid input field name
        message = f"'{error.args[0]}' key is not found"
        logging.error(f"{message}: {error}")
        raise InvalidUsage(message, status_code=HTTPStatus.BAD_REQUEST)

    except AttributeError as error:
        # ex. Text/Languge should be string
        message = "Input should be string"
        logging.error(f"{message}")
        raise InvalidUsage(message, status_code=HTTPStatus.BAD_REQUEST)

    return jsonify(response), status_code


if __name__ == "__main__":
    app.run(debug=True, port=8204)

