import streamlit as st
import os
from dotenv import load_dotenv
from utils import extract_and_clean_pdf, get_text_stats
from ai_engine import setup_model, generate_policy_summary, generate_scenario_draft, translate_text

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(layout="wide", page_title="National AI Policy Adapter", page_icon="🇱🇰")

# SIDEBAR: Instructions & Metadata
with st.sidebar:
    st.title("📌 Project Info")
    st.markdown("""
    **Project:** AI-Assisted Policy Adapter  
    **Document:** Sri Lanka National AI Strategy  
    ---
    **How to use:**
    1. Upload the PDF on the left.
    2. Click 'Generate Summary'.
    3. Use the right panel to adapt the policy for specific Sri Lankan scenarios.
    """)
    if not API_KEY:
        API_KEY = st.text_input("Enter Gemini API Key", type="password")

if not API_KEY:
    st.warning("Please provide an API Key to continue.")
    st.stop()

model = setup_model(API_KEY)

st.title("🏛️ National AI Policy Adaptation System")
st.markdown("---")

# Main Layout
left_panel, right_panel = st.columns(2, gap="large")

# LEFT PANEL 
with left_panel:
    st.header("1. Policy Summarisation")
    uploaded_file = st.file_uploader("Upload Policy (PDF)", type="pdf")
    
    if uploaded_file:
        if st.button("Generate Strategy Summary"):
            with st.spinner("Extracting and Summarizing..."):
                text = extract_and_clean_pdf(uploaded_file)
                summary = generate_policy_summary(text, model)
                st.session_state['summary'] = summary

    if 'summary' in st.session_state:
        st.subheader("Summary Output")
        st.info(st.session_state['summary'])
        
        st.divider()
        st.subheader("🌐 Local Language Translation")
        target_lang = st.radio("Translate summary for local stakeholders:", ["None", "Sinhala", "Tamil"], horizontal=True)
        
        if target_lang != "None":
            if st.button(f"Translate to {target_lang}"):
                with st.spinner("Translating..."):
                    translation = translate_text(st.session_state['summary'], target_lang, model)
                    st.success(f"**{target_lang} Translation:**")
                    st.write(translation)



#  RIGHT PANEL 
with right_panel:
    st.header("2. Scenario Adaptation")
    
    if 'summary' not in st.session_state:
        st.info("👈 Please generate a summary on the left to start adaptation.")
    else:
        # Scenario Selection
        scenario = st.selectbox(
            "Select Target Audience/Scenario:",
            [
                "Education: Rural Schools",
                "Business: SME Adoption",
                "Legal: AI Governance"
            ]
        )

        # SELECT STYLE 
        st.write("---")
        st.subheader("Adaptation Settings")
        selected_style = st.select_slider(
            "Select Style:", 
            options=["Simple", "Professional", "Technical/Legal"],
            value="Professional",
            help="Choose how the AI should rewrite the policy draft."
        )

        if st.button("Generate Adapted Draft"):
            with st.spinner(f"Generating {selected_style} draft..."):
                draft = generate_scenario_draft(
                    st.session_state['summary'], 
                    scenario, 
                    selected_style, 
                    model
                )
                st.session_state['draft'] = draft

    if 'draft' in st.session_state:
        st.divider()
        st.subheader("📝 Adapted Policy Draft")
        st.success(st.session_state['draft'])
        
        st.download_button(
            label="Download Adapted Draft",
            data=st.session_state['draft'],
            file_name="adapted_policy_draft.txt",
            mime="text/plain"
        )