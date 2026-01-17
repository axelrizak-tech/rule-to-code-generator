# Rule-to-Code Automation Generator
# Google Colab Ready

import os
import pandas as pd
from google.colab import files

# =========================
# CONFIG
# =========================
OUTPUT_DIR = "generated_code"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# UPLOAD RULES FILE
# =========================
print("Upload CSV file with business rules")
uploaded = files.upload()
file_name = list(uploaded.keys())[0]

# =========================
# LOAD RULES
# =========================
rules_df = pd.read_csv(file_name)

required_columns = {"field", "operator", "value", "action"}
if not required_columns.issubset(rules_df.columns):
    raise ValueError(f"CSV must contain columns: {required_columns}")

# =========================
# CODE GENERATION
# =========================
generated_lines = []
generated_lines.append("def evaluate_record(record):")
generated_lines.append("    decision = 'AUTO'\n")

for idx, row in rules_df.iterrows():
    field = row["field"]
    operator = row["operator"]
    value = row["value"]
    action = row["action"]

    # Detect numeric vs string
    try:
        float(value)
        value_repr = value
    except ValueError:
        value_repr = f"'{value}'"

    condition = f"record.get('{field}') {operator} {value_repr}"

    if idx == 0:
        generated_lines.append(f"    if {condition}:")
    else:
        generated_lines.append(f"    elif {condition}:")

    generated_lines.append(f"        decision = '{action}'")

generated_lines.append("\n    return decision")

generated_code = "\n".join(generated_lines)

# =========================
# SAVE OUTPUT
# =========================
output_path = os.path.join(OUTPUT_DIR, "decision_engine.py")
with open(output_path, "w") as f:
    f.write(generated_code)

print("Generated Python decision engine:\n")
print(generated_code)

print(f"\nSaved to: {output_path}")
