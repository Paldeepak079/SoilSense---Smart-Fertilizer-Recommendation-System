"""
File parser service for extracting soil data from uploaded files
Supports: CSV, Excel (.xlsx, .xls), PDF, Word (.docx), and Images (OCR)
"""
import pandas as pd
import re
from typing import Dict, Optional
from fastapi import UploadFile, HTTPException
import os
import tempfile
from pathlib import Path


class FileParser:
    """Parse uploaded files and extract soil nutrient data"""
    
    @staticmethod
    async def parse_file(file: UploadFile) -> Dict[str, Optional[float]]:
        """
        Parse uploaded file and extract soil data
        
        Args:
            file: Uploaded file object
        
        Returns:
            Dictionary with soil parameters: N, P, K, pH, EC, etc.
        """
        file_ext = Path(file.filename).suffix.lower()
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            if file_ext == '.csv':
                result = FileParser._parse_csv(tmp_file_path)
            elif file_ext in ['.xlsx', '.xls']:
                result = FileParser._parse_excel(tmp_file_path)
            elif file_ext == '.pdf':
                result = FileParser._parse_pdf(tmp_file_path)
            elif file_ext == '.docx':
                result = FileParser._parse_word(tmp_file_path)
            elif file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
                result = FileParser._parse_image(tmp_file_path)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {file_ext}. Supported: CSV, Excel, PDF, Word, Images"
                )
            
            return result
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
    
    @staticmethod
    def _parse_csv(file_path: str) -> Dict[str, Optional[float]]:
        """Parse CSV file"""
        try:
            df = pd.read_csv(file_path)
            return FileParser._extract_from_dataframe(df)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing CSV: {str(e)}")
    
    @staticmethod
    def _parse_excel(file_path: str) -> Dict[str, Optional[float]]:
        """Parse Excel file"""
        try:
            df = pd.read_excel(file_path)
            return FileParser._extract_from_dataframe(df)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing Excel: {str(e)}")
    
    @staticmethod
    def _parse_pdf(file_path: str) -> Dict[str, Optional[float]]:
        """Parse PDF file"""
        try:
            import PyPDF2
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return FileParser._extract_from_text(text)
        except ImportError:
            raise HTTPException(status_code=500, detail="PyPDF2 not installed. Run: pip install PyPDF2")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing PDF: {str(e)}")
    
    @staticmethod
    def _parse_word(file_path: str) -> Dict[str, Optional[float]]:
        """Parse Word document"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return FileParser._extract_from_text(text)
        except ImportError:
            raise HTTPException(status_code=500, detail="python-docx not installed. Run: pip install python-docx")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing Word document: {str(e)}")
    
    @staticmethod
    def _parse_image(file_path: str) -> Dict[str, Optional[float]]:
        """Parse image using OCR with preprocessing"""
        try:
            from PIL import Image, ImageEnhance, ImageFilter
            import pytesseract
            import numpy as np
            
            # Open and preprocess image
            image = Image.open(file_path)
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Enhance image for better OCR
            # 1. Convert to grayscale
            image = image.convert('L')
            
            # 2. Increase contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # 3. Sharpen
            image = image.filter(ImageFilter.SHARPEN)
            
            # 4. Threshold to binary
            threshold = 128
            image = image.point(lambda p: 255 if p > threshold else 0)
            
            # Perform OCR
            text = pytesseract.image_to_string(image, config='--psm 6')
            
            print(f"[FileParser] OCR extracted text length: {len(text)} characters")
            
            return FileParser._extract_from_text(text)
        except ImportError as e:
            if "PIL" in str(e):
                raise HTTPException(status_code=500, detail="Pillow not installed. Run: pip install Pillow")
            elif "pytesseract" in str(e):
                raise HTTPException(status_code=500, detail="pytesseract not installed. Run: pip install pytesseract and install Tesseract OCR")
        except Exception as e:
            print(f"[FileParser] Error parsing image: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Error parsing image: {str(e)}")
    
    @staticmethod
    def _extract_from_dataframe(df: pd.DataFrame) -> Dict[str, Optional[float]]:
        """
        Extract soil data from pandas DataFrame
        Tries to find columns with nutrient names
        """
        result = {
            'nitrogen': None,
            'phosphorus': None,
            'potassium': None,
            'ph': None,
            'ec': None,
            'moisture': None,
            'organic_carbon': None
        }
        
        # Normalize column names to lowercase
        df.columns = df.columns.str.lower().str.strip()
        
        # Mapping of possible column names to standard names
        column_mappings = {
            'nitrogen': ['nitrogen', 'n', 'n%', 'n(%)'],
            'phosphorus': ['phosphorus', 'p', 'p%', 'p(%)', 'phosphorous'],
            'potassium': ['potassium', 'k', 'k%', 'k(%)'],
            'ph': ['ph', 'p.h', 'p.h.', 'ph value'],
            'ec': ['ec', 'e.c', 'electrical conductivity', 'conductivity'],
            'moisture': ['moisture', 'water content', 'moisture%', 'moisture (%)'],
            'organic_carbon': ['organic carbon', 'oc', 'o.c', 'carbon', 'organic c']
        }
        
        # Try to find and extract values
        for standard_name, possible_names in column_mappings.items():
            for col in df.columns:
                if any(name in col for name in possible_names):
                    try:
                        # Get first non-null value
                        value = df[col].dropna().iloc[0] if not df[col].dropna().empty else None
                        if value is not None:
                            result[standard_name] = float(value)
                            break
                    except (ValueError, IndexError):
                        continue
        
        return result
    
    @staticmethod
    def _extract_from_text(text: str) -> Dict[str, Optional[float]]:
        """
        Extract soil data from plain text using regex patterns
        Enhanced with multiple pattern variations for better extraction
        """
        result = {
            'nitrogen': None,
            'phosphorus': None,
            'potassium': None,
            'ph': None,
            'ec': None,
            'moisture': None,
            'organic_carbon': None
        }
        
        print(f"[FileParser] Extracting from text: {text[:200]}...")  # Log first 200 chars
        
        # Enhanced regex patterns with multiple variations
        patterns = {
            'nitrogen': [
                r'(?:nitrogen|N|Nitrogen)\s*[:=]?\s*([\\d.]+)',
                r'N\s*[:=\-]\s*([\\d.]+)',
                r'(?:nitrogen\s*content|N\s*content)\s*[:=]?\s*([\\d.]+)',
                r'(?:total\s*nitrogen|Total\s*N)\s*[:=]?\s*([\\d.]+)',
                r'N\s*\(?(?:mg/kg|ppm|%)\)?\s*[:=]?\s*([\\d.]+)',
            ],
            'phosphorus': [
                r'(?:phosphorus|phosphorous|P|Phosphorus)\s*[:=]?\s*([\\d.]+)',
                r'P\s*[:=\-]\s*([\\d.]+)',
                r'(?:phosphorus\s*content|P\s*content)\s*[:=]?\s*([\\d.]+)',
                r'(?:available\s*phosphorus|Available\s*P)\s*[:=]?\s*([\\d.]+)',
                r'P\s*\(?(?:mg/kg|ppm|%)\)?\s*[:=]?\s*([\\d.]+)',
                r'P2O5\s*[:=]?\s*([\\d.]+)',
            ],
            'potassium': [
                r'(?:potassium|K|Potassium)\s*[:=]?\s*([\\d.]+)',
                r'K\s*[:=\-]\s*([\\d.]+)',
                r'(?:potassium\s*content|K\s*content)\s*[:=]?\s*([\\d.]+)',
                r'(?:available\s*potassium|Available\s*K)\s*[:=]?\s*([\\d.]+)',
                r'K\s*\(?(?:mg/kg|ppm|%)\)?\s*[:=]?\s*([\\d.]+)',
                r'K2O\s*[:=]?\s*([\\d.]+)',
            ],
            'ph': [
                r'(?:pH|PH|Ph|p\.H|P\.H)\s*[:=]?\s*([\\d.]+)',
                r'(?:pH\s*value|PH\s*value)\s*[:=]?\s*([\\d.]+)',
                r'(?:soil\s*pH|Soil\s*pH)\s*[:=]?\s*([\\d.]+)',
            ],
            'ec': [
                r'(?:EC|E\.C|ec|Electrical\s*Conductivity)\s*[:=]?\s*([\\d.]+)',
                r'(?:EC\s*value)\s*[:=]?\s*([\\d.]+)',
                r'(?:conductivity)\s*[:=]?\s*([\\d.]+)',
                r'EC\s*\(?(?:dS/m|mS/cm|μS/cm)\)?\s*[:=]?\s*([\\d.]+)',
            ],
            'moisture': [
                r'(?:moisture|Moisture|water\s*content|Water\s*Content)\s*[:=]?\s*([\\d.]+)',
                r'(?:soil\s*moisture|Soil\s*Moisture)\s*[:=]?\s*([\\d.]+)',
                r'moisture\s*\(?%\)?\s*[:=]?\s*([\\d.]+)',
            ],
            'organic_carbon': [
                r'(?:organic\s*carbon|Organic\s*Carbon|OC|O\.C)\s*[:=]?\s*([\\d.]+)',
                r'(?:carbon\s*content)\s*[:=]?\s*([\\d.]+)',
                r'OC\s*\(?%\)?\s*[:=]?\s*([\\d.]+)',
            ]
        }
        
        # Try each pattern variant for each parameter
        for param, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    try:
                        value = float(match.group(1))
                        result[param] = value
                        print(f"[FileParser] Extracted {param}: {value}")
                        break  # Stop after first successful match
                    except ValueError:
                        continue
        
        # Check if at least one value was extracted
        extracted_count = sum(1 for v in result.values() if v is not None)
        print(f"[FileParser] Successfully extracted {extracted_count}/7 parameters")
        
        return result

