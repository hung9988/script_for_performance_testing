import psycopg2
import re
import sqlparse
# Connect to your postgres DB
conn = psycopg2.connect(
    dbname="student_manager",
    user="postgres",
    password="0000",
    host="localhost",
    port="5432"
)

# Open a cursor to perform database operations
cur = conn.cursor()

# The query you want to analyze
with open('query.sql', 'r') as file:
    query = file.read().replace('\n', ' ')
# This will store the total execution time
total_time = 0
formatted_query = sqlparse.format(query, reindent=True, keyword_case='upper')

cur.execute("BEGIN;")
cur.execute("SET myapp.user_id=20220000;")
cur.execute("SET myapp.user_role='teacher';")
cur.execute("SET enable_seqscan=off;")
cur.execute("COMMIT;")

print("The query is: \n")
print(f"{formatted_query} \n")
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
avg_time = total_time / 10

# Format the average execution time with 4 decimal points
avg_time_formatted = format(avg_time, '.4f')

print(f"Average execution time of 10 executions: {avg_time_formatted} ms")

# Close communication with the database
cur.close()
conn.close()