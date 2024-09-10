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
        printobj = dict(self.dnsobject)
        return json.dumps(printobj, sort_keys=False, indent=4)

    def generate_uuid(self):
        """Return an UUID v 4."""
        import uuid

        if self.uuid != None:
            if self.debug:
                print("DEBUG: Error - Attempting to re-initialise collection structure.\n")
            return False
        self.uuid = uuid.uuid4()
        if self.debug:
            print("DEBUG: Generated new UUID: {}".format(str(self.uuid)))
        return True

    def init_struct(self):
        """Initialise empty structure."""
        if self.collection != None:
            if self.debug:
                print("DEBUG: Error - Attempting to re-initialise collection structure.\n")
            return False
        collection = dict()
        collection["UUID"] = str(self.uuid)
        collection["product_name"] = None
        collection["product_version"] = None
        collection["product_release_date"] = None
        collection["version"] = 0
        collection["author_name"] = None
        collection["author_org"] = None
        collection["author_email"] = None
        collection["artefacts"] = list()

        self.collection = collection


class artefact:
    """TEA Collection artefact handling"""
    artefact = None

    def __init__(self, debug):
        """Initialise collection object"""
        self.debug = debug

    def __str__(self):
        """Return a printable dnsobject in json."""
        import json
        printobj = dict(self.dnsobject)
        return json.dumps(printobj, sort_keys=False, indent=4)
    
    def init_struct(self):
        import uuid
        is self.artefact != None:
            if self.debug:
                    print("DEBUG: Error - Attempting to re-initialise artefact structure.\n")
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

    def init_format(self):
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
        return format


