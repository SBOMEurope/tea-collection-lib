#!/usr/bin/env python3

"""TEA collection command line client.

For testing."""

import argparse
import sys


def testcollection(collection: str, debug: bool):
    """Test a single collection file"""

    return True


def main():
    """Run the command line TCP manager."""
    debug = False

    parser = argparse.ArgumentParser(
        description='Tool for the TEA Collections.',
        add_help=False)
    maincommands = parser.add_mutually_exclusive_group()
    maincommands.add_argument('--help', '-h',
                              action="store_true",
                              help='Get help with this command')
    parser.add_argument('-d', '--debug',
                        action="store_true",
                        help='Turn on debug output for developers')
    args = parser.parse_args()
    # Parse and set debug early
    if args.debug:
        debug = True
        print("DEBUG: Debugging enabled.")
    if args.help:
        parser.print_help()
        sys.exit(0)

if __name__ == "__main__":
    main()
