#!/usr/bin/env python3

"""TEA collection command line client.

For testing."""

import argparse
import sys


def testcollection(collection: str, debug: bool):
    """Test a single collection file"""

    return True


def run_base_test(debug: bool):
    """Test creating a collection with artefacts"""
    from tea_collection import collection
    from tea_collection import artefact
    from tea_collection import format

    if debug:
        print("DEBUG: Creating collection\n")
    mycol = collection(debug)
    mycol.init_struct()
    mycol.set_collection_version(12)
    mycol.set_author(
        name="Ford Prefect",
        org="The Heart of Gold, inc",
        email="ford.prefect@hog.example.com")
    mycol.set_product(
        name="Spaceship Mega3000 XL",
        version="23.43.34",
        releasedate="20240423",
        teiid="purl:alsdkfjlaskdfjlaskdfjlöaskdf"
    )

    # Create artefact
    myart = artefact(debug)
    myart.init_struct()
    myart.set_author(
        name="Ford Prefect",
        org="The Heart of Gold, inc",
        email="ford.prefect@hog.example.com")
    myart.set_name("SBOM")
    myart.set_description("CycloneDX SBOM for the software")
    if debug:
        print("DEBUG: Artefact created: {}".format(myart))
    # Add the artefact
    mycol.add_artefact(myart)

    # Create format object for the artefact
    myform = format(debug=debug)
    myform.init_struct()
    myform.set_mediatype("application/cyclonedx")
    myform.set_url(
        "https://product.example.com/stuff.json",
        "https://product.example.com/stuff.sbom.sig")
    myform.set_attributes(hash=None, size=74747474)
    myform.set_attributes(hash="lkasdfjlkasdfj", size=None)
    formid = myart.add_format(myform)

    # Create new format object
    otherform = format(debug=debug)
    otherform.init_struct()
    formid = myart.add_format(otherform)

    # Create new artefact
    newart = artefact(debug)
    newart.init_struct()
    newart.set_name("VEX file")
    mycol.add_artefact(newart)

    print("Collection\n{}\n".format(str(mycol)))
    return True


def main():
    """Run the command line TCP manager."""
    debug = False

    parser = argparse.ArgumentParser(
        description='Tool for the TEA Collections.',
        add_help=False)
    maincommands = parser.add_mutually_exclusive_group()
    parser.add_argument(
        '--help', '-h',
        action="store_true",
        help='Get help with this command')
    parser.add_argument(
        '-d', '--debug',
        action="store_true",
        help='Turn on debug output for developers')
    maincommands.add_argument(
        '--test', '-t',
        action="store_true",
        help='Test run of creating a collection')
    args = parser.parse_args()
    # Parse and set debug early
    if args.debug:
        debug = True
        print("DEBUG: Debugging enabled.")
    if args.help:
        parser.print_help()
        sys.exit(0)
    if args.test:
        run_base_test(debug)

    print("--Done.")


if __name__ == "__main__":
    main()
