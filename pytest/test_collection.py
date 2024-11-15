"""Test the TEA collection library.

(C) Copyright Olle E. Johansson, Edvina AB - oej@edvina.net

SPDX-License-Identifier: BSD
"""
import os
import pytest

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TESTDATA_DIR = os.path.join(THIS_DIR, os.pardir, 'test_data' + os.sep)


@pytest.fixture
def def_collection():
    """A default empty collection."""
    from tea_collection import tea_collection

    mycol = tea_collection(debug=True)
    return mycol


@pytest.fixture
def def_artefact():
    """A default empty artefact."""
    from tea_collection import artefact

    myart = artefact(debug=True)
    return myart


@pytest.fixture
def def_format():
    """A default empty artefact."""
    from tea_collection import format

    myformat = format(debug=True)
    return myformat


def test_coll_01(capsys, request, def_collection):
    """Test creation of basic collection."""

    col = def_collection
    noform = col.artefact_numbers()
    captured = capsys.readouterr()
    with capsys.disabled():
        print(
            "\nDEBUG {}: output: \n{}\n"
            .format(request.node.name, captured.out))
        print("DEBUG: Number of artefacts: {}".format(noform))
        print("DEBUG: Type of collection: {}".format(type(col)))
    assert noform == 0


def test_coll_02(capsys, request, def_collection, def_artefact):
    """Test creation of basic collection."""

    col = def_collection
    art = def_artefact
    col.add_artefact(art=art)
    noform = col.artefact_numbers()
    captured = capsys.readouterr()
    with capsys.disabled():
        print(
            "\nDEBUG {}: output: \n{}\n"
            .format(request.node.name, captured.out))
        print("DEBUG: Number of artefacts: {}".format(noform))
        print("DEBUG: Type of collection: {}".format(type(col)))
    assert noform == 1


class TestCollection:
    """Test collection class"""

    def test_serialise(self, capsys, request, def_collection):
        """Test serialise."""
        import re
        import json
        mycol = def_collection
        strcol = str(mycol)
        newcol = json.loads(strcol)
        captured = capsys.readouterr()
        with capsys.disabled():
            print(
                "\nDEBUG {}: output: \n{}\n"
                .format(request.node.name, captured.out))
            print("JSON: {}".format(strcol))
            print("Newjson: {}".format(newcol))
        assert re.search(
            'product_name',
            strcol
        ) is not None

    def test_set_author_01(self, capsys, request, def_collection):
        """Test set author."""
        mycol = def_collection
        tname = "Ford Prefect"
        torg = "The Heart of Gold, inc"
        temail = "ford.prefect@hog.example.com"
        res = mycol.set_author(
            name=tname,
            org=torg,
            email=temail)
        name, org, email = mycol.get_author()
        captured = capsys.readouterr()
        with capsys.disabled():
            print(
                "\nDEBUG {}: output: \n{}\n"
                .format(request.node.name, captured.out))
        assert name == tname
        assert email == temail
        assert org == torg
        assert res is True

    def test_set_author_02(self, capsys, request, def_collection):
        """Test set author empty data."""
        mycol = def_collection
        tname = None
        torg = None
        temail = None
        res = mycol.set_author(
            name=tname,
            org=torg,
            email=temail)
        name, org, email = mycol.get_author()
        captured = capsys.readouterr()
        with capsys.disabled():
            print(
                "\nDEBUG {}: output: \n{}\n"
                .format(request.node.name, captured.out))
        assert res is False

    def test_set_author_03(self, capsys, request, def_collection):
        """Test set author empty data."""
        import re

        mycol = def_collection
        tname = 123
        torg = capsys
        temail = self
        res = mycol.set_author(
            name=tname,
            org=torg,
            email=temail)
        name, org, email = mycol.get_author()
        captured = capsys.readouterr()
        with capsys.disabled():
            print(
                "\nDEBUG {}: output: \n{}\n"
                .format(request.node.name, captured.out))
        assert res is False
        assert re.search(
            "Name is not str",
            captured.out
        ) is not None
