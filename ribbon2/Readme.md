
# Petruskan Ribbon2 SIS

Ribbon2 is a modern SIS built on postgreSQL.

# Ribbon2 Database

**📝Notice:** This guide assumes the supported distros of Rocky Linux (Rocky) or Oracle Linux (OL) 9.4 or higher. It should also work with RHEL 9.4 or higher, if subscriptions and repositories are properly set up. We reccomend Rocky or Oracle Linux 10.0 or higher for security.

**📝Notice:** This guide assumes the default DB name of ribbon2. You are welcome to add environment based prefixes like -prod or -pprd. Make sure to append this anywhere you'd list the database name.

## Prerequisites

To set up the Ribbon2 SIS, you will need to install PostgreSQL. For the latest version of PostgreSQL supported by the distro, run the following commands:

1. Remove the default PostgreSQL module
```bash
$: dnf module disable postgresql -y
$: dnf clean all
```

2. Install PostgreSQL 16 via [this web link](https://www.postgresql.org/download/linux/redhat/ "PGDG Install Instructions for Red Hat Family"), ensuring the correct OL/Rocky version is selected. 

## Setup

1. Connect to the postgreSQL termobal as the linux account postgres

```bash
postgres#: psql -d postgres
```

2. create the ribbon2 user as follows:

```sql
CREATE USER ribbon2 WITH PASSWORD 'your_secure_password_here';
ALTER USER ribbon2 CREATEDB;
ALTER USER ribbon2 WITH CREATEROLE;
```

3. create the database ribbon2 as follows:

```sql
CREATE DATABASE ribbon2 WITH OWNER "ribbon2";
GRANT CONNECT ON DATABASE ribbon2 TO "ribbon2";
```

5. Exit the postgreSQL terminal

```sql
\q
```

6. Modify the pg_hba.conf */var/lib/pgsql/16/data/pg_hba.conf* file to add the following line:

```conf
local   all     all                                     md5
```

8. cd to the install scripts in the git repository, and Run the following scripts, to built the Ribbon2 SIS database

```bash
postgres$: cd (/path/to/)ribbon2helmsman/ribbon2/install_scripts
postgres$: psql -U ribbon2 -d ribbon2 -f 1-general.sql
postgres$: psql -U ribbon2 -d ribbon2 -f 2-finance.sql
postgres$: psql -U ribbon2 -d ribbon2 -f 3-student.sql
postgres$: psql -U ribbon2 -d ribbon2 -f 4-ireland_inserts.sql
postgres$: psql -U ribbon2 -d ribbon2 -f 5-roles.sql
postgres$: psql -U ribbon2 -d ribbon2 -f 6-helmsman.sql
```

9. Connect to ribbon2 as user ribbon2

```bash
postgres$: psql -U ribbon2 -d ribbon2
```

10. Change the password for the petruskan user

```sql
\password petruskan
```

11. Exit the postgreSQL terminal

```sql
\q
```

12. Modify the pg_hba.conf */var/lib/pgsql/16/data/pg_hba.conf* file to add the following line, allowing connection from helmsman

```conf
host    ribbon2     all     <helmsman-server-ip>/32   md5
```

13. Make sure all created accounts are mapped properly to one of the following roles

* sis_admin
* sis_application
* sis_instructor
* sis_advisor
* sis_registrar
* sis_readonly