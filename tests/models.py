from django.db import models
from django_json_subfields import JSONBooleanField, JSONIntegerField, JSONCharField


class SimpleBool(models.Model):
    json = models.JSONField(default=dict)
    json_bool = JSONBooleanField(json)


class SimpleBoolDefault(models.Model):
    json = models.JSONField(default=dict)
    json_bool = JSONBooleanField(json, default=True)


class SimpleInt(models.Model):
    json = models.JSONField(default=dict)
    json_int = JSONIntegerField(json)


class SimpleIntDefault(models.Model):
    json = models.JSONField(default=dict)
    json_int = JSONIntegerField(json, default=1)


class SimpleChar(models.Model):
    json = models.JSONField(default=dict)
    json_char = JSONCharField(json)
