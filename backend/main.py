from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from readNcleanPdf import(
    extractPageLines,
    findRepeated,
    removeRepeatedText
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.post("/readPDF")
async def readPDF(file: UploadFile = File(...)):
    rawData = await file.read()
    pages = extractPageLines(rawData)
    repeated = findRepeated(pages)
    cleanedPages = removeRepeatedText(pages,repeated["repeatedCanon"])
    
    return{
        "fileName": file.filename, 
        "pageCount":len(pages), 
        "headerFooter":repeated,
        "pages":cleanedPages
    }
