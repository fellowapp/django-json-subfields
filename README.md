# django-json-subfields

This project provides virtual Django model fields which are backed by an
underlying JSONField. This allows combining the ergonomic benefits of using real
fields (e.g. automatic admin fields, validation) with JSON-based storage.

## Quickstart

To use JSON subfields, first define a normal JSONField on a model, then use the
provided field wrappers by passing the JSONField as the first argument:

```python
from django.db import models
import django_json_subfields as jsonfields

class Person(models.Model):
    info = models.JSONField(default=dict)

    num_children = jsonfields.IntegerField(info)
    birth_city = jsonfields.CharField(info, max_length=128)
    is_enrolled = jsonfields.BooleanField(info)
```

The subfields can then be queried or used just like any other model fields. The
attributes are proxied directly from the JSON field:

```python
>>> person = Person(num_children=2, birth_city="Montreal")
>>> person.info
{"num_children": 2, "birth_city": "Montreal"}
>>> person.info["num_children"] = 3
>>> person.num_children
3
```

## When To Use

Most of the time, you probably don't need JSON fields. They are more difficult
to index and query, and relational databases are best suited to structured data.
Much of the functionality of JSON fields can also be replicated using
[Entity-Attribute-Value models][eav].

[eav]:
  https://en.wikipedia.org/wiki/Entity%E2%80%93attribute%E2%80%93value_model

However, they can be useful in specific circumstances:

- Sparse data
- Fields which change often
- Extensibility
- Prototyping without needing database migrations.

## Running Tests

Start a mysql container:

    docker run --rm --publish-all --env MYSQL_ROOT_PASSWORD=pass --detach mysql:latest

Run tests:

    MYSQL_ROOT_PASSWORD=pass MYSQL_PORT=3306 py.test
