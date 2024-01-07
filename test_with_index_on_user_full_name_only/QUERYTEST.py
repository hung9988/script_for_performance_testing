import psycopg2
import re

# Connect to your postgres DB
conn = psycopg2.connect(
    dbname="hust_student_manager",
    user="postgres",
    password="0000",
    host="localhost",
    port="5432"
)

# Open a cursor to perform database operations
cur = conn.cursor()
cur.execute("BEGIN;")
cur.execute("SET myapp.user_role='admin';")
cur.execute("COMMIT;")
# The query you want to analyze
with open('query.sql', 'r') as file:
    query = file.read().replace('\n', ' ')
with open('querymiddle.sql', 'r') as file:
    querymiddle = file.read().replace('\n', ' ')
with open('queryafter.sql', 'r') as file:
    queryafter = file.read().replace('\n', ' ')
# This will store the total execution time
total_time = 0

# Run the EXPLAIN ANALYZE query 10 times
for _ in range(10):
    cur.execute("BEGIN;")
    cur.execute(f"EXPLAIN ANALYZE {query}")
    rows = cur.fetchall()
    cur.execute("ROLLBACK;")
   
    last_row = rows[-1][0]
    print(last_row)
   
    match = re.search(r'Execution Time: (\d+\.\d+) ms', last_row)
    if match:
        exec_time = float(match.group(1))
        total_time += exec_time

# Calculate the average execution time
avg_time_before = total_time / 10

# Format the average execution time with 4 decimal points
avg_time_formatted_before = format(avg_time_before, '.4f')

print(f"Average execution time BEFORE: {avg_time_formatted_before} ms")

if querymiddle != "":
    cur.execute(f"{querymiddle}")

total_time = 0

# Run the EXPLAIN ANALYZE query 10 times
for _ in range(10):
    cur.execute("BEGIN;")
    cur.execute(f"EXPLAIN ANALYZE {query}")
    rows = cur.fetchall()
    cur.execute("ROLLBACK;")
   
    last_row = rows[-1][0]
    print(last_row)
   
    match = re.search(r'Execution Time: (\d+\.\d+) ms', last_row)
    if match:
        exec_time = float(match.group(1))
        total_time += exec_time

# Calculate the average execution time
avg_time_after = total_time / 10

# Format the average execution time with 4 decimal points
avg_time_formatted_after = format(avg_time_after, '.4f')

print(f"Average execution time AFTER: {avg_time_formatted_after} ms")
if queryafter != "":
    cur.execute(f"{queryafter}")

print(f"Percentage increase: {format((1-(avg_time_after/avg_time_before))*100,'.2f')}%")
print(f"Time difference: {format(avg_time_after-avg_time_before,'.2f')}")
# Close communication with the database
cur.close()
conn.close()