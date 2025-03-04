from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
import uuid
import fitz  # PyMuPDF for efficient PDF text extraction
from io import BytesIO
from dotenv import load_dotenv
from pydub import AudioSegment  # For combining audio files
from pydub.playback import play  # For audio playback (optional)
import pytesseract  # For OCR
from PIL import Image  # For image processing

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Allow requests from this origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Set your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure pydub to use ffmpeg
AudioSegment.converter = "ffmpeg"
AudioSegment.ffmpeg = "ffmpeg"

# Root endpoint
@app.get("/")
def read_root():
    return JSONResponse(content={"message": "Welcome to the Text-to-Speech API!"})

def extract_text_from_pdf(file):
    """
    Extract text from a PDF file using PyMuPDF (fitz).
    If the PDF is a scanned image, use OCR (Tesseract) to extract text.
    """
    text = ""
    try:
        # Open the PDF file
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                # Try to extract text directly
                page_text = page.get_text()
                if page_text.strip():  # If text is found
                    text += page_text
                else:
                    # If no text is found, assume it's a scanned image and use OCR
                    pix = page.get_pixmap()  # Convert the page to an image
                    img = Image.open(BytesIO(pix.tobytes()))  # Open the image using PIL
                    page_text = pytesseract.image_to_string(img)  # Perform OCR
                    text += page_text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text from PDF: {str(e)}")
    return text

def split_text_into_chunks(text, chunk_size=4096):
    """
    Split the text into chunks of a specified size (default: 4096 characters).
    """
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

async def generate_audio_from_text_chunks(text_chunks, voice="alloy"):
    """
    Generate audio from text chunks using OpenAI's TTS API.
    """
    audio_segments = []
    for chunk in text_chunks:
        try:
            response = openai.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=chunk
            )
            # Save the audio chunk to a temporary file
            chunk_filename = f"{uuid.uuid4()}.mp3"
            with open(chunk_filename, "wb") as chunk_file:
                chunk_file.write(response.content)
            audio_segments.append(chunk_filename)
        except openai.BadRequestError as e:
            raise HTTPException(status_code=400, detail=f"OpenAI API error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    return audio_segments

def combine_audio_files(audio_files, output_filename):
    """
    Combine multiple audio files into a single file using pydub.
    """
    combined_audio = AudioSegment.empty()
    for audio_file in audio_files:
        combined_audio += AudioSegment.from_file(audio_file)
    combined_audio.export(output_filename, format="mp3")

@app.post("/text-to-speech")
async def text_to_speech(
    file: UploadFile = File(..., max_size=100 * 1024 * 1024),  # Allow files up to 100 MB
    background_tasks: BackgroundTasks = None
):
    """
    Convert text from a PDF or text file to speech using OpenAI's TTS API.
    Handles large text inputs by splitting them into chunks.
    """
    # Ensure the file is a PDF or text file
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code=400, detail="Only .pdf and .txt files are allowed")

    # Process the file in chunks to avoid memory issues
    text = ""
    try:
        if file.content_type == "application/pdf":
            # Use BytesIO to handle binary data
            file_content = await file.read()
            text = extract_text_from_pdf(BytesIO(file_content))
        else:
            # Process text files in chunks
            while chunk := await file.read(1024 * 1024):  # Read 1 MB at a time
                text += chunk.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process file: {str(e)}")

    # Validate the extracted text
    if not text or len(text.strip()) == 0:
        raise HTTPException(status_code=400, detail="The file is empty or contains no text.")

    # Split the text into chunks of 4096 characters (or any size you prefer)
    text_chunks = split_text_into_chunks(text, chunk_size=4096)

    # Generate audio for each chunk
    audio_chunk_files = await generate_audio_from_text_chunks(text_chunks)

    # Combine the audio chunks into a single file
    combined_audio_filename = f"{uuid.uuid4()}.mp3"
    combine_audio_files(audio_chunk_files, combined_audio_filename)

    # Schedule the temporary audio chunk files for deletion
    for chunk_file in audio_chunk_files:
        background_tasks.add_task(os.remove, chunk_file)

    # Schedule the combined audio file for deletion
    background_tasks.add_task(os.remove, combined_audio_filename)

    # Return the combined audio file as a response
    return FileResponse(combined_audio_filename, media_type="audio/mpeg", filename=combined_audio_filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)