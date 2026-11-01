
import os
import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚"
)

st.title("📚 AI Study Assistant")
st.write("Your AI-powered learning companion!")

# Read API key securely
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("Gemini API key not found. Please configure it securely.")
    st.stop()

client = genai.Client(api_key=api_key)

task = st.selectbox(
    "Choose what you want AI to do:",
    ["Explain a Topic", "Summarise a Topic", "Generate Quiz Questions"]
)

topic = st.text_area(
    "Enter your topic or question:",
    placeholder="Example: Explain Machine Learning"
)

level = st.selectbox(
    "Choose your learning level:",
    ["Beginner", "Intermediate", "Advanced"]
)

if st.button("Generate Answer"):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        if task == "Explain a Topic":
            prompt = (
                f"Explain {topic} for a {level} student "
                "using simple English and examples."
            )
        elif task == "Summarise a Topic":
            prompt = (
                f"Summarise {topic} for a {level} student "
                "using clear headings and bullet points."
            )
        else:
            prompt = (
                f"Generate 5 multiple-choice quiz questions "
                f"about {topic} for a {level} student. "
                "Include four options and the correct answers."
            )

        with st.spinner("AI is preparing your response..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                st.subheader("AI Response")
                st.markdown(response.text)

            except Exception as error:
                st.error(f"Something went wrong: {error}")
