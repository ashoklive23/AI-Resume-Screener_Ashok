import streamlit as st
import pandas as pd
from datetime import datetime
import re
from pathlib import Path
import json
from resume_parser import ResumeParser
from band_classifier import BandClassifier
from skills_analyzer import SkillsAnalyzer

# Page Configuration
st.set_page_config(
    page_title="AI Resume Screener - Procurement & Sourcing",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Dark Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    .candidate-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        border: 1px solid rgba(148, 163, 184, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .candidate-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(59, 130, 246, 0.3);
        border-color: rgba(59, 130, 246, 0.5);
    }
    
    .band-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        margin: 4px;
        animation: fadeIn 0.5s ease;
    }
    
    .band-5A {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
    }
    
    .band-5B {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        color: white;
    }
    
    .band-4A {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .band-4B {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }
    
    .band-4C {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
    
    .skill-tag {
        display: inline-block;
        background: rgba(59, 130, 246, 0.2);
        color: #60a5fa;
        padding: 6px 12px;
        border-radius: 6px;
        margin: 4px;
        font-size: 12px;
        border: 1px solid rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
    }
    
    .skill-tag:hover {
        background: rgba(59, 130, 246, 0.3);
        transform: scale(1.05);
    }
    
    .skill-tag.premium {
        background: rgba(245, 158, 11, 0.2);
        color: #fbbf24;
        border-color: rgba(245, 158, 11, 0.3);
    }
    
    .metric-container {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(147, 51, 234, 0.1) 100%);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(148, 163, 184, 0.2);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.2);
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #60a5fa;
        margin: 8px 0;
    }
    
    .metric-label {
        color: #94a3b8;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(59, 130, 246, 0.5);
    }
    
    .upload-section {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 2px dashed rgba(59, 130, 246, 0.5);
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: rgba(59, 130, 246, 0.8);
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analyzed_resumes' not in st.session_state:
    st.session_state.analyzed_resumes = []

def main():
    # Header
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='font-size: 48px; margin-bottom: 8px;'>🎯 AI Resume Screener</h1>
            <p style='color: #94a3b8; font-size: 18px;'>Procurement & Sourcing Excellence</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📊 Band Classification Guide")
        st.markdown("""
        <div style='background: rgba(30, 41, 59, 0.6); padding: 16px; border-radius: 12px; margin: 8px 0;'>
            <div class='band-badge band-5A'>5A - Analyst</div>
            <p style='color: #94a3b8; font-size: 12px; margin: 8px 0;'>0-1 years experience</p>
        </div>
        <div style='background: rgba(30, 41, 59, 0.6); padding: 16px; border-radius: 12px; margin: 8px 0;'>
            <div class='band-badge band-5B'>5B - Senior Analyst</div>
            <p style='color: #94a3b8; font-size: 12px; margin: 8px 0;'>2-3 years experience</p>
        </div>
        <div style='background: rgba(30, 41, 59, 0.6); padding: 16px; border-radius: 12px; margin: 8px 0;'>
            <div class='band-badge band-4A'>4A - Management Trainee</div>
            <p style='color: #94a3b8; font-size: 12px; margin: 8px 0;'>4-7 years experience</p>
        </div>
        <div style='background: rgba(30, 41, 59, 0.6); padding: 16px; border-radius: 12px; margin: 8px 0;'>
            <div class='band-badge band-4B'>4B - Assistant Manager</div>
            <p style='color: #94a3b8; font-size: 12px; margin: 8px 0;'>8-11 years experience</p>
        </div>
        <div style='background: rgba(30, 41, 59, 0.6); padding: 16px; border-radius: 12px; margin: 8px 0;'>
            <div class='band-badge band-4C'>4C - Manager</div>
            <p style='color: #94a3b8; font-size: 12px; margin: 8px 0;'>12+ years experience</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🎯 Key Skills Tracked")
        st.markdown("""
        - 📦 Procurement & Sourcing
        - 📊 Advanced Excel
        - 📈 Power BI
        - 📉 Tableau
        - 🤝 Vendor Management
        - 💰 Cost Optimization
        """)
    
    # Main Content
    tab1, tab2, tab3 = st.tabs(["📤 Upload Resumes", "📊 Analytics Dashboard", "💾 Export Results"])
    
    with tab1:
        upload_resumes_section()
    
    with tab2:
        analytics_dashboard()
    
    with tab3:
        export_results()

def upload_resumes_section():
    st.markdown("### 📤 Upload Candidate Resumes")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class='upload-section'>
            <h3 style='color: #60a5fa; margin-bottom: 16px;'>📁 Drop your resumes here</h3>
            <p style='color: #94a3b8;'>Supports PDF and DOCX formats</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_files = st.file_uploader(
            "Choose resume files",
            type=['pdf', 'docx'],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully")
            
            if st.button("🚀 Start Analysis", use_container_width=True):
                analyze_resumes(uploaded_files)
    
    with col2:
        st.markdown("### ℹ️ Analysis Features")
        st.markdown("""
        <div style='background: rgba(30, 41, 59, 0.6); padding: 16px; border-radius: 12px;'>
            <ul style='color: #94a3b8; line-height: 1.8;'>
                <li>✨ AI-powered parsing</li>
                <li>🎯 Experience extraction</li>
                <li>🔍 Skills identification</li>
                <li>📊 Domain assessment</li>
                <li>🏆 Auto band classification</li>
                <li>📈 Premium skills detection</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def analyze_resumes(uploaded_files):
    parser = ResumeParser()
    classifier = BandClassifier()
    skills_analyzer = SkillsAnalyzer()
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, file in enumerate(uploaded_files):
        status_text.text(f"Analyzing {file.name}...")
        
        # Parse resume
        resume_data = parser.parse(file)
        
        # Classify band
        band_info = classifier.classify(resume_data['experience'])
        
        # Analyze skills
        skills_info = skills_analyzer.analyze(resume_data['text'])
        
        # Combine results
        result = {
            'filename': file.name,
            'name': resume_data.get('name', 'Unknown'),
            'email': resume_data.get('email', 'Not found'),
            'phone': resume_data.get('phone', 'Not found'),
            'experience': resume_data['experience'],
            'band': band_info['band'],
            'designation': band_info['designation'],
            'procurement_skills': skills_info['procurement_skills'],
            'premium_skills': skills_info['premium_skills'],
            'domain_score': skills_info['domain_score'],
            'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        st.session_state.analyzed_resumes.append(result)
        
        progress_bar.progress((idx + 1) / len(uploaded_files))
    
    status_text.text("✅ Analysis completed!")
    st.balloons()

def analytics_dashboard():
    st.markdown("### 📊 Analytics Dashboard")
    
    if not st.session_state.analyzed_resumes:
        st.info("📭 No resumes analyzed yet. Please upload resumes in the 'Upload Resumes' tab.")
        return
    
    # Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_candidates = len(st.session_state.analyzed_resumes)
    avg_experience = sum(r['experience'] for r in st.session_state.analyzed_resumes) / total_candidates
    
    band_counts = {}
    for resume in st.session_state.analyzed_resumes:
        band = resume['band']
        band_counts[band] = band_counts.get(band, 0) + 1
    
    premium_count = sum(1 for r in st.session_state.analyzed_resumes if len(r['premium_skills']) > 0)
    
    with col1:
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Total Candidates</div>
            <div class='metric-value'>{total_candidates}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Avg Experience</div>
            <div class='metric-value'>{avg_experience:.1f}y</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Premium Skills</div>
            <div class='metric-value'>{premium_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        top_band = max(band_counts, key=band_counts.get) if band_counts else "N/A"
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Top Band</div>
            <div class='metric-value' style='font-size: 24px;'>{top_band}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Candidate Cards
    st.markdown("### 👥 Candidate Details")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_band = st.multiselect(
            "Filter by Band",
            options=["5A", "5B", "4A", "4B", "4C"],
            default=[]
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sort by",
            options=["Experience (High to Low)", "Experience (Low to High)", "Domain Score", "Name"]
        )
    
    # Apply filters and sorting
    filtered_resumes = st.session_state.analyzed_resumes
    if filter_band:
        filtered_resumes = [r for r in filtered_resumes if r['band'] in filter_band]
    
    if sort_by == "Experience (High to Low)":
        filtered_resumes = sorted(filtered_resumes, key=lambda x: x['experience'], reverse=True)
    elif sort_by == "Experience (Low to High)":
        filtered_resumes = sorted(filtered_resumes, key=lambda x: x['experience'])
    elif sort_by == "Domain Score":
        filtered_resumes = sorted(filtered_resumes, key=lambda x: x['domain_score'], reverse=True)
    else:
        filtered_resumes = sorted(filtered_resumes, key=lambda x: x['name'])
    
    # Display candidates
    for resume in filtered_resumes:
        display_candidate_card(resume)

def display_candidate_card(resume):
    st.markdown(f"""
    <div class='candidate-card'>
        <div style='display: flex; justify-content: space-between; align-items: start;'>
            <div>
                <h3 style='margin: 0 0 8px 0; color: #ffffff;'>👤 {resume['name']}</h3>
                <p style='color: #94a3b8; margin: 4px 0;'>📧 {resume['email']}</p>
                <p style='color: #94a3b8; margin: 4px 0;'>📱 {resume['phone']}</p>
            </div>
            <div>
                <div class='band-badge band-{resume['band']}'>{resume['band']} - {resume['designation']}</div>
            </div>
        </div>
        
        <div style='margin: 16px 0;'>
            <div style='display: inline-block; background: rgba(59, 130, 246, 0.1); padding: 8px 16px; border-radius: 8px; margin-right: 16px;'>
                <span style='color: #94a3b8;'>Experience:</span>
                <span style='color: #60a5fa; font-weight: 600; margin-left: 8px;'>{resume['experience']} years</span>
            </div>
            <div style='display: inline-block; background: rgba(16, 185, 129, 0.1); padding: 8px 16px; border-radius: 8px;'>
                <span style='color: #94a3b8;'>Domain Score:</span>
                <span style='color: #34d399; font-weight: 600; margin-left: 8px;'>{resume['domain_score']}/100</span>
            </div>
        </div>
        
        <div style='margin: 16px 0;'>
            <p style='color: #94a3b8; margin-bottom: 8px; font-weight: 600;'>🎯 Procurement Skills:</p>
            <div>
                {''.join([f"<span class='skill-tag'>{skill}</span>" for skill in resume['procurement_skills']]) if resume['procurement_skills'] else "<span style='color: #94a3b8;'>No specific skills detected</span>"}
            </div>
        </div>
        
        <div style='margin: 16px 0;'>
            <p style='color: #94a3b8; margin-bottom: 8px; font-weight: 600;'>⭐ Premium Skills:</p>
            <div>
                {''.join([f"<span class='skill-tag premium'>{skill}</span>" for skill in resume['premium_skills']]) if resume['premium_skills'] else "<span style='color: #94a3b8;'>No premium skills detected</span>"}
            </div>
        </div>
        
        <div style='margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(148, 163, 184, 0.2);'>
            <p style='color: #64748b; font-size: 12px;'>📅 Analyzed: {resume['analysis_date']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def export_results():
    st.markdown("### 💾 Export Results")
    
    if not st.session_state.analyzed_resumes:
        st.info("📭 No data to export. Please analyze some resumes first.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Export to Excel")
        if st.button("📥 Download Excel Report", use_container_width=True):
            df = pd.DataFrame(st.session_state.analyzed_resumes)
            df['procurement_skills'] = df['procurement_skills'].apply(lambda x: ', '.join(x))
            df['premium_skills'] = df['premium_skills'].apply(lambda x: ', '.join(x))
            
            # Create Excel file
            excel_path = "resume_analysis_report.xlsx"
            df.to_excel(excel_path, index=False)
            
            with open(excel_path, 'rb') as f:
                st.download_button(
                    label="⬇️ Download",
                    data=f,
                    file_name=f"resume_screening_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
    
    with col2:
        st.markdown("#### 📄 Export to JSON")
        if st.button("📥 Download JSON Report", use_container_width=True):
            json_data = json.dumps(st.session_state.analyzed_resumes, indent=2)
            st.download_button(
                label="⬇️ Download",
                data=json_data,
                file_name=f"resume_screening_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    st.markdown("---")
    st.markdown("### 📋 Preview Data")
    df_preview = pd.DataFrame(st.session_state.analyzed_resumes)
    st.dataframe(df_preview, use_container_width=True)

if __name__ == "__main__":
    main()
