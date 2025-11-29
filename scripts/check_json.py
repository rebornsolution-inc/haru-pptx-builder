import json
import sys

try:
    with open('projects/icecreammedia/presentation.json', 'r', encoding='utf-8') as f:
        data = f.read()
    json.loads(data)
    print("JSON is valid")
except json.JSONDecodeError as e:
    print(f"JSON Decode Error: {e}")
    lines = data.splitlines()
    print(f"Error at line {e.lineno}:")
    print(lines[e.lineno-1])
    print("Context:")
    start = max(0, e.lineno - 5)
    end = min(len(lines), e.lineno + 5)
    for i in range(start, end):
        print(f"{i+1}: {lines[i]}")
