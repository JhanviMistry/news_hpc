'''from .connection import engine


def test_connection():
    with engine.connect() as connection:
        print("Successfully connected to PostgreSQL!")


if __name__ == "__main__":
    test_connection()
'''

from .connection import engine
from .models import Base


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()