## Data Layer

The database is built using PostgreSQL. This can be deployed locally or as a cloud service.

#### 1) Create Database and insert reference data

1.1. Create database 'virtual_clinic'

1.2. Connect to the database 'virtual_clinic'. For example, in psql run:
```
\c virtual_clinic
```

1.3. This script contains the create tables, constraints and the role vc_user. The script can be executed in pgAdmin or psql command line

**_Note:_** Before executing this script please read the instructions in the header of this file if you have changed from the default database and/or user name
```
/virtual-clinic/database_scripts/create_tables_1.1.sql
```
1.4. This script contains the insert statements to load the reference data into the reference tables. The script can be run using pgAdmin or using the psql command line
```
/virtual-clinic/database_scripts/insert_reference_data_1.1.sql
```

#### 2) .ini File

The .ini file contains a number of parameters for the database connection that are used by the Python data access object classes. The values in the .ini file have been defaulted to those used in the scripts. If you have used any different values they need to be changed here. The .ini file is located:
```
/virtual-clinic/virtual_clinic/api/app/dao/database.ini
```

This file has a number of sections:
```
[postgresql]

host = 127.0.0.1 (name of the host database server)

database = virtual_clinic (name of the database)

user = vc_user (name of the database user/role that is used to connect to the database)

password = password123 (password of the database user/role)
```
The following section relates to the database connection pooling
```
[pool]

min = the minimum number of connections in the pool e.g. 2

max = the maximum number of connections in the pool e.g. 4
```
