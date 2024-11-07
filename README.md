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

3. In ``apply-intelligence/``create a .env file:
- Option A: Get the .env file from Anton
- Option B: Create your own .env file with

    ```OPENAI_API_KEY=your_api_key_here```

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