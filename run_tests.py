import requests
import time
import json
import sys
import os

BASE_URL = "http://localhost:8000"
TESTCASE_FILE = "test_cases.json"

BASE_DIR = os.path.dirname(__file__)
TESTCASE_FILE = os.path.join(BASE_DIR, "test_cases.json")

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
        response = requests.post(f"{BASE_URL}/intelligence_profiler", json=test["input"])
        response.raise_for_status()
        result = response.json()

        profiler_data = result.get("optimal_response", {})
        actual_temp = profiler_data.get("temperature")

        if actual_temp is None:
            print("❌ Temperature field not found in response.")
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
