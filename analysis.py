import pandas as pd
import os
from datetime import datetime

# ======== CONFIGURABLE PATHS ========
raw_input_dir = "data/raw"  # Directory containing input files
converted_output_dir = "data/converted"  # Output for parsed CSV files
rt_output_dir = "data/RTs"  # Output for RT results
base_name = "actr_trace_raw"  # Base name for converted files
# ====================================

# Create output directories if they don't exist
os.makedirs(converted_output_dir, exist_ok=True)
os.makedirs(rt_output_dir, exist_ok=True)

# Get list of files to process
input_files = [f for f in os.listdir(raw_input_dir) if os.path.isfile(os.path.join(raw_input_dir, f))]

# Generate timestamp for this batch
batch_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Process each file
for counter, filename in enumerate(input_files, start=1):
    # ======== FILE NAMING ========
    converted_csv_name = f"{counter}_{base_name}_{batch_timestamp}.csv"
    rt_csv_name = f"{counter}_reaction_times_{batch_timestamp}.csv"

    # ======== FULL PATHS ========
    input_path = os.path.join(raw_input_dir, filename)
    converted_csv_path = os.path.join(converted_output_dir, converted_csv_name)
    rt_csv_path = os.path.join(rt_output_dir, rt_csv_name)
    # ============================

    # Load and parse file
    with open(input_path, "r") as f:
        lines = f.readlines()

    parsed_data = []
    for line in lines:
        line = line.strip()
        if line.startswith("(") and line.endswith(")"):
            try:
                t = eval(line)
                if len(t) == 3:
                    parsed_data.append(t)
            except:
                continue

    # Create and save converted CSV
    df = pd.DataFrame(parsed_data, columns=["time", "module", "action"])
    df.to_csv(converted_csv_path, index=False)

    # Calculate reaction times
    a_events = df[
        (df['module'] == 'visual') &
        (df['action'].str.contains('AUTOMATIC BUFFERING.*value= A', regex=True))
        ]['time'].tolist()

    key_events = df[
        (df['module'] == 'manual') &
        (df['action'].str.startswith('KEY PRESSED: 1'))
        ]['time'].tolist()

    rt_data = []
    key_idx = 0
    for a_time in a_events:
        while key_idx < len(key_events) and key_events[key_idx] <= a_time:
            key_idx += 1
        if key_idx < len(key_events):
            rt = key_events[key_idx] - a_time
            rt_data.append({'RTs': rt, 'start': a_time, 'end': key_events[key_idx]})
            key_idx += 1

    # Save RT results
    rt_df = pd.DataFrame(rt_data, columns=['RTs', 'start', 'end'])
    rt_df.to_csv(rt_csv_path, index=False)
    print(f"Processed {filename}")
    print(f"│─ Converted: {converted_csv_name}")
    print(f"└─ RTs: {rt_csv_name}\n")

print("\nBatch processing complete!")
print(f"Converted CSV files: {converted_output_dir}")
print(f"Reaction time files: {rt_output_dir}")