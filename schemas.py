
from enum import Enum
from pydantic import BaseModel, Field

class SubdomainStatus(str, Enum):
    active = "active"
    inactive = "inactive"

class Subdomain(BaseModel):
    status: SubdomainStatus
    title: str | None = None

class Target(BaseModel):
    subdomains: dict[str, Subdomain] = Field(default=None)
    program_url: str = Field(max_length=200)
    notes: str | None = Field(default=None, max_length=140)