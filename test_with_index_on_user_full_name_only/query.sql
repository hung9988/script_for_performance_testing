 select * from subjects where
school_id = (select school_id from teachers where teacher_id=current_setting('myapp.user_id')::integer LIMIT 1) 
and (subject_id LIKE 'AC%' OR subject_name LIKE 'AC%')
OFFSET 0 LIMIT 10;

