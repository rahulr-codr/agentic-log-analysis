from lookup_models import Quote


def extract_product_ids(quote: Quote) -> set[str]:
    """
    Extract all unique product IDs from a quote.

    Args:
        quote: The Quote object to extract from

    Returns:
        set[str]: Set of unique product IDs referenced in the quote
    """
    return {item.product_id for item in quote.items}


def extract_contact_ids(quote: Quote) -> dict[str, str]:
    """
    Extract all contact IDs from a quote.

    Args:
        quote: The Quote object to extract from

    Returns:
        dict[str, str]: Dictionary containing:
            - 'customer_contact_id': The customer's contact ID
            - 'sales_rep_id': The sales rep's contact ID
    """
    return {
        "customer_contact_id": quote.customer.contact_id,
        "sales_rep_id": quote.sales_rep.id,
    }
