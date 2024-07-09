import argparse
from tasks import app
import logging
import uuid

logging.basicConfig(level=logging.INFO, filename="worker.log")
logger = logging.getLogger(__name__)

def main(broker_address, worker_name, concurrency=None, autoscale=None):
    host = broker_address.split(":")[0]
    if "@" not in host:
        print(f"Running worker with host {host}")
        logger.info(f"Running worker with host {host}")
        app.conf.update(backend=f"redis://{host}:6379/0")

    app.conf.update(broker=f"pyamqp://{broker_address}")

    argv=["worker", "--loglevel=info", "-n", worker_name]
    if concurrency:
        argv.extend(["-c", str(concurrency)])
        
    if autoscale:
        argv.extend(["--autoscale", autoscale ])

    print(f"Broker and redis set to {app.conf.broker}")

    app.start(argv)

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="Sudoku Solver Worker")
    parser.add_argument(
        "-b", "--broker", type=str, help="Broker address", default="guest@localhost")

    parser.add_argument(
        "-n", "--name", type=str, help="Worker name", default=f"worker{uuid.uuid4()}")
    
    parser.add_argument(
        "-c", "--concurrency", type=int, help="Worker concurrency")
    
    # add auto scaling
    parser.add_argument(
        "-a", "--autoscale", type=str, help="Worker autoscale: max,min")
    
    args = parser.parse_args()

    # call main with concurrency and autoscale if provided, dont add them to the args if they are None
    main(args.broker, args.name, concurrency=args.concurrency, autoscale=args.autoscale)