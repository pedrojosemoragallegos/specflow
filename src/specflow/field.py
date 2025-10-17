from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypeVar, overload

from .core.types import Array, Boolean, Integer, Number, String

if TYPE_CHECKING:
    from specflow.core.schema import Schema

    from .core.types.constraints import Constraint

T = TypeVar("T", str, int, float, bool)


@overload
def Field(
    title: str,
    type_: Literal["string"],
    description: str | None = None,
    default: str | None = None,
    const: str | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    pattern: str | None = None,
    enum: list[str] | None = None,
    constraints: list[Constraint[str]] | None = None,
    *,
    nullable: bool = False,
) -> String: ...


@overload
def Field(
    title: str,
    type_: Literal["integer"],
    description: str | None = None,
    default: int | None = None,
    minimum: int | None = None,
    maximum: int | None = None,
    exclusive_minimum: int | None = None,
    exclusive_maximum: int | None = None,
    mult: int | None = None,
    constraints: list[Constraint[int]] | None = None,
    *,
    nullable: bool = False,
) -> Integer: ...


@overload
def Field(
    title: str,
    type_: Literal["number"],
    description: str | None = None,
    default: float | None = None,
    minimum: float | None = None,
    maximum: float | None = None,
    exclusive_minimum: float | None = None,
    excluvie_maximum: float | None = None,
    mult: float | None = None,
    constraints: list[Constraint[float]] | None = None,
    *,
    nullable: bool = False,
) -> Number: ...


@overload
def Field(
    title: str,
    type_: Literal["boolean"],
    description: str | None = None,
    constraints: list[Constraint[bool]] | None = None,
    *,
    nullable: bool = False,
    default: bool | None = None,
) -> Boolean: ...


@overload
def Field(
    title: str,
    type_: Literal["array"],
    description: str | None = None,
    min_items: int | None = None,
    max_items: int | None = None,
    min_contains: int | None = None,
    max_contains: int | None = None,
    items: String | Number | Integer | Boolean | Schema | None = None,
    prefix_items: list[String | Number | Integer | Boolean | Schema] | None = None,
    *,
    nullable: bool = False,
) -> Array: ...


# Inferred type overloads (when type_ is not provided)


# String inference - based on string-specific parameters
@overload
def Field(
    title: str,
    description: str | None = None,
    default: str | None = None,
    *,
    const: str,
    min_length: int | None = None,
    max_length: int | None = None,
    pattern: str | None = None,
    enum: list[str] | None = None,
    constraints: list[Constraint[str]] | None = None,
    nullable: bool = False,
) -> String: ...


@overload
def Field(
    title: str,
    description: str | None = None,
    default: str | None = None,
    const: str | None = None,
    *,
    min_length: int,
    max_length: int | None = None,
    pattern: str | None = None,
    enum: list[str] | None = None,
    constraints: list[Constraint[str]] | None = None,
    nullable: bool = False,
) -> String: ...


@overload
def Field(
    title: str,
    description: str | None = None,
    default: str | None = None,
    const: str | None = None,
    min_length: int | None = None,
    *,
    max_length: int,
    pattern: str | None = None,
    enum: list[str] | None = None,
    constraints: list[Constraint[str]] | None = None,
    nullable: bool = False,
) -> String: ...


@overload
def Field(
    title: str,
    description: str | None = None,
    default: str | None = None,
    const: str | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    *,
    pattern: str,
    enum: list[str] | None = None,
    constraints: list[Constraint[str]] | None = None,
    nullable: bool = False,
) -> String: ...


@overload
def Field(
    title: str,
    description: str | None = None,
    default: str | None = None,
    const: str | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    pattern: str | None = None,
    *,
    enum: list[str],
    constraints: list[Constraint[str]] | None = None,
    nullable: bool = False,
) -> String: ...


# Integer inference - based on integer-specific parameters
@overload
def Field(
    title: str,
    description: str | None = None,
    default: int | None = None,
    *,
    minimum: int,
    maximum: int | None = None,
    exclusive_minimum: int | None = None,
    exclusive_maximum: int | None = None,
    mult: int | None = None,
    constraints: list[Constraint[int]] | None = None,
    nullable: bool = False,
) -> Integer: ...


@overload
def Field(
    title: str,
    description: str | None = None,
    default: int | None = None,
    minimum: int | None = None,
    *,
    maximum: int,
    exclusive_minimum: int | None = None,
    exclusive_maximum: int | None = None,
    mult: int | None = None,
    constraints: list[Constraint[int]] | None = None,
    nullable: bool = False,
) -> Integer: ...


@overload
def Field(
    title: str,
    description: str | None = None,
    default: int | None = None,
    minimum: int | None = None,
    maximum: int | None = None,
    *,
    exclusive_minimum: int,
    exclusive_maximum: int | None = None,
    mult: int | None = None,
    constraints: list[Constraint[int]] | None = None,
    nullable: bool = False,
) -> Integer: ...


@overload
def Field(
    title: str,
    description: str | None = None,
    default: int | None = None,
    minimum: int | None = None,
    maximum: int | None = None,
    exclusive_minimum: int | None = None,
    *,
    exclusive_maximum: int,
    mult: int | None = None,
    constraints: list[Constraint[int]] | None = None,
    nullable: bool = False,
) -> Integer: ...


@overload
def Field(
    title: str,
    description: str | None = None,
    default: int | None = None,
    minimum: int | None = None,
    maximum: int | None = None,
    exclusive_minimum: int | None = None,
    exclusive_maximum: int | None = None,
    *,
    mult: int,
    constraints: list[Constraint[int]] | None = None,
    nullable: bool = False,
) -> Integer: ...


# Number/Float inference - based on float-specific parameters
@overload
def Field(
    title: str,
    description: str | None = None,
    default: float | None = None,
    *,
    minimum: float,
    maximum: float | None = None,
    exclusive_minimum: float | None = None,
    excluvie_maximum: float | None = None,
    mult: float | None = None,
    constraints: list[Constraint[float]] | None = None,
    nullable: bool = False,
) -> Number: ...


@overload
def Field(
    title: str,
    description: str | None = None,
    default: float | None = None,
    minimum: float | None = None,
    *,
    maximum: float,
    exclusive_minimum: float | None = None,
    excluvie_maximum: float | None = None,
    mult: float | None = None,
    constraints: list[Constraint[float]] | None = None,
    nullable: bool = False,
) -> Number: ...


@overload
def Field(
    title: str,
    description: str | None = None,
    default: float | None = None,
    minimum: float | None = None,
    maximum: float | None = None,
    *,
    exclusive_minimum: float,
    excluvie_maximum: float | None = None,
    mult: float | None = None,
    constraints: list[Constraint[float]] | None = None,
    nullable: bool = False,
) -> Number: ...


@overload
def Field(
    title: str,
    description: str | None = None,
    default: float | None = None,
    minimum: float | None = None,
    maximum: float | None = None,
    exclusive_minimum: float | None = None,
    *,
    excluvie_maximum: float,
    mult: float | None = None,
    constraints: list[Constraint[float]] | None = None,
    nullable: bool = False,
) -> Number: ...


@overload
def Field(
    title: str,
    description: str | None = None,
    default: float | None = None,
    minimum: float | None = None,
    maximum: float | None = None,
    exclusive_minimum: float | None = None,
    excluvie_maximum: float | None = None,
    *,
    mult: float,
    constraints: list[Constraint[float]] | None = None,
    nullable: bool = False,
) -> Number: ...


# Array inference - based on array-specific parameters
@overload
def Field(
    title: str,
    description: str | None = None,
    *,
    min_items: int,
    max_items: int | None = None,
    min_contains: int | None = None,
    max_contains: int | None = None,
    items: String | Number | Integer | Boolean | Schema | None = None,
    prefix_items: list[String | Number | Integer | Boolean | Schema] | None = None,
    nullable: bool = False,
) -> Array: ...


@overload
def Field(
    title: str,
    description: str | None = None,
    min_items: int | None = None,
    *,
    max_items: int,
    min_contains: int | None = None,
    max_contains: int | None = None,
    items: String | Number | Integer | Boolean | Schema | None = None,
    prefix_items: list[String | Number | Integer | Boolean | Schema] | None = None,
    nullable: bool = False,
) -> Array: ...


@overload
def Field(
    title: str,
    description: str | None = None,
    min_items: int | None = None,
    max_items: int | None = None,
    *,
    min_contains: int,
    max_contains: int | None = None,
    items: String | Number | Integer | Boolean | Schema | None = None,
    prefix_items: list[String | Number | Integer | Boolean | Schema] | None = None,
    nullable: bool = False,
) -> Array: ...


@overload
def Field(
    title: str,
    description: str | None = None,
    min_items: int | None = None,
    max_items: int | None = None,
    min_contains: int | None = None,
    *,
    max_contains: int,
    items: String | Number | Integer | Boolean | Schema | None = None,
    prefix_items: list[String | Number | Integer | Boolean | Schema] | None = None,
    nullable: bool = False,
) -> Array: ...


@overload
def Field(
    title: str,
    description: str | None = None,
    min_items: int | None = None,
    max_items: int | None = None,
    min_contains: int | None = None,
    max_contains: int | None = None,
    *,
    items: String | Number | Integer | Boolean | Schema,
    prefix_items: list[String | Number | Integer | Boolean | Schema] | None = None,
    nullable: bool = False,
) -> Array: ...


@overload
def Field(
    title: str,
    description: str | None = None,
    min_items: int | None = None,
    max_items: int | None = None,
    min_contains: int | None = None,
    max_contains: int | None = None,
    items: String | Number | Integer | Boolean | Schema | None = None,
    *,
    prefix_items: list[String | Number | Integer | Boolean | Schema],
    nullable: bool = False,
) -> Array: ...


# Implementation
def Field(
    title: str,
    type_: Literal["string", "integer", "number", "boolean", "array"] | None = None,
    description: str | None = None,
    default: str | float | bool | None = None,
    # String specific
    const: str | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    pattern: str | None = None,
    enum: list[str] | None = None,
    # Integer specific
    minimum: float | None = None,
    maximum: float | None = None,
    exclusive_minimum: float | None = None,
    exclusive_maximum: float | None = None,
    mult: float | None = None,
    # Number specific (uses same params as integer but with float types)
    excluvie_maximum: float | None = None,
    # Array specific
    min_items: int | None = None,
    max_items: int | None = None,
    min_contains: int | None = None,
    max_contains: int | None = None,
    items: String | Number | Integer | Boolean | Schema | None = None,
    prefix_items: list[String | Number | Integer | Boolean | Schema] | None = None,
    # Generic
    constraints: list[Constraint] | None = None,  # type: ignore
    nullable: bool = False,
) -> String | Integer | Number | Boolean | Array:
    # If type is explicitly provided, use it
    if type_ == "string":
        return String(
            title=title,
            description=description,
            default=default,  # type: ignore
            const=const,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            enum=enum,
            constraints=constraints,  # type: ignore
            nullable=nullable,
        )
    if type_ == "integer":
        return Integer(
            title=title,
            description=description,
            default=default,  # type: ignore
            minimum=minimum,  # type: ignore
            maximum=maximum,  # type: ignore
            exclusive_minimum=exclusive_minimum,  # type: ignore
            exclusive_maximum=exclusive_maximum,  # type: ignore
            mult=mult,  # type: ignore
            constraints=constraints,  # type: ignore
            nullable=nullable,
        )
    if type_ == "number":
        return Number(
            title=title,
            description=description,
            default=default,  # type: ignore
            minimum=minimum,  # type: ignore
            maximum=maximum,  # type: ignore
            exclusive_minimum=exclusive_minimum,  # type: ignore
            excluvie_maximum=excluvie_maximum or exclusive_maximum,  # type: ignore
            mult=mult,  # type: ignore
            constraints=constraints,  # type: ignore
            nullable=nullable,
        )
    if type_ == "boolean":
        return Boolean(
            title=title,
            description=description,
            default=default,  # type: ignore
            constraints=constraints,  # type: ignore
            nullable=nullable,
        )
    if type_ == "array":
        return Array(
            title=title,
            description=description,
            min_items=min_items,
            max_items=max_items,
            min_contains=min_contains,
            max_contains=max_contains,
            items=items,
            prefix_items=prefix_items,
            nullable=nullable,
        )

    # Infer type based on parameters provided
    # String-specific parameters
    if any([const, min_length, max_length, pattern, enum]):
        return String(
            title=title,
            description=description,
            default=default,  # type: ignore
            const=const,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            enum=enum,
            constraints=constraints,  # type: ignore
            nullable=nullable,
        )

    # Array-specific parameters
    if any([min_items, max_items, min_contains, max_contains, items, prefix_items]):
        return Array(
            title=title,
            description=description,
            min_items=min_items,
            max_items=max_items,
            min_contains=min_contains,
            max_contains=max_contains,
            items=items,
            prefix_items=prefix_items,
            nullable=nullable,
        )

    # Check if parameters suggest float (Number) vs int (Integer)
    # If any parameter is explicitly a float, use Number
    if any(
        isinstance(val, float)
        for val in [
            default,
            minimum,
            maximum,
            exclusive_minimum,
            exclusive_maximum,
            excluvie_maximum,
            mult,
        ]
        if val is not None
    ):
        return Number(
            title=title,
            description=description,
            default=default,  # type: ignore
            minimum=minimum,  # type: ignore
            maximum=maximum,  # type: ignore
            exclusive_minimum=exclusive_minimum,  # type: ignore
            excluvie_maximum=excluvie_maximum or exclusive_maximum,  # type: ignore
            mult=mult,  # type: ignore
            constraints=constraints,  # type: ignore
            nullable=nullable,
        )

    # Integer-specific parameters (or integer default)
    if any(
        [minimum, maximum, exclusive_minimum, exclusive_maximum, mult],
    ) or isinstance(
        default,
        int,
    ):
        return Integer(
            title=title,
            description=description,
            default=default,  # type: ignore
            minimum=minimum,  # type: ignore
            maximum=maximum,  # type: ignore
            exclusive_minimum=exclusive_minimum,  # type: ignore
            exclusive_maximum=exclusive_maximum,  # type: ignore
            mult=mult,  # type: ignore
            constraints=constraints,  # type: ignore
            nullable=nullable,
        )

    # If default is a bool, infer Boolean
    if isinstance(default, bool):
        return Boolean(
            title=title,
            description=description,
            default=default,
            constraints=constraints,  # type: ignore
            nullable=nullable,
        )

    # If default is a string, infer String
    if isinstance(default, str):
        return String(
            title=title,
            description=description,
            default=default,
            constraints=constraints,  # type: ignore
            nullable=nullable,
        )

    # Default to String if no type can be inferred
    return String(
        title=title,
        description=description,
        default=default,  # type: ignore
        constraints=constraints,  # type: ignore
        nullable=nullable,
    )
