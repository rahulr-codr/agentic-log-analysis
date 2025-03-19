from typing import Dict, Any, List
from lookup_models import Quote, EnrichedQuote, EnrichedQuoteItem, Product, Contact


class QuoteTransformer:
    @staticmethod
    def to_enriched_quote(
        quote: Quote,
        products: Dict[str, Product],
        customer_contact: Contact,
        sales_rep_contact: Contact,
    ) -> EnrichedQuote:
        """
        Transform a Quote into an EnrichedQuote with product and contact details

        Args:
            quote: The base Quote object
            product_map: Dictionary mapping product_id to Product objects
            customer_contact: Customer contact details
            sales_rep_contact: Sales representative contact details

        Returns:
            EnrichedQuote: The enriched quote object
        """
        # Create enriched quote items with product details
        enriched_items = []
        for item in quote.items:
            product = products.get(item.product_id)
            enriched_item = EnrichedQuoteItem(**item.model_dump(), product=product)
            enriched_items.append(enriched_item)

        # Create and return the enriched quote
        return EnrichedQuote(
            quote_number=quote.quote_number,
            revision_number=quote.revision_number,
            status=quote.status,
            created_at=quote.created_at,
            updated_at=quote.updated_at,
            valid_until=quote.valid_until,
            customer=quote.customer,
            sales_rep=quote.sales_rep,
            opportunity=quote.opportunity,
            items=enriched_items,
            bundle=quote.bundle,
            totals=quote.totals,
            terms_and_conditions=quote.terms_and_conditions,
            metadata=quote.metadata,
            customer_contact=customer_contact,
            sales_rep_contact=sales_rep_contact,
        )
