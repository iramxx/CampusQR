#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cgitb
cgitb.enable()

print("Content-Type: text/html\n")

import sys
import os
import pwd

def run_diagnostics():
    print("<html><head><title>Server Diagnostics</title>")
    print("<style>body { font-family: monospace; padding: 20px; } h2 { color: #0f4c6e; } pre { background-color: #f0f0f0; padding: 10px; border: 1px solid #ccc; white-space: pre-wrap; word-wrap: break-word; }</style>")
    print("</head><body>")
    print("<h1>Apache/Python Environment Diagnostics</h1>")
    
    try:
        user_info = pwd.getpwuid(os.getuid())
        username = user_info[0]
        print(f"<h2>1. Script is running as user:</h2><p><b>{username}</b></p>")
        if username == 'kjurabaev':
            print("<p><i>(Good! suexec seems to be working correctly.)</i></p>")
        else:
            print("<p><i>(Note: Script is running as a generic web server user.)</i></p>")

        py_version = sys.version
        print(f"<h2>2. Python Version:</h2><p>{py_version}</p>")
        
        py_path = sys.path
        print("<h2>3. Python Library Search Path (sys.path):</h2>")
        print("<pre>")
        for path in py_path:
            print(path)
        print("</pre>")
        
        print("<h2>4. Testing 'mysql.connector' import:</h2>")
        try:
            import mysql.connector
            print("<p style='color: green;'><b>SUCCESS:</b> 'mysql.connector' module was successfully imported.</p>")
            print(f"<p>Location: {mysql.connector.__file__}</p>")
        except Exception as e:
            print(f"<p style='color: red;'><b>FAILURE:</b> Could not import 'mysql.connector'.</p>")
            print(f"<p><b>Error Details:</b> {e}</p>")
            
    except Exception as e:
        print("<h2>A critical error occurred during diagnostics:</h2>")
        print(f"<p style='color: red;'>{e}</p>")
        
    print("</body></html>")

if __name__ == "__main__":
    run_diagnostics()