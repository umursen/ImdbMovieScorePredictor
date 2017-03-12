# sudo -u postgres psql -e -c "DROP DATABASE IMDb;"
sudo -u postgres psql -e -c "CREATE DATABASE IMDb ENCODING 'UTF-8';"
sudo -u postgres psql -e -c "GRANT ALL PRIVILEGES ON DATABASE IMDb TO postgresqluser;"
