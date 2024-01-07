import psycopg2
import re
from psycopg2.extensions import parse_dsn, make_dsn

# Connect to your database
dsn = make_dsn(database="hust_student_manager", user="postgres", password="0000", host="localhost", port="5432")
dsn_dict = parse_dsn(dsn)
dsn_dict["options"] = "-c client_min_messages=notice"  # Enable notices
conn = psycopg2.connect(**dsn_dict)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)  # Set isolation level to AUTOCOMMIT to receive notices immediately
cur = conn.cursor()

# Read the query from a file
with open('query.sql', 'r') as f:
    query = f.read()

# Initialize total times for each part
total_times = [0, 0, 0, 0, 0]

# Execute the query 10 times and calculate the average execution time for each part
for _ in range(10):
    # Start a transaction block
    cur.execute("BEGIN;")
    cur.execute(query)
    cur.execute("ROLLBACK;")
    # Fetch notices and extract times
    # Fetch notices and extract times
notices = conn.notices
for notice in notices:
    match = re.search(r"Trigger execution time for checking Part (\d+): (\d+:\d+:\d+\.\d+)", notice)
    if match:
        part = int(match.group(1))  # Convert part to integer
        time_str = match.group(2)
        h, m, s = map(float, time_str.split(':'))
        time = h * 3600 + m * 60 + s  # Convert time to seconds
        total_times[part - 1] += time
# Calculate average times
average_times_ms = [round(total_time * 1000 / 10, 4) for total_time in total_times]
print("Average execution times for each part: {} ms".format(average_times_ms))

# Close the cursor and connection
cur.close()
conn.close()