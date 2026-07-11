# Python_Notion-OS-Automation
# 📊 Notion Task Progress Tracker

A Python utility that connects to the Notion API, retrieves all tasks from a Notion database, calculates project progress, displays a terminal progress bar, and logs the daily completion status to a local text file.

---

## Features

- Connects to the Notion API
- Retrieves every page from a Notion database
- Handles database pagination automatically
- Extracts task names and statuses
- Groups tasks by status
- Displays all unique status values
- Calculates completed tasks
- Shows a progress bar using `tqdm`
- Logs daily project progress to `notion_output.txt`
- Updates today's log instead of creating duplicate entries

---

## Demo

```
Fetching data from Notion...

=== All Status Values ===
Task 1                          → Done
Task 2                          → In Progress
Task 3                          → Done

=== Unique Statuses (3) ===
Done
In Progress
Not Started

=== Tasks Grouped by Status ===

[Done] (5 tasks)
    - Literature Review
    - Chapter 1

Task Progress Percentage: 45%|██████████████████          | 5/11
```

---

# Project Structure

```
.
├── main.py
├── notion_output.txt
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Requirements

- Python 3.10+
- Notion Integration Token
- Notion Database

Python libraries:

- requests
- tqdm

Install dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pip install requests tqdm
```

---

# Configuration

Inside the script, update the following variables:

```python
NOTION_TOKEN = "your_notion_token"
DATABASE_ID = "your_database_id"
total = 11
```

| Variable | Description |
|----------|-------------|
| NOTION_TOKEN | Internal Integration Token from Notion |
| DATABASE_ID | Database ID of your task database |
| total | Total number of expected tasks |

---

# How It Works

```
                Notion Database
                      │
                      ▼
             query_database()
                      │
                      ▼
             Extract Task Status
                      │
                      ▼
            Group Tasks by Status
                      │
                      ▼
          Count Completed ("Done")
                      │
                      ▼
              Generate Progress Bar
                      │
                      ▼
            Save Daily Progress Log
```

---

# Functions

## query_database()

Retrieves all pages from a Notion database.

Handles pagination automatically.

Returns

```python
list[dict]
```

---

## extract_status()

Extracts

- Task name
- Task status

Returns

```python
{
    "task": "...",
    "status": "Done"
}
```

---

## get_progressbar()

Displays a terminal progress bar using **tqdm**.

Parameters

```python
total
update_count
```

---

## write_output_to_file()

Redirects terminal output to an in-memory buffer and formats it for logging.

Returns

```python
str
```

---

## update_log_file()

Updates the current day's log inside

```
notion_output.txt
```

instead of appending duplicate entries.

---

## log_once()

Determines whether today's log already exists.

Returns

```
"a"
```

or

```
"w"
```

---

## main()

Main execution flow.

1. Retrieve database
2. Extract task status
3. Print summary
4. Count completed tasks
5. Display progress bar
6. Save today's progress

---

# Example Output File

```
2026-07-11 - Task Progress Percentage: 45% |██████████████████          |
```

---

# Requirements File

Create a `requirements.txt`

```
requests
tqdm
```

Install with

```bash
pip install -r requirements.txt
```

---

# Future Improvements

- [ ] Store API token in `.env`
- [ ] Automatic total task count
- [ ] Percentage calculation
- [ ] Export to CSV
- [ ] Export to Excel
- [ ] Email daily progress report
- [ ] Desktop notification
- [ ] GUI using Tkinter or PyQt
- [ ] GitHub Actions automation
- [ ] Logging with Python `logging` module

---

# Security

⚠ **Do not expose your Notion Integration Token.**

Instead of

```python
NOTION_TOKEN = "ntn_xxxxxxxxx"
```

use

```python
import os

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
```

and store it in a `.env` file or as an environment variable.

Also add to `.gitignore`:

```
.env
```

---

# Technologies Used

- Python
- Notion API
- Requests
- tqdm
- JSON
- defaultdict
- StringIO
- File I/O

---

# License

MIT License

---

# Author

Psalm Yoseff C. Aguilar

University of Santo Thomas

IS Research / Embedded Systems / Python Development
