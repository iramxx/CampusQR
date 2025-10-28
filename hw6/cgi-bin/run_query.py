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
    print(f"<div class='auth-container'><div class='role-selection-wrapper' style='text-align:left;'><h2>{title}</h2>")

def print_html_footer(back_link_url):
    print(f"<br><a href='{back_link_url}' class='back-link'>← Back</a></div></div></body></html>")

def main():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    form = cgi.FieldStorage()
    query_type = form.getvalue('query')

    if query_type == '1_results':
        organizer_id = form.getvalue('organizer_id')
        cursor.execute("""
            SELECT E.event_id, E.title, E.event_date 
            FROM Events E JOIN Creates C ON E.event_id = C.event_id 
            WHERE C.user_id = %s
        """, (organizer_id,))
        results = cursor.fetchall()
        
        print_html_header(f"Query 1 Results: Events by Organizer")
        print("<ul>")
        for row in results:
            print(f"<li><a href='run_query.py?query=1_detail&event_id={row['event_id']}'>{row['title']}</a> ({row['event_date']})</li>")
        print("</ul>")
        print_html_footer(f"query_form_generator.py?query=1")

    elif query_type == '1_detail':
        event_id = form.getvalue('event_id')
        cursor.execute("SELECT * FROM Events WHERE event_id = %s", (event_id,))
        result = cursor.fetchone()

        print_html_header(f"Detail for Event: {result['title']}")
        print("<ul>")
        for key, value in result.items():
            print(f"<li><b>{key.replace('_', ' ').title()}:</b> {value}</li>")
        print("</ul>")
        print_html_footer(f"javascript:history.back()")

    elif query_type == '2_results':
        event_id = form.getvalue('event_id')
        cursor.execute("""
            SELECT U.user_id, U.name, A.student_id 
            FROM Users U 
            JOIN Attendee A ON U.user_id = A.user_id
            JOIN Register_to R ON U.user_id = R.user_id
            WHERE R.event_id = %s
        """, (event_id,))
        results = cursor.fetchall()
        
        print_html_header(f"Query 2 Results: Attendees for Event")
        print("<ul>")
        for row in results:
            print(f"<li><a href='run_query.py?query=2_detail&user_id={row['user_id']}'>{row['name']}</a> (Student ID: {row['student_id']})</li>")
        print("</ul>")
        print_html_footer(f"query_form_generator.py?query=2")

    elif query_type == '2_detail':
        user_id = form.getvalue('user_id')
        cursor.execute("""
            SELECT U.user_id, U.name, U.email, A.student_id 
            FROM Users U JOIN Attendee A ON U.user_id = A.user_id 
            WHERE U.user_id = %s
        """, (user_id,))
        result = cursor.fetchone()

        print_html_header(f"Detail for Attendee: {result['name']}")
        print("<ul>")
        for key, value in result.items():
            print(f"<li><b>{key.replace('_', ' ').title()}:</b> {value}</li>")
        print("</ul>")
        print_html_footer(f"javascript:history.back()")
        
    elif query_type == '3_results' or query_type == '3_detail':
        ticket_id = form.getvalue('ticket_id')
        cursor.execute("""
            SELECT T.*, E.title AS event_title, U.name AS owner_name
            FROM Tickets T
            LEFT JOIN Generates G ON T.ticket_id = G.ticket_id
            LEFT JOIN Events E ON G.event_id = E.event_id
            LEFT JOIN StudentTicket ST ON T.ticket_id = ST.ticket_id
            LEFT JOIN Users U ON ST.user_id = U.user_id
            WHERE T.ticket_id = %s
        """, (ticket_id,))
        result = cursor.fetchone()

        print_html_header(f"Detail for Ticket ID: {result['ticket_id']}")
        print("<ul>")
        for key, value in result.items():
            print(f"<li><b>{key.replace('_', ' ').title()}:</b> {value}</li>")
        print("</ul>")
        print_html_footer(f"query_form_generator.py?query=3")

    else:
        print_html_header("Error")
        print("<p>Unknown query results requested.</p>")
        print_html_footer("queries.html")

    if conn.is_connected():
        cursor.close()
        conn.close()

try:
    main()
except Exception as e:
    print("Content-Type: text/html\n")
    print(f"<h1>A critical error occurred in run_query.py</h1><pre>{e}</pre>")