from flask import Flask
from flask_restful import Api
from controllers.users_list import UserList, AuthenticationHandler
from flask import request
from logging.config import dictConfig


app = Flask(__name__)
api = Api(app)


# token check before request
@app.before_request
def before_request(*args, **kwargs):

    url = str(request.path)
    print(url.strip())
    if url != "/login":
        try:
            token = request.headers['token']
            if token:
                app.logger.info("Got token: " + token)
            else:
                app.logger.info("Token not found ")
                return {"msg": "Access denied"}

        except KeyError as e:
            app.logger.error("token not found")
            return {"msg": "Access denied"}


# create routes
api.add_resource(UserList, "/users")
api.add_resource(AuthenticationHandler, "/login")

# server setup
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)


# setup logger
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
