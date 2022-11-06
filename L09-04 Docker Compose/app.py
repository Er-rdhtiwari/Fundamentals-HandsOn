import time
import redis
from flask import Flask
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    logger.info(f"--------info------count:{count}")
    logger.debug(f"--------debug------count:{count}")
    logger.critical(f"-------critical-------count:{count}")
    logger.error(f"---------error-----count:{count}")
    return "What's up Docker Deep Divers! You've visited me {} times.\n".format(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
