<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Go/No-Go Task (PyACT-R)</title>
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: auto; padding: 20px; }
    h1, h2 { color: #2c3e50; }
    code { background: #f4f4f4; padding: 2px 4px; border-radius: 4px; }
    .folder { font-weight: bold; color: #34495e; }
    .disclaimer { background: #fff3cd; padding: 15px; border-left: 5px solid #ffc107; margin-top: 30px; }
  </style>
</head>
<body>
  <h1>Go/No-Go Task Implementation</h1>
  <p>This project is a simple implementation of the classic Go/No-Go psychological task using <code>pyactr</code>.</p>

  <h2>Task Overview</h2>
  <ul>
    <li><strong>Go Trials</strong>: Indicated by the letter <code>'A'</code>.</li>
    <li><strong>No-Go Trials</strong>: Indicated by the letter <code>'O'</code>.</li>
    <li><strong>Stimulus Duration</strong>: Each stimulus is presented for 1000 ms.</li>
    <li><strong>Inter-Stimulus Interval (ISI)</strong>: A blank screen is displayed between stimuli.</li>
    <li><strong>Trial Distribution</strong>: By default, 75% of the trials are Go trials, with a total of 125 trials.</li>
  </ul>

  <p>Most task settings (e.g., trial count, Go probability, timings) are configurable within the script.</p>

  <h2>Output</h2>
  <p>The simulation script produces ACT-R trace files in plain text format.</p>

  <h2>Analysis</h2>
  <ul>
    <li>Trace files (<code>.txt</code>) are converted into <code>.csv</code> files for analysis.</li>
    <li><strong>Reaction Time (RT)</strong> is calculated as:</li>
  </ul>
  <pre><code>RT = time of keypress - time when Go stimulus is processed in the visual buffer</code></pre>

  <h2>Folder Structure</h2>
  <ul>
    <li><span class="folder">data/</span> - Main directory containing all output data.</li>
    <li><span class="folder">raw/</span> - Contains raw <code>.txt</code> ACT-R trace files.</li>
    <li><span class="folder">converted/</span> - Contains <code>.csv</code> files converted from raw traces.</li>
    <li><span class="folder">RTs/</span> - Contains final <code>.csv</code> files with calculated RTs.</li>
  </ul>

  <div class="disclaimer">
    <strong>Disclaimer:</strong> This project was developed as an undergraduate research exercise. It is not validated for use in real experimental settings. If you intend to use or adapt this code for scientific experiments, please thoroughly review the logic, methodology, and implementation.
  </div>

</body>
</html>

