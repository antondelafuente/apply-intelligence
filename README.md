# Apply Intelligence

## Local Development

1. Clone the repository:
```
git clone https://github.com/antondelafuente/apply-intelligence.git
```

2. Install dependencies:
```
cd apply-intelligence
pip install -r requirements.txt
```

3. Get the OpenAI api key from Anton. In ``apply-intelligence/`` create a file called ``.env`` with the contents:
```
OPENAI_API_KEY=your_api_key_here
```
4. Run the development server:
```
uvicorn main:app --reload
```

5. Open http://localhost:8000

## Production

The app is deployed at: https://apply-intelligence.up.railway.app

Any pushes to main will automatically deploy to production via Railway.

## Tech Stack

- OpenAI API
- FastAPI
- HTMX
- Alpine.js
- Tailwind CSS
- Railway