import pyactr as actr
import contextlib
from datetime import datetime
import random
import math
import os

# SPECIFY OUTPUT PATH
output_dir = "data/raw"


def generate_trials(total_trials, go_prob=0.75):
    """
    Generate a randomized list of go/nogo trials with inter-stimulus intervals.

    Args:
        total_trials (int): Total number of actual trials (excluding spaces and DONE)
        go_prob (float): Probability of go trials (0.0-1.0)

    Returns:
        list: Trial sequence with spaces and DONE marker
    """
    # Calculate number of go/nogo trials
    go_trials = math.ceil(total_trials * go_prob)
    nogo_trials = total_trials - go_trials

    # Create trial list
    trials = ["A"] * go_trials + ["O"] * nogo_trials
    random.shuffle(trials)

    # Add spaces between trials and DONE at end
    sequence = []
    for trial in trials:
        sequence.append(trial)
        sequence.append(" ")  # Add inter-stimulus interval

    sequence.append("DONE")  # Final marker

    return sequence


# Configuration with termination signal
letters = generate_trials(125, go_prob=0.75)
letter_duration = 1
screen_center = (320, 185)

# Create environment
environ = actr.Environment(focus_position=screen_center)

# Initialize model
m = actr.ACTRModel(environment=environ, subsymbolic=True)

# Declare chunk types
actr.chunktype("read", "state, finished")
actr.chunktype("image", "img")

# Initialize buffers with termination flag
m.goal.add(actr.chunkstring(name="reading", string="""
    isa     read
    state   start
    finished no"""))

g2 = m.set_goal("g2")
g2.delay = 0.2

m.productionstring(name="encode_letter", string="""
    =g>
        isa     read
        state   start
        finished no
    =visual>
        isa     _visual
        value  =letter
        value ~"DONE"
    ==>
    =g>
        isa     read
        state   processing
        finished no
    +g2>
        isa     image
        img     =letter""")

m.productionstring(name="respond_to_A", string="""
    =g>
        isa     read
        state   processing
        finished no
    =g2>
        isa     image
        img     "A"
    ?manual>
        state   free
    ==>
    =g>
        isa     read
        state   done
        finished no
    +manual>
        isa     _manual
        cmd     press_key
        key     "1" """)

m.productionstring(name="ignore_non_A", string="""
    =g>
        isa     read
        state   processing
        finished no
    =g2>
        isa     image
        img     =letter
    ?manual>
        state   free
    ==>
    =g>
        isa     read
        state   done
        finished no""")

m.productionstring(name="reset_goal", string="""
    =g>
        isa     read
        state   done
        finished no
    ==>
    =g>
        isa     read
        state   start
        finished no""")

# termination production rules
m.productionstring(name="detect_finish", string="""
    =g>
        isa read
        state None
        finished no
    =visual>
        isa     _visual
        value   "DONE"
    ==>
    =g>
        isa     read
        state None
        finished yes""")

m.productionstring(name="terminate", string="""
    =g>
        isa     read
        state None
        finished yes
    ==>
    ~g>""")

# Create stimuli with termination signal
stimuli = []
for i, letter in enumerate(letters):
    key = f"stimulus{i}-0time"
    stimuli.append({key: {"text": letter, "position": screen_center}})

if __name__ == "__main__":
    sim = m.simulation(
        realtime=False,
        environment_process=environ.environment_process,
        stimuli=stimuli,
        triggers=letters,
        times=letter_duration
    )
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename with timestamp
    base_name = 'actr_trace_raw'
    ext = '.txt'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_name}_{timestamp}{ext}"

    # Join directory and filename
    filepath = os.path.join(output_dir, filename)

    # Write output
    with open(filepath, 'w') as f:
        with contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
            sim.run(letter_duration)

    print(f"Raw traces saved to: {filepath}")
