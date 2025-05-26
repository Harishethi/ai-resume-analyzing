import streamlit as st
from openai import OpenAI

# Load API key from Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Resume Analyzer & Builder", page_icon="📄")

st.title("📄 AI Resume Analyzer & Builder")
st.markdown("This app analyzes your resume and also helps you generate a professional one.")

st.sidebar.title("Choose Mode")
mode = st.sidebar.radio("Select what you want to do:", ("Analyze Resume", "Build Resume"))

def analyze_resume(resume_text, job_title=""):
    prompt = f"""
You are a professional resume reviewer. Analyze the following resume and provide:

1. Resume Score (Excellent, Good, Average, Poor)
2. Key Strengths
3. Weaknesses
4. Suggestions for Improvement
5. Sample Improved Summary (if applicable)

Resume Text:
\"\"\"{resume_text}\"\"\"

Job Title Target: {job_title if job_title else "Not specified"}

Respond with clear headings.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=700
    )
    return response.choices[0].message.content.strip()

def build_resume(name, job_title, experience):
    prompt = f"""
Create a professional resume using the following information:

Name: {name}
Job Title: {job_title}
Experience: {experience}

Include:
- A strong professional summary
- Key skills
- Achievements
- Education (you can add placeholders if not provided)

Format clearly.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=700
    )
    return response.choices[0].message.content.strip()

if mode == "Analyze Resume":
    st.subheader("🔍 Resume Analyzer")
    job = st.text_input("Target Job Title (optional):")
    resume = st.text_area("Paste your resume content here:", height=300)
    
    if st.button("Analyze Resume"):
        if resume.strip():
            st.info("Analyzing resume...")
            feedback = analyze_resume(resume, job)
            st.markdown(feedback)
        else:
            st.warning("Please paste your resume first.")

elif mode == "Build Resume":
    st.subheader("🛠 Resume Builder")
    name = st.text_input("Your Full Name:")
    job_title = st.text_input("Job Title:")
    experience = st.text_area("Briefly describe your experience:", height=200)

    if st.button("Generate Resume"):
        if name and job_title and experience:
            st.info("Generating resume...")
            resume_output = build_resume(name, job_title, experience)
            st.markdown(resume_output)
        else:
            st.warning("Please fill in all fields.")
