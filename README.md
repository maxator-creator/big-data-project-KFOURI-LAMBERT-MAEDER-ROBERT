# big-data-project-KFOURI-LAMBERT-MAEDER-ROBERT


This project was created by Maxime Maeder, Cyril Kfouri, Maxime Lambert, and Mathias Robert.

ECE Big Data Processing - Final Project

This project implements two distinct data processing pipelines: a batch analysis on the IMDb dataset and a real-time streaming analysis of Wikimedia edits.

📜 Description
Batch Analysis: The Jupyter notebook explores a large IMDb dataset (loaded from .tsv files) to answer specific analytical questions, such as finding the highest-rated comedy, identifying the earliest birth year, and computing statistics on genres and runtimes.

Stream Analysis: A standalone Python script connects to the Wikimedia EventStream to monitor edits in real time. It tracks specific entities, collects metrics, and implements an alerting mechanism for particular events or users.

📁 Project Structure and File Roles
Below is a description of the key files in this repository:

notebook.ipynb

Role: Core of the batch analysis.

Description: This Jupyter notebook contains all Python code (using Pandas) to:

- Download, decompress and load IMDb .tsv data files.
- Clean and analyze the data.
- Answer the analytical questions posed in the first part of the project.

wiki_stream_processor.py

Role: Core of the streaming analysis.

Description: This standalone Python script connects to Wikimedia's EventStream API and is designed to run continuously.

- It tracks 5 specific entities (for example: Tom_Hanks, The_Shawshank_Redemption).
- It collects edit metrics into `wiki_metrics.json`.
- It logs alerts (for example edits flagged by ClueBot NG) into `wiki_alerts.log`.
- It saves its position in the stream to `stream_state.json` so it can resume after a restart.

.gitignore

Role: Git configuration file.

Description: Lists files and folders for Git to ignore. This prevents committing very large data files (.tsv) and data directories (like `imdb_data/`) to the GitHub repository.

README.md

Role: Project documentation.

Description: The file you are reading now. It explains what the project is and how to use it.

Generated Files (Not Checked Into Git)
`imdb_data/` (directory)

Role: Contains raw data files.

Description: This directory is created to store the .tsv files downloaded from IMDb. It is ignored by Git.

`wiki_metrics.json`

Role: Streaming script output.

Description: JSON file that contains counts and metrics for the tracked entities.

`wiki_alerts.log`

Role: Streaming script output.

Description: Log file containing full JSON entries for each alert event.

`stream_state.json`

Role: Streaming script state file.

Description: Stores the stream bookmark (`latest_event_id`) so the script knows where to resume after a disconnect.

How to Run the Project

📦 Dependencies
Make sure you have the required Python libraries installed:

Bash:
pip install pandas requests requests-sse

Part 1: Batch Analysis (Notebook)

Run the notebook:

-Open and run the cells in `notebook.ipynb` using Jupyter Notebook or JupyterLab.

Part 2: Streaming Analysis (Script)
Run the script:

-Open a terminal (not inside Jupyter).

-Ensure the dependencies (especially `requests-sse`) are installed.

Run the script:

Bash:
python wiki_stream_processor.py


Observe the output:

-Leave the terminal open. The script runs indefinitely.

You will see messages like "Metrics saved at..." appearing periodically.

You can inspect `wiki_metrics.json` and `wiki_alerts.log` (if any alerts occurred) to see the incoming data in real time.

Stop the script:


-Press Ctrl+C in the terminal. The script saves a final state and exits gracefully.

