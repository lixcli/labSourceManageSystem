# _*_ coding: utf-8 _*_

user = 'sa'
pwd = 'admin'
server = 'localhost'
dbname = 'DB_laboratory'
driver = "ODBC Driver 17 for SQL Server"
# ####
DEBUG = True
FLASK_APP='run.py'
SECRET_KEY = 'hard to guess string'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{user}:{pwd}@{server}/{dbname}?driver={driver}"
