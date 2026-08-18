from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from collections.abc import Generator


def connect_db():
   try:
     DATABASE_URL = "postgresql+psycopg2://postgres:Pyromanial1234##@localhost:5432/fastapiai"
     engine = create_engine(DATABASE_URL)

     print("Database connected successfully!")
     

     return engine

   except Exception as e:

      print(f"Database connection failed: {e}")


engine = connect_db()

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
