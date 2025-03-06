import streamlit as st
from cognitive_load_analyzer import analyze_cognitive_load

st.title("Cognitive Load Analyzer")

uploaded_file = st.file_uploader("Upload a UI Screenshot", type=["png", "jpg", "jpeg"])

if uploaded_file:
    with open("temp_image.png", "wb") as f:
        f.write(uploaded_file.getbuffer())

    results = analyze_cognitive_load("temp_image.png")
    
    st.write("### Cognitive Load Analysis Results")
    st.write(f"**Contrast:** {results['Contrast']}")
    st.write(f"**Text Density:** {results['Text Density']}")
    st.write(f"**Unique Colors:** {results['Unique Colors']}")
    st.write(f"**Cognitive Load Score:** {results['Cognitive Load Score']}")
