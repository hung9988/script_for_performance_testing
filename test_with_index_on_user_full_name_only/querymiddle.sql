CREATE INDEX IF NOT EXISTS idx_fullname
    ON public.users USING btree
    (((first_name::text || ' '::text) || last_name::text) COLLATE pg_catalog."default" text_pattern_ops ASC NULLS LAST)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;
