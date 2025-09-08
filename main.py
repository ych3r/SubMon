from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any

app = FastAPI()

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
        "subdomains": {
            "api.example.com": {
                "status": "active",
                "title": "API Endpoint"
            },
            "blog.example.com": {
                "status": "active",
                "title": "Blog"
            },
            "shop.example.com": {
                "status": "inactive",
                "title": "Shop"
            }
        },
        "program_url": "https://bugbounty.example.com",
        "notes": "Main site and all listed subdomains are in scope."
    },
    "testsite.org": {
        "subdomains": {
            "dev.testsite.org": {
                "status": "active",
                "title": "Development"
            },
            "admin.testsite.org": {
                "status": "inactive",
                "title": "Admin Panel"
            }
        },
        "program_url": "https://testsite.org/bug-bounty",
        "notes": "Program paused until Q4."
    },
    "acme.io": {
        "subdomains": {
            "portal.acme.io": {
                "status": "active",
                "title": "Portal"
            },
            "api.acme.io": {
                "status": "active",
                "title": "API"
            },
            "support.acme.io": {
                "status": "inactive",
                "title": "Support"
            }
        },
        "program_url": "https://acme.io/security",
        "notes": "Only portal and api subdomains are in scope."
    }
}

# --------------------- Target Endpoints --------------------- #

@app.get("/target")
def get_target(domain: str | None = None) -> dict[str, Any]:
    if not domain:
        return targets
    if domain not in targets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given domain doesn't exist."
        )
    return targets[domain]

@app.post("/target")
def add_target(domain: str, body: dict[str, Any]) -> dict[str, Any]:
    if domain in targets:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Already had that domain."
        )
    targets[domain] = {
        "subdomains": body['subdomains'],
        "program_url": body['program_url'],
        "notes": body['notes'],
    }
    return {"domain": domain}

@app.patch("/target")
def update_target(domain: str, body: dict[str, Any]) -> dict[str, Any]:
    if domain not in targets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given domain doesn't exist."
        )
    targets[domain].update(body)
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

@app.get("/target/{domain}/subdomains")
def get_subdomains(domain: str) -> dict[str, Any]:
    if domain not in targets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given domain doesn't exist."
        )
    return targets[domain].get('subdomains')

@app.patch("/target/{domain}/subdomains")
def update_subdomains(domain: str, body: dict[str, Any]) -> dict[str, Any]:
    if domain not in targets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given domain doesn't exist."
        )
    targets[domain].get('subdomains').update(body)
    return targets[domain]