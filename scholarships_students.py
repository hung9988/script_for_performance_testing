import psycopg2
import random
from faker import Faker

# Create a Faker instance
fake = Faker()

# Connect to your database
conn = psycopg2.connect(
    host="localhost",
    database="hust_student_manager",
    user="postgres",
    password="0000"
)

# Create a cursor
cur = conn.cursor()

# Fetch all enterprise_id values from the enterprises table
cur.execute("SELECT student_id FROM students")
students = [item[0] for item in cur.fetchall()]

# Get all scholarship_ids from the scholarships table
cur.execute("SELECT scholarship_id FROM scholarships")
scholarships = [item[0] for item in cur.fetchall()]
cur.execute("SELECT student_id, scholarship_id FROM students_scholarships")
# Insert 1000 rows of fake data into the students_scholarships table
existing_pairs = set(cur.fetchall())

# Generate new pairs and insert them into the students_scholarships table
for _ in range(1000):
    while True:
        new_pair = (random.choice(students), random.choice(scholarships))
        if new_pair not in existing_pairs:
            break
    cur.execute("""
        INSERT INTO students_scholarships (student_id, scholarship_id)
        VALUES (%s, %s)
    """, new_pair)
    existing_pairs.add(new_pair)  # Add the new pair to the set of existing pairs

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()