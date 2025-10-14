import os
import json
import logging
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class AIAnalyzer:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
    
    def analyze_data(self, excel_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            analysis_data = self.prepare_data_for_analysis(excel_data)
            logger.info(f"Prepared analysis data: {json.dumps(analysis_data, indent=2)}")
            prompt = self.prompt_for_analysis(analysis_data)
            logger.info(f"Generated prompt length: {len(prompt)}")
            response = self.call_llm(prompt)
            logger.info(f"LLM response: {response}")
            return {
                "summary": response.get("summary", ""),
                "key_findings": response.get("key_findings", []),
                "data_quality": response.get("data_quality", {}),
                "recommendations": response.get("recommendations", []),
                "statistics": response.get("statistics", {}),
                "insights": response.get("insights", [])
            }     
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            return {
                "summary": f"Analysis failed: {str(e)}",
                "key_findings": ["Analysis error occurred"],
                "data_quality": {"completeness": "Error", "accuracy": "Error", "consistency": "Error"},
                "statistics": {"total_records": "Error"},
                "insights": ["Unable to perform analysis"],
                "recommendations": ["Please check your configuration and try again"]
            }
    
    def prepare_data_for_analysis(self, excel_data: Dict[str, Any]) -> Dict[str, Any]:
        prepared_data = {
            "filename": excel_data.get("filename", "Unknown"),
            "total_sheets": excel_data.get("total_sheets", 0),
            "sheets_summary": [],
            "sample_data": []
        }
        
        for sheet in excel_data.get("sheets", []):
            sheet_summary = {
                "sheet_name": sheet.get("sheet_name", "Unknown"),
                "total_rows": sheet.get("total_rows", 0),
                "total_columns": sheet.get("total_columns", 0),
                "columns": sheet.get("columns", []),
                "data_types": sheet.get("data_types", {})
            }
            prepared_data["sheets_summary"].append(sheet_summary)
            
            chunks = sheet.get("chunks", [])
            if chunks and chunks[0].get("data"):
                sample_rows = chunks[0]["data"][:5]
                prepared_data["sample_data"].extend(sample_rows)
        
        return prepared_data
    
    def prompt_for_analysis(self, data: Dict[str, Any]) -> str:
        """Build comprehensive analysis prompt"""
        return f"""
        Analyze the following Excel data and provide a comprehensive analysis:
        
        File: {data['filename']}
        Sheets: {data['total_sheets']}
        
        Sheet Summary:
        {json.dumps(data['sheets_summary'], indent=2)}
        
        Sample Data (first 5 rows):
        {json.dumps(data['sample_data'], indent=2)}
        
        Please provide:
        1. Executive Summary
        2. Key Findings (list of 5-10 important findings)
        3. Data Quality Assessment (completeness, accuracy, consistency)
        4. Statistical Summary (if applicable)
        5. Business Insights (3-5 actionable insights)
        6. Recommendations (3-5 specific recommendations)
        
        Format your response as JSON with the following structure:
        {{
            "summary": "Executive summary here",
            "key_findings": ["finding1", "finding2", ...],
            "data_quality": {{"completeness": "X%", "accuracy": "assessment", "consistency": "assessment"}},
            "statistics": {{"total_records": X, "unique_values": X, ...}},
            "insights": ["insight1", "insight2", ...],
            "recommendations": ["recommendation1", "recommendation2", ...]
        }}
        
        """
    
    def call_llm(self, prompt: str) -> Dict[str, Any]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data analyst expert. Analyze the provided data and respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            content = content.strip()
            start = content.find('{')
            end = content.rfind('}')
            
            if start != -1 and end != -1:
                content = content[start:end+1]
            logger.info(f"Original LLM response: {content}")
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON response, returning default structure")
                return {
                    "summary": "Analysis completed but response format was invalid",
                    "key_findings": ["Unable to parse AI response"],
                    "data_quality": {"completeness": "Unknown", "accuracy": "Unknown", "consistency": "Unknown"},
                    "statistics": {"total_records": "Unknown"},
                    "insights": ["AI response parsing failed"],
                    "recommendations": ["Please check the data format and try again"]
                }
                
        except Exception as e:
            logger.error(f"Error calling LLM: {str(e)}")
            return {
                "summary": f"AI analysis failed: {str(e)}",
                "key_findings": ["Analysis error occurred"],
                "data_quality": {"completeness": "Error", "accuracy": "Error", "consistency": "Error"},
                "statistics": {"total_records": "Error"},
                "insights": ["Unable to perform analysis"],
                "recommendations": ["Please check your API key and try again"]
            }
    
    def health_check(self) -> str:

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return "healthy"
        except Exception as e:
            logger.error(f"AI service health check failed: {str(e)}")
            return "unhealthy"
