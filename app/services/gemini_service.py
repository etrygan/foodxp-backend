import google.generativeai as genai
from app.core.config import settings
import logging

# Configure the Gemini client with the API key from settings
# This will run once when the application starts.
try:
    genai.configure(api_key=settings.GOOGLE_API_KEY)
    logging.info("Gemini API configured successfully.")
except Exception as e:
    # Log a critical error if the API key is missing or invalid.
    # The application will likely fail to handle requests if this happens.
    logging.error(f"FATAL: Failed to configure Gemini API. Is GOOGLE_API_KEY set? Error: {e}")

async def analyze_image(image_bytes: bytes, barcode_data: str) -> str:
    """
    Analyzes an image and barcode data using the Gemini 1.5 Flash model.

    Args:
        image_bytes: The image file as bytes.
        barcode_data: The data scanned from the barcode.

    Returns:
        A text analysis of the product in the image.
    """
    try:
        # Use a modern, fast, and vision-capable model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Prepare the image data for the API
        image_part = {
            "mime_type": "image/jpeg", # Assuming JPEG, but the model is robust
            "data": image_bytes
        }

        # Create a more detailed and structured prompt for better results
        prompt = (
            "You are a helpful product analysis assistant. "
            f"Analyze the product in the image, which has the barcode data: '{barcode_data}'.\n\n"
            "Provide a concise, user-friendly analysis formatted exactly like this:\n"
            "**Product Name:** [Your identified product name]\n"
            "**Description:** [A single, engaging sentence describing the product]\n"
            "**Key Features:**\n"
            "* [Feature 1]\n"
            "* [Feature 2]\n"
            "* [Feature 3]"
        )

        # Generate content using the prompt and the image
        # Using the async version is good practice in FastAPI
        response = await model.generate_content_async([prompt, image_part])

        return response.text
    except Exception as e:
        logging.error(f"Error during Gemini API call: {e}")
        # Re-raise the exception to be handled by the API endpoint,
        # which will return a user-friendly HTTP 500 error.
        raise