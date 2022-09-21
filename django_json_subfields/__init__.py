import json
from typing import cast, Any, Optional, Type
from django.db import models
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models.expressions import Col
from django.db.models.fields.json import JSONExact, KeyTransform, KeyTransformStartsWith


class JSONExtract(models.Func):
    function = "JSON_EXTRACT"


class JSONUnquote(models.Func):
    function = "JSON_UNQUOTE"


class JSONAttribute:
    """ """

    def __init__(self, field: "JSONValue"):
        self.field = field

    def __get__(self, instance: models.Model, owner: Type[models.Model]) -> Any:
        store = getattr(instance, self.field.json_field.attname)
        result = store.get(self.field.attname)
        return result if result is not None else self.field.get_default()

    def __set__(self, instance: models.Model, value: Any):
        getattr(instance, self.field.json_field.attname)[self.field.attname] = value


class JSONValue(models.Field):
    """ """

    descriptor_class = JSONAttribute
    json_field: models.JSONField

    def __init__(self, json_field, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.json_field = json_field

    def db_type(self, connection: BaseDatabaseWrapper) -> Optional[str]:
        return None

    def get_prep_value(self, value: Any) -> Any:
        if value is None:
            return value
        return json.dumps(value)

    def contribute_to_class(
        self, cls: Type[models.Model], name: str, private_only: bool = False
    ) -> None:
        super().contribute_to_class(cls, name, True)

        self.concrete = False
        self.column = None

    def get_col(self, alias: str, output_field: models.Field = None) -> Col:
        # return KeyTransform(self.attname, self.json_field.get_col(alias, output_field))
        # return models.ExpressionWrapper(KeyTransform("json_bool"), output_field=self)
        return models.ExpressionWrapper(
            JSONExtract(
                self.json_field.get_col(alias, output_field),
                models.Value(f"$.{self.attname}"),
                output_field=self,
            ),
            output_field=self,
        )


JSONValue.register_lookup(JSONExact)


class JSONBooleanField(JSONValue, models.BooleanField):
    pass


class JSONIntegerField(JSONValue, models.IntegerField):
    pass


class JSONCharField(JSONValue, models.CharField):
    pass


class JSONTextLookup(models.Expression):
    def process_lhs(self, compiler, connection, lhs=None):
        return super().process_lhs(
            compiler, connection, lhs=JSONUnquote(lhs or self.lhs)
        )


class JSONLookupStartsWith(JSONTextLookup, models.lookups.StartsWith):
    pass


class JSONLookupEndsWith(JSONTextLookup, models.lookups.EndsWith):
    pass


JSONCharField.register_lookup(JSONLookupStartsWith)
JSONCharField.register_lookup(JSONLookupEndsWith)
