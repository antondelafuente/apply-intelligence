# Apply Intelligence

A minimal starter kit integrating OpenAI's GPT-4 with FastAPI and HTMX.

## Local Development

1. Clone the repository:
git clone https://github.com/antondelafuente/apply-intelligence.git

2. Create a `.env` file in the root directory:
OPENAI_API_KEY=sk-proj-xxxxx
(You'll receive the actual API key separately)

3. Install dependencies:
pip install -r requirements.txt

4. Run the development server:
uvicorn main:app --reload

5. Open http://localhost:8000

## Production

The app is deployed at: https://apply-intelligence.up.railway.app

Any pushes to main will automatically deploy to production via Railway.

## Tech Stack

- FastAPI backend
- HTMX frontend
- Tailwind CSS
- OpenAI GPT-4
- Railway for deployment
