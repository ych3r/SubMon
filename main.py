from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any

from schemas import Target, Subdomain
from database import Database

app = FastAPI()

db = Database()

# Scalar Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )

# ========================================================= #

# TODO: move this to database
# for test
targets = {
    "example.com": {
        "subdomains": [
            {
                "name": "api.example.com",
                "status": "active",
                "title": "API Endpoint"
            },
            {
                "name": "blog.example.com",
                "status": "active",
                "title": "Blog"
            },
            {
                "name": "shop.example.com",
                "status": "inactive",
                "title": "Shop"
            }
        ],
        "program_url": "https://bugbounty.example.com",
        "notes": "Main site and all listed subdomains are in scope."
    },
    "testsite.org": {
        "subdomains": [
            {
                "name": "dev.testsite.org",
                "status": "active",
                "title": "Development"
            },
            {
                "name": "admin.testsite.org",
                "status": "inactive",
                "title": "Admin Panel"
            }
        ],
        "program_url": "https://testsite.org/bug-bounty",
        "notes": "Program paused until Q4."
    },
    "acme.io": {
        "subdomains": [
            {
                "name": "portal.acme.io",
                "status": "active",
                "title": "Portal"
            },
            {
                "name": "api.acme.io",
                "status": "active",
                "title": "API"
            },
            {
                "name": "support.acme.io",
                "status": "inactive",
                "title": "Support"
            }
        ],
        "program_url": "https://acme.io/security",
        "notes": "Only portal and api subdomains are in scope."
    }
}

# --------------------- Target Endpoints --------------------- #

@app.get("/target", response_model=Target)
def get_target(domain: str | None = None):
    if not domain:
        return targets
    if domain not in targets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given domain doesn't exist."
        )
    return targets[domain]

@app.post("/target")
def add_target(domain: str, target: Target) -> dict[str, Any]:
    if domain in targets:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Already had that domain."
        )
    targets[domain] = {
        **target.model_dump()
    }
    return {"domain": domain}

@app.patch("/target", response_model=Target)
def update_target(domain: str, target: Target):
    if domain not in targets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given domain doesn't exist."
        )
    targets[domain].update(target)
    return targets[domain]

@app.delete("/target")
def delete_target(domain: str) -> dict[str, Any]:
    if domain not in targets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given domain doesn't exist."
        )
    targets.pop(domain)
    return {"detail": f"Target with domain '{domain}' is deleted!"}

# --------------------- Subdomain Endpoints --------------------- #

@app.get("/target/{domain}/subdomains", response_model=list[Subdomain])
def get_subdomains(domain: str):
    if domain not in targets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given domain doesn't exist."
        )
    return targets[domain].get('subdomains')

@app.patch("/target/{domain}/subdomains", response_model=Target)
def update_subdomains(domain: str, subdomain_list: list[Subdomain]):
    if domain not in targets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given domain doesn't exist."
        )
    targets[domain].get('subdomains').extend(subdomain_list)
    return targets[domain]