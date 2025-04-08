import requests
import time
import json
import sys
import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = "http://localhost:8000"
TESTCASE_FILE = "test_cases.json"

BASE_DIR = os.path.dirname(__file__)
TESTCASE_FILE = os.path.join(BASE_DIR, "test_cases.json")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER")  #'openai' , 'groq' etc
MODEL_NAME = os.getenv("MODEL_NAME")  # gpt-3.5-turbo, gemma2-9b-it 

# Wait until server is ready
print("⏳ Waiting for FastAPI server...")
for _ in range(10):
    try:
        r = requests.get(f"{BASE_URL}/docs")
        if r.status_code == 200:
            print("✅ Server is ready.")
            break
    except Exception:
        time.sleep(2)
else:
    print("❌ Server did not start in time.")
    sys.exit(1)

# Load test cases
try:
    with open(TESTCASE_FILE, "r") as f:
        testcases = json.load(f)
except Exception as e:
    print(f"❌ Failed to load {TESTCASE_FILE}: {e}")
    sys.exit(1)

# Run test cases
failures = 0

for i, test in enumerate(testcases, 1):
    print(f"\n▶️ Running Test Case #{i}")
       
    try:
        print("📨 Input Sent:", json.dumps(test["input"], indent=2))
        response = requests.post(f"{BASE_URL}/intelligence_profiler_advanced", json=test["input"])
        response.raise_for_status()
        result = response.json()

        print("📦 Full Response:", json.dumps(result, indent=2))

        # Safely extract and parse the response string
        raw_response = result.get("optimal_response", {}).get("response", "")
        if not raw_response:
            print("❌ Response field is missing or empty.")
            failures += 1
            continue

        try:
            parsed_response = json.loads(raw_response)
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse response string as JSON: {e}")
            failures += 1
            continue

        actual_temp = parsed_response.get("temperature")
        if actual_temp is None:
            print("❌ Temperature field not found in parsed response.")
            failures += 1
            continue

        low, high = test["expected_range"]
        if low <= actual_temp <= high:
            print(f"✅ Passed: temperature={actual_temp:.3f} is within range ({low}, {high})")
        else:
            print(f"❌ Failed: temperature={actual_temp:.3f} not in expected range ({low}, {high})")
            failures += 1

    except Exception as e:
        print(f"❌ Error: {e}")
        failures += 1

# Final report
total = len(testcases)
print(f"\n🔍 Final Report: {total - failures} passed, {failures} failed")
if failures > 0:
    sys.exit(1)
