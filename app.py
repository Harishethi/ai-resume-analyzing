import os
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

# Load API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise Exception("❌ OPENAI_API_KEY not found in environment variables!")

client = OpenAI(api_key=api_key)
console = Console()

# === Resume Analyzer ===
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

Give your response in clear headings.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=800
    )
    return response.choices[0].message.content.strip()

# === Resume Builder ===
def build_resume(name, job_title, experience):
    prompt = f"""
You are a resume writer. Generate a professional resume for:

Name: {name}
Job Title: {job_title}
Experience: {experience}

Include the following sections:
- Name and Title
- Professional Summary
- Key Skills
- Work Experience
- Education (assume a relevant degree)
- Contact Info (mock)

Format the response cleanly using markdown.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=900
    )
    return response.choices[0].message.content.strip()

# === Display Utilities ===
def print_header():
    header = Text()
    header.append("📄 AI Resume Toolkit\n", style="bold magenta")
    header.append("Analyze or Build Your Resume with AI\n", style="italic cyan")
    console.rule(header)

def print_result(content, title="Output"):
    md = Markdown(content)
    panel = Panel(md, title=title, border_style="bright_blue")
    console.print(panel)

# === Main Program ===
if __name__ == "__main__":
    print_header()
    console.print("[bold yellow]Select an option:[/bold yellow]")
    console.print("[cyan]1.[/cyan] Resume Analyzer")
    console.print("[cyan]2.[/cyan] Resume Builder")

    choice = console.input("[bold green]Enter 1 or 2: [/bold green] ")

    if choice == "1":
        job = console.input("\n[bold green]Enter the target job title (optional): [/bold green] ")
        console.print("\n[bold green]Paste your resume content below (press Enter twice to submit):[/bold green]")
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        resume_input = "\n".join(lines)
        console.print("\n[bold yellow]Analyzing your resume...[/bold yellow]")
        result = analyze_resume(resume_input, job)
        print_result(result, "Resume Analysis")

    elif choice == "2":
        name = console.input("\n[bold green]Enter your name: [/bold green] ")
        job_title = console.input("[bold green]Enter your desired job title: [/bold green] ")
        experience = console.input("[bold green]Briefly describe your experience: [/bold green] ")
        console.print("\n[bold yellow]Building your resume...[/bold yellow]")
        result = build_resume(name, job_title, experience)
        print_result(result, "Generated Resume")

    else:
        console.print("[red]Invalid choice. Please restart the program.[/red]")
