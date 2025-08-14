from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Annotated
from app.services import gemini_service

# Create an API router
router = APIRouter()

@router.post("/scan")
async def analyze_barcode_image(
    image: Annotated[UploadFile, File()],
    barcode_data: Annotated[str, Form()]
):
    """
    Receives an image and barcode data, analyzes the image using an AI service,
    and returns the analysis.
    """
    # Ensure the uploaded file is an image
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image.")

    try:
        # Read the image content as bytes
        image_bytes = await image.read()

        # Pass the data to the Gemini service for analysis
        analysis = await gemini_service.analyze_image(image_bytes, barcode_data)

        return {"barcode": barcode_data, "analysis": analysis}
    except Exception as e:
        # Handle potential errors from the AI service
        raise HTTPException(status_code=500, detail=f"An error occurred during analysis: {str(e)}")