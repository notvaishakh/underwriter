from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import io
import pdfplumber

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.post("/readPDF")
async def readPDF(file: UploadFile = File(...)):
    rawData = await file.read()
    pages=[]
    with pdfplumber.open(io.BytesIO(rawData)) as pdf:
        for i, page in enumerate(pdf.pages):
            text=page.extract_text() or ""
            pages.append({
                "pageNumber": i,
                "text": text
            })
    return{"fileName": file.filename, "pageCount":len(pages), "pages":pages}
