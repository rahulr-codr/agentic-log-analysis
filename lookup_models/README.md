# Lookup Models

This package contains the Pydantic models used by the lookup service. It includes models for:

- Customers
- Sales Representatives
- Opportunities
- Quotes and Quote Items
- Products and Product Configurations
- Contacts and Addresses

## Installation

Using `uv`:

```bash
uv pip install lookup-models
```

## Usage

```python
from lookup_models import Customer, Quote, Product

# Create instances of the models
customer = Customer(
    id="123",
    contact_id="456",
    account_id="789"
)
```

## Development

To build the package:

```bash
uv pip install build
python -m build
``` 