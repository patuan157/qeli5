# qELI5 - PostgreSQL Query Plan Vocalizer
## Major Dependencies
```
wxPython
psycopg2
dotenv
```
## Setting up .env
Rename `.env.example` to `.env` and modify accordingly.
```
DB_NAME=<db_name>
DB_HOST=<db_host>
DB_USER=<db_user>
DB_PWD=<db_password>
```
## Run
### With nodemon
```
npm run dev
```
Frame is auto-restarted (with changes) after being closed.

Use `Ctrl+C` to from within the running console stop.
### Without nodemon
```
npm start
```
Start script simply acts as a wrapper for `python main.py`.