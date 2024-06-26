import argparse
from tasks import app

def main(broker_address):
    app.conf.update(broker=f"pyamqp://{broker_address}")

    app.start(argv=["worker"])

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="Sudoku Solver Worker")
    parser.add_argument(
        "-b", "--broker", type=str, help="Broker address", default="guest@localhost"
    )
    args = parser.parse_args()

    main(args.broker)