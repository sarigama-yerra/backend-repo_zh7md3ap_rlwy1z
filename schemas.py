"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Existing example schemas (kept for reference)
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Sponsorisily schemas
class Pack(BaseModel):
    platform: str = Field(..., description="Platform(s) for the pack, e.g., Facebook & Instagram")
    name: str = Field(..., description="Pack display name")
    price_DA: Optional[str] = Field(None, description="Price in Algerian Dinar (formatted)")
    duration: Optional[str] = Field(None, description="Duration label, e.g., 7 jours")
    results: List[str] = Field(default_factory=list, description="Expected results highlights")
    advantages: List[str] = Field(default_factory=list, description="Advantages list")
    objective: Optional[str] = Field(None, description="Primary marketing objective")
    logo: Optional[str] = Field(None, description="Logo URL for the platform")

class QuoteRequest(BaseModel):
    full_name: str = Field(..., description="Client full name")
    email: Optional[EmailStr] = Field(None, description="Client email")
    phone: Optional[str] = Field(None, description="Client phone")
    message: Optional[str] = Field(None, description="Additional message")
    pack_name: Optional[str] = Field(None, description="Selected pack name")
    platform: Optional[str] = Field(None, description="Selected platform")

class Consultation(BaseModel):
    full_name: str = Field(..., description="Client full name")
    phone: str = Field(..., description="Client phone")
    preferred_time: Optional[str] = Field(None, description="Preferred time slot")
    notes: Optional[str] = Field(None, description="Additional notes")
