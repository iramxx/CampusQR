#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cgitb
cgitb.enable()

import cgi
import mysql.connector
from mysql.connector import Error
import os

db_config = { 'host': 'localhost', 'database': 'db_kjurabaev', 'user': 'kjurabaev', 'password': '5tr8zjbrDq1GchfY' }
username = os.environ.get('USER', 'kjurabaev')

def print_html_header(title):
    print("Content-Type: text/html\n")
    print(f"<html><head><title>{title}</title><link rel='stylesheet' href='/~{username}/auth-style.css'></head><body>")
    print(f"<div class='auth-container'><div class='form-container'><h2>{title}</h2>")

def print_html_footer():
    print(f"<a href='/~{username}/queries.html' class='back-link'>← Back to Queries</a></div></div></body></html>")

def get_select_options(cursor, query):
    cursor.execute(query)
    items = cursor.fetchall()
    options = ""
    for item in items:
        options += f"<option value='{item[0]}'>{item[1]}</option>\n"
    return options

def main():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    form_data = cgi.FieldStorage()
    query_type = form_data.getvalue('query')
    
    if query_type == '1':
        print_html_header("Query 1: Select an Organizer")
        options = get_select_options(cursor, "SELECT U.user_id, U.name FROM Users U JOIN Organizers O ON U.user_id = O.user_id ORDER BY U.name")
        print('<form action="run_query.py?query=1_results" method="POST">')
        print(f'<div class="form-group"><label>Show events for Organizer:</label><select name="organizer_id" class="form-group" style="width:100%; padding:15px;">{options}</select></div>')
        print('<button type="submit" class="btn-submit">Run Query</button></form>')

    elif query_type == '2':
        print_html_header("Query 2: Select an Event")
        options = get_select_options(cursor, "SELECT event_id, title FROM Events ORDER BY title")
        print('<form action="run_query.py?query=2_results" method="POST">')
        print(f'<div class="form-group"><label>Show attendees for Event:</label><select name="event_id" class="form-group" style="width:100%; padding:15px;">{options}</select></div>')
        print('<button type="submit" class="btn-submit">Run Query</button></form>')

    elif query_type == '3':
        print_html_header("Query 3: Select a Ticket")
        options = get_select_options(cursor, "SELECT ticket_id, qr_code_data FROM Tickets ORDER BY ticket_id DESC")
        print('<form action="run_query.py?query=3_results" method="POST">')
        print(f'<div class="form-group"><label>Show details for Ticket:</label><select name="ticket_id" class="form-group" style="width:100%; padding:15px;">{options}</select></div>')
        print('<button type="submit" class="btn-submit">Run Query</button></form>')
    
    else:
        print_html_header("Error")
        print("<p>Unknown query type requested.</p>")

    print_html_footer()

    if conn.is_connected():
        cursor.close()
        conn.close()

try:
    main()
except Exception as e:
    print("Content-Type: text/html\n")
    print(f"<h1>A critical error occurred</h1><pre>{e}</pre>")