import re
from collections import Counter
import math
import pdfplumber
import io

def extractPageLines(rawData):
    pages = []
    with pdfplumber.open(io.BytesIO(rawData)) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            lines = [
                ln.strip() 
                for ln in text.splitlines() 
                if ln.strip()
            ]
            pages.append({
                "pageNumber": i,
                "text": text,
                "lines": lines
            })
    return pages
        
pageFra = re.compile(r"\b\d+\s*/\s*\d+\b", re.I)  
pageOf  = re.compile(r"\b(?:page|pg|p\.?)\s+\d+\s+(?:of|/)\s+\d+\b", re.I)  
time   = re.compile(r"\b\d{1,2}:\d{2}\s*(?:AM|PM)?\b", re.I)               
tz      = re.compile(r"\bGMT[+-]\d{2}:\d{2}\b", re.I)                       
num     = re.compile(r"\d+")
spaces  = re.compile(r"\s+")

def canon(line):
    cLine = line.strip().lower()
    cLine = pageOf.sub("page #/#", cLine)
    cLine = pageFra.sub("#/#", cLine)
    cLine = time.sub("#:##", cLine)
    cLine = tz.sub("gmt#:#", cLine)
    cLine = num.sub("#", cLine)
    cLine = spaces.sub(" ", cLine)

    return cLine
def findRepeated(pages, minFrac=0.5):
    totalPages=len(pages)
    threshold = max(1, math.ceil(totalPages * minFrac))

    pageCanons = []

    for p in pages:
        canons=set(
            canon(ln) 
            for ln in p["lines"])
        pageCanons.append(canons)

    count = Counter()

    for canons in pageCanons:
        count.update(canons)
    
    repeatedCanon = { c for c, k in count.items() 
                    if k>=threshold
                    }
    perPageFlagged=[]

    for p in pages:
        flagged = [ln for ln in p["lines"] 
                    if canon(ln) in repeatedCanon]
        perPageFlagged.append(
            {
                "pageNumber": p["pageNumber"],
                "flagged": flagged
            }
        )
    
    return {
        "totalPages":totalPages,
        "minFrac": minFrac,
        "threshold": threshold,
        "repeatedCanon":list(sorted(repeatedCanon)),
        "perPageFlagged":perPageFlagged,
        "counts": dict(count),
    }


def removeRepeatedText(pages, repeatedCanon):
    cleanedData = []
    rep=set(repeatedCanon)
    for p in pages:
        removed = []
        clean = []
        for ln in p["lines"]:
            if canon(ln) in rep:
                removed.append(ln)
            else:
                clean.append(ln)
        
        cleanedData.append({
            "pageNumber": p["pageNumber"],
            "text": p["text"],
            "lines": p["lines"],
            "cleanLines":clean,
            "removedLines":removed
        })

    return cleanedData
        
        
            



        
