import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from os import environ


load_dotenv()

SQLALCHEMY_TEST_DATABASE_URL = "postgresql://%s:%s@%s:%d/%s" \
                               % (environ.get('TEST_DB_LOGIN'),
                                  environ.get('TEST_DB_PASS'),
                                  environ.get('TEST_DB_HOST'),
                                  int(environ.get('TEST_DB_PORT')),
                                  environ.get('TEST_DB_NAME'))

engine_test = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base = declarative_base()


def get_test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

