# 🧪 DoCoreAI Pulse
Welcome to the official test runner for DoCoreAI — a framework that dynamically optimizes LLM responses based on intelligence parameters like reasoning, creativity, precision, and temperature.

This repo helps you evaluate the performance of intelligence_profiler — a single-step API endpoint from DoCoreAI — by comparing generated temperature values against expected ranges for diverse test prompts.

## 🚀 What Does It Do?  
- Sends test prompts (user_content + role) to /intelligence_profiler.  
- Parses the response.  
- Extracts the predicted temperature.  
- Validates it against the expected range.  
- Prints a clean report with ✅ passes and ❌ failures.

## 📂 Folder Structure
```
.
├── run_tests.py          # Main test runner
├── test_cases.json       # Test prompts + expected temperature ranges
├── .env                  # API keys and model info (not committed)
└── ...
```

## ⚙️ Setup [**Optimized for ChatGPT · Expanding to More LLMs Soon**]
### Option 1: Test DoCoreAI in 1 Minute — Right on GitHub!
No need for local setup. You can run all tests directly inside GitHub Actions with just a few clicks.

✅ Just follow these simple steps:  
1. Fork this repository (top-right corner → Fork).  
2. Go to your fork → Settings → Secrets and variables → Actions.  
3. Click New repository secret:  
- Name: OPENAI_API_KEY  
- Value: Your OpenAI secret key  
- Then click Add secret.  
4. Now, go to the Actions tab in your fork.  
5. If prompted, click "I understand my workflows" → Enable workflows.  
6. Under "All Workflows", click on "DoCoreAI PyPI Test" (our sample test workflow).  
7. Click "Run workflow" → Choose main branch → Hit Run.  
8. Wait a few seconds for the test to begin.  
9. Once it turns green ✅, click into it → Run tests → View live execution of each test case.  

### Option 2:
1. Clone the Repo  
```
git clone https://github.com/SajiJohnMiranda/DoCoreAI-Pulse.git
cd DoCoreAI-Pulse
```
2. Install Dependencies  
```
pip install -r requirements.txt
```
3. Create a .env file  
```
OPENAI_API_KEY=your-openai-key
GROQ_API_KEY=your-groq-key
MODEL_PROVIDER=openai
MODEL_NAME=gpt-3.5-turbo
```

4. Start the DoCoreAI Server
```
uvicorn api.main:app --reload
```
run in a new terminal window
```
python run_tests.py
```

Make sure the /intelligence_profiler endpoint is running locally at http://localhost:8000.

## 🧪 Run Tests  
You'll see each test input, actual response, and whether the predicted temperature falls in the expected range.

Example output:
```
▶️ Running Test Case #1
✅ Passed: temperature=0.250 is within range (0.1, 0.3)

▶️ Running Test Case #2
❌ Failed: temperature=0.600 not in expected range (0.8, 1.0)

🔍 Final Report: 4 passed, 1 failed
```
💡 If you run this in GitHub Actions, the test will fail the workflow if any test fails. You can modify it to soft-fail with only a warning.  

## 💡 Customizing Test Cases
Edit test_cases.json to add your own inputs and expected temperature ranges:
```
[
  {
    "input": {
      "user_content": "Invent a brand-new type of sport.",
      "role": "Creative Thinker"
    },
    "expected_range": [0.9, 1.0]
  }
]

```

## 🛠️ Notes
This runner is independent of the main DoCoreAI repo, as long as:

- The /intelligence_profiler API is running.

- Your .env has valid API keys.

- You have a valid test_cases.json.

## 🙌 Contributing

Have an idea to improve the test coverage? Spot an issue? Feel free to:

- Open an issue

- Submit a PR

- Or suggest improvements to the test logic!

## 📢 License
Creative Commons Attribution-NonCommercial (CC BY-NC 4.0) — do what you want, just don’t forget to give credit ✨







