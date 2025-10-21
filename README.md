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
from specflow import Schema
from specflow.types import String, Integer, Boolean, Array

# Define a user schema
user_schema = Schema(
    title="User",
    description="A user object",
    properties=[
        String(
            title="username",
            description="User's username",
            min_length=3,
            max_length=20,
            pattern=r"^[a-zA-Z0-9_]+$"
        ),
        String(
            title="email",
            description="User's email address",
            pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        ),
        Integer(
            title="age",
            description="User's age",
            minimum=0,
            maximum=150
        ),
        Boolean(
            title="is_active",
            description="Whether the user account is active",
            default=True
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

### Types

SpecFlow provides four primitive types:

#### String

```python
from specflow.types import String

String(
    title="username",
    description="User's username",
    min_length=3,
    max_length=20,
    pattern=r"^[a-zA-Z0-9_]+$",
    enum=["admin", "user", "guest"],  # Optional
    const="fixed_value",  # Optional
    nullable=False
)
```

#### Integer

```python
from specflow.types import Integer

Integer(
    title="age",
    minimum=0,
    maximum=150,
    exclusive_minimum=0,  # > 0
    exclusive_maximum=100,  # < 100
    mult=5,  # Multiple of 5
    nullable=False
)
```

#### Number (Float)

```python
from specflow.types import Number

Number(
    title="price",
    minimum=0.0,
    maximum=999.99,
    exclusive_minimum=0.0,
    mult=0.01,  # Precision to 2 decimal places
    nullable=False
)
```

#### Boolean

```python
from specflow.types import Boolean

Boolean(
    title="is_active",
    default=True,
    nullable=False
)
```

### Arrays

```python
from specflow.types import Array, String, Integer

# Array with single item type
Array(
    title="tags",
    items=String(title="tag"),
    min_items=1,
    max_items=10
)

# Array with tuple validation (prefix items)
Array(
    title="coordinates",
    prefix_items=[
        Number(title="latitude"),
        Number(title="longitude")
    ]
)

# Mixed array with prefix items and additional items
Array(
    title="mixed",
    prefix_items=[
        String(title="name"),
        Integer(title="age")
    ],
    items=Boolean(title="flags")  # Additional items must be boolean
)
```

### Schemas

Schemas are composite objects that group multiple properties:

```python
from specflow import Schema
from specflow.types import String, Integer

address_schema = Schema(
    title="Address",
    properties=[
        String(title="street"),
        String(title="city"),
        String(title="zipcode", pattern=r"^\d{5}$")
    ]
)

# Nested schemas
user_schema = Schema(
    title="User",
    properties=[
        String(title="name"),
        address_schema  # Nested schema
    ]
)
```

### Compositions

#### AnyOf

Validates if the data matches **at least one** of the specified schemas:

```python
from specflow import AnyOf, Schema
from specflow.types import String, Integer

contact_schema = Schema(
    title="Contact",
    properties=[
        String(title="name"),
        AnyOf(
            String(title="email"),
            String(title="phone")
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
from specflow import OneOf
from specflow.types import String, Integer

payment_method = OneOf(
    String(title="credit_card"),
    String(title="paypal_email"),
    String(title="bank_account")
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
from specflow import Not, Schema
from specflow.types import String

schema = Schema(
    title="Example",
    properties=[
        String(title="username"),
        Not(
            String(title="banned_word", const="admin")
        )
    ]
)
```

### Conditions

Define conditional validation rules with if/then/else logic:

```python
from specflow import Schema, Condition
from specflow.types import String, Integer

# If country is "US", then require state; otherwise require province
address_schema = Schema(
    title="Address",
    properties=[
        String(title="country"),
        String(title="state", nullable=True),
        String(title="province", nullable=True)
    ],
    conditions=[
        Condition(
            if_=String(title="country", const="US"),
            then_=String(title="state", min_length=2),
            else_=String(title="province", min_length=1)
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
from specflow import Schema
from specflow.types import String, Integer, Array

schema = Schema(
    title="User",
    properties=[
        String(title="name"),
        Array(
            title="addresses",
            items=Schema(
                title="Address",
                properties=[
                    String(title="street"),
                    String(title="zipcode", pattern=r"^\d{5}$")
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
from specflow import Schema, OneOf, AnyOf
from specflow.types import String, Number, Integer, Array, Boolean

product_schema = Schema(
    title="Product",
    description="E-commerce product",
    properties=[
        String(
            title="id",
            pattern=r"^PRD-\d{6}$"
        ),
        String(
            title="name",
            min_length=3,
            max_length=100
        ),
        String(
            title="description",
            max_length=1000
        ),
        Number(
            title="price",
            minimum=0.01,
            mult=0.01
        ),
        Integer(
            title="stock",
            minimum=0
        ),
        Array(
            title="categories",
            items=String(title="category"),
            min_items=1,
            max_items=5
        ),
        Array(
            title="tags",
            items=String(title="tag"),
            max_items=10
        ),
        Boolean(
            title="in_stock",
            default=True
        ),
        OneOf(
            String(title="color"),
            String(title="size"),
            String(title="material")
        )
    ]
)
```

### API Response Schema with Conditions

```python
from specflow import Schema, Condition, AnyOf
from specflow.types import String, Integer, Boolean

api_response = Schema(
    title="APIResponse",
    properties=[
        Integer(title="status_code"),
        Boolean(title="success"),
        String(title="message", nullable=True),
        String(title="data", nullable=True),
        String(title="error", nullable=True)
    ],
    conditions=[
        Condition(
            if_=Boolean(title="success", const=True),
            then_=String(title="data", min_length=1),
            else_=String(title="error", min_length=1)
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
