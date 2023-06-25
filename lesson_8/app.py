from flask import Flask, request, jsonify
from creditcard import CreditCard
from code_db import save_to_database, get_from_database

app = Flask(__name__)


@app.route('/cards', methods=['POST'])
def create_card():
    data = request.get_json()
    card = CreditCard(**data)
    save_to_database(card)
    return jsonify({'message': 'Card created successfully'})


@app.route('/cards/<card_number>', methods=['GET'])
def get_card(card_number):
    card = get_from_database(card_number)
    if card:
        return jsonify(card.__dict__)
    else:
        return jsonify({'message': 'Card not found'})


if __name__ == '__main__':
    app.run()
