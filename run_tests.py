import requests
import json
import time

with open("test_cases.json", "r") as f:
    test_cases = json.load(f)

time.sleep(3)

passed = 0
failed = 0

for test in test_cases:
    input_data = test["input"]
    expected_range = test["expected_temperature_range"]

    try:
        response = requests.post("http://localhost:8000/intelli_profiler", json=input_data)
        result = response.json()
        temp = result["DoCoreAI-Dynamic-Temperature-Profiler"]["temperature"]

        if expected_range[0] <= temp <= expected_range[1]:
            print(f"✅ Passed: Temperature {temp:.2f} in range {expected_range}")
            passed += 1
        else:
            print(f"❌ Failed: Temperature {temp:.2f} not in range {expected_range}")
            failed += 1

    except Exception as e:
        print(f"❌ Error: {e}")
        failed += 1

print(f"\n🔍 Final Report: {passed} passed, {failed} failed")
exit(1 if failed else 0)
