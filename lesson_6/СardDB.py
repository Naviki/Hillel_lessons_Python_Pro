import sqlite3

DATABASE = 'cards.db'


def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS cards (card_number TEXT, expiration_date TEXT, "
        "cvv TEXT, issue_date TEXT, owner_id TEXT, status TEXT)"
    )
    conn.commit()
    conn.close()


def save_to_database(card):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cards VALUES (?, ?, ?, ?, ?, ?)",
                   (card.card_number, card.expiration_date, card.cvv,
                    card.issue_date, str(card.owner_id), card.status))
    conn.commit()
    conn.close()


def get_from_database(card_number):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cards WHERE card_number=?", (card_number,))
    result = cursor.fetchone()
    conn.close()

    if result:
        from Card import CreditCard
        card = CreditCard(*result)
        return card
    else:
        return None
