import psycopg2
import os
from lesson_8.creditcard import CreditCard


DATABASE = {
    'host': "127.0.0.1",
    'port': '5432',
    'dbname': "test_database",
    'user': "Guest_user",
    'password': os.environ.get("DB_PASSWORD", "1488")
}


def create_table():
    with psycopg2.connect(**DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS cards (card_number TEXT, expiration_date DATE, "
                "cvv TEXT, issue_date DATE, owner_id TEXT, status TEXT)"
            )
            conn.commit()


def save_to_database(card):
    with psycopg2.connect(**DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO cards VALUES (%s, %s, %s, %s, %s, %s)",
                           (card.card_number, card.expiration_date, card.cvv,
                            card.issue_date.strftime("%Y-%m-%d"), str(card.owner_id), card.status))
            conn.commit()


def get_from_database(card_number):
    with psycopg2.connect(**DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM cards WHERE card_number=%s", (card_number,))
            result = cursor.fetchone()

            if result:
                card = CreditCard(*result)
                return card
            else:
                return None


if __name__ == '__main__':
    create_table()
