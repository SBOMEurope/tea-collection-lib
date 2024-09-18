"""The TCO - Transparency Exchange Collection - parsing library

(C) Copyright Olle E. Johansson, Edvina AB - oej@edvina.net

SPDX-License-Identifier: BSD
"""


class collection:
    """TEA Collection object handling"""
    debug = False
    name = None
    collection = None
    uuid = None
    # Vocabulary for the full collection, including artefacts and formats
    vocabulary = (
        "tcoFormat",
        "specVersion",
        "UUID",
        "product_name",
        "product_version",
        "product_release_date",
        "product_tei_id",
        "version",
        "author_name",
        "author_org",
        "author_email",
        "artefacts",
        "uuid",
        "name",
        "description",
        "author_name",
        "author_org",
        "author_email",
        "formats",
        "bom-identifier",
        "mediatype",
        "category",
        "url",
        "sigurl",
        "hash",
        "size",
        "bom-identifier",
        "mediatype",
        "category",
        "url",
        "sigurl",
        "hash",
        "size",
        "name",
        "description",
        "author_name",
        "author_org",
        "author_email",
        "formats"
    )

    def __init__(self, debug):
        """Initialise collection object"""
        self.debug = debug
        self.generate_uuid()
        self.init_struct()

    def __str__(self):
        """Return a printable dnsobject in json."""
        import json
        if self.collection is None:
            return "n/a"
        newcol = dict(self.collection)
        artlist = self.collection["artefacts"]
        newcol["artefacts"] = list()
        for art in artlist:
            artstruct = art.get_struct()
            newart = dict(artstruct)
            if self.debug:
                print(
                    "DEBUG: Artefact: {}"
                    .format(str(newart)))
            newart["formats"] = art.get_formats()
            newcol["artefacts"].append(newart)
        return json.dumps(newcol, sort_keys=False, indent=4)

    def generate_uuid(self):
        """Return an UUID v 4."""
        import uuid

        if self.uuid is not None:
            if self.debug:
                print(
                    "DEBUG: Error - Attempting to re-initialise "
                    "collection structure.\n")
            return False
        self.uuid = uuid.uuid4()
        if self.debug:
            print("DEBUG: Generated new UUID: {}".format(str(self.uuid)))
        return True

    def replace_uuid(self, uuidstr: str):
        """Set UUID (from import)."""
        import uuid
        try:
            self.uuid = uuid.UUID(uuidstr)
        except TypeError:
            if self.debug:
                print("DEBUG: UUID failure: {}".format(uuidstr))
            return False
        except ValueError:
            if self.debug:
                print("DEBUG: UUID ValueError: {}".format(uuidstr))
            return False
        if self.debug:
            print("DEBUG: Replaced artefact UUID to {}".format(uuidstr))
        self.collection["uuid"] = uuidstr
        return True

    def init_struct(self):
        """Initialise empty structure."""
        if self.collection is not None:
            if self.debug:
                print(
                    "DEBUG: Error - Attempting to re-initialise "
                    "collection structure.\n")
            return False
        collection = dict()
        collection["UUID"] = str(self.uuid)
        collection["product_name"] = None
        collection["product_version"] = None
        collection["product_release_date"] = None
        collection["product_tei_id"] = None
        collection["version"] = 0
        collection["author_name"] = None
        collection["author_org"] = None
        collection["author_email"] = None
        collection["artefacts"] = list()

        self.collection = collection

    def set_author(self, name: str, org: str, email: str):
        """Set author.

        Empty string or None will not update values.
        All values None will return false
        """
        if name is None and org is None and email is None:
            return False
        if name is not None and name != "":
            self.collection["author_name"] = name
        if org is not None and name != "":
            self.collection["author_org"] = org
        if email is not None and email != "":
            self.collection["author_email"] = email
        return True

    def get_author(self):
        """Get author details."""
        return self.collection["author_name"], \
            self.collection["author_org"], \
            self.collection["author_email"]

    def set_product(
            self,
            name: str,
            version: str,
            releasedate: str,
            teiid: str):
        """Set product metadata.

        Empty string or None will not update values.
        """
        if name is not None and name != "":
            self.collection["product_name"] = name
        if version is not None and version != "":
            self.collection["product_version"] = version
        if releasedate is not None and releasedate != "":
            self.collection["product_release_date"] = releasedate
        if teiid is not None and teiid != "":
            self.collection["product_tei_id"] = teiid
        return True

    def set_version(self, version: int):
        """Set collection version."""
        self.collection["version"] = version
        return True

    def add_artefact(self, art):
        """Add artefact to collection."""
        from tea_collection import artefact
        if not isinstance(art, artefact):
            if self.debug:
                print("ERROR: Bad artefact type.")
            return False
        self.collection["artefacts"].append(art)
        if self.debug:
            print("DEBUG: Adding artefact - type {}".format(type(art)))
        return True

    def artefact_numbers(self):
        """Return number of artefacts."""
        return len(self.collection["artefacts"])

    def check_key(self, key):
        """Check if key is in vocabulary."""

        if key in self.vocabulary:
            return True
        if self.debug:
            print("DEBUG. Check_key: {} not in vocabulary".format(key))
        return False

    def key_exists(self, key):
        """Check if key exists in artefact."""
        if key not in self.collection.keys():
            return False
        return True

    def is_valid(self):
        """Check if the collection (base) is valid."""
        errors = 0
        errmsg = list()

        if not self.key_exists("product_name"):
            errors += 1
            errmsg.append("ERROR: Collection has no product name")
        elif self.collection["product_name"] is None:
            errors += 1
            errmsg.append("ERROR: Collection has empty product name")
        if self.collection["version"] is None:
            errors += 1
            errmsg.append("ERROR: Collection has no version")
        if self.debug:
            if errors > 0:
                print("DEBUG: Collection is not valid.")
            else:
                print("DEBUG: Collection is valid. OK!")
        return errors, errmsg


class artefact:
    """TEA Collection artefact handling"""
    artefact = None
    debug = False
    _valid_keys = (
        "uuid",
        "name",
        "description",
        "author_name",
        "author_org",
        "author_email",
        "formats"
    )

    def __init__(self, debug):
        """Initialise artefact object"""
        self.debug = debug
        self.init_struct()

    def __str__(self):
        """Return a printable dnsobject in json."""
        import json
        # Create copy object
        newart = dict(self.artefact)
        formlist = self.get_formats()
        newart["formats"] = formlist

        return json.dumps(newart, sort_keys=False, indent=4)

    def init_struct(self):
        import uuid
        if self.artefact is not None:
            if self.debug:
                print(
                    "DEBUG: Error - Attempting to re-initialise "
                    "artefact structure.\n")
            return False
        artefact = dict()
        artefact["uuid"] = str(uuid.uuid4())
        artefact["name"] = None
        artefact["description"] = None
        artefact["author_name"] = None
        artefact["author_org"] = None
        artefact["author_email"] = None
        artefact["formats"] = list()
        self.artefact = artefact
        return artefact

    def replace_uuid(self, uuidstr: str):
        """Set UUID (from import)."""
        import uuid
        try:
            _ = uuid.UUID(uuidstr)
        except TypeError:
            if self.debug:
                print("DEBUG: UUID failure: {}".format(uuidstr))
            return False
        except ValueError:
            if self.debug:
                print("DEBUG: UUID ValueError: {}".format(uuidstr))
            return False
        self.artefact["uuid"] = uuidstr
        return True

    def valid_key(self, key):
        """Check if key is valid"""
        if key in self._valid_keys:
            return True
        return False

    def key_exists(self, key):
        """Check if key exists in artefact."""
        if key not in self.artefact.keys():
            return False
        return True

    def get_keylist(self) -> list():
        """Return list of all keys"""
        return self._valid_keys

    def add_format(self, format):
        """Add format to artefact."""
        self.artefact["formats"].append(format)
        return len(self.artefact["formats"])

    def get_formats(self):
        """Get data structures from formats in list."""
        formlist = self.artefact["formats"]
        structlist = list()
        for form in formlist:
            if self.debug:
                print(
                    "DEBUG: format: {}"
                    .format(form))
            structlist.append(form.get_struct())
        return structlist

    def add_blank_format(self):
        """Add blank initialised format to artefact."""
        from tea_collection import format

        newform = format(debug=self.debug)
        newform.init_format()
        allformats = self.add_format(newform)
        if self.debug:
            print("DEBUG: Added blank format #{}.".format(allformats))
        return newform

    def get_struct(self):
        return self.artefact

    def set_author(self, name: str, org: str, email: str):
        """Set author.

        Empty string or None will not update values.
        """
        if name is not None and name != "":
            self.artefact["author_name"] = name
        if org is not None and name != "":
            self.artefact["author_org"] = org
        if email is not None and email != "":
            self.artefact["author_email"] = email
        return True

    def set_name(self, name: str):
        """Set artefact name."""
        self.artefact["name"] = name
        return True

    def set_description(self, desc: str):
        """Set artefact description."""
        if desc is None or desc == "":
            return False
        self.artefact["description"] = desc
        return True

    def is_valid(self):
        """Check if artefact is valid."""
        errors = 0
        errmsg = list()
        if self.key_exists("name"):
            if self.artefact["name"] is None:
                errors += 1
                errmsg.append("ERROR: Artefact name is None.")
        else:
            errors += 1
            errmsg.append("ERROR: Artefact name is missing.")
        if errors > 0:
            if self.debug:
                print("DEBUG: Artefact is not valid.")
        return errors, errmsg


class format():
    """A format object for an artefact."""
    format = None
    debug = False
    _valid_keys = (
        "uuid",
        "bom-identifier",
        "mediatype",
        "category",
        "url",
        "sigurl",
        "hash",
        "size"
    )

    def __init__(self, debug):
        """Initialise artefact format object"""
        self.debug = debug
        if self.debug:
            print("DEBUG: Initialising artefact format")
        self.init_struct()

    def __str__(self):
        """Return a printable dnsobject in json."""
        import json
        return json.dumps(self.format, sort_keys=False, indent=4)

    def get_struct(self):
        return self.format

    def init_struct(self):
        import uuid
        format = dict()
        format["uuid"] = str(uuid.uuid4())
        format["bom-identifier"] = None
        format["mediatype"] = None
        format["category"] = None
        format["url"] = None
        format["sigurl"] = None
        format["hash"] = None
        format["size"] = 0
        self.format = format
        if self.debug:
            print("DEBUG: Initialised format: {}".format(str(format)))
        return format

    def set_mediatype(self, mediatype: str):
        """Set media type of doc."""
        self.format["mediatype"] = mediatype
        return True

    def set_category(self, category: str):
        """Set category of doc."""
        self.format["category"] = category
        return True

    def set_hash(self, hash: str):
        """Set hash of doc."""
        self.format["hash"] = hash
        return True

    def set_size(self, size: str):
        """Set size of doc."""
        self.format["size"] = int(size)
        return True

    def set_attributes(self, hash: str, size: int):
        """Set hash and size of artefact."""
        if hash is not None:
            self.format["hash"] = hash
        if size is not None:
            self.format["size"] = size
        return True

    def set_url(self, url: str, sigurl: str):
        """Set url and optionally signature URL."""
        if url is None or url == "":
            return False
        self.format["url"] = url
        if sigurl is not None and sigurl != "":
            self.format["sigurl"] = sigurl
        return True

    def set_bomidentifier(self, bomid: str):
        """Set nom identifier."""
        if bomid is None or bomid == "":
            return False
        self.format["bom-identifier"] = bomid
        return True

    def valid_key(self, key):
        """Check if key is valid"""
        if key in self._valid_keys:
            return True
        return False

    def get_keylist(self) -> list():
        """Return list of all keys"""
        return self._valid_keys

    def key_exists(self, key):
        """Check if key exists in artefact."""
        if key not in self.format.keys():
            return False
        return True

    def replace_uuid(self, uuidstr: str):
        """Set UUID (from import)."""
        import uuid
        try:
            _ = uuid.UUID(uuidstr)
        except TypeError:
            if self.debug:
                print("DEBUG: UUID failure: {}".format(uuidstr))
            return False
        except ValueError:
            if self.debug:
                print("DEBUG: UUID ValueError: {}".format(uuidstr))
            return False
        self.format["uuid"] = uuidstr
        return True

    def is_valid(self):
        """Check if format is valid."""
        errors = 0
        errmsg = list()
        if self.key_exists("url"):
            if self.format["url"] is None:
                errors += 1
                errmsg.append("ERROR: Format has empty URL.")
        else:
            errors += 1
            errmsg.append("ERROR: Format lacks URL.")

        if errors > 0:
            if self.debug:
                print("DEBUG: Format is not valid.")

        return errors, errmsg
