
# Ribbon2 Helmsman Frontend

A django Frontend for the Ribbon2 SIS


## Prerequisites

**📝Notice:** This guide assumes the supported distros of Rocky Linux (Rocky) or Oracle Linux (OL) 10.0 or higher. It should also work with RHEL 10.0 or higher. Lower versions are not supported due to issues with Python3 version.

#### Ribbon2 database

In the helmsman source code tree, there is a folder named ribbon2. On a separate server, please follow the install instructions provided there.

#### Django DB

To set up Django Admin for Ribbon2 Helmsman, you will need to install PostgreSQL. For the latest version of PostgreSQL supported by the distro, run the following commands:

1. Remove the default PostgreSQL module, as root or sudo:
    
    ```bash
    dnf module disable postgresql -y
    dnf clean all
    ```

2. Install PostgreSQL ***16*** via [this web link](https://www.postgresql.org/download/linux/redhat/ "PGDG Install Instructions for Red Hat Family"), ensuring the correct OL/Rocky version is selected. 

#### Nginx

We reccomend using the nginx version shipped with Rocky/OL.
To install nginx on Oracle Linux or Rocky Linux, run the following commands.

1. Install nginx, as root or sudo:
    
    ```bash
    dnf update -y
    dnf install -y nginx
    ```

2. open SSL port, as root or sudo:
   
    ```bash 
    firewall-cmd --permanent --add-service=https
    firewall-cmd --reload
    ```

#### install remaining requirements

Ensure python, gcc, gunicorn, and git are installed and up to date, as root or sudo:

```bash
dnf install -y python3 python3-pip python3-devel gcc git
```

#### Create the helmsman db user

1. Switch to the postgres user and connect to the postgres database, as root or sudo:

    ```bash
    su - postgres
    psql -d postrgres
    ```

2. create the helmsman user and database, and exit

    ```sql
    CREATE USER hemlsman WITH PASSWORD 'secure_password_here';
    CREATE DATABASE hemlsman_db OWNER hemlsman;
    GRANT ALL PRIVILEGES ON DATABASE hemlsman_db TO hemlsman;
    \q
    ```

#### Setup configuration fire

Add these lines to the file */var/lib/pgsql/16/data/pg_hba.conf*

```conf
host    hemlsman_db    helmsman    127.0.0.1/32    md5
host    hemlsman_db    helmsman    ::1/128         md5
```    
this allows a host type connection to the database helmsman_db from the helmsman user over 1pv4 and 1pv6 local host.

**📝Notice:** Ensure this HBA file is setup properly. This will cause issues with migration if incorrect.


## Installation

**📝Notice:** This guide assumes the supported distros of Rocky Linux (Rocky) or Oracle Linux (OL) 9.4 or higher

1. Create the Helmsman user and home directory, as root or sudo:

    ```bash
    mkdir -p /opt/helmsman
    useradd --no-create-home --home-dir /opt/helmsman helmsman
    chown helmsman:helmsman /opt/helmsman
    
    ```

2. Login as helmsman, and create the app directory, as root or sudo:

    ```bash
    su - helmsman
    cd ~
    mkdir app && cd app
    ```

3. Continuing, ull the git repository

   **📝Notice:** Steps 2-10 assume you stay in the same terminal window. If you leave the terminal window at all in these steps, ensure you are in the correct directory. For for 3-8, that is /opt/helmsman/app, for 9 and 10, that is /opt/helmsman/app/helmsman

    ```bash
    git clone https://github.com/bubbly853/ribbon2helmsman.git .
    ```

4. Generate a secret key and record it somewhere:

    ```bash
    python3 -c "import secrets; print(secrets.token_urlsafe(50))"
    ```

5. Create the .env file

    ```bash
    touch .env
    ```

6. Ensure the .env file is set up according as below

    ```python
    DJANGO_DB_PASSWORD="<Password created for User: helmsman>"
    DJANGO_DB_HOST=<127.0.0.1 or ::1>
    DJANGO_DB_PORT=5432
    
    SIS_DB_NAME=<ribbon2 database name>
    SIS_DB_HOST=<ip address of ribbon2 database server>
    SIS_DB_PORT=5432
    
    ALLOWED_HOSTS=<comma separated list of hostnames used to access helmsman>
    CSRF_TRUSTED_ORIGINS=<comma separated list of hostnames used to access helmsman>
    SECRET_KEY="<Key generated in step 4>"
    ```
    
    * Django DB Settings
        * DJANGO_DB_PASSWORD: Ensure this is the password created when setting up the helmsman user on the django database
        * DJANGO_DB_HOST: Choose 127.0.0.1 for IPV4 or ::1 for IPV6
        * DJANGO_DB_PORT: Unless you have changed the default PostgreSQL port on the django database, leave this as 5432.
    * SIS DB Settings
        * SIS_DB_NAME: The default is ribbon2, but environment postfixes like ribbon2-prod can be used. Make sure to name the database accordingly when setting up the Ribbon2 database.
        * SIS_DB_HOST: The IP address of the Ribbon2 SIS database
        * DJANGO_DB_PORT: Unless you have changed the default PostgreSQL port on the Ribbon2 SIS database, leave this as 5432.
    * Django Server Settings
        * ALLOWED_HOSTS: A comma separated list of every hostname/IP that will be used to HOST this server. This includes the server's own IP, and/or the FQDN used to access the server, I.e. helmsman.college.edu. Ensure that there are no whitespaces before or after the commas.
        * CSRF_TRUSTED_ORIGINS: This should match ALLOWED_HOSTS
        * SECRET_KEY: This is the secret key generated in step 4

7. Create the venv and activate it:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

8. Install base requirements

    ```bash
    pip install -r requirements.txt
    ```

9. CD into the helmsman directory, and check the env file and database accessibility

    ```bash
    cd helmsman
    python manage.py check
    ```

10. If not presented with errors, migrate the django db helmsman_db and move static files

    ```bash
    python manage.py migrate --database=default
    python manage.py collectstatic --noinput
    ```
    **📝Notice:** If this step fails, there are multiple possible reasons. The traceback will be long, but look for the postgres error code. Here are a few common errors:
    * FATAL:  password authentication failed for user "helmsman":
        * Ensure the password set up for the 'helmsman' user matches the password in the .env file.
    * no pg_hba.conf entry for host "local", user "helmsman", database "helmsman_db":
        * Ensure the pg_hba.conf step was followed correctly.
    *  FATAL:  database "helmsman_db" does not exist:
        * The database "helmsman_db" was not set up. Ensure that the database is set up properly.

12. as root, create the gunicorn file */etc/systemd/system/helmsman.service* as shows

    ```service
    [Unit]
    Description=Helmsman Django App
    After=network.target
    
    [Service]
    User=www-data
    Group=www-data
    WorkingDirectory=/opt/helmsman/app/helmsman
    ExecStart=/opt/helmsman/app/.venv/bin/gunicorn \
        --workers 3 \
        --bind unix:/run/helmsman.sock \
        helmsman.wsgi:application
    ExecReload=/bin/kill -s HUP $MAINPID
    Restart=always
    
    [Install]
    WantedBy=multi-user.target
    ```
 
13. reload systemd and start the service, as root or sudo:

    ```bash
    systemctl daemon-reload
    systemctl enable helmsman
    systemctl start helmsman
    systemctl status helmsman
    ```

14. Create and edit the nginx helmsman config file */etc/nginx/conf.d/helmsman.conf as shown

    ```conf
    server {
        listen 80;
        server_name _;
        return 301 https://$host$request_uri;
    }
    
    server {
        listen 443 ssl;
        server_name yourhostname.university.edu;
    
        ssl_certificate     /etc/pki/tls/certs/helmsman.crt;
        ssl_certificate_key /etc/pki/tls/private/helmsman.key;
    
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
    
        location /static/ {
            alias /opt/helmsman/app/static/;
        }
    
        location /media/ {
            alias /opt/helmsman/app/media/;
        }
    
        location / {
            proxy_pass http://unix:/run/helmsman.sock;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```

    Make sure your certificates are up to date, and they are in the /etc/pki/tls/certs directory.

15. Ensure proper functionality of the system. If you cannot reach the SIS DB, ensure the pg_hba.conf on the SIS server allows access from the Helmsman server IP address, and firewalls allow them to communicate on the DB port. Firewall can be set up via the following, as root or sudo:

    ```bash
    firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="<django-server-ip>" port port="5432" protocol="tcp" accept'
    firewall-cmd --reload
    ```
