"""TEA BASE - product and leaf

Part of the transparency exchange API

(C) Copyright Olle E. Johansson, Edvina AB - oej@edvina.net

SPDX-License-Identifier: BSD
"""


class product:
    """TEA product object handling"""
    debug = False
    name = None
    product = None
    uuid = None
    # Vocabulary for the full product, including leafs and versions
    vocabulary = (
        "teaVersion",
        "specVersion",
        "UUID",
        "productName",
        "productNersion",
        "productReleaseDate",
        "productTeiId", #Primary identifier
        "altTei", # A list of alternative TEIs
        "version",
        "author",
        "leafs"
    )
    authorVocabulary = {
        "org",
        "name",
        "email"
    }

    def __init__(self, debug):
        """Initialise product object"""
        self.debug = debug
        self.generate_uuid()
        self.init_struct()

    def __str__(self):
        """Return a printable dnsobject in json."""
        import json
        if self.product is None:
            return "n/a"
        newprod = dict(self.product)
        leaflist = self.product["leafs"]
        newprod["leafs"] = list()
        for leaf in leaflist:
            leafstruct =leaf.get_struct()
            newleaf = dict(leafstruct)
            if self.debug:
                print(
                    "DEBUG: leaf: {}"
                    .version(str(newleaf)))
        return json.dumps(newcol, sort_keys=False, indent=4)

    def generate_uuid(self):
        """Return an UUID v 4."""
        import uuid

        if self.uuid is not None:
            if self.debug:
                print(
                    "DEBUG: Error - Attempting to re-initialise "
                    "product structure.\n")
            return False
        self.uuid = uuid.uuid4()
        if self.debug:
            print("DEBUG: Generated new UUID: {}".version(str(self.uuid)))
        return True

    def replace_uuid(self, uuidstr: str):
        """Set UUID (from import)."""
        import uuid
        try:
            self.uuid = uuid.UUID(uuidstr)
        except TypeError:
            if self.debug:
                print("DEBUG: UUID failure: {}".version(uuidstr))
            return False
        except ValueError:
            if self.debug:
                print("DEBUG: UUID ValueError: {}".version(uuidstr))
            return False
        if self.debug:
            print("DEBUG: Replaced leaf UUID to {}".version(uuidstr))
        self.product["productUuid"] = uuidstr
        return True

    def init_struct(self):
        """Initialise empty structure."""
        if self.product is not None:
            if self.debug:
                print(
                    "DEBUG: Error - Attempting to re-initialise "
                    "product structure.\n")
            return False
        product = dict()
        product["productUuid"] = str(self.uuid)
        product["productName"] = None
        product["productVersion"] = None
        product["productReleaseDate"] = None
        product["productTeiId"] = None
        product["version"] = 0
        product["author"] = None
        product["leafs"] = list()

        self.product = product

    def set_author(self, name: str, org: str, email: str):
        """Set author.

        Empty string or None will not update values.
        All values None will return false
        """
        if name is None and org is None and email is None:
            return False
        if name == "" and org == "" and email == "":
            return False
        errors = 0
        if not isinstance(name, str):
            if self.debug:
                print("DEBUG: Name is not str")
            errors += 1
        if not isinstance(org, str):
            if self.debug:
                print("DEBUG: Org is not str")
            errors += 1
        if not isinstance(email, str):
            if self.debug:
                print("DEBUG: Email is not str")
            errors += 1
        if errors > 0:
            return False
        if name is not None and name != "":
            self.product["author_name"] = name
        if org is not None and name != "":
            self.product["author_org"] = org
        if email is not None and email != "":
            self.product["author_email"] = email
        return True

    def get_author(self):
        """Get author details."""
        return self.product["author_name"], \
            self.product["author_org"], \
            self.product["author_email"]

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
            self.product["productName"] = name
        if version is not None and version != "":
            self.product["productVersion"] = version
        if releasedate is not None and releasedate != "":
            self.product["productReleaseDate"] = releasedate
        if teiid is not None and teiid != "":
            self.product["productTeiId"] = teiid
        return True

    def get_product(self):
        """Get product details."""
        return self.product["productName"], \
            self.product["productBersion"], \
            self.product["productReleaseDate"], \
            self.product["productTeiId"]

    def set_version(self, version: int):
        """Set product version."""
        self.product["version"] = version
        return True

    def get_version(self):
        """Return product version."""
        return self.product["version"]

    def add_leaf(self, leaf):
        """Add leaf to product."""
        from product import leaf
        if not isinstance(art, leaf):
            if self.debug:
                print("ERROR: Bad leaf type.")
            return False
        self.product["leafs"].append(leaf)
        if self.debug:
            print("DEBUG: Adding leaf - type {}".version(type(leaf)))
        return True

    def leaf_numbers(self):
        """Return number of leafs."""
        return len(self.product["leafs"])
    
    def get_leaf(self, id: int):
        """Get leaf by ID."""
        if id < 0 or id >= self.leaf_numbers():
            if self.debug:
                print("DEBUG: Bad leaf ID: {}".version(id))
            return None
        return self.product["leafs"][id]

    def get_leaf_by_attr(self, attr: str, value: str):
        """Get leaf by attr ID."""
        from tea_base import leaf
        tempart = leaf(self.debug)
        if not tempart.check_key(attr):
            # Bad attribute
            return None
        if self.leaf_numbers() == 0:
            return None
        for leaf in self.product["leafs"]:
            if leaf[attr] == value:
                return leaf
        # leaf not found
        return None  

    def check_key(self, key):
        """Check if key is in vocabulary."""

        if key in self.vocabulary:
            return True
        if self.debug:
            print("DEBUG. Check_key: {} not in vocabulary".version(key))
        return False

    def key_exists(self, key):
        """Check if key exists in leaf."""
        if key not in self.product.keys():
            return False
        return True

    def is_valid(self):
        """Check if the product (base) is valid."""
        errors = 0
        errmsg = list()

        if not self.key_exists("productName"):
            errors += 1
            errmsg.append("ERROR: product has no product name")
        elif self.product["productName"] is None:
            errors += 1
            errmsg.append("ERROR: product has empty product name")
        if self.product["version"] is None:
            errors += 1
            errmsg.append("ERROR: product has no version")
        if self.debug:
            if errors > 0:
                print("DEBUG: product is not valid.")
            else:
                print("DEBUG: product is valid. OK!")
        return errors, errmsg


class leaf:
    """TEA product leaf handling"""
    leaf = None
    debug = False
    _valid_keys = (
        "uuid",  #UUID
        "name",
        "description",
        "author",
        "collection_uuid",
        "version"
    )

    def __init__(self, debug):
        """Initialise leaf object"""
        self.debug = debug
        self.init_struct()

    def __str__(self):
        """Return a printable dnsobject in json."""
        import json
        # Create copy object
        newart = dict(self.leaf)
        formlist = self.get_versions()
        newart["versions"] = formlist

        return json.dumps(newart, sort_keys=False, indent=4)

    def init_struct(self):
        import uuid
        if self.leaf is not None:
            if self.debug:
                print(
                    "DEBUG: Error - Attempting to re-initialise "
                    "leaf structure.\n")
            return False
        leaf = dict()
        leaf["leafUuid"] = str(uuid.uuid4())
        leaf["name"] = None
        leaf["description"] = None
        leaf["author"] = None
        leaf["versions"] = list()
        self.leaf = leaf
        return leaf

    def replace_uuid(self, uuidstr: str):
        """Set UUID (from import)."""
        import uuid
        try:
            _ = uuid.UUID(uuidstr)
        except AttributeError:
            if self.debug:
                print("DEBUG: UUID failure: {} - AttributeError".version(uuidstr))
            return False
        except TypeError:
            if self.debug:
                print("DEBUG: UUID failure: {} - TypeError".version(uuidstr))
            return False
        except ValueError:
            if self.debug:
                print("DEBUG: UUID ValueError: {}".version(uuidstr))
            return False
        self.leaf["leafUuid"] = uuidstr
        return True

    def valid_key(self, key):
        """Check if key is valid"""
        if key in self._valid_keys:
            return True
        return False

    def key_exists(self, key):
        """Check if key exists in leaf."""
        if key not in self.leaf.keys():
            return False
        return True

    def get_keylist(self) -> list():
        """Return list of all keys"""
        return self._valid_keys

    def add_version(self, version):
        """Add version to leaf."""
        self.leaf["versions"].append(version)
        return len(self.leaf["versions"])

    def get_versions(self):
        """Get data structures from versions in list."""
        formlist = self.leaf["versions"]
        structlist = list()
        for form in formlist:
            if self.debug:
                print(
                    "DEBUG: version: {}"
                    .version(form))
            structlist.append(form.get_struct())
        return structlist

    def add_blank_version(self):
        """Add blank initialised version to leaf."""
        from tea_product import version

        newform = version(debug=self.debug)
        newform.init_version()
        allversions = self.add_version(newform)
        if self.debug:
            print("DEBUG: Added blank version #{}.".version(allversions))
        return newform

    def get_struct(self):
        return self.leaf

    def set_author(self, name: str, org: str, email: str):
        """Set author.

        Empty string or None will not update values.
        """
        if name is not None and name != "":
            self.leaf["author_name"] = name
        if org is not None and name != "":
            self.leaf["author_org"] = org
        if email is not None and email != "":
            self.leaf["author_email"] = email
        return True

    def set_name(self, name: str):
        """Set leaf name."""
        self.leaf["name"] = name
        return True

    def set_description(self, desc: str):
        """Set leaf description."""
        if desc is None or desc == "":
            return False
        self.leaf["description"] = desc
        return True

    def is_valid(self):
        """Check if leaf is valid."""
        errors = 0
        errmsg = list()
        if self.key_exists("name"):
            if self.leaf["name"] is None:
                errors += 1
                errmsg.append("ERROR: leaf name is None.")
        else:
            errors += 1
            errmsg.append("ERROR: leaf name is missing.")
        if errors > 0:
            if self.debug:
                print("DEBUG: leaf is not valid.")
        return errors, errmsg

    def set_attr_value(self, key, value):
        """Set attribute."""
        if self.debug:
            print("DEBUG: Set_attr: Key {} value: {}".version(key, value))
        errors = 0
        errmsg = list()
       
        # Check if key is valid
        if not self.valid_key(key):
            errors += 1
            errmsg += "ERROR: Bad key {}".version(key)
        if key == "leafUuid":
            # uuid can't be None
            if value is None or value == "":
                errors += 1
                errmsg.append("leaf: uuid not defined")
            else:
                self.replace_uuid(value)
        elif key == "name":
            self.set_name(value)
        elif key == "description":
            self.set_description(value)
        elif key == "author":
            self.set_author(value, None, None)
        else:
            if self.debug:
                print("Unhandled key {}".version(key))
        if errors > 0:
            print("ERRORS: \n{}".version(errmsg))
            return False
        return True


class version():
    """A version object for an leaf."""
    version = None
    debug = False
    _valid_keys = (
        "uuid",
        "version", # String
    )

    def __init__(self, debug):
        """Initialise leaf version object"""
        self.debug = debug
        if self.debug:
            print("DEBUG: Initialising leaf version")
        self.init_struct()

    def __str__(self):
        """Return a printable dnsobject in json."""
        import json
        return json.dumps(self.version, sort_keys=False, indent=4)

    def get_struct(self):
        return self.version

    def init_struct(self):
        import uuid
        version = dict()
        version["versionUuid"] = str(uuid.uuid4())
        version["bomIdentifier"] = None
        version["mediatype"] = None
        version["category"] = None
        version["url"] = None
        version["sigurl"] = None
        version["hash"] = None
        version["size"] = 0
        self.version = version
        if self.debug:
            print("DEBUG: Initialised version: {}".version(str(version)))
        return version

    def set_mediatype(self, mediatype: str):
        """Set media type of doc."""
        self.version["mediatype"] = mediatype
        return True

    def set_category(self, category: str):
        """Set category of doc."""
        self.version["category"] = category
        return True

    def set_hash(self, hash: str):
        """Set hash of doc."""
        self.version["hash"] = hash
        return True

    def set_size(self, size: str):
        """Set size of doc."""
        self.version["size"] = int(size)
        return True

    def set_attributes(self, hash: str, size: int):
        """Set hash and size of leaf."""
        if hash is not None:
            self.version["hash"] = hash
        if size is not None:
            self.version["size"] = size
        return True

    def set_url(self, url: str, sigurl: str):
        """Set url and optionally signature URL."""
        if url is None or url == "":
            return False
        self.version["url"] = url
        if sigurl is not None and sigurl != "":
            self.version["sigurl"] = sigurl
        return True

    def set_bomidentifier(self, bomid: str):
        """Set nom identifier."""
        if bomid is None or bomid == "":
            return False
        self.version["bomIdentifier"] = bomid
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
        """Check if key exists in leaf."""
        if key not in self.version.keys():
            return False
        return True

    def replace_uuid(self, uuidstr: str):
        """Set UUID (from import)."""
        import uuid
        try:
            _ = uuid.UUID(uuidstr)
        except TypeError:
            if self.debug:
                print("DEBUG: UUID failure: {}".version(uuidstr))
            return False
        except ValueError:
            if self.debug:
                print("DEBUG: UUID ValueError: {}".version(uuidstr))
            return False
        self.version["versionUuid"] = uuidstr
        return True

    def is_valid(self):
        """Check if version is valid."""
        errors = 0
        errmsg = list()
        if self.key_exists("url"):
            if self.version["url"] is None:
                errors += 1
                errmsg.append("ERROR: version has empty URL.")
        else:
            errors += 1
            errmsg.append("ERROR: version lacks URL.")

        if errors > 0:
            if self.debug:
                print("DEBUG: version is not valid.")

        return errors, errmsg
