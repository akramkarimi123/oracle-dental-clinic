CREATE USER c##ahmad
IDENTIFIED BY 123
DEFAULT TABLESPACE users
TEMPORARY TABLESPACE temp
QUOTA UNLIMITED ON users;

GRANT CONNECT, RESOURCE TO c##ahmad;

CREATE USER c##karimi
IDENTIFIED BY 123
DEFAULT TABLESPACE users
TEMPORARY TABLESPACE temp
QUOTA UNLIMITED ON users;

GRANT CONNECT, RESOURCE TO c##karimi;



-- making the role by name the admin and the staff 
CREATE ROLE c##admin;
CREATE ROLE c##staff;

-- adding grent to each staff and the admin
-- staff
GRANT SELECT, INSERT, UPDATE, DELETE ON patients TO c##staff;
GRANT SELECT, INSERT, UPDATE, DELETE ON appointments TO c##staff;
GRANT SELECT ON treatments TO c##staff;

-- admin
GRANT ALL PRIVILEGES ON patients TO c##admin;
GRANT ALL PRIVILEGES ON appointments TO c##admin;
GRANT ALL PRIVILEGES ON billing TO c##admin;

-- assign to each user 
GRANT c##staff TO c##ahmad;
GRANT c##admin TO c##karimi;
