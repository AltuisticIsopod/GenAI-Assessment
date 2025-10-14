from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from excel_parser import ExcelParser
from AI_analyzer import AIAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(), 
        logging.FileHandler('log_output.log') 
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Excel Data Analyzer",
    description="AI-powered Excel file analysis",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

excel_parser = ExcelParser(chunk_size=1000)
ai_analyzer = AIAnalyzer()

@app.get("/")
async def root():
    return {"message": "Excel Data Analyzer API is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        parsed_data = excel_parser.parse(content, file.filename)
        
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "message": "File processed successfully",
            "data": parsed_data
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to process Excel file"
        }

@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Starting analysis for file: {file.filename}")
        content = await file.read()
        logger.info(f"File size: {len(content)} bytes")
        
        parsed_data = excel_parser.parse(content, file.filename)
        logger.info(f"Excel parsing completed. Sheets: {parsed_data.get('total_sheets', 0)}")
        
        ai_analysis = ai_analyzer.analyze_data(parsed_data)
        logger.info(f"AI analysis completed. Summary length: {len(ai_analysis.get('summary', ''))}")
        
        return {
            "filename": file.filename,
            "message": "File analyzed successfully",
            "ai_analysis": ai_analysis
        }
    except Exception as e:
        logger.error(f"Analysis failed for {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    try:
        ai_status = ai_analyzer.health_check()
        return {
            "status": "healthy" if ai_status == "healthy" else "degraded",
            "services": {
                "excel_parser": "operational",
                "ai_analyzer": ai_status
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)