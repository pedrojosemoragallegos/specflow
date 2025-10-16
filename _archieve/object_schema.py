from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .schema import Schema

if TYPE_CHECKING:
    from specflow.typing import JSONValue


class ObjectSchema(Schema):
    def __init__(  # noqa: C901, PLR0912, PLR0915
        self,
        id_: str | None = None,
        schema: str | None = None,
        ref: str | None = None,
        dynamic_ref: str | None = None,
        recursive_ref: str | None = None,
        definitions: dict[str, Schema] | None = None,
        defs: dict[str, Schema] | None = None,
        comment: str | None = None,
        anchor: str | None = None,
        dynamic_anchor: str | None = None,
        vocabulary: dict[str, bool] | None = None,
        title: str | None = None,
        description: str | None = None,
        properties: dict[str, Schema] | None = None,
        pattern_properties: dict[str, Schema] | None = None,
        required: list[str] | None = None,
        property_names: Schema | None = None,
        min_properties: int | None = None,
        max_properties: int | None = None,
        dependent_required: dict[str, list[str]] | None = None,
        dependent_schemas: dict[str, Schema] | None = None,
        all_of: list[Schema] | None = None,
        any_of: list[Schema] | None = None,
        one_of: list[Schema] | None = None,
        not_: Schema | None = None,
        if_: Schema | None = None,
        then: Schema | None = None,
        else_: Schema | None = None,
        *,
        additional_properties: Schema | bool | None = None,
        unevaluated_properties: Schema | bool | None = None,
        recursive_anchor: bool | None = None,
        deprecated: bool | None = None,
        read_only: bool | None = None,
        write_only: bool | None = None,
    ) -> None:
        super().__init__(
            id_=id_,
            schema=schema,
            ref=ref,
            dynamic_ref=dynamic_ref,
            recursive_ref=recursive_ref,
            definitions=definitions,
            defs=defs,
            comment=comment,
            anchor=anchor,
            dynamic_anchor=dynamic_anchor,
            vocabulary=vocabulary,
            title=title,
            description=description,
            recursive_anchor=recursive_anchor,
            deprecated=deprecated,
            read_only=read_only,
            write_only=write_only,
        )

        if properties is not None:
            if not isinstance(properties, dict):  # type: ignore
                raise TypeError("properties must be a dictionary")
            for key, value in properties.items():
                if not isinstance(key, str) or not key.strip():  # type: ignore
                    raise ValueError("properties keys must be non-empty strings")
                if not isinstance(value, Schema):  # type: ignore
                    raise TypeError("properties values must be Schema instances")

        if pattern_properties is not None:
            if not isinstance(pattern_properties, dict):  # type: ignore
                raise TypeError("patternProperties must be a dictionary")
            for key, value in pattern_properties.items():
                if not isinstance(key, str) or not key.strip():  # type: ignore
                    raise ValueError("patternProperties keys must be non-empty strings")
                try:
                    re.compile(key)
                except re.error as e:
                    raise ValueError(
                        f"patternProperties key must be a valid regular expression: {e}",
                    ) from e
                if not isinstance(value, Schema):  # type: ignore
                    raise TypeError("patternProperties values must be Schema instances")

        if additional_properties is not None:  # noqa: SIM102
            if not isinstance(additional_properties, (Schema, bool)):  # type: ignore
                raise TypeError(
                    "additionalProperties must be a Schema instance or boolean",
                )

        if unevaluated_properties is not None:  # noqa: SIM102
            if not isinstance(unevaluated_properties, (Schema, bool)):  # type: ignore
                raise TypeError(
                    "unevaluatedProperties must be a Schema instance or boolean",
                )

        if required is not None:
            if not isinstance(required, list):  # type: ignore
                raise TypeError("required must be a list")
            if not required:
                raise ValueError("required must contain at least one property name")
            for prop in required:
                if not isinstance(prop, str) or not prop.strip():  # type: ignore
                    raise ValueError(
                        "required property names must be non-empty strings",
                    )

        if property_names is not None:  # noqa: SIM102
            if not isinstance(property_names, Schema):  # type: ignore
                raise TypeError("propertyNames must be a Schema instance")

        if min_properties is not None:
            if not isinstance(min_properties, int):  # type: ignore
                raise TypeError("minProperties must be an integer")
            if min_properties < 0:
                raise ValueError("minProperties must be non-negative")

        if max_properties is not None:
            if not isinstance(max_properties, int):  # type: ignore
                raise TypeError("maxProperties must be an integer")
            if max_properties < 0:
                raise ValueError("maxProperties must be non-negative")

        if (min_properties is not None) and (max_properties is not None):  # noqa: SIM102
            if min_properties > max_properties:
                raise ValueError("minProperties cannot be greater than maxProperties")

        if dependent_required is not None:
            if not isinstance(dependent_required, dict):  # type: ignore
                raise TypeError("dependentRequired must be a dictionary")
            for key, value in dependent_required.items():
                if not isinstance(key, str) or not key.strip():  # type: ignore
                    raise ValueError("dependentRequired keys must be non-empty strings")
                if not isinstance(value, list):  # type: ignore
                    raise TypeError("dependentRequired values must be lists")
                if not value:
                    raise ValueError(
                        "dependentRequired lists must contain at least one property name",
                    )
                for prop in value:
                    if not isinstance(prop, str) or not prop.strip():  # type: ignore
                        raise ValueError(
                            "dependentRequired property names must be non-empty strings",
                        )

        if dependent_schemas is not None:
            if not isinstance(dependent_schemas, dict):  # type: ignore
                raise TypeError("dependentSchemas must be a dictionary")
            for key, value in dependent_schemas.items():
                if not isinstance(key, str) or not key.strip():  # type: ignore
                    raise ValueError("dependentSchemas keys must be non-empty strings")
                if not isinstance(value, Schema):  # type: ignore
                    raise TypeError("dependentSchemas values must be Schema instances")

        if all_of is not None:
            if not isinstance(all_of, list):  # type: ignore
                raise TypeError("allOf must be a list")
            if not all_of:
                raise ValueError("allOf must contain at least one schema")
            for schema_item in all_of:
                if not isinstance(schema_item, Schema):  # type: ignore
                    raise TypeError("All allOf items must be Schema instances")

        if any_of is not None:
            if not isinstance(any_of, list):  # type: ignore
                raise TypeError("anyOf must be a list")
            if not any_of:
                raise ValueError("anyOf must contain at least one schema")
            for schema_item in any_of:
                if not isinstance(schema_item, Schema):  # type: ignore
                    raise TypeError("All anyOf items must be Schema instances")

        if one_of is not None:
            if not isinstance(one_of, list):  # type: ignore
                raise TypeError("oneOf must be a list")
            if not one_of:
                raise ValueError("oneOf must contain at least one schema")
            for schema_item in one_of:
                if not isinstance(schema_item, Schema):  # type: ignore
                    raise TypeError("All oneOf items must be Schema instances")

        if not_ is not None:  # noqa: SIM102
            if not isinstance(not_, Schema):  # type: ignore
                raise TypeError("not must be a Schema instance")

        if (then is not None or else_ is not None) and if_ is None:
            raise ValueError("'then' and 'else' require 'if' to be specified")

        if if_ is not None:  # noqa: SIM102
            if not isinstance(if_, Schema):  # type: ignore
                raise TypeError("if must be a Schema instance")

        if then is not None:  # noqa: SIM102
            if not isinstance(then, Schema):  # type: ignore
                raise TypeError("then must be a Schema instance")

        if else_ is not None:  # noqa: SIM102
            if not isinstance(else_, Schema):  # type: ignore
                raise TypeError("else must be a Schema instance")

        if required is not None and properties is not None:
            for prop in required:
                if prop not in properties:
                    raise ValueError(
                        f"required property '{prop}' is not defined in properties",
                    )

        self._properties = properties
        self._pattern_properties = pattern_properties
        self._additional_properties = additional_properties
        self._unevaluated_properties = unevaluated_properties
        self._required = required
        self._property_names = property_names
        self._min_properties = min_properties
        self._max_properties = max_properties
        self._dependent_required = dependent_required
        self._dependent_schemas = dependent_schemas
        self._all_of = all_of
        self._any_of = any_of
        self._one_of = one_of
        self._not = not_
        self._if = if_
        self._then = then
        self._else = else_

    def to_dict(self) -> dict[str, JSONValue]:  # noqa: C901, PLR0912
        result: dict[str, JSONValue] = super().to_dict()

        result["type"] = "object"

        if self._properties is not None:
            result["properties"] = {
                key: value.to_dict() for key, value in self._properties.items()
            }
        if self._pattern_properties is not None:
            result["patternProperties"] = {
                key: value.to_dict() for key, value in self._pattern_properties.items()
            }
        if self._additional_properties is not None:
            if isinstance(self._additional_properties, bool):
                result["additionalProperties"] = self._additional_properties
            else:
                result["additionalProperties"] = self._additional_properties.to_dict()
        if self._unevaluated_properties is not None:
            if isinstance(self._unevaluated_properties, bool):
                result["unevaluatedProperties"] = self._unevaluated_properties
            else:
                result["unevaluatedProperties"] = self._unevaluated_properties.to_dict()
        if self._required is not None:
            result["required"] = self._required
        if self._property_names is not None:
            result["propertyNames"] = self._property_names.to_dict()
        if self._min_properties is not None:
            result["minProperties"] = self._min_properties
        if self._max_properties is not None:
            result["maxProperties"] = self._max_properties
        if self._dependent_required is not None:
            result["dependentRequired"] = self._dependent_required
        if self._dependent_schemas is not None:
            result["dependentSchemas"] = {
                key: value.to_dict() for key, value in self._dependent_schemas.items()
            }
        if self._all_of is not None:
            result["allOf"] = [schema.to_dict() for schema in self._all_of]
        if self._any_of is not None:
            result["anyOf"] = [schema.to_dict() for schema in self._any_of]
        if self._one_of is not None:
            result["oneOf"] = [schema.to_dict() for schema in self._one_of]
        if self._not is not None:
            result["not"] = self._not.to_dict()
        if self._if is not None:
            result["if"] = self._if.to_dict()
        if self._then is not None:
            result["then"] = self._then.to_dict()
        if self._else is not None:
            result["else"] = self._else.to_dict()

        return result
