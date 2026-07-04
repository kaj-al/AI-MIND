import streamlit as st 
import requests
import re
from datetime import datetime


def normalize_value(value):
    if isinstance(value, dict):
        if "content" in value and len(value) == 1:
            return value["content"]
        return {k: normalize_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize_value(v) for v in value]
    if hasattr(value, "content"):
        return value.content
    return value


def normalize_result(result):
    normalized = {k: normalize_value(v) for k, v in result.items()}
    normalized["main_response"] = normalized.get("main_response") or normalized.get("ans")
    bias_text = normalized.get("bias", "")
    normalized["bias_analysis"] = normalized.get("bias_analysis") or bias_text

    # Extract bias level
    if normalized.get("bias_level"):
        pass
    else:
        match = re.search(r'Bias Level\s*:\s*(High|Medium|Low|Neutral)', bias_text, re.IGNORECASE)
        if match:
            normalized["bias_level"] = match.group(1).title()
        else:
            normalized["bias_level"] = "Unknown"
    if "claims" not in normalized and "claim" in normalized:
        normalized["claims"] = [normalized["claim"]] if normalized["claim"] else []
    normalized["claims_count"] = normalized.get("claims_count") or len(normalized.get("claims", []))
    normalized["bias_analysis"] = normalized.get("bias_analysis") or normalized.get("bias")
    return normalized

# Page configuration
st.set_page_config(
    page_title="AI Claim Analyzer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .bias-high { color: #d32f2f; font-weight: bold; }
    .bias-medium { color: #f57c00; font-weight: bold; }
    .bias-low { color: #388e3c; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([0.85, 0.15])
with col1:
    st.markdown('<div class="main-title">AI Claim Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Evaluate claims with multi-agent AI analysis</div>', unsafe_allow_html=True)
with col2:
    st.info("Live Analysis")

st.divider()

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    analysis_depth = st.select_slider(
        "Analysis Depth",
        options=["Quick", "Standard", "Deep"],
        value="Standard"
    )
    show_sources = st.checkbox("Show Retrieved Sources", value=True)
    show_reasoning = st.checkbox("Show AI Reasoning", value=True)

# Main input section
st.subheader("Enter Your Claim or Question")
query = st.text_area(
    "What would you like me to analyze?",
    placeholder="Enter a claim, statement, or question here...",
    height=100,
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    submit_button = st.button("Analyze", use_container_width=True)
with col2:
    clear_button = st.button("Clear", use_container_width=True)
if clear_button:
    st.rerun()

# Results section
if submit_button and query:
    with st.spinner(" Analyzing your claim or question..."):
        try:
            response = requests.post(
                "http://localhost:8000/chat",
                params={"query": query},
                timeout=30
            )
            
            if response.status_code == 200:
                    result = normalize_result(response.json())
                    
                    # Display main response
                    st.success(" Analysis Complete")
                    
                    # Create tabs for different analysis views
                    tab1, tab2, tab3, tab4, tab5 = st.tabs([
                        "Summary", 
                        "Bias Analysis", 
                        "Claims", 
                        "Sources",
                        "Details"
                    ])
                    
                    with tab1:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric(
                                "Confidence Score",
                                f"{result.get('confidence', 'N/A')}",
                                delta="positive"
                            )
                        with col2:
                            st.metric(
                                "Bias Level",
                                result.get('bias_level', 'Unknown'),
                                delta="neutral"
                            )
                        with col3:
                            st.metric(
                                "Claims Found",
                                result.get('claims_count', 0),
                                delta="info"
                            )
                        
                        st.write("### Main Response")
                        main_answer = result.get('main_response', 'No response available')
                        st.write(main_answer)
                    
                    with tab2:
                        bias_data = result.get('bias_analysis', 'No bias assessment available')
                        st.write("### Bias Assessment")
                        st.write(bias_data)
                    
                    with tab3:
                        claims_data = result.get('claims', [])
                        st.write("### Detected Claims")
                        if isinstance(claims_data, list) and claims_data:
                            for i, claim in enumerate(claims_data, 1):
                                st.write(f"**Claim {i}**: {claim}")
                        else:
                            st.write("No claims detected")
                    
                    with tab4:
                        if show_sources:
                            sources = result.get('sources', [])
                            st.write("### Retrieved Sources")
                            if isinstance(sources, list) and sources:
                                for i, source in enumerate(sources, 1):
                                    st.write(f"**Source {i}**: {source}")
                            else:
                                st.write("No sources retrieved")
                    
                    with tab5:
                        st.write("### Full Analysis Details")
                        st.json(result)
                
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to backend. Make sure the FastAPI server is running on http://localhost:8000")
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif submit_button:
    st.warning("Please enter a claim or question to analyze")