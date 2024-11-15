#!/usr/bin/env python3

"""TEA collection command line client.

For testing."""

import argparse
import sys


def generate_hash_sha256(stuff, debug):
    """Generate a hash of stuff."""
    import hashlib
    m = hashlib.sha256()
    m.update(stuff)
    dig = m.hexdigest()
    if debug:
        print("DEBUG: digest: {}".format(dig))
    return dig


def test_file_exists(filename: str, debug=False) -> bool:
    """Check if file exists."""
    from pathlib import Path
    from os import path

    if filename is None or filename == "":
        if debug:
            print("ERROR: File name not given (None)")
        return False

    if path.exists(filename) is False:
        if debug:
            print("ERROR: File does not exist: {}".format(filename))
        return False

    if path.isfile(filename) is False:
        if debug:
            print(
                "ERROR: File is not a regular file: {}"
                .format(filename))
        return False

    # non zero size
    if Path(filename).stat().st_size == 0:
        if debug:
            print("ERROR: File is empty: {}".format(filename))
        return False
    if debug:
        print("DEBUG: File exists and is not empty: {}".format(filename))

    return True


# Read file as buffer
def getfile(filename: str, debug: bool):
    filehandle = open(filename, "r")
    filetext = filehandle.read()
    filehandle.close()
    return filetext


def run_base_test(debug: bool):
    """Test creating a collection with artefacts"""
    from tea_collection import tea_collection
    from tea_collection import artefact
    from tea_collection import format

    if debug:
        print("DEBUG: Creating collection\n")
    mycol = tea_collection(debug=debug)
    mycol.set_version(12)
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
    myform.set_mediatype("application/cyclonedx")
    myform.set_url(
        "https://product.example.com/stuff.json",
        "https://product.example.com/stuff.sbom.sig")
    myform.set_attributes(hash=None, size=74747474)
    myhash = generate_hash_sha256(
        stuff=str.encode(myform.format["uuid"]),
        debug=debug)
    myform.set_attributes(hash=myhash, size=None)
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

    error, errmsg = mycol.is_valid()
    if error > 0:
        print("Collection not valid:\n{}".format(errmsg))
        return False
    print("Collection\n{}\n".format(str(mycol)))
    return True

# {'tcoFormat': 'TEA-collection',
# 'specVersion': '1.0',
# 'UUID': 'cf4cb929-8e14-4a13-9ae8-22c3f9c216d6',
# 'product_name': 'Spaceship Mega3000 XL',
# 'product_version': '23.43.34',
# 'product_release_date': '20240423',
# 'product_tei_id': 'purl:alsdkfjlaskdfjlaskdfjlöaskdf',
# 'version': 12,
# 'author_name': 'Ford Prefect',
# 'author_org': 'The Heart of Gold, inc',
# 'author_email': 'ford.prefect@hog.example.com',
# 'artefacts': [
#   {'uuid': 'cde71066-db8f-4b5e-a26c-71cc3b04ec69',
#   'name': 'SBOM',
#   'description': 'CycloneDX SBOM for the software',
#   'author_name': 'Ford Prefect',
#   'author_org': 'The Heart of Gold, inc',
#   'author_email': 'ford.prefect@hog.example.com',
#   'formats': [
#       {'uuid': '320130b6-e64f-472b-b115-134dadcee218',
#       'bom-identifier': None,
#       'mediatype': 'application/cyclonedx',
#       'category': None,
#       'url': 'https://product.example.com/stuff.json',
#       'sigurl': 'https://product.example.com/stuff.sbom.sig',
#       'hash': 'lkasdfjlkasdfj', 'size': 74747474},
#       {'uuid': '9f86d936-20e7-44c1-9643-c0383f412ce2',
#       'bom-identifier': None, 'mediatype': None,
#       'category': None,
#       'url': None,
#       'sigurl': None,
#       'hash': None,
#        'size': 0}]},
#     {'uuid': '1d10caf0-3a18-413d-9b59-5e2a97977301',
#      'name': 'VEX file',
#       'description': None,
#       'author_name': None,
#       'author_org': None,
#       'author_email': None,
#       'formats': []}]}


def check_if_in_dict(thisdict, key, debug):
    """Check if key is in dict"""
    if not isinstance(thisdict, dict):
        print("ERROR: check_if_in_dict: Not a dict.")
        if debug:
            print("DEBUG: No dict={}".format(thisdict))
        return 1, list("Not a dict")

    if key not in thisdict.keys():
        return 1, list("Key {} missing".format(key))
    return 0, None


def check_artefact(tco, thisart: dict, debug):
    """Check artefact syntax.

    Add artefact to object if ok."""
    from tea_collection import artefact

    if debug:
        print("DEBUG: *** check_artefact: {}".format(thisart["name"]))
    myart = artefact(debug=debug)
    errors = 0
    errmsg = list()

    keylist = myart.get_keylist()
    # Check if all required keys are in the object
    for key in keylist:
        newerr, newmsg = check_if_in_dict(thisart, key, debug)
        if newerr > 0:
            errors += newerr
            errmsg += newmsg
        res = myart.set_attr_value(key, thisart[key])
        if res is False:
            errors += 1
            errmsg.append("artefact: Failed to set values")

    # Check if artefact is valid
    newerr, newmsg = myart.is_valid()
    errors += newerr
    errmsg += newmsg

    if errors == 0:
        # Add artefact
        if not tco.add_artefact(myart):
            errors += 1
            errmsg.append("Error adding artefact to collection")
    return myart, errors, errmsg


def check_format(art, thisformat: dict, debug):
    """Check format syntax.

    Add artefact to artefact object if ok."""
    from tea_collection import format

    myformat = format(debug=debug)
    errors = 0
    errmsg = list()

    keylist = myformat.get_keylist()
    # Check if all required keys are in the object
    for key in keylist:
        newerr, newmsg = check_if_in_dict(thisformat, key, debug)
        if newerr > 0:
            errors += newerr
            errmsg += newmsg
        if key == "uuid":
            # uuid can't be None
            if thisformat[key] is None or thisformat[key] == "":
                errors += 1
                errmsg.append("artefact: uuid not defined")
            else:
                myformat.replace_uuid(thisformat[key])
        elif key == "bom-identifier":
            myformat.set_bomidentifier(thisformat[key])
        elif key == "mediatype":
            myformat.set_mediatype(thisformat[key])
        elif key == "category":
            myformat.set_category(thisformat[key])
        elif key == "url":
            myformat.set_url(thisformat[key], None)
        elif key == "sigurl":
            myformat.set_url(None, thisformat[key])
        elif key == "hash":
            myformat.set_hash(thisformat[key])
        elif key == "size":
            myformat.set_size(thisformat[key])
        else:
            print("Unknown key: {}".format(key))

    # Check if the format is valid
    newerr, newmsg = myformat.is_valid()
    errors += newerr
    errmsg += newmsg

    # Add other keys to check
    if errors == 0:
        # Add artefact
        if not art.add_format(myformat):
            errors += 1
            errmsg.append("Error adding format to collection")
    return errors, errmsg


def traversedict(tco, art, thisdict: dict, thiskey: str, debug):
    """Traverse a collection object to check syntax."""

    if debug and thiskey is not None:
        print("DEBUG: *** Checking dict {}".format(thiskey))
    errors = 0
    errdict = list()
    thisart = None
    for key in thisdict.keys():
        if debug:
            print("DEBUG: Checking key: {}".format(key))
        if not tco.check_key(key):
            errors += 1
            errdict.append("Not a known key: {}".format(key))
        if isinstance(thisdict[key], dict):
            newerr, newdict = traversedict(
                tco=tco,
                thisdict=thisdict[key],
                thiskey=key,
                debug=debug)
            errors += newerr
            errdict += newdict
        elif isinstance(thisdict[key], list):
            if debug:
                print("DEBUG: Going throught list named {}".format(key))
            for stuff in thisdict[key]:
                if debug:
                    print("DEBUG: Checking list object: {}".format(stuff))
                # Add object if it's an artefact
                if key == "artefacts":
                    thisart, newerr, newdict = check_artefact(
                        tco=tco, thisart=stuff, debug=debug)
                    errors += newerr
                    errdict += newdict
                if key == "formats":
                    if art is None:
                        print("ERROR: Missing ART: {}".format(art))
                        errors += 1
                        errdict.append("Code error. missing ART")
                    else:
                        newerr, newdict = check_format(
                            art=art, thisformat=stuff, debug=debug)
                        errors += newerr
                        errdict += newdict
                # Traverse the dict
                newerr, newdict = traversedict(
                    tco=tco,
                    art=thisart,
                    thisdict=stuff,
                    thiskey=key,
                    debug=debug)
                errors += newerr
                errdict += newdict
        elif key == "product_name":
            tco.set_product(thisdict[key], None, None, None)
        elif key == "product_version":
            tco.set_product(None, thisdict[key], None, None)
        elif key == "product_release_date":
            tco.set_product(None, None, thisdict[key], None)
        elif key == "product_tei_id":
            tco.set_product(None, None, None, thisdict[key])
        elif key == "version":
            tco.set_version(thisdict[key])
        elif key == "author_name":
            tco.set_author(thisdict[key], None, None)
        elif key == "author_org":
            tco.set_author(None, thisdict[key], None)
        elif key == "author_email":
            tco.set_author(None, None, thisdict[key])
        else:
            if debug:
                print("DEBUG: Unhandled key: {}".format(key))

    if errors > 0:
        print("DEBUG: Errors: {}".format(errors))
    return errors, errdict


def dict2object(colldict, debug: bool):
    """Convert a raw data structure to objects.

    (like input from a json file)
    """
    from tea_collection import tea_collection

    if debug:
        print("DEBUG: dict2object converting data")
    # Create a collection object
    mycol = tea_collection(debug=debug)
    errors = 0
    errmsg = list()

    # Check syntax and add artefacts and formats
    # ERROR: Needs to handle lists
    errors, errmsg = traversedict(
        tco=mycol,
        art=None,
        thisdict=colldict,
        thiskey=None,
        debug=debug)

    # Check for TCOFormat and version
    if "tcoFormat" not in colldict.keys():
        errors += 1
        errmsg.append("No tcoFormat.")
    else:
        if colldict['tcoFormat'] != "TEA-collection":
            errors += 1
            errmsg.append("Not a TEA collection.")
    if "specVersion" not in colldict.keys():
        errors += 1
        errmsg.append("No specVersion.")
    else:
        if colldict['specVersion'] != "1.0":
            errors += 1
            errmsg.append("Not supported specVersion")

    newerr, newmsg = mycol.is_valid()
    errors += newerr
    errmsg += newmsg

    # Handle errors
    if errors > 0:
        print("ERRORS {}:".format(errors))
        for msg in errmsg:
            print("  - {}".format(msg))
        return None
    if debug:
        print("DEBUG: Validated the file ok.")
    return mycol


def validate_collection(
        file: str,
        debug: bool
        ):
    """Read a json file and validate it."""

    import json

    if debug:
        print("DEBUG: Validate file: {}".format(file))
    if not test_file_exists(filename=file, debug=debug):
        print(
            "ERROR: File does not exist: {}"
            .format(file))
        return False
    print("DEBUG: File exists and will be read.")
    colldata = getfile(filename=file, debug=debug)

    try:
        collection = json.loads(colldata)
    except Exception:
        print("ERROR: Failed parsing data file")
        return False

    # We have a data file
    if debug:
        print("DEBUG: Data read: {}".format(collection))
    col = dict2object(
        colldict=collection,
        debug=debug)
    if col is None:
        print("ERROR: Validation failed.")
        return False
    if debug:
        print("DEBUG: Collection\n{}\n".format(str(col)))
    return True


def main():
    """Run the command line TCO manager."""
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
    maincommands.add_argument(
        '--validate', '-v',
        nargs='*',
        type=str,
        action='append',
        help='Validate a collection file. Add filename.')
    args = parser.parse_args()
    # Parse and set debug early
    if args.debug:
        debug = True
        print("DEBUG: Debugging enabled.")
    if args.help:
        parser.print_help()
        sys.exit(0)
    validate = args.validate
    test = args.test

    # If no args are given on command line, print help
    if not validate and not test:
        parser.print_help()
        sys.exit(1)

    if validate and len(validate) > 1:
        print("ERROR: --sign can only be passed once.")
        sys.exit(1)
    elif validate and len(validate[0]) == 0:
        print("ERROR: --validate requires an option.")
        sys.exit(1)
    elif validate:
        # we get a list in a list when using append, we need a string
        collectionfile = validate[0][0]
        print("DEBUG: Validating file: {}".format(collectionfile))
        validate_collection(
            file=collectionfile,
            debug=debug)
        sys.exit(0)
    if args.test:
        run_base_test(debug)

    print("--Done.")


if __name__ == "__main__":
    main()
