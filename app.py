# app.py

import sys
from functions.say_hi_dev import say_hi_dev
from functions.say_hi_prod import say_hi_prod


def main():
    if len(sys.argv) < 2:
        print("Usage: python app.py [prod|dev]")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "prod":
        print(say_hi_prod())
    elif mode == "dev":
        print(say_hi_dev())
    else:
        print("Unknown mode. Use 'prod' or 'dev'.")


if __name__ == "__main__":
    main()
