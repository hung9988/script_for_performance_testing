(
  SELECT 
    users.*, 
    school_id, 
    hired_year, 
    qualification 
  FROM 
    teachers 
    JOIN users ON user_id = teacher_id 
  WHERE 
    teacher_id::varchar LIKE '2022%' 
  OFFSET 0 LIMIT 10
) 
UNION 
(
  SELECT 
    users.*, 
    school_id, 
    hired_year, 
    qualification 
  FROM 
    teachers 
    JOIN users ON user_id = teacher_id 
  WHERE 
    (first_name ||' '||last_name) LIKE '2022%' 
  OFFSET 0 LIMIT 10
);