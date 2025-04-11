import time
import json
import sys
import re
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
            print("🔍 MODEL_PROVIDER:", os.getenv("MODEL_PROVIDER"))  # DEBUG
@@ -75,49 +76,60 @@
            failures += 1
            continue

        # Clean up if response is wrapped in Markdown-style code block for gemma model outputs
        if raw_response.strip().startswith("```"):
            # Use regex to extract JSON from inside the code block
            match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", raw_response, re.DOTALL)
            if match:
                raw_response = match.group(1).strip()
            else:
                print("❌ Could not extract valid JSON from code block.")
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
        expected_center = (low + high) / 2
        deviation = min(abs(actual_temp - low), abs(actual_temp - high))  


        if low <= actual_temp <= high:
            print(f"✅ Passed: temperature={actual_temp:.1f} is within expected range ({low}, {high})")
            passes += 1
        elif deviation <= 0.1:
            print(f"⚠️ Soft Fail: temperature={actual_temp:.1f} is outside range, but deviation ({deviation:.1f}) ≤ 0.1")
            soft_failures += 1
        else:
            print(f"❌ Hard Fail: temperature={actual_temp:.1f} is outside range, deviation ({deviation:.1f}) > 0.1")
            hard_failures += 1

    except Exception as e:
        print(f"❌ Error: {e}")
        hard_failures += 1

# Final report
total = len(testcases)
print(f"\n🔍 Final Report:")
print(f"✅ Passed: {passes}")
print(f"⚠️ Soft Fails (minor deviation): {soft_failures}")
print(f"❌ Hard Fails: {hard_failures}")
print(f"📊 Total: {total} cases evaluated")

if hard_failures > 0:
    print("🚨 Some tests had hard failures. Investigate immediately.")
elif soft_failures > 0:
    print("⚠️ Minor deviations found. Review soft fails.")
else:
    print("🎉 All tests passed within acceptable range.")
