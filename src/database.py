import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from os import environ
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s:%d/%s" \
                          % (environ.get('DB_LOGIN'),
                             environ.get('DB_PASS'),
                             environ.get('DB_HOST'),
                             int(environ.get('DB_PORT')),
                             environ.get('DB_NAME'))

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
