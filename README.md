# Go/No-Go Task Implementation

This project is a simple implementation of the classic Go/No-Go psychological task using `pyactr`.

## Task Overview

- **Go Trials**: Indicated by the letter `'A'`.
- **No-Go Trials**: Indicated by the letter `'O'`.
- **Stimulus Duration**: Each stimulus is presented for 1000 ms.
- **Inter-Stimulus Interval (ISI)**: A blank screen is displayed between stimuli.
- **Trial Distribution**: By default, 75% of the trials are Go trials, with a total of 125 trials.

Most task settings (e.g., trial count, Go probability, timings) are configurable within the script.

## Output

The simulation script produces ACT-R trace files in plain text format.

## Analysis

- Trace files (`.txt`) are converted into `.csv` files for analysis.
- **Reaction Time (RT)** is calculated as:

```
RT = time of keypress - time when Go stimulus is processed in the visual buffer
```

## Folder Structure

- `data/` - Main directory containing all output data.
- `raw/` - Contains raw `.txt` ACT-R trace files.
- `converted/` - Contains `.csv` files converted from raw traces.
- `RTs/` - Contains final `.csv` files with calculated RTs.

> **Disclaimer**: This project was developed as an undergraduate research exercise. It is not validated for use in real experimental settings. If you intend to use or adapt this code for scientific experiments, please thoroughly review the logic, methodology, and implementation.

And that, dear mortals, concludes the README. You’re welcome.


