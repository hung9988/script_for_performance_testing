import psycopg2
import random

# Connect to your postgres DB
conn = psycopg2.connect("dbname=student_manager user=postgres password=0000 host=localhost")
cur = conn.cursor()

# Fetch all subject_ids from subjects table
cur.execute("SELECT subject_id FROM subjects")
subject_ids = [row[0] for row in cur.fetchall()]

# Keep track of main_subject_ids and their counts
main_subject_counts = {}

# Number of distinct main_subject_ids to create
num_main_subjects = 100

# Keep track of existing pairs to avoid duplicates and opposites
existing_pairs = set()

while len(main_subject_counts) < num_main_subjects:
    # Select random main_subject_id and required_subject_id
    main_subject_id = random.choice(subject_ids)
    required_subject_id = random.choice(subject_ids)

    # Skip if pair or opposite pair already exists
    if ((main_subject_id, required_subject_id) in existing_pairs or
        (required_subject_id, main_subject_id) in existing_pairs):
        continue

    # Skip if main_subject_id has already occurred 2 times
    if main_subject_counts.get(main_subject_id, 0) >= 2:
        continue

    # Insert into subjects_conditions table
    cur.execute("""
        INSERT INTO subjects_conditions (main_subject_id, required_subject_id)
        VALUES (%s, %s)
    """, (main_subject_id, required_subject_id))

    # Update counts and existing pairs
    main_subject_counts[main_subject_id] = main_subject_counts.get(main_subject_id, 0) + 1
    existing_pairs.add((main_subject_id, required_subject_id))

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()