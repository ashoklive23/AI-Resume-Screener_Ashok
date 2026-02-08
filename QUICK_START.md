# 🚀 Quick Start Guide - AI Resume Screener

## ✅ Installation Complete!

Your AI Resume Screener is now ready to use. Follow these steps to get started:

## 📋 What's Been Set Up

✅ **Main Application** (`app.py`) - Premium dark-themed Streamlit interface
✅ **Resume Parser** (`resume_parser.py`) - PDF/DOCX text extraction
✅ **Band Classifier** (`band_classifier.py`) - Experience-based classification
✅ **Skills Analyzer** (`skills_analyzer.py`) - Procurement & premium skills detection
✅ **Sample Resumes** - 5 test resumes generated (all experience bands)

## 🎯 How to Use

### Step 1: Access the Application

The application is already running! Open your browser and go to:
- **Local URL**: http://localhost:8501
- **Network URL**: http://192.168.0.100:8501

### Step 2: Upload Resumes

1. Navigate to the **"📤 Upload Resumes"** tab
2. Click the upload area or drag & drop resume files
3. Supported formats: **PDF** and **DOCX**
4. Click **"🚀 Start Analysis"** button

### Step 3: View Analytics

1. Switch to the **"📊 Analytics Dashboard"** tab
2. View summary metrics:
   - Total candidates analyzed
   - Average experience
   - Candidates with premium skills
   - Most common band
3. Use filters to find specific candidates:
   - Filter by band (5A, 5B, 4A, 4B, 4C)
   - Sort by experience or domain score

### Step 4: Export Results

1. Go to the **"💾 Export Results"** tab
2. Choose export format:
   - **Excel** - Full spreadsheet with all data
   - **JSON** - Machine-readable format
3. Download the report

## 🧪 Test with Sample Resumes

We've generated 5 sample resumes for you to test:

1. `sample_resume_band_5A_analyst.docx` - 0-1 years (Analyst)
2. `sample_resume_band_5B_senior_analyst.docx` - 2-3 years (Senior Analyst)
3. `sample_resume_band_4A_management_trainee.docx` - 4-7 years (Management Trainee)
4. `sample_resume_band_4B_assistant_manager.docx` - 8-11 years (Assistant Manager)
5. `sample_resume_band_4C_manager.docx` - 12+ years (Manager)

**To test:** Upload all 5 sample resumes and click "Start Analysis"

## 📊 Band Classification System

| Band | Designation | Experience |
|------|-------------|------------|
| **5A** | Analyst | 0-1 years |
| **5B** | Senior Analyst | 2-3 years |
| **4A** | Management Trainee | 4-7 years |
| **4B** | Assistant Manager | 8-11 years |
| **4C** | Manager | 12+ years |

## 🎯 What Gets Analyzed

### Core Procurement Skills
- Strategic Sourcing
- Vendor/Supplier Management
- Contract Negotiation
- RFP/RFQ Management
- Cost Reduction & Optimization
- Category Management
- SAP MM / Oracle Procurement
- Compliance & Risk Management
- E-Procurement
- Total Cost of Ownership (TCO)

### Premium Skills (Added Advantage)
- ⭐ Advanced Excel (VLOOKUP, Pivot Tables, Macros, VBA)
- ⭐ Power BI (Dashboards, DAX)
- ⭐ Tableau (Data Visualization)
- ⭐ Python & SQL
- ⭐ Data Analytics
- ⭐ Process Automation (RPA)

### Domain Scoring (0-100)
Each resume gets a comprehensive score based on:
- **40%** - Procurement knowledge depth
- **30%** - Advanced procurement concepts
- **20%** - Premium technical skills
- **10%** - Keyword density & expertise

## 🎨 UI Features

- **Premium Dark Theme** - Professional navy/slate design
- **Real-time Analysis** - Progress bars and status updates
- **Interactive Cards** - Hover effects on candidate profiles
- **Color-Coded Bands** - Each band has unique colors
- **Responsive Design** - Works on all screen sizes
- **Smooth Animations** - Polished user experience

## 🔧 Commands Reference

### Start the Application
```bash
streamlit run app.py
```

### Generate New Sample Resumes
```bash
python generate_sample_resumes.py
```

### Install Dependencies (if needed)
```bash
pip install -r requirements.txt
```

## 💡 Pro Tips

1. **Batch Upload**: You can upload multiple resumes at once (10-50 at a time)
2. **Filter First**: Use band filters to quickly find qualified candidates
3. **Domain Score**: Candidates with 70+ domain score show strong procurement expertise
4. **Premium Skills**: Look for candidates with 2+ premium skills for analytics roles
5. **Export Early**: Export results frequently to avoid data loss

## 🐛 Troubleshooting

### Application won't start
```bash
# Make sure you're in the correct directory
cd "d:\Ashok Project -Kaggle\AI Resume Screener"

# Try reinstalling dependencies
pip install streamlit pandas openpyxl PyPDF2 python-docx
```

### PDF/DOCX parsing errors
- Ensure files are not password-protected
- Try converting to a newer format
- Check if files are corrupted

### Slow performance
- Upload fewer resumes at once (20-30 max)
- Close other browser tabs
- Restart the Streamlit server

## 📞 Support

For issues or questions:
1. Check the README.md file
2. Review error messages in the terminal
3. Verify file formats are supported (PDF/DOCX only)

---

## 🎉 Ready to Go!

Your AI Resume Screener is fully set up and running. Try uploading the sample resumes to see it in action!

**Next Steps:**
1. Open http://localhost:8501 in your browser
2. Upload the 5 sample resumes
3. Explore the analytics dashboard
4. Export your first report

**Enjoy screening resumes with AI! 🚀**
