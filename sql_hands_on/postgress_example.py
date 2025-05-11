import psycopg2


with psycopg2.connect(database="postgres",
                      host="127.0.0.1",
                      user="postgres",
                      password="admin",
                      port="5432") as connection:

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS public."Users"
    (
        id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
        username text COLLATE pg_catalog."default" NOT NULL,
        email text COLLATE pg_catalog."default" NOT NULL,
        created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT "Users_pkey" PRIMARY KEY (id)
    );
    """)

    cursor.execute("""
    INSERT INTO public."Users" (username, email) VALUES ('newuser', 'newuser@example.com');
    INSERT INTO public."Users" (username, email) VALUES ('other', 'other@example.com');
    INSERT INTO public."Users" (username, email) VALUES ('some', 'some@example.com');
    """)

    connection.commit()  # If there is no open transaction, this method is a no-op.

    cursor.execute(""" SELECT * FROM public."Users" """)
    rows = cursor.fetchall()
    print(*rows, sep="\n")

    cursor.execute(""" SELECT * FROM public."Users" WHERE username = %s """, ("other", ))
    row = cursor.fetchone()
    print("\n", row)
