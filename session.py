import psycopg2
import random

# Connect to your database
conn = psycopg2.connect(database="hust_student_manager", user="postgres", password="0000", host="localhost", port="5432")
cur = conn.cursor()

# Fetch user_id and role from the users table
cur.execute("SELECT user_id, role FROM users")
users = cur.fetchall()

# Generate 1000 random insert statements
for _ in range(1000):
    user_id, role = random.choice(users)
    cur.execute(f"""
        INSERT INTO sessions (user_id, role)
        VALUES ({user_id}, '{role}')
    """)

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()