from turtle import update
import requests, time, sys, io, os
from datetime import date
import json
from tqdm import tqdm
from collections import defaultdict
 
# ── CONFIG ────────────────────────────────────────────────────────────────────
NOTION_TOKEN  = ""  # https://www.notion.so/my-integrations
DATABASE_ID   = ""               # 32-char ID from the database URL
total = 11            #tqdm total count (for progress bar, if needed)
# ─────────────────────────────────────────────────────────────────────────────
 
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}
 
 
def query_database(database_id: str) -> list[dict]:
    """Fetches all pages from a Notion database (handles pagination)."""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    results = []
    payload = {}
 
    while True:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()
 
        results.extend(data.get("results", []))
 
        # Notion paginates at 100 items; keep fetching if there's more
        if data.get("has_more"):
            payload["start_cursor"] = data["next_cursor"]
        else:
            break
 
    return results
 
 
def extract_status(page: dict) -> dict:
    """Extracts task name and status from a Notion page."""
    props = page.get("properties", {})
 
    # Task name — usually a "title" property
    task_name = ""
    for prop in props.values():
        if prop.get("type") == "title":
            title_parts = prop.get("title", [])
            task_name = "".join(t.get("plain_text", "") for t in title_parts)
            break
 
    # Status — look for a property named "Status"
    status_value = "Unknown"
    status_prop = props.get("Status", {})
    prop_type = status_prop.get("type")
 
    if prop_type == "status":          # Native Notion Status field
        s = status_prop.get("status") or {}
        status_value = s.get("name", "Unknown")
    elif prop_type == "select":        # Select field used as status
        s = status_prop.get("select") or {}
        status_value = s.get("name", "Unknown")
 
    return {"task": task_name, "status": status_value}

# ── PROGRESS BAR (OPTIONAL) ───────────────────────────────────────────────
def get_progressbar(total, update_count):
    progress = tqdm(total = total, desc = "Task Progress Percentage")
    update_count = update_count
    for _ in range(int(update_count)):
        time.sleep(0.1) #simulation of progress
        progress.update(1)
 
    progress.close()

# - Optional: write output to file
def  write_output_to_file(arb_func, today : str = str(date.today())) -> str:
    print("\nWriting output to notion_output.txt...")

    buffer = io.StringIO('')
    content = ""

    #change standard output to buffer
    old_stdout = sys.stdout
    sys.stdout = buffer
    old_stderr = sys.stderr
    sys.stderr = buffer

    try:
        arb_func()
    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        # Reset standard output to console
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    print("Captured output:\n", repr(buffer.getvalue()))
    content = (today + " - " + (buffer.getvalue().split("\r")[-1]).replace("#", "█"))
    return content




def update_log_file(content) -> None:
    today = str(date.today())
    LOG_FILE = "notion_output.txt"

    lines = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()

    update = False

    for i, line in enumerate(lines):
        if line.startswith(today):
            lines[i]  = f"{today} - {content}\n"
            update  = True
            break

    if not update:
        lines.append(f"{today} - {content}\n")

    with open(LOG_FILE, "w", encoding='utf-8') as f:
        f.writelines(lines)
        f.write(" :: sys.stdout is writable: {_} \n".format(_ = str(sys.stdout.writable())))


# Function to determine the write mode for the log file

def log_once() -> str:
    today = str(date.today())
    log_file = "notion_output.txt"

    if os.path.exists(log_file):
        print(f"Log file '{log_file}' exists. Checking last entry...")

        with open(log_file, "r") as f:
            lines = f.readlines()

        # Handle empty file
        if not lines:
            return "a"

        last_line = lines[-1].strip()

        if today in last_line:
            return "w"
        else:
            return "a"

    else:
        print(f"Log file '{log_file}' does not exist. Creating a new one...")
        return "a"
 
 
def main():
    print("Fetching data from Notion...\n")
    pages = query_database(DATABASE_ID)
    tasks = [extract_status(p) for p in pages]
    update = 0
 
    # ── All statuses ──────────────────────────────────────────────────────────
    print("=== All Status Values ===")
    for t in tasks:
        print(f"  {t['task']:<35} → {t['status']}")
 
    # ── Unique statuses ───────────────────────────────────────────────────────
    unique = list(dict.fromkeys(t["status"] for t in tasks))
    print(f"\n=== Unique Statuses ({len(unique)}) ===")
    for s in unique:
        print(f"  {s}")
 
    # ── Grouped by status ─────────────────────────────────────────────────────
    grouped = defaultdict(list)
    for t in tasks:
        grouped[t["status"]].append(t["task"])
 
    print("\n=== Tasks Grouped by Status ===")
    for status, task_list in grouped.items():
        print(f"\n  [{status}] ({len(task_list)} tasks)")
        if status == "Done":
            update = len(task_list)
        for task in task_list:
            print(f"    - {task}")

# Optional: show progress bar if there are many tasks
    get_progressbar(total, update)
    bol = write_output_to_file(lambda: get_progressbar(total, update))
    update_log_file(bol)
    
 
 
if __name__ == "__main__":
    main()
    

print("Current working directory:", os.getcwd())
print("File will be written to:", os.path.abspath("notion_output.txt"))



