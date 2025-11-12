import os
from collections import Counter
from datetime import datetime

ACCESS_LOG_PATH = '/var/log/apache2/access_log'
ERROR_LOG_PATH = '/var/log/apache2/error_log'
TARGET_USER = 'kjurabaev'

def parse_access_log(log_path, username):
    log_entries = []
    page_counter = Counter()
    filter_string = f"~{username}"

    try:
        with open(log_path, 'r', errors='ignore') as f:
            for line in f:
                if filter_string in line:
                    parts = line.split('"')
                    if len(parts) < 3:
                        continue 

                    try:
                        main_parts = parts[0].split()
                        request_parts = parts[1].split()
                        
                        entry = {
                            'ip': main_parts[0],
                            'timestamp': main_parts[3].strip('['),
                            'page': request_parts[1] if len(request_parts) > 1 else request_parts[0],
                            'user_agent': parts[5]
                        }

                        log_entries.append(entry)
                        page_counter[entry['page']] += 1
                    except (IndexError, ValueError):
                        continue
    except FileNotFoundError:
        print(f"ERROR: Access log not found at '{log_path}'.")
        return None, None
    except PermissionError:
        print(f"ERROR: Permission denied to read '{log_path}'.")
        return None, None
        
    return log_entries, page_counter

def parse_error_log(log_path, username):
    log_entries = []
    return log_entries

def main():
    print("--- APACHE LOG ANALYZER ---")
    
    access_entries, page_counts = parse_access_log(ACCESS_LOG_PATH, TARGET_USER)
    
    if access_entries:
        print("\n\n--- ACCESS LOG ANALYSIS ---\n")
        
        print("1. Page Access Frequency:")
        if not page_counts:
            print("  - No pages specific to your user found in the access log.")
        else:
            for page, count in page_counts.most_common():
                print(f"  - {page}: {count} times")
            
        print("\n2. Detailed Access Timeline (Last 20 entries):")
        sorted_entries = sorted(access_entries, key=lambda x: datetime.strptime(x['timestamp'], '%d/%b/%Y:%H:%M:%S'), reverse=True)
        for entry in sorted_entries[:20]:
            dt_object = datetime.strptime(entry['timestamp'], '%d/%b/%Y:%H:%M:%S')
            formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
            print(f"  - Time: {formatted_time} | IP: {entry['ip']} | Page: {entry['page']} | Browser: {entry['user_agent']}")
    else:
        print("\n\n--- ACCESS LOG ANALYSIS ---\n")
        print("  - Could not process or find any entries in the access log.")

    error_entries = parse_error_log(ERROR_LOG_PATH, TARGET_USER)
    
    if error_entries is not None:
        print("\n\n--- ERROR LOG ANALYSIS ---\n")
        if not error_entries:
            print("  - No error log entries specific to your user found.")

if __name__ == '__main__':
    main()