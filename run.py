#!/usr/bin/env python3
import sys

from envsensing import app, db


def print_help():
    print("Syntax: %s <COMMAND>" % sys.argv[0])
    print(
    """COMMAND:
        run - Start the server.
        create_db - Initialize the database, create all tables.
    """)
    sys.exit(1)


def main():
    if (len(sys.argv) != 2):
        print_help()
    cmd = sys.argv[1]
    if (cmd == 'run'):
        app.run()
    elif (cmd == 'create_db'):
        db.create_all()
        print("done.")
    else:
        print_help()


if __name__ == '__main__':
    main()

