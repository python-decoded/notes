BEGIN;

CREATE TABLE IF NOT EXISTS public."Users"
    (
        id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
        username text COLLATE pg_catalog."default" NOT NULL,
        email text COLLATE pg_catalog."default" NOT NULL,
        created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT "Users_pkey" PRIMARY KEY (id)
    );



INSERT INTO public."Users" (username, email) VALUES ('newuser', 'newuser@example.com');
INSERT INTO public."Users" (username, email) VALUES ('other', 'other@example.com');
INSERT INTO public."Users" (username, email) VALUES ('some', 'some@example.com');

COMMIT;
