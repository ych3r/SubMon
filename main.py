from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any

from schemas import TargetRead, TargetCreate, Subdomain
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


# --------------------- Target Endpoints --------------------- #


@app.get("/target", response_model=TargetRead)
def get_target(domain: str | None = None):
    target = db.get_target(domain)
    if target is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given domain doesn't exist."
        )
    return target


@app.post("/target")
def add_target(domain: str, target: TargetCreate) -> dict[str, Any]:
    return db.create_target(domain, target)


@app.patch("/target", response_model=TargetRead)
def update_target(domain: str, target: TargetCreate):
    return db.update_target(domain, target)


@app.delete("/target")
def delete_target(domain: str) -> dict[str, Any]:
    db.delete_target(domain)
    return {"detail": f"Target with domain '{domain}' is deleted!"}


# --------------------- Subdomain Endpoints --------------------- #


@app.get("/target/{domain}/subdomains", response_model=list[Subdomain])
def get_subdomains(domain: str):
    return db.get_subdomains(domain)


@app.patch("/target/{domain}/subdomains", response_model=list[Subdomain])
def add_subdomains(domain: str, subdomain_list: list[Subdomain]):
    return db.add_subdomains(domain, subdomain_list)
