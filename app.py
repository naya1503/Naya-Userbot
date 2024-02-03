import os

from dotenv import load_dotenv

load_dotenv()

if os.environ.get("HEROKU_API"):
    from heroku3 import from_key

    heroku_api = os.environ.get("HEROKU_API")
    heroku_app_name = os.environ.get("HEROKU_APP_NAME")
    heroku_conn = from_key(heroku_api)
    heroku_app = heroku_conn.apps()[heroku_app_name]
    heroku_config = heroku_app.config()

    redis_url = os.environ.get("REDISCLOUD_URL")
    if redis_url and redis_url.startswith("redis://"):
        redis_url = redis_url.replace("redis://", "", 1)
        redis_uri_password, redis_host = redis_url.split("@")
        redis_uri, redis_password = redis_uri_password.split(":")

        heroku_config["REDIS_URI"] = redis_host
        heroku_config["REDIS_PASSWORD"] = redis_password
