from __future__ import annotations

from typing import TYPE_CHECKING

from .schema import Schema

if TYPE_CHECKING:
    from specflow.typing import JSONValue


class ArraySchema(Schema):
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
        items: Schema | list[Schema] | None = None,
        prefix_items: list[Schema] | None = None,
        contains: Schema | None = None,
        min_items: int | None = None,
        max_items: int | None = None,
        min_contains: int | None = None,
        max_contains: int | None = None,
        all_of: list[ArraySchema] | None = None,
        any_of: list[ArraySchema] | None = None,
        one_of: list[ArraySchema] | None = None,
        not_: ArraySchema | None = None,
        if_: ArraySchema | None = None,
        then: ArraySchema | None = None,
        else_: ArraySchema | None = None,
        *,
        unique_items: bool | None = None,
        unevaluated_items: Schema | bool | None = None,
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

        if items is not None:
            if isinstance(items, list):
                for item in items:
                    if not isinstance(item, Schema):  # type: ignore
                        raise TypeError(
                            "All items in 'items' list must be Schema instances",
                        )
            elif not isinstance(items, Schema):  # type: ignore
                raise TypeError(
                    "items must be a Schema instance or list of Schema instances",
                )

        if prefix_items is not None:
            if not isinstance(prefix_items, list):  # type: ignore
                raise TypeError("prefixItems must be a list")
            for item in prefix_items:
                if not isinstance(item, Schema):  # type: ignore
                    raise TypeError("All items in prefixItems must be Schema instances")

        if contains is not None:  # noqa: SIM102
            if not isinstance(contains, Schema):  # type: ignore
                raise TypeError("contains must be a Schema instance")

        if min_items is not None:
            if not isinstance(min_items, int):  # type: ignore
                raise TypeError("minItems must be an integer")
            if min_items < 0:
                raise ValueError("minItems must be non-negative")

        if max_items is not None:
            if not isinstance(max_items, int):  # type: ignore
                raise TypeError("maxItems must be an integer")
            if max_items < 0:
                raise ValueError("maxItems must be non-negative")

        if (min_items is not None) and (max_items is not None):  # noqa: SIM102
            if min_items > max_items:
                raise ValueError("minItems cannot be greater than maxItems")

        if min_contains is not None:
            if not isinstance(min_contains, int):  # type: ignore
                raise TypeError("minContains must be an integer")
            if min_contains < 0:
                raise ValueError("minContains must be non-negative")
            if contains is None:
                raise ValueError("minContains requires contains to be specified")

        if max_contains is not None:
            if not isinstance(max_contains, int):  # type: ignore
                raise TypeError("maxContains must be an integer")
            if max_contains < 0:
                raise ValueError("maxContains must be non-negative")
            if contains is None:
                raise ValueError("maxContains requires contains to be specified")

        if (min_contains is not None) and (max_contains is not None):  # noqa: SIM102
            if min_contains > max_contains:
                raise ValueError("minContains cannot be greater than maxContains")

        if unique_items is not None:  # noqa: SIM102
            if not isinstance(unique_items, bool):  # type: ignore
                raise TypeError("uniqueItems must be a boolean")

        if unevaluated_items is not None:  # noqa: SIM102
            if not isinstance(unevaluated_items, (Schema, bool)):  # type: ignore
                raise TypeError("unevaluatedItems must be a Schema instance or boolean")

        if all_of is not None:
            if not isinstance(all_of, list):  # type: ignore
                raise TypeError("allOf must be a list")
            if not all_of:
                raise ValueError("allOf must contain at least one schema")
            for schema_item in all_of:
                if not isinstance(schema_item, ArraySchema):  # type: ignore
                    raise TypeError("All allOf items must be ArraySchema instances")

        if any_of is not None:
            if not isinstance(any_of, list):  # type: ignore
                raise TypeError("anyOf must be a list")
            if not any_of:
                raise ValueError("anyOf must contain at least one schema")
            for schema_item in any_of:
                if not isinstance(schema_item, ArraySchema):  # type: ignore
                    raise TypeError("All anyOf items must be ArraySchema instances")

        if one_of is not None:
            if not isinstance(one_of, list):  # type: ignore
                raise TypeError("oneOf must be a list")
            if not one_of:
                raise ValueError("oneOf must contain at least one schema")
            for schema_item in one_of:
                if not isinstance(schema_item, ArraySchema):  # type: ignore
                    raise TypeError("All oneOf items must be ArraySchema instances")

        if not_ is not None:  # noqa: SIM102
            if not isinstance(not_, ArraySchema):  # type: ignore
                raise TypeError("not must be an ArraySchema instance")

        if (then is not None or else_ is not None) and if_ is None:
            raise ValueError("'then' and 'else' require 'if' to be specified")

        if if_ is not None:  # noqa: SIM102
            if not isinstance(if_, ArraySchema):  # type: ignore
                raise TypeError("if must be an ArraySchema instance")

        if then is not None:  # noqa: SIM102
            if not isinstance(then, ArraySchema):  # type: ignore
                raise TypeError("then must be an ArraySchema instance")

        if else_ is not None:  # noqa: SIM102
            if not isinstance(else_, ArraySchema):  # type: ignore
                raise TypeError("else must be an ArraySchema instance")

        self._items = items
        self._prefix_items = prefix_items
        self._contains = contains
        self._min_items = min_items
        self._max_items = max_items
        self._min_contains = min_contains
        self._max_contains = max_contains
        self._unique_items = unique_items
        self._unevaluated_items = unevaluated_items
        self._all_of = all_of
        self._any_of = any_of
        self._one_of = one_of
        self._not = not_
        self._if = if_
        self._then = then
        self._else = else_

    def to_dict(self) -> dict[str, JSONValue]:  # noqa: C901, PLR0912
        result: dict[str, JSONValue] = super().to_dict()

        result["type"] = "array"

        if self._items is not None:
            if isinstance(self._items, list):
                result["items"] = [item.to_dict() for item in self._items]
            else:
                result["items"] = self._items.to_dict()
        if self._prefix_items is not None:
            result["prefixItems"] = [item.to_dict() for item in self._prefix_items]
        if self._contains is not None:
            result["contains"] = self._contains.to_dict()
        if self._min_items is not None:
            result["minItems"] = self._min_items
        if self._max_items is not None:
            result["maxItems"] = self._max_items
        if self._min_contains is not None:
            result["minContains"] = self._min_contains
        if self._max_contains is not None:
            result["maxContains"] = self._max_contains
        if self._unique_items is not None:
            result["uniqueItems"] = self._unique_items
        if self._unevaluated_items is not None:
            if isinstance(self._unevaluated_items, bool):
                result["unevaluatedItems"] = self._unevaluated_items
            else:
                result["unevaluatedItems"] = self._unevaluated_items.to_dict()
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
