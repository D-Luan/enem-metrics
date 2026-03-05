import os
from dotenv import load_dotenv

load_dotenv()

def get_db_config():
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_NAME")
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "5432")

    if not all([user, password, db_name]):
        raise ValueError("Erro ao chamar as variáveis DB_USER, DB_PASSWORD e DB_NAME.")
    
    return {
        "user": user,
        "password": password,
        "db_name": db_name,
        "host": host,
        "port": port
    }

def get_postgres_uri():
    conf = get_db_config()
    return f"postgresql://{conf["user"]}:{conf["password"]}@{conf["host"]}:{conf["port"]}/{conf["db_name"]}" 