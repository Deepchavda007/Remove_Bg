from process import *
from termcolor import colored
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest


###--------------------------------------------------------------------------###


def create_app():
    app = Flask(__name__)
    cors = CORS(app)
    app.config["CORS_HEADERS"] = "Content-Type"

    app.logger = logger

    return app


app = create_app()


###--------------------------------------------------------------------------###


def create_response(status, message, data, code):
    return jsonify({"status": status, "message": message, "data": data}), code

###--------------------------------------------------------------------------###

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    app.logger.error(f"BadRequest: {e.description}")
    return create_response(False, str(e), {}, 400)


@app.errorhandler(500)
def handle_server_error(e):
    app.logger.error("Internal Server Error")
    return create_response(False, "Internal Server Error", {}, 500)


###--------------------------------------------------------------------------###


def handle_request(func):
    try:
        # par = request.json if request.method == "POST" else request.args
        par = request.json
        app.logger.info(colored(par, "cyan"))
        print(colored(f'Input Payload {par}', "cyan"))
        response, status_code = func(par)
        return response, status_code
    except Exception as e:
        log_exception(e)
        return {
            "data": {},
            "status": False,
            "message": f"Error: An error occurred {e}",
        }, 400


###--------------------------------------------------------------------------###
    

@app.route("/remove_bg", methods=["POST"])
@cross_origin()
def chat_route():
    return handle_request(remove_background_and_upload)


###--------------------------------------------------------------------------###


def main():
    # Start the Flask app.
    app.run(host="0.0.0.0", port=8000, debug=False)


###--------------------------------------------------------------------------###


if __name__ == "__main__":
    main()