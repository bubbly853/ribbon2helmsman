
# Petruskan Ribbon2 SIS

Ribbon2 is a modern SIS built on postgreSQL.

# Ribbon2 Database

## Prerequisites

To set up the Ribbon2 SIS database, you will need to install PostgreSQL. We reccomend Oracle Linux or Rocky Linux. The latest version of PostgreSQL can be found [here](https://www.postgresql.org/download/linux/redhat/ "RHEL/Yum PostgreSQL official repos"), as well as instructions to install the distro provided version, and instructions to set up PostgreSQL after installation.

If you wish to install on another linux ditsro, PostgreSQL has instructions [here](https://www.postgresql.org/download/linux/ "Linux download instructions for PostgreSQL").

PostgreSQL provides instructions for and supports Windows, but we do not support installing Ribbon2 SIS on Windows. 

## Setup

1. Connect to the postgreSQL terminal as the local DBA, as the linux account postgres

```bash
postgres$: psql -d postgres
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

6. Modify the pg_hba.conf file

* if using postgreSQL repo

```bash
#: vi (or nano) /var/lib/pgsql/<version_number>/data/pg_hba.conf
```

* if using shipped postgreSQL

```bash
#: vi (or nano) /var/lib/pgsql/data/pg_hba.conf
```

7. Add the following line, then save and exit:

```conf
local   all     all                                     md5
```

8. cd to the install scripts in the git repository, and Run the following scripts, to built the Ribbon2 SIS database

```bash
$: cd (/path/to/)ribbon2helmsman/ribbon2/install_scripts
$: psql -U ribbon2 -d ribbon2 -f 1-general.sql
$: psql -U ribbon2 -d ribbon2 -f 2-finance.sql
$: psql -U ribbon2 -d ribbon2 -f 3-student.sql
$: psql -U ribbon2 -d ribbon2 -f 4-ireland_inserts.sql
$: psql -U ribbon2 -d ribbon2 -f 5-roles.sql
```

9. Connect to ribbon2 as user ribbon2

```bash
$: psql -U ribbon2 -d ribbon2
```

10. Change the password for the petruskan user

```sql
\password username
```

11. Exit the postgreSQL terminal

```sql
\q
```