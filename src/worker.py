import argparse
from tasks import app
import logging
import uuid

logging.basicConfig(level=logging.INFO, filename="worker.log")
logger = logging.getLogger(__name__)

def main(broker_address, worker_name):
    host = broker_address.split(":")[0]
    if "@" not in host:
        print(f"Running worker with host {host}")
        logger.info(f"Running worker with host {host}")
        app.conf.update(backend=f"redis://{host}:6379/0")

    app.conf.update(broker=f"pyamqp://{broker_address}")

    app.start(argv=["worker", "--loglevel=info", "-n", worker_name])

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="Sudoku Solver Worker")
    parser.add_argument(
        "-b", "--broker", type=str, help="Broker address", default="guest@localhost")
    id = str(uuid.uuid4())
    worker_name = f"worker{id}"
    parser.add_argument(
        "-n", "--name", type=str, help="Worker name", default=worker_name)
    args = parser.parse_args()


    main(args.broker, args.name)