select
  *
from
  classes
where
  subject_id in(
    select
      subject_id
    from
      subjects_programs
    where
      program_id = (
        select program_id from students WHERE
        student_id =current_setting('myapp.user_id')::integer LIMIT 1
      )
  )
  AND semester = '20232'
  AND (class_id::varchar ILIKE '%2022%' OR subject_id ILIKE '%2022%')
  OFFSET 0 LIMIT 10;