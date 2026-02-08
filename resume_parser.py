import re
import PyPDF2
import docx
from io import BytesIO
import spacy
from spacy.matcher import Matcher

class ResumeParser:
    """
    Parse resumes in PDF and DOCX formats to extract key information
    """
    
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            # If spacy model not available, will use basic extraction
            self.nlp = None
    
    def parse(self, uploaded_file):
        """
        Parse uploaded resume file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            dict: Parsed resume data
        """
        # Extract text based on file type
        if uploaded_file.name.endswith('.pdf'):
            text = self._extract_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith('.docx'):
            text = self._extract_from_docx(uploaded_file)
        else:
            text = ""
        
        # Extract information
        return {
            'text': text,
            'name': self._extract_name(text),
            'email': self._extract_email(text),
            'phone': self._extract_phone(text),
            'experience': self._extract_experience(text)
        }
    
    def _extract_from_pdf(self, file):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return ""
    
    def _extract_from_docx(self, file):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(BytesIO(file.read()))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
            return ""
    
    def _extract_name(self, text):
        """Extract candidate name from resume text"""
        if not text:
            return "Unknown"
        
        # Try to get name from first few lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return "Unknown"
        
        # First non-empty line is usually the name
        potential_name = lines[0]
        
        # Clean up common titles
        potential_name = re.sub(r'\b(Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.)\b', '', potential_name, flags=re.IGNORECASE)
        potential_name = potential_name.strip()
        
        # If name seems too long or contains numbers, try next line
        if len(potential_name) > 50 or re.search(r'\d', potential_name):
            if len(lines) > 1:
                potential_name = lines[1].strip()
        
        # Use spacy for name extraction if available
        if self.nlp:
            doc = self.nlp(text[:500])  # Check first 500 chars
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    return ent.text
        
        return potential_name if potential_name else "Unknown"
    
    def _extract_email(self, text):
        """Extract email address from resume text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else "Not found"
    
    def _extract_phone(self, text):
        """Extract phone number from resume text"""
        # Indian phone number patterns
        phone_patterns = [
            r'\+91[-.\s]?\d{10}',
            r'\+91[-.\s]?\d{5}[-.\s]?\d{5}',
            r'\d{10}',
            r'\d{5}[-.\s]?\d{5}',
            r'\(\d{3}\)[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                return phones[0]
        
        return "Not found"
    
    def _extract_experience(self, text):
        """
        Extract years of experience from resume text
        
        Returns:
            float: Years of experience
        """
        text_lower = text.lower()
        
        # Pattern 1: "X years of experience"
        pattern1 = r'(\d+\.?\d*)\s*(?:\+)?\s*(?:years?|yrs?)\s+(?:of\s+)?experience'
        matches = re.findall(pattern1, text_lower)
        if matches:
            return float(matches[0])
        
        # Pattern 2: "Experience: X years"
        pattern2 = r'experience\s*:?\s*(\d+\.?\d*)\s*(?:\+)?\s*(?:years?|yrs?)'
        matches = re.findall(pattern2, text_lower)
        if matches:
            return float(matches[0])
        
        # Pattern 3: Calculate from work history dates
        experience_years = self._calculate_from_dates(text)
        if experience_years > 0:
            return experience_years
        
        # Pattern 4: Generic "X years" or "X+ years"
        pattern4 = r'(\d+\.?\d*)\s*\+?\s*(?:years?|yrs?)'
        matches = re.findall(pattern4, text_lower)
        if matches:
            # Get the highest number found
            return max([float(m) for m in matches])
        
        return 0.0
    
    def _calculate_from_dates(self, text):
        """
        Calculate total experience from work history dates
        """
        # Date patterns (Month Year - Month Year)
        date_pattern = r'(\w+\s+\d{4})\s*[-–—to]+\s*(\w+\s+\d{4}|present|current)'
        
        matches = re.findall(date_pattern, text.lower())
        
        if not matches:
            return 0.0
        
        from datetime import datetime
        
        total_months = 0
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        for start_date, end_date in matches:
            try:
                # Parse start date
                start = datetime.strptime(start_date.strip(), "%B %Y")
            except:
                try:
                    start = datetime.strptime(start_date.strip(), "%b %Y")
                except:
                    continue
            
            # Parse end date
            if 'present' in end_date or 'current' in end_date:
                end = datetime(current_year, current_month, 1)
            else:
                try:
                    end = datetime.strptime(end_date.strip(), "%B %Y")
                except:
                    try:
                        end = datetime.strptime(end_date.strip(), "%b %Y")
                    except:
                        continue
            
            # Calculate months
            months = (end.year - start.year) * 12 + (end.month - start.month)
            total_months += months
        
        return round(total_months / 12, 1)
