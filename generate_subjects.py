import psycopg2
from faker import Faker
import random
import string

# Connect to your postgres DB
conn = psycopg2.connect("dbname=student_manager user=postgres password=0000 host=localhost")
cur = conn.cursor()

# Initialize Faker
fake = Faker()

# Number of subjects to create
num_subjects = 1000
cur.execute("SELECT subject_id FROM subjects")
existing_subject_ids = set(row[0] for row in cur.fetchall())

for _ in range(num_subjects):
    # Generate data
    while True:
        subject_id = ''.join(random.choices(string.ascii_uppercase, k=2)) + ''.join(random.choices(string.digits, k=4))
        if subject_id not in existing_subject_ids:
            existing_subject_ids.add(subject_id)
            break
    subject_name = fake.catch_phrase()
    school_id = random.randint(1, 6)
    credit = random.randint(2, 4)
    weight = random.choice([0.5, 0.6, 0.7])
    subject_description = fake.text()

    # Insert into subjects table
    cur.execute("""
        INSERT INTO subjects (subject_id, subject_name, school_id, credit, weight, subject_description)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (subject_id, subject_name, school_id, credit, weight, subject_description))

    # Generate program_id and insert into subjects_programs table
    sp_pair=set()
    random_num = random.randint(1, 10)
    for _ in range(random_num):
        while True:
            program_id = random.randint(50, 101)
        # Check if pair already exists
            if (subject_id, program_id) not in sp_pair:
                sp_pair.add((subject_id, program_id))
                break

        cur.execute("""
            INSERT INTO subjects_programs (subject_id, program_id)
            VALUES (%s, %s)
        """, (subject_id, program_id))

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()