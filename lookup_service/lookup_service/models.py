from pydantic import BaseModel, Field, RootModel
from typing import Optional, List, Dict, Any, Union
from datetime import datetime


class Customer(BaseModel):
    id: str
    contact_id: str
    account_id: str
    billing_address_id: Optional[str] = None
    shipping_address_id: Optional[str] = None


class SalesRep(BaseModel):
    id: str
    name: str
    email: str


class Opportunity(BaseModel):
    id: str
    name: str


class ItemConfiguration(RootModel):
    # Using a dynamic model since configuration varies by item type
    root: Dict[str, Any]


class QuoteItem(BaseModel):
    line_number: int
    product_id: str
    quantity: int
    unit_price: float
    discount_percentage: float
    term_months: Optional[int] = None
    billing_frequency: Optional[str] = None
    configuration: ItemConfiguration


class Totals(BaseModel):
    subtotal: float
    discount_amount: Optional[float] = None
    tax_amount: float
    total: float
    shipping_amount: Optional[float] = None
    monthly_recurring: Optional[Dict[str, float]] = None
    total_contract_value: Optional[float] = None
    list_price: Optional[float] = None
    bundle_discount: Optional[float] = None
    additional_discount: Optional[float] = None
    annual_recurring: Optional[float] = None


class TermsAndConditions(BaseModel):
    payment_terms: str
    delivery_terms: Optional[str] = None
    special_terms: Optional[str] = None
    warranty_terms: Optional[str] = None
    return_policy: Optional[str] = None
    service_level_agreement: Optional[str] = None
    usage_terms: Optional[str] = None
    data_processing_terms: Optional[str] = None
    expenses: Optional[str] = None
    cancellation_terms: Optional[str] = None
    intellectual_property: Optional[str] = None
    hardware_delivery: Optional[str] = None
    training_validity: Optional[str] = None
    sla_terms: Optional[str] = None


class Metadata(BaseModel):
    currency: str
    locale: str
    timezone: str
    deal_type: Optional[str] = None


class Quote(BaseModel):
    quote_number: str
    revision_number: int
    status: str
    created_at: datetime
    updated_at: datetime
    valid_until: datetime
    customer: Customer
    sales_rep: SalesRep
    opportunity: Opportunity
    items: List[QuoteItem]
    totals: Totals
    terms_and_conditions: TermsAndConditions
    metadata: Metadata
    # Optional fields for different quote types
    shipping: Optional[Dict[str, Any]] = None
    project: Optional[Dict[str, Any]] = None
    subscription: Optional[Dict[str, Any]] = None
    bundle: Optional[Dict[str, Any]] = None


# Product-related models
class VolumeDiscount(BaseModel):
    min_quantity: int
    discount_percentage: float


class WarrantyOption(BaseModel):
    duration: str
    price: float


class Edition(BaseModel):
    name: str
    features: List[str]
    min_users: Optional[int] = None
    max_users: Optional[int] = None
    storage_included: Optional[str] = None


class ProductPricing(BaseModel):
    base_price: float
    unit: Optional[str] = None
    volume_discounts: Optional[List[VolumeDiscount]] = None
    warranty_options: Optional[List[WarrantyOption]] = None
    installation_included: Optional[bool] = None
    subscription_required: Optional[bool] = None
    minimum_term: Optional[int] = None
    billing_frequency: Optional[List[str]] = None


class HardwareSpecifications(BaseModel):
    processor: Optional[str] = None
    ram_options: Optional[List[str]] = None
    storage_options: Optional[List[str]] = None
    form_factor: Optional[str] = None
    power_supply: Optional[str] = None
    capacity_options: Optional[List[str]] = None
    raid_support: Optional[List[str]] = None
    connectivity: Optional[List[str]] = None
    throughput: Optional[str] = None
    concurrent_sessions: Optional[int] = None
    interfaces: Optional[List[str]] = None
    redundancy: Optional[List[str]] = None


class ServiceDetails(BaseModel):
    duration_days: Optional[Dict[str, int]] = None
    technicians: Optional[Dict[str, int]] = None


class SubscriptionFeatures(BaseModel):
    tiers: Optional[List[Dict[str, Any]]] = None
    usage_limits: Optional[Dict[str, Any]] = None


class Product(BaseModel):
    id: str
    name: str
    type: str
    category: str
    description: str
    status: str
    editions: Optional[List[Edition]] = None
    features: Optional[Union[List[str], Dict[str, Any]]] = None
    specifications: Optional[HardwareSpecifications] = None
    service_details: Optional[ServiceDetails] = None
    pricing: ProductPricing


class Address(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str


class ContactPreferences(BaseModel):
    newsletter: bool = False
    product_updates: Optional[bool] = None
    billing_notifications: Optional[bool] = None
    maintenance_notifications: Optional[bool] = None
    executive_briefings: Optional[bool] = None
    security_alerts: Optional[bool] = None
    compliance_updates: Optional[bool] = None
    workshop_invitations: Optional[bool] = None


class Contact(BaseModel):
    id: str
    type: str
    first_name: str
    last_name: str
    title: str
    email: str
    phone: str
    mobile: str
    preferred_contact_method: str
    language: str
    timezone: str
    account_id: str
    customer_id: str
    address: Address
    preferences: ContactPreferences
    last_contacted: datetime
