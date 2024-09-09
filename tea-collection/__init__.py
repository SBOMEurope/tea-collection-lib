"""The TCO - Transparency Exchange Collection - parsing library

(C) Copyright Olle E. Johansson, Edvina AB - oej@edvina.net

SPDX-License-Identifier: BSD
"""

class collection:
    """TEA Collection object handling"""
    debug = False
    name = None
    collection = None

    def __init__(self, debug):
        """Initialise collection object"""
        self.debug = debug

    def __str__(self):
        """Return a printable dnsobject in json."""
        import json
        printobj = dict(self.dnsobject)
        return json.dumps(printobj, sort_keys=False, indent=4)


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
