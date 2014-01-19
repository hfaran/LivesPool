# Create a DB called **cutthroat**
    CREATE DATABASE IF NOT EXISTS cutthroat;

# Create and populate DB tables
    USE cutthroat;
    # Add more stuff here . . .

# Create a user called **cutthroat-dev** with password 'pooltable' and grant full permissions
    GRANT ALL ON cutthroat to 'cutthroat-dev'@'localhost' IDENTIFIED BY 'pooltable';
    GRANT ALL PRIVILEGES ON *.* TO 'cutthroat-dev'@'localhost' WITH GRANT OPTION;
