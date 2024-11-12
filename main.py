# main.py
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from dotenv import load_dotenv
from urllib.parse import parse_qs
import os

load_dotenv()
app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Explicitly get the env var


@app.post("/api/cover-letter")
async def generate_cover_letter(request: Request):
    body = (await request.body()).decode()
    data = parse_qs(body)

    resume = data['resume'][0]
    job_description = data['job_description'][0]

    response = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[{
            "role": "user",
            "content": f"""
            Generate a short (~200 words) cover letter that matches the resume experience to the job requirements.
            Use simple and clear language without too much marketing or sales speak.
            Start directly with "Dear Hiring Manager," and focus on the content only.
            Do not include any header information (no names, dates, addresses, contact info).

            Here is the resume:
            {resume}

            Here is the job description:
            {job_description}
            """
        }]
    )

    return PlainTextResponse(response.choices[0].message.content)


app.mount("/", StaticFiles(directory=".", html=True))