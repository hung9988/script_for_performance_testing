import psycopg2
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

# Fetch all class_id and subject_id values from the classes table
cur.execute("SELECT class_id, subject_id FROM classes")
classes = cur.fetchall()

# Fetch all student_id and program_id values from the students table
cur.execute("SELECT student_id, program_id FROM students")
students = cur.fetchall()

# Fetch all subject_id and program_id values from the subjects_programs table
cur.execute("SELECT subject_id, program_id FROM subjects_programs")
subjects_programs = cur.fetchall()

inserted_pairs = set()
values = []
cur.execute("SELECT main_subject_id, required_subject_id FROM subjects_conditions")
subjects_conditions = cur.fetchall()

# Create a dictionary where the keys are main_subject_id values and the values are lists of required_subject_id values
required_subjects = {}
for main_subject_id, required_subject_id in subjects_conditions:
    if main_subject_id not in required_subjects:
        required_subjects[main_subject_id] = []
    required_subjects[main_subject_id].append(required_subject_id)

def has_passed_required_subjects(student_id, required_subject_ids):
    if not required_subject_ids:  # If the list is empty, return True
        return True
    # Add single quotes around each subject_id
    subject_ids = ', '.join(f"'{id}'" for id in required_subject_ids)
    cur.execute(f"""
        SELECT COUNT(*) 
        FROM enrollments 
        INNER JOIN classes ON enrollments.class_id = classes.class_id
        WHERE student_id = {student_id} AND classes.subject_id IN ({subject_ids}) AND passed = TRUE
    """)
    return cur.fetchone()[0] == len(required_subject_ids)
for _ in range(1000):
    while True:
        class_id, subject_id = fake.random_element(elements=classes)
        student_id, program_id = fake.random_element(elements=students)
        if (subject_id, program_id) in subjects_programs and (class_id, student_id) not in inserted_pairs and has_passed_required_subjects(student_id, required_subjects.get(subject_id, [])):
            break
    values.append(f"({class_id}, {student_id})")
    inserted_pairs.add((class_id, student_id))

# Generate a single INSERT statement
query_string = f"INSERT INTO enrollments (class_id, student_id) VALUES {', '.join(values)};"

# Write the query string to a file
with open('outputenrollment.sql', 'w') as f:
    f.write(query_string)