import pandas as pd
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

class ExcelParser:
    def __init__(self, chunk_size: int = 1000):
        self.chunk_size = chunk_size
        
    def parse(self, file_content: bytes, filename: str):
        try:
            excel_file = pd.ExcelFile(BytesIO(file_content))
            result = {
                "filename": filename,
                "total_sheets": len(excel_file.sheet_names),
                "sheets": []
            }
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                json_data = self.dataframe_to_json(df)
                chunks = self.create_chunks(json_data, sheet_name)
                
                sheet_info = {
                    "sheet_name": sheet_name,
                    "total_rows": len(df),
                    "total_columns": len(df.columns),
                    "columns": list(df.columns),
                    "data_types": df.dtypes.astype(str).to_dict(),
                    "chunks": chunks
                }
                result["sheets"].append(sheet_info)
            return result
            
        except Exception as e:
            logger.error(f"Error parsing Excel file: {str(e)}")
            raise Exception(f"Failed to parse Excel file: {str(e)}")
    
    def dataframe_to_json(self, df: pd.DataFrame):       
        df_clean = df.fillna("")
        records = df_clean.to_dict('records')
        json_records = []
        for record in records:
            json_record = {}
            for key, value in record.items():
                if pd.isna(value):
                    json_record[key] = None
                elif isinstance(value, (pd.Timestamp, pd.DatetimeIndex)):
                    json_record[key] = value.isoformat()
                else:
                    json_record[key] = value
            json_records.append(json_record)
        
        return json_records
    
    def create_chunks(self, json_data, sheet_name: str):
        chunks = []
        total_rows = len(json_data)
        
        if total_rows <= self.chunk_size:
            return [{
                "chunk_id": 0,
                "sheet_name": sheet_name,
                "start_row": 0,
                "end_row": total_rows - 1,
                "row_count": total_rows,
                "data": json_data
            }]
        
        for i in range(0, total_rows, self.chunk_size):
            chunk_data = json_data[i:i + self.chunk_size]
            
            chunk = {
                "chunk_id": len(chunks),
                "sheet_name": sheet_name,
                "start_row": i,
                "end_row": min(i + self.chunk_size - 1, total_rows - 1),
                "row_count": len(chunk_data),
                "data": chunk_data
            }
            chunks.append(chunk)
        
        return chunks