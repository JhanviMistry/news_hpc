from .connection import engine


def test_connection():
    with engine.connect() as connection:
        print("Successfully connected to PostgreSQL!")


if __name__ == "__main__":
    test_connection()