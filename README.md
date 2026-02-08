# AI Resume Screener for Procurement & Sourcing

A powerful AI-powered resume screening application specifically designed for Procurement and Sourcing roles. This application automatically analyzes resumes, extracts relevant information, identifies skills, and classifies candidates into appropriate job bands based on their experience.

## 🎯 Features

### Smart Resume Analysis
- **Multi-format Support**: Processes both PDF and DOCX resume formats
- **AI-Powered Extraction**: Automatically extracts name, email, phone, and experience
- **Experience Calculation**: Intelligently calculates total years of experience from work history

### Band Classification System
The application automatically classifies candidates into the following bands:

| Band | Designation | Experience Range |
|------|-------------|------------------|
| **5A** | Analyst | 0-1 years |
| **5B** | Senior Analyst | 2-3 years |
| **4A** | Management Trainee | 4-7 years |
| **4B** | Assistant Manager | 8-11 years |
| **4C** | Manager | 12+ years |

### Skills Detection
- **Core Procurement Skills**: Sourcing, vendor management, negotiation, RFP/RFQ, cost reduction, contract management, SAP, compliance, etc.
- **Premium Skills** (Added Advantage):
  - Advanced Excel (VLOOKUP, Pivot Tables, Macros, VBA)
  - Power BI (Dashboards, DAX)
  - Tableau (Visualizations)
  - Python, SQL, Data Analytics
  - Process Automation (RPA)

### Domain Expertise Scoring
Each resume is scored on a 0-100 scale based on:
- Procurement and sourcing knowledge (40 points)
- Advanced procurement concepts (30 points)
- Premium technical skills (20 points)
- Keyword density and expertise depth (10 points)

### Beautiful Analytics Dashboard
- **Summary Metrics**: Total candidates, average experience, premium skills count
- **Candidate Cards**: Rich visual cards with all extracted information
- **Filtering & Sorting**: Filter by band, sort by experience or domain score
- **Export Options**: Download results in Excel or JSON format

## 🚀 Installation

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Download spaCy language model** (if not automatically installed):
```bash
python -m spacy download en_core_web_sm
```

## 💻 Usage

1. **Run the application**:
```bash
streamlit run app.py
```

2. **Access the web interface**:
   - The application will automatically open in your default browser
   - Or navigate to `http://localhost:8501`

3. **Upload resumes**:
   - Click on the "Upload Resumes" tab
   - Drag and drop or select PDF/DOCX resume files
   - Click "Start Analysis"

4. **View results**:
   - Navigate to the "Analytics Dashboard" tab
   - Filter and sort candidates
   - Review detailed skill assessments and band classifications

5. **Export data**:
   - Go to the "Export Results" tab
   - Download Excel or JSON reports

## 📁 Project Structure

```
AI Resume Screener/
├── app.py                  # Main Streamlit application
├── resume_parser.py        # Resume parsing and text extraction
├── band_classifier.py      # Experience-based band classification
├── skills_analyzer.py      # Skills detection and domain scoring
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🎨 UI Features

- **Premium Dark Theme**: Modern, professional dark mode interface
- **Responsive Design**: Works seamlessly on all screen sizes
- **Interactive Cards**: Hover effects and smooth animations
- **Color-Coded Bands**: Each band has a distinct color scheme
- **Glassmorphism Effects**: Modern UI with backdrop blur effects

## 🔧 Technical Details

### Technologies Used
- **Streamlit**: Web application framework
- **spaCy**: Natural language processing for entity extraction
- **PyPDF2**: PDF file parsing
- **python-docx**: DOCX file parsing
- **pandas**: Data manipulation and export
- **openpyxl**: Excel file generation

### Key Algorithms
1. **Experience Extraction**: 
   - Pattern matching for "X years of experience"
   - Date range calculation from work history
   - Multiple fallback patterns for accuracy

2. **Skills Detection**:
   - Keyword matching with domain-specific dictionaries
   - Category-based grouping
   - Advanced concept recognition

3. **Domain Scoring**:
   - Multi-factor scoring algorithm
   - Weighted components (40-30-20-10 distribution)
   - Normalized 0-100 scale

## 📊 Sample Output

For each candidate, the system provides:
- ✅ Name, email, and phone number
- ✅ Total years of experience
- ✅ Automatic band classification
- ✅ List of procurement/sourcing skills found
- ✅ Premium skills detected
- ✅ Domain expertise score (0-100)
- ✅ Analysis timestamp

## 🎯 Use Cases

- **HR Teams**: Quickly screen hundreds of resumes for procurement roles
- **Recruitment Agencies**: Standardize candidate evaluation
- **Hiring Managers**: Get data-driven insights on candidate expertise
- **Talent Acquisition**: Build a qualified candidate pipeline

## 🔐 Data Privacy

- All processing happens locally on your machine
- No data is sent to external servers
- Resume files are processed in memory and not stored permanently

## 🤝 Support

For issues, questions, or feature requests, please contact the development team.

## 📝 License

This project is proprietary software for internal use.

---

**Built with ❤️ for Procurement Excellence**
