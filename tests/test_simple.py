import pytest
from django.db import models, connection
from django_json_subfields import JSONBooleanField
from django.test.utils import isolate_apps

from tests.models import SimpleBool, SimpleBoolDefault, SimpleInt, SimpleChar


def test_simple_bool():
    obj1 = SimpleBool()
    obj2 = SimpleBool(json_bool=None)
    obj3 = SimpleBool(json_bool=True)
    obj4 = SimpleBool(json_bool=False)

    assert obj1.json_bool is None
    assert obj1.json == {}

    assert obj2.json_bool == None
    assert obj2.json == {"json_bool": None}

    assert obj3.json_bool == True
    assert obj3.json == {"json_bool": True}

    assert obj4.json_bool == False
    assert obj4.json == {"json_bool": False}

    obj3.save()
    obj = SimpleBool.objects.first()
    assert obj.json_bool == True
    obj.json_bool = False
    assert obj.json_bool == False
    assert obj.json == {"json_bool": False}


def test_subfield_takes_precedence():
    obj = SimpleBool(json={"json_bool": False}, json_bool=True)

    assert obj.json_bool == True
    assert obj.json == {"json_bool": True}


def test_saving_with_update_fields():
    obj = SimpleBool(json_bool=True)
    obj.save()


def test_querying_with_subfield():
    obj1 = SimpleBool.objects.create(json_bool=None)
    obj2 = SimpleBool.objects.create(json_bool=True)
    obj3 = SimpleBool.objects.create(json_bool=False)

    assert list(SimpleBool.objects.filter(json_bool=None)) == [obj1]
    assert list(SimpleBool.objects.filter(json_bool=True)) == [obj2]
    assert list(SimpleBool.objects.filter(json_bool=False)) == [obj3]


def test_unspecified_defaults():
    obj = SimpleBoolDefault()

    assert obj.json == {}
    assert obj.json_bool == True


def test_integer_subfield():
    obj = SimpleInt(json_int=4)

    assert obj.json_int == 4
    assert obj.json == {"json_int": 4}

    obj.save()

    assert list(SimpleInt.objects.filter(json_int=None)) == []
    assert list(SimpleInt.objects.filter(json_int=2)) == []
    assert list(SimpleInt.objects.filter(json_int=4)) == [obj]


def test_char_subfield():
    obj = SimpleChar(json_char="hello, world!")

    assert obj.json_char == "hello, world!"
    assert obj.json == {"json_char": "hello, world!"}

    obj.save()

    assert list(SimpleChar.objects.filter(json_char=None)) == []
    assert list(SimpleChar.objects.filter(json_char="hello")) == []
    assert list(SimpleChar.objects.filter(json_char="hello, world!")) == [obj]

    assert list(SimpleChar.objects.filter(json_char__contains="universe")) == []
    assert list(SimpleChar.objects.filter(json_char__contains="world")) == [obj]

    assert list(SimpleChar.objects.filter(json_char__startswith="hello")) == [obj]
    assert list(SimpleChar.objects.filter(json_char__startswith="goodbye")) == []

    assert list(SimpleChar.objects.filter(json_char__endswith="world!")) == [obj]
    assert list(SimpleChar.objects.filter(json_char__endswith="universe!")) == []
