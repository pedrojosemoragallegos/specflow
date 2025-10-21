# SpecFlow

A modern, type-safe Python library for JSON Schema validation with a fluent, composable API. SpecFlow provides an intuitive way to define, validate, and serialize JSON schemas programmatically.

## Features

- **Type-Safe Validation** - Built with Python type hints for better IDE support and type checking
- **Composable Schemas** - Combine schemas using `AnyOf`, `OneOf`, and `Not` compositions
- **Conditional Logic** - Define conditional validation rules with `if/then/else` conditions
- **Rich Constraints** - Support for string patterns, numeric ranges, array constraints, and more
- **Clear Error Messages** - Descriptive validation errors with path information
- **JSON Schema Compatible** - Export schemas to JSON Schema format

## Installation

```bash
pip install specflow
```

## Quick Start

```python
from specflow import Schema, Field

# Define a user schema
user_schema = Schema(
    title="User",
    description="A user object",
    properties=[
        Field(
            title="username",
            description="User's username",
            min_length=3,
            max_length=20,
            pattern=r"^[a-zA-Z0-9_]+$"
        ),
        Field(
            title="email",
            description="User's email address",
            pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        ),
        Field(
            title="age",
            description="User's age",
            minimum=0,
            maximum=150,
            default=25  # int default infers Integer type
        ),
        Field(
            title="is_active",
            description="Whether the user account is active",
            default=True  # bool default infers Boolean type
        )
    ]
)

# Validate data
data = {
    "username": "john_doe",
    "email": "john@example.com",
    "age": 25,
    "is_active": True
}

try:
    user_schema(data)
    print("✓ Validation passed!")
except ValidationError as e:
    print(f"✗ Validation failed: {e}")
```

## Core Components

### Field Function with Type Inference

SpecFlow provides a smart `Field()` function that automatically infers the field type based on the parameters you provide. You can also explicitly specify the type using the `type_` parameter.

#### Automatic Type Inference

The `Field()` function infers the type based on:

- **String-specific parameters**: `min_length`, `max_length`, `pattern`, `enum`, `const`, or a `str` default
- **Integer-specific parameters**: numeric constraints with an `int` default
- **Number (Float) parameters**: numeric constraints with a `float` default  
- **Boolean**: a `bool` default value
- **Array-specific parameters**: `min_items`, `max_items`, `items`, `prefix_items`

#### String Fields

```python
from specflow import Field

# Inferred as String due to string-specific parameters
Field(
    title="username",
    description="User's username",
    min_length=3,
    max_length=20,
    pattern=r"^[a-zA-Z0-9_]+$"
)

# With enum
Field(
    title="role",
    enum=["admin", "user", "guest"]
)

# With const
Field(
    title="version",
    const="1.0.0"
)

# Explicit type
Field(
    title="name",
    type_="string",
    default="Anonymous"
)
```

#### Integer Fields

```python
from specflow import Field

# Inferred as Integer due to int default
Field(
    title="age",
    minimum=0,
    maximum=150,
    default=25  # int default
)

# With multiple of constraint
Field(
    title="quantity",
    minimum=1,
    mult=5,  # Must be multiple of 5
    default=10
)

# Explicit type
Field(
    title="count",
    type_="integer",
    minimum=0
)
```

#### Number (Float) Fields

```python
from specflow import Field

# Inferred as Number due to float default
Field(
    title="price",
    minimum=0.0,
    maximum=999.99,
    default=19.99  # float default
)

# With precision constraint
Field(
    title="rating",
    minimum=0.0,
    maximum=5.0,
    mult=0.5,  # Increments of 0.5
    default=4.5
)

# Explicit type
Field(
    title="temperature",
    type_="number",
    minimum=-273.15
)
```

#### Boolean Fields

```python
from specflow import Field

# Inferred as Boolean due to bool default
Field(
    title="is_active",
    default=True
)

# Explicit type
Field(
    title="enabled",
    type_="boolean",
    default=False
)
```

### Arrays

```python
from specflow import Field

# Array with single item type (inferred as Array due to items parameter)
Field(
    title="tags",
    items=Field(title="tag", type_="string"),
    min_items=1,
    max_items=10
)

# Array with tuple validation (prefix items)
Field(
    title="coordinates",
    prefix_items=[
        Field(title="latitude", type_="number"),
        Field(title="longitude", type_="number")
    ]
)

# Mixed array with prefix items and additional items
Field(
    title="mixed",
    prefix_items=[
        Field(title="name", type_="string"),
        Field(title="age", default=0)  # Integer inferred
    ],
    items=Field(title="flags", default=False)  # Boolean inferred
)

# Explicit type
Field(
    title="numbers",
    type_="array",
    items=Field(title="num", default=0)
)
```

### Schemas

Schemas are composite objects that group multiple properties:

```python
from specflow import Schema, Field

address_schema = Schema(
    title="Address",
    properties=[
        Field(title="street", type_="string"),
        Field(title="city", type_="string"),
        Field(title="zipcode", pattern=r"^\d{5}$")
    ]
)

# Nested schemas
user_schema = Schema(
    title="User",
    properties=[
        Field(title="name", type_="string"),
        address_schema  # Nested schema
    ]
)
```

### Compositions

#### AnyOf

Validates if the data matches **at least one** of the specified schemas:

```python
from specflow import AnyOf, Schema, Field

contact_schema = Schema(
    title="Contact",
    properties=[
        Field(title="name", type_="string"),
        AnyOf(
            Field(title="email", type_="string"),
            Field(title="phone", type_="string")
        )
    ]
)

# Valid: has name and email
data1 = {"name": "John", "email": "john@example.com"}

# Valid: has name and phone
data2 = {"name": "Jane", "phone": "+1234567890"}

# Valid: has all three
data3 = {"name": "Bob", "email": "bob@example.com", "phone": "+1234567890"}
```

#### OneOf

Validates if the data matches **exactly one** of the specified schemas:

```python
from specflow import OneOf, Field

payment_method = OneOf(
    Field(title="credit_card", type_="string"),
    Field(title="paypal_email", type_="string"),
    Field(title="bank_account", type_="string")
)

# Valid: exactly one payment method
data = {"credit_card": "4111-1111-1111-1111"}

# Invalid: multiple payment methods
invalid_data = {
    "credit_card": "4111-1111-1111-1111",
    "paypal_email": "user@example.com"
}
```

#### Not

Validates if the data **does not** match the specified schema:

```python
from specflow import Not, Schema, Field

schema = Schema(
    title="Example",
    properties=[
        Field(title="username", type_="string"),
        Not(
            Field(title="banned_word", const="admin")
        )
    ]
)
```

### Conditions

Define conditional validation rules with if/then/else logic:

```python
from specflow import Schema, Condition, Field

# If country is "US", then require state; otherwise require province
address_schema = Schema(
    title="Address",
    properties=[
        Field(title="country", type_="string"),
        Field(title="state", type_="string", nullable=True),
        Field(title="province", type_="string", nullable=True)
    ],
    conditions=[
        Condition(
            if_=Field(title="country", const="US"),
            then_=Field(title="state", min_length=2),
            else_=Field(title="province", min_length=1)
        )
    ]
)
```

## Validation

### Basic Validation

```python
try:
    schema(data)
    print("Validation passed!")
except ValidationError as e:
    print(f"Validation error: {e}")
```

### Strict vs Non-Strict Mode

```python
# Strict mode (default): extra fields not allowed
schema(data, strict=True)

# Non-strict mode: extra fields allowed
schema(data, strict=False)
```

### Error Paths

SpecFlow provides detailed error paths for nested validation failures:

```python
from specflow import Schema, Field

schema = Schema(
    title="User",
    properties=[
        Field(title="name", type_="string"),
        Field(
            title="addresses",
            items=Schema(
                title="Address",
                properties=[
                    Field(title="street", type_="string"),
                    Field(title="zipcode", pattern=r"^\d{5}$")
                ]
            )
        )
    ]
)

data = {
    "name": "John",
    "addresses": [
        {"street": "123 Main St", "zipcode": "12345"},
        {"street": "456 Oak Ave", "zipcode": "INVALID"}
    ]
}

try:
    schema(data)
except ValidationError as e:
    print(e)
    # Output: Validation failed at addresses[1].zipcode: Must match pattern: ^\d{5}$, got INVALID
```

## Schema Export

Export schemas to JSON Schema format:

```python
schema_dict = schema.to_dict()
print(schema_dict)
```

## Advanced Examples

### E-commerce Product Schema

```python
from specflow import Schema, OneOf, Field

product_schema = Schema(
    title="Product",
    description="E-commerce product",
    properties=[
        Field(
            title="id",
            pattern=r"^PRD-\d{6}$"
        ),
        Field(
            title="name",
            min_length=3,
            max_length=100
        ),
        Field(
            title="description",
            max_length=1000
        ),
        Field(
            title="price",
            minimum=0.01,
            mult=0.01,
            default=0.0  # Float default infers Number
        ),
        Field(
            title="stock",
            minimum=0,
            default=0  # Int default infers Integer
        ),
        Field(
            title="categories",
            items=Field(title="category", type_="string"),
            min_items=1,
            max_items=5
        ),
        Field(
            title="tags",
            items=Field(title="tag", type_="string"),
            max_items=10
        ),
        Field(
            title="in_stock",
            default=True
        ),
        OneOf(
            Field(title="color", type_="string"),
            Field(title="size", type_="string"),
            Field(title="material", type_="string")
        )
    ]
)
```

### API Response Schema with Conditions

```python
from specflow import Schema, Condition, Field

api_response = Schema(
    title="APIResponse",
    properties=[
        Field(title="status_code", default=200),
        Field(title="success", default=True),
        Field(title="message", type_="string", nullable=True),
        Field(title="data", type_="string", nullable=True),
        Field(title="error", type_="string", nullable=True)
    ],
    conditions=[
        Condition(
            if_=Field(title="success", default=True),
            then_=Field(title="data", min_length=1),
            else_=Field(title="error", min_length=1)
        )
    ]
)
```

## Error Handling

SpecFlow raises `ValidationError` exceptions with detailed information:

```python
from specflow.core.exceptions import ValidationError

try:
    schema(data)
except ValidationError as e:
    print(f"Message: {e.message}")
    print(f"Path: {e.path}")
    print(f"Full error: {e}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/yourusername/specflow).
