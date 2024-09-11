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

    def __init__(self, debug):
        """Initialise collection object"""
        self.debug = debug
        self.generate_uuid()

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
        """
        if name is not None and name != "":
            self.collection["author_name"] = name
        if org is not None and name != "":
            self.collection["author_org"] = org
        if email is not None and email != "":
            self.collection["author_email"] = email
        return True

    def set_product(self, name: str, version, releasedate: str, teiid: str):
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

    def set_collection_version(self, version: int):
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


class artefact:
    """TEA Collection artefact handling"""
    artefact = None
    debug = False

    def __init__(self, debug):
        """Initialise artefact object"""
        self.debug = debug

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

        newform = artefact_format(debug=self.debug)
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


class format():
    """A format object for an artefact."""
    format = None
    debug = False

    def __init__(self, debug):
        """Initialise artefact format object"""
        self.debug = debug
        if self.debug:
            print("DEBUG: Initialising artefact format")

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
