from lookup_models import Agreement, AgreementTemplate, EnrichedQuote, Quote

from app.client import contact_client, product_client
from app.common.quote_utils import extract_contact_ids, extract_product_ids
from app.transformer.quote_transformer import QuoteTransformer
from ..client.quote_client import QuoteClient
import structlog

logger = structlog.get_logger()


class QuoteService:
    def __init__(self, lookup_api_url: str = "http://localhost:8000"):
        self.quote_client = QuoteClient(lookup_api_url)
        self.product_client = product_client.ProductClient(lookup_api_url)
        self.contact_client = contact_client.ContactClient(lookup_api_url)
        self.quote_transformer = QuoteTransformer()

    async def create_agreement(
        self, quote_number: str, revision_number: int
    ) -> EnrichedQuote:
        """
        Lookup a quote using the quote client

        Args:
            quote_number: The quote number to look up
            revision_number: The revision number to look up

        Returns:
            Quote: The retrieved quote
        """
        logger.info(
            "Getting quote", quote_number=quote_number, revision_number=revision_number
        )
        quote = await self.quote_client.get_quote(quote_number, revision_number)
        logger.info("Quote retrieved successfully")
        logger.info("Starting quote enrichment process")

        product_ids = extract_product_ids(quote)
        contact_ids = extract_contact_ids(quote)

        products = {}
        for product_id in product_ids:
            product = await self.product_client.get_product(product_id)
            products[product_id] = product

        customer_contact = await self.contact_client.get_contact(
            contact_ids["customer_contact_id"]
        )
        sales_rep_contact = await self.contact_client.get_contact(
            contact_ids["sales_rep_id"]
        )

        return self.quote_transformer.to_enriched_quote(
            quote=quote,
            products=products,
            customer_contact=customer_contact,
            sales_rep_contact=sales_rep_contact,
        )
