from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

# Scalar Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )

