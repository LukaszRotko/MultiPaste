import json
number_of_fields = 10
data = {f"field_{i:04d}": f"Sample value {i:04d}" for i in range(1, number_of_fields+1)}
file_test_json_name="test_"+str(number_of_fields)+".json"

with open(file_test_json_name, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)