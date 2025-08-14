from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import scanner  # Correctly import the scanner router
import logging

# --- App Initialization ---
# Configure logging
logging.basicConfig(level=logging.INFO)

# Create the FastAPI app instance
app = FastAPI(
    title="Intelligent Scanner API",
    version="1.0.0",
    description="API to analyze product images and barcodes with Google Gemini."
)


# --- CORS (Cross-Origin Resource Sharing) Middleware ---
# This allows your React Native app (on a different "origin") to communicate with the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. For production, you might restrict this.
    allow_credentials=True,
    allow_methods=["GET", "POST"], # Specify allowed methods
    allow_headers=["*"], # Allows all headers
)


# --- API Routers ---
# Include the scanner router. All routes defined in `scanner.py` will now be active.
# They will be automatically prefixed with `/api/v1` as defined here.
app.include_router(scanner.router, prefix="/api/v1", tags=["Scanner"])


# --- Root Endpoint ---
@app.get("/")
def read_root():
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"status": "ok", "message": "Welcome to the Intelligent Scanner API"}