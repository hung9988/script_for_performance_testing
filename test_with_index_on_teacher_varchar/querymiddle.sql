CREATE INDEX IF NOT EXISTS teachers_teacher_id_idx
    ON public.teachers USING btree
    ((teacher_id::character varying) text_pattern_ops ASC NULLS LAST)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;
