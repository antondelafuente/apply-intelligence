from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import json
import os

load_dotenv()
app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.get("/info/healthcheck")
def healthcheck():
    return {"status": "ok"}

# API Models
class JobSelect(BaseModel):
    jobId: str


class ResumeSubmit(BaseModel):
    resume: str


class ResumeSelect(BaseModel):
    resumeId: str


class ChatMessage(BaseModel):
    message: str
    currentPage: str  # "job_select" | "resume" | "screener" | "cover_letter"


def reset_state():
    global current_state, JOBS, RESUMES
    current_state = {
        "selected_job_id": None,
        "resume": None,
        "chat_history": []
    }
    with open('jobs.json') as f:
        JOBS = json.load(f)['jobs']
    with open('resumes.json') as f:
        RESUMES = json.load(f)['resumes']

reset_state()

@app.get("/api/jobs")
async def get_jobs():
    return {"jobs": JOBS}


@app.get("/api/resumes")
async def get_resumes():
    return {"resumes": RESUMES}


@app.post("/api/select_job")
async def select_job(job: JobSelect):
    current_state["selected_job_id"] = job.jobId
    return {"success": True}


@app.post("/api/submit_resume")
async def submit_resume(resume: ResumeSubmit):
    current_state["resume"] = resume.resume
    return {"success": True}


@app.post("/api/select_resume")
async def select_resume(resume: ResumeSelect):
    current_state["selected_resume_id"] = resume.resumeId
    return {"success": True}


PAGE_CONTEXTS = {
    "skills": """
       Based on the user's resume and the job description, suggest 3-5 most relevant skills as simple bullet points.
   """,

    "screener": """
       For these screening questions:
       {screener_questions}
       Based on the user's resume and the job description, suggest key talking points as simple bullets first.
   """,

    "cover_letter": """
       Based on the user's resume and the job description, start with 2-3 key short and simple bullet points to include.
   """
}

@app.post("/api/chat")
async def chat(message: ChatMessage):
    job = next((job for job in JOBS if job["id"] == current_state["selected_job_id"]), None)
    resume = next((resume for resume in RESUMES if resume["id"] == current_state["selected_resume_id"]), None)

    # Get page context and format if needed
    page_context = PAGE_CONTEXTS[message.currentPage]
    if message.currentPage == "screener" and job:
        questions = "\n".join([f"- {q['question']}" for q in job['screenerQuestions']])
        page_context = page_context.format(screener_questions=questions)

    response = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[{
            "role": "user",
            "content": f"""
            You are an AI assistant helping a job seeker fill out a job application.
            Answer any user questions short and simply.
            The user is currently on the {message.currentPage} page.
            {page_context}

            Job Description:
            {job['description'] if job else 'No job selected yet'}

            Resume:
            {resume['summary'] if resume else 'No resume selected yet'}
            Experience:
            {resume['experience'] if resume else 'No resume selected yet'}

            Previous conversation:
            {current_state["chat_history"][-3:] if current_state["chat_history"] else 'No previous messages'}

            User question: {message.message}
            Respond with short and simple answers.
            """
        }]
    )

    # Store in history
    current_state["chat_history"].append({
        "message": message.message,
        "response": response.choices[0].message.content
    })

    return {"response": response.choices[0].message.content}
@app.get("/api/debug")
async def debug(include_jobs: bool = False):
    if include_jobs:
        return {**current_state, "jobs": JOBS}
    return current_state


@app.post("/api/reset")
async def reset():
    reset_state()
    return {"success": True}


app.mount("/", StaticFiles(directory=".", html=True))

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv('PORT', '8080'))  # Default to 8080 for Marvin
    uvicorn.run(app, host="0.0.0.0", port=port)