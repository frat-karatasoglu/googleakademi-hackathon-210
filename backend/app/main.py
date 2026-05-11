import sys
from pathlib import Path

# Ensure project root is on sys.path so `app` package is importable
# when running `python main.py` from the `app` directory.
root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import demo, admin, company, customer, storefront

app = FastAPI(title="Koopilot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(demo.router)
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(company.router, prefix="/company", tags=["company"])
app.include_router(customer.router, prefix="/customer", tags=["customer"])
app.include_router(storefront.router, prefix="/storefront/ege", tags=["storefront-ege"])


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
