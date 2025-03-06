# Text-To-Speech API

This project is a Text-To-Speech (TTS) application with a FastAPI backend and an Angular frontend. It allows you to convert text from PDF or text files into speech using OpenAI's TTS API. The generated audio files are saved in a dedicated directory.

## Features

- Extract text from PDF files using PyMuPDF (fitz)
- Perform OCR on scanned PDF files using Tesseract
- Split large text inputs into manageable chunks
- Generate audio from text chunks using OpenAI's TTS API
- Combine multiple audio files into a single file using pydub
- Serve the combined audio file as a downloadable response
- User-friendly frontend built with Angular

## Requirements

- Python 3.7+
- Node.js and npm
- FastAPI
- PyMuPDF
- pytesseract
- pydub
- openai
- uvicorn
- ffmpeg
- Angular CLI

## Installation

### Backend

1. Clone the repository:

git clone https://github.com/yourusername/Text_To_Speech.git
cd Text_To_Speech/webapp/backend

2. Ensure you have your python interpreter chosen and activated. If you want to use venv, run:

python3 -m venv venv
source venv/bin/activate

3. Install the required dependencies:
pip install -r requirements.txt

4. Set up your environment variables:
Create a .env file in the backend directory and add your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key

5. Ensure ffmpeg is installed and available in your system's PATH.

6. Start the FastAPI server:
uvicorn main:app --reload

### Frontend:

1. Navigate to frontend directory:

cd ../frontend

2. Install the required dependencies:

npm install

3. Start the angular development server

ng serve

4. Open your browser and navigate to http://localhost:4200.


### License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

Acknowledgements
FastAPI
PyMuPDF
pytesseract
pydub
OpenAI
Angular


Make sure to replace `yourusername` with your actual GitHub username and `your_openai_api_key` with your actual OpenAI API key. Save this content in a file named [README.md](http://_vscodecontentref_/1) in the root of your project directory.

