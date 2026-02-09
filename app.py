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

# Custom CSS for Premium Light Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: #f8fafc;
    }
    
    .stApp {
        background: #f8fafc;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #0f172a !important;
        font-weight: 700 !important;
    }
    
    p, span, div {
        color: #475569;
    }
    
    .candidate-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .candidate-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: #3b82f6;
    }
    
    .band-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 13px;
        margin: 4px;
        color: white !important;
    }
    
    .band-5A { background: #3b82f6; }
    .band-5B { background: #8b5cf6; }
    .band-4A { background: #10b981; }
    .band-4B { background: #f59e0b; }
    .band-4C { background: #ef4444; }
    
    .skill-tag {
        display: inline-block;
        background: #eff6ff;
        color: #2563eb;
        padding: 4px 10px;
        border-radius: 4px;
        margin: 4px;
        font-size: 12px;
        border: 1px solid #dbeafe;
        font-weight: 500;
    }
    
    .skill-tag.premium {
        background: #fffbeb;
        color: #d97706;
        border-color: #fcd34d;
    }
    
    .metric-container {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #0f172a;
        margin: 8px 0;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    
    .stButton>button {
        background: #2563eb;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
    }
    
    /* Style for the Reset button (Primary - Red Gradient) */
    div[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        box-shadow: 0 4px 16px rgba(239, 68, 68, 0.3) !important;
        border: none !important;
        color: white !important;
    }
    
    div[data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(239, 68, 68, 0.5) !important;
    }
    
    .upload-section {
        background: #ffffff;
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 32px;
        text-align: center;
    }
    
    .sidebar .sidebar-content {
        background: #f1f5f9;
        border-right: 1px solid #e2e8f0;
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
            <h1 style='font-size: 42px; margin-bottom: 8px; color: #0f172a;'>🎯 AI Resume Screener</h1>
            <p style='color: #475569; font-size: 16px;'>Procurement & Sourcing Excellence</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        if st.sidebar.button("🔄 Reset", use_container_width=True):
            st.session_state.analyzed_resumes = []
            st.rerun()

        st.markdown("### 📊 Band Guide")
        st.markdown("""
        <div style='background: #ffffff; padding: 8px; border-radius: 8px; margin-bottom: 6px; border: 1px solid #e2e8f0;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span class='band-badge band-5A' style='font-size: 11px; padding: 4px 8px; margin: 0;'>5A</span>
                <span style='color: #475569; font-size: 11px;'>0-2 yrs (Analyst)</span>
            </div>
        </div>
        <div style='background: #ffffff; padding: 8px; border-radius: 8px; margin-bottom: 6px; border: 1px solid #e2e8f0;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span class='band-badge band-5B' style='font-size: 11px; padding: 4px 8px; margin: 0;'>5B</span>
                <span style='color: #475569; font-size: 11px;'>2-4 yrs (Sr Analyst)</span>
            </div>
        </div>
        <div style='background: #ffffff; padding: 8px; border-radius: 8px; margin-bottom: 6px; border: 1px solid #e2e8f0;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span class='band-badge band-4A' style='font-size: 11px; padding: 4px 8px; margin: 0;'>4A</span>
                <span style='color: #475569; font-size: 11px;'>4-8 yrs (Mgmt Trainee)</span>
            </div>
        </div>
        <div style='background: #ffffff; padding: 8px; border-radius: 8px; margin-bottom: 6px; border: 1px solid #e2e8f0;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span class='band-badge band-4B' style='font-size: 11px; padding: 4px 8px; margin: 0;'>4B</span>
                <span style='color: #475569; font-size: 11px;'>8-12 yrs (Asst Mgr)</span>
            </div>
        </div>
        <div style='background: #ffffff; padding: 8px; border-radius: 8px; margin-bottom: 6px; border: 1px solid #e2e8f0;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span class='band-badge band-4C' style='font-size: 11px; padding: 4px 8px; margin: 0;'>4C</span>
                <span style='color: #475569; font-size: 11px;'>12+ yrs (Manager)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 📈 Scoring")
        st.caption("Total: 100 Points")
        st.markdown("""
        - **Base Skills**: 40 pts
        - **Adv. Concepts**: 30 pts
        - **Premium Skills**: 20 pts
        - **Density**: 10 pts
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
            <h3 style='color: #2563eb; margin-bottom: 16px;'>📁 Drop your resumes here</h3>
            <p style='color: #64748b;'>Supports PDF and DOCX formats</p>
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
        st.markdown("### 📈 Scoring Methodology")
        st.markdown("""
        <div style='background: #ffffff; padding: 16px; border-radius: 12px; font-size: 13px; border: 1px solid #e2e8f0;'>
            <p style='margin-bottom: 8px; color: #0f172a;'>Total Score: <strong>100 Points</strong></p>
            <ul style='color: #475569; padding-left: 20px; margin: 0;'>
                <li><strong>30 pts:</strong> Base Procurement Skills</li>
                <li><strong>30 pts:</strong> Advanced Concepts (TCO, JIT, etc.)</li>
                <li><strong>20 pts:</strong> Premium Skills (Python, PowerBI)</li>
                <li><strong>10 pts:</strong> Keyword Density (Source/Vendor)</li>
                <li><strong>10 pts:</strong> Stability (>2 yrs/role)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def analyze_resumes(uploaded_files):
    # Clear previous results to ensure only the latest batch is shown
    st.session_state.analyzed_resumes = []
    
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
        skills_info = skills_analyzer.analyze(resume_data['text'], resume_data['experience'])
        
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
            'score_breakdown': skills_info.get('score_breakdown', {}),
            'suitability': skills_info.get('suitability', {}),
            'best_fit_role': skills_info.get('best_fit_role', 'General Procurement'),
            'pros': skills_info.get('pros', []),
            'cons': skills_info.get('cons', []),
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

def _generate_suitability_html(suitability):
    html = ""
    for role, data in suitability.items():
        fit = data.get('fit', 'Low')
        color = '#10b981' if fit == 'High' else '#f59e0b' if fit == 'Medium' else '#ef4444'
        html += f"""
        <div style='text-align: center; padding: 8px; background: rgba(255, 255, 255, 0.05); border-radius: 8px;'>
            <div style='font-size: 12px; color: #94a3b8; margin-bottom: 4px;'>{role}</div>
            <div style='color: {color}; font-weight: 700;'>{fit} Fit</div>
        </div>
        """
    return html

def display_candidate_card(resume):
    with st.container():
        # Use a bordered container styled with CSS or just native elements
        st.markdown("""---""")
        
        # Header Section
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### 👤 {resume['name']}")
            st.caption(f"📧 {resume['email']} | 📱 {resume['phone']}")
        with col2:
            st.markdown(f"**{resume['band']}**")
            st.caption(resume['designation'])

        # Metrics Section
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Experience", f"{resume['experience']} Years")
        with m2:
            st.metric("Domain Score", f"{resume['domain_score']}/100")
        with m3:
            st.metric("Best Fit", resume.get('best_fit_role', 'General'))
            
        # Skills Section
        st.markdown("**🎯 Procurement Skills**")
        if resume['procurement_skills']:
            st.markdown(", ".join([f"`{s}`" for s in resume['procurement_skills']]))
        else:
            st.caption("No specific skills detected")
            
        st.markdown("**⭐ Premium Skills**")
        if resume['premium_skills']:
            st.markdown(", ".join([f"`{s}`" for s in resume['premium_skills']]))
        else:
            st.caption("No premium skills detected")

        # Role Fitment Section
        st.markdown("##### 📊 Role Fitment")
        f1, f2, f3 = st.columns(3)
        suitability = resume.get('suitability', {})
        
        with f1:
            fit = suitability.get('Sourcing', {}).get('fit', 'Low')
            color = "green" if fit == 'High' else "orange" if fit == 'Medium' else "red"
            st.markdown(f"**Sourcing**: :{color}[{fit}]")
        with f2:
            fit = suitability.get('Procurement', {}).get('fit', 'Low')
            color = "green" if fit == 'High' else "orange" if fit == 'Medium' else "red"
            st.markdown(f"**Procurement**: :{color}[{fit}]")
        with f3:
            fit = suitability.get('Vendor Development', {}).get('fit', 'Low')
            color = "green" if fit == 'High' else "orange" if fit == 'Medium' else "red"
            st.markdown(f"**Vendor Dev**: :{color}[{fit}]")

        # Scoring Breakdown Expander
        with st.expander("📈 View Scoring Breakdown"):
            breakdown = resume.get('score_breakdown', {})
            b1, b2, b3, b4, b5 = st.columns(5)
            b1.metric("Base", f"{breakdown.get('Base Skills', 0)}/30")
            b2.metric("Advanced", f"{breakdown.get('Advanced Concepts', 0)}/30")
            b3.metric("Premium", f"{breakdown.get('Premium Skills', 0)}/20")
            b4.metric("Density", f"{breakdown.get('Density (Role Keywords)', 0)}/10")
            b5.metric("Stability", f"{breakdown.get('Stability (>2yr Avg)', 0)}/10")
            
        # Conclusion Box
        st.info(f"**Conclusion**: {resume['name']} is a **{resume['band']} ({resume['designation']})** candidate with **{resume['experience']} years** exp. Best suited for **{resume.get('best_fit_role', 'General')}**.")
        
        # Pros and Cons
        c1, c2 = st.columns(2)
        with c1:
            if resume.get('pros'):
                st.markdown("✅ **Strengths**")
                for pro in resume['pros']:
                    st.markdown(f"<span style='color: #16a34a; font-size: 14px;'>• {pro}</span>", unsafe_allow_html=True)
                    
        with c2:
            if resume.get('cons'):
                st.markdown("⚠️ **Areas for Improvement**")
                for con in resume['cons']:
                     st.markdown(f"<span style='color: #dc2626; font-size: 14px;'>• {con}</span>", unsafe_allow_html=True)

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
