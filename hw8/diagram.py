import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ========= 1. Paste the full log text here =========
text = """


--- ACCESS LOG ANALYSIS ---

1. Page Access Frequency:
  - /~kjurabaev/auth-style.css: 26 times
  - /~kjurabaev/cgi-bin/form_generator.py?form=maintenance_hub: 12 times
  - /~kjurabaev/maintenance.html: 11 times
  - /~kjurabaev/style.css: 10 times
  - /~kjurabaev/logo.png: 10 times
  - /~kjurabaev/Kamronbek.jpeg: 10 times
  - /~kjurabaev/Taha.png: 10 times
  - /~kjurabaev/Ahmed.png: 10 times
  - /~kjurabaev/cgi-bin/query_form_generator.py?query=1: 8 times
  - /~kjurabaev/cgi-bin/query_form_generator.py?query=3: 7 times
  - /~kjurabaev/: 6 times
  - /~kjurabaev/cgi-bin/run_query.py?query=1_results: 6 times
  - /~kjurabaev/index.html: 5 times
  - /~kjurabaev/cgi-bin/run_query.py?query=3_results: 4 times
  - /~kjurabaeve: 3 times
  - /~kjurabaev/cgi-bin/form_generator.py?form=link_creates&admin_user=admin&admin_pass=SuperSecret123: 3 times
  - /favicon.ico: 3 times
  - /~kjurabaev/queries.html: 3 times
  - /~kjurabaev: 2 times
  - /~kjurabaev/start.html: 2 times
  - /~kjurabaev/cgi-bin/form_generator.py?form=add_user&admin_user=admin&admin_pass=SuperSecret123: 1 times
  - /~kjurabaev/cgi-bin/process_form.py?action=add_user: 1 times
  - /~kjurabaev/cgi-bin/form_generator.py?form=add_organizer&admin_user=admin&admin_pass=SuperSecret123: 1 times
  - /~kjurabaev/cgi-bin/process_form.py?action=add_organizer: 1 times
  - /~kjurabaev/cgi-bin/form_generator.py?form=add_talk&admin_user=admin&admin_pass=SuperSecret123: 1 times
  - /~kjurabaev/cgi-bin/process_form.py?action=add_talk: 1 times
  - /~kjurabaev/login.html: 1 times
  - /~kjurabaev/cgi-bin/run_query.py?query=1_detail&event_id=3: 1 times
  - /~kjurabaev/login.html?type=attendee: 1 times
  - /~kjurabaev/cgi-bin/query_form_generator.py?query=2: 1 times
  - /~kjurabaev/cgi-bin/query_form_generator.py?query=4: 1 times
  - /~kjurabaev/cgi-bin/run_query.py?query=2_results: 1 times
  - /~kjurabaev/cgi-bin/run_query.py?query=4_results: 1 times

2. Detailed Access Timeline (Last 20 entries):
  - Time: 2025-11-12 20:05:45 | IP: 172.16.113.5 | Page: /~kjurabaev/cgi-bin/form_generator.py?form=maintenance_hub | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
  - Time: 2025-11-12 20:05:28 | IP: 172.16.113.5 | Page: /~kjurabaev/cgi-bin/form_generator.py?form=maintenance_hub | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
  - Time: 2025-11-12 20:05:12 | IP: 172.16.113.5 | Page: /~kjurabaev/cgi-bin/form_generator.py?form=maintenance_hub | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
  - Time: 2025-11-12 20:05:01 | IP: 172.16.113.5 | Page: /~kjurabaev/cgi-bin/form_generator.py?form=maintenance_hub | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
  - Time: 2025-11-12 20:04:56 | IP: 172.16.113.5 | Page: /~kjurabaev/auth-style.css | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
  - Time: 2025-11-12 20:04:55 | IP: 172.16.113.5 | Page: /~kjurabaev/maintenance.html | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
  - Time: 2025-11-12 20:04:54 | IP: 172.16.113.5 | Page: /~kjurabaev/ | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
  - Time: 2025-11-12 20:04:54 | IP: 172.16.113.5 | Page: /~kjurabaev/style.css | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
  - Time: 2025-11-12 20:04:54 | IP: 172.16.113.5 | Page: /~kjurabaev/logo.png | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
  - Time: 2025-11-12 20:04:54 | IP: 172.16.113.5 | Page: /~kjurabaev/Kamronbek.jpeg | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
  - Time: 2025-11-12 20:04:54 | IP: 172.16.113.5 | Page: /~kjurabaev/Taha.png | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
  - Time: 2025-11-12 20:04:54 | IP: 172.16.113.5 | Page: /~kjurabaev/Ahmed.png | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
  - Time: 2025-11-12 20:04:54 | IP: 172.16.113.5 | Page: /favicon.ico | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
  - Time: 2025-11-12 17:58:31 | IP: 172.16.123.86 | Page: /~kjurabaev/cgi-bin/run_query.py?query=1_results | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 OPR/123.0.0.0
  - Time: 2025-11-12 17:58:30 | IP: 172.16.123.86 | Page: /~kjurabaev/cgi-bin/query_form_generator.py?query=1 | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 OPR/123.0.0.0
  - Time: 2025-11-12 17:57:21 | IP: 172.16.123.86 | Page: /~kjurabaev/cgi-bin/query_form_generator.py?query=1 | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 OPR/123.0.0.0
  - Time: 2025-11-12 17:57:20 | IP: 172.16.123.86 | Page: /~kjurabaev/cgi-bin/query_form_generator.py?query=1 | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 OPR/123.0.0.0
  - Time: 2025-11-12 17:57:18 | IP: 172.16.123.86 | Page: /~kjurabaev/cgi-bin/query_form_generator.py?query=1 | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 OPR/123.0.0.0
  - Time: 2025-11-12 17:57:15 | IP: 172.16.123.86 | Page: /~kjurabaev/cgi-bin/run_query.py?query=1_results | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 OPR/123.0.0.0
  - Time: 2025-11-12 17:57:12 | IP: 172.16.123.86 | Page: /~kjurabaev/cgi-bin/query_form_generator.py?query=1 | Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 OPR/123.0.0.0



--- ERROR LOG ANALYSIS ---

  - No error log entries specific to your user found.

"""

# ========= 2. Parse Access Log Section =========
# --- Page access frequency ---
freq_pattern = re.compile(r'- ([^\:]+): (\d+) times')
freq_data = freq_pattern.findall(text)
df_freq = pd.DataFrame(freq_data, columns=['Page', 'Count'])
df_freq['Count'] = df_freq['Count'].astype(int)
df_freq = df_freq.sort_values('Count', ascending=False)

# --- Access timeline entries ---
timeline_pattern = re.compile(
    r'Time: ([\d\-: ]+) \| IP: ([\d\.]+) \| Page: ([^|]+) \| Browser: (.+)'
)
timeline_data = timeline_pattern.findall(text)
df_time = pd.DataFrame(timeline_data, columns=['Time', 'IP', 'Page', 'Browser'])
if not df_time.empty:
    df_time['Time'] = pd.to_datetime(df_time['Time'], errors='coerce')

# ========= 3. Parse Error Log Section =========
error_section_match = re.search(r'--- ERROR LOG ANALYSIS ---([\s\S]*)', text)
error_lines = []
if error_section_match:
    error_section = error_section_match.group(1)
    error_lines = [line.strip('- ').strip() for line in error_section.splitlines() if line.strip()]
    # Filter meaningful error lines (ignore "no error" text)
    error_lines = [e for e in error_lines if not e.lower().startswith("no error")]

# ========= 4. Save CSVs =========
df_freq.to_csv("page_frequency.csv", index=False)
df_time.to_csv("access_timeline.csv", index=False)
print("✅ Saved: page_frequency.csv, access_timeline.csv")

if error_lines:
    df_err = pd.DataFrame(error_lines, columns=["Error"])
    df_err.to_csv("error_log.csv", index=False)
    print("✅ Saved: error_log.csv")
else:
    df_err = pd.DataFrame(columns=["Error"])
    df_err.to_csv("error_log.csv", index=False)
    print("✅ Saved: empty error_log.csv (no errors)")

# ========= 5. Create Visual Diagrams =========
plt.style.use('seaborn-v0_8-whitegrid')

# --- Page Frequency Chart ---
plt.figure(figsize=(10, 6))
plt.barh(df_freq['Page'], df_freq['Count'], color='steelblue')
plt.title("Page Access Frequency")
plt.xlabel("Access Count")
plt.ylabel("Page")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("page_frequency_chart.png")
plt.close()
print("✅ Saved: page_frequency_chart.png")

# --- Access Timeline Chart ---
if not df_time.empty:
    df_time.set_index('Time', inplace=True)
    df_time.resample('1T').size().plot(kind='line', figsize=(8, 4), color='orange')
    plt.title("Access Frequency Over Time")
    plt.ylabel("Requests per Minute")
    plt.xlabel("Time")
else:
    # Empty chart if no data
    plt.figure(figsize=(8, 4))
    plt.title("Access Frequency Over Time")
    plt.ylabel("Requests per Minute")
    plt.xlabel("Time")
plt.tight_layout()
plt.savefig("timeline_chart.png")
plt.close()
print("✅ Saved: timeline_chart.png")

# --- Error Charts ---
if not df_err.empty:
    # Frequency of each error message
    error_counts = df_err["Error"].value_counts()
    # Error occurrences over time (if any timestamp found)
    time_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
    error_times = []
    for e in df_err["Error"]:
        match = time_pattern.search(e)
        if match:
            error_times.append(datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S"))
    df_time_err = pd.DataFrame(error_times, columns=["Time"]) if error_times else pd.DataFrame(columns=["Time"])
else:
    error_counts = pd.Series(dtype=int)
    df_time_err = pd.DataFrame(columns=["Time"])

# --- Error Frequency Chart ---
plt.figure(figsize=(8, 4))
if not error_counts.empty:
    error_counts.plot(kind='bar', color='lightcoral')
else:
    plt.bar([], [])
plt.title("Error Occurrences by Type")
plt.xlabel("Error Type / Message")
plt.ylabel("Occurrences")
plt.tight_layout()
plt.savefig("error_frequency_chart.png")
plt.close()
print("✅ Saved: error_frequency_chart.png")

# --- Error Timeline Chart ---
plt.figure(figsize=(8, 4))
if not df_time_err.empty:
    df_time_err.set_index("Time").resample("1H").size().plot(kind="line", color='red')
else:
    plt.plot([], [])
plt.title("Error Frequency Over Time")
plt.xlabel("Time")
plt.ylabel("Number of Errors")
plt.tight_layout()
plt.savefig("error_timeline_chart.png")
plt.close()
print("✅ Saved: error_timeline_chart.png")

print("\n🎯 All analysis completed successfully!")