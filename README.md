# qELI5 - PostgreSQL Query Plan Vocalizer
## npm Dependencies
```
nodemon
yarn (global, optional)
```
Run `yarn` or `npm install` to install packages.
## Python Dependencies
```
wxPython
psycopg2
dotenv
```
Make use of `pip` or `virtualenv` to install packages. 
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
Run `yarn dev` or `npm run dev`.

In this mode the main frame is auto-recreated (with changes) after being closed. Use `Ctrl+C` from within the running console to stop.
### Without nodemon
Run `yarn start` or `npm start`.

In this mode the start script, which simply acts as a wrapper for `python main.py`, is called.