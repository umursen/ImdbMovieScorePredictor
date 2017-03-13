psql -e -c "DROP DATABASE imdb;"
psql -e -c "CREATE DATABASE imdb ENCODING 'UTF-8';"
psql -e -c "GRANT ALL PRIVILEGES ON DATABASE imdb TO umur;"
