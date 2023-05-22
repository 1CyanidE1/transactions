import json
import uuid
import hashlib


def get_user_log(user_id: str):

    try:
        with open(f'{user_id}_log.json', 'r') as user_data:
            data = json.load(user_data)

    except FileNotFoundError:
        with open(f'{user_id}_log.json', 'w+') as user_data:
            data = {'balance': 0, 'transactions': []}
            json.dump(data, user_data)

    return data


def get_history_log(user_id: str):
    try:
        with open(f'{user_id}_history_log.json', 'r') as user_history:
            history = json.load(user_history)

    except FileNotFoundError:
        with open(f'{user_id}_history_log.json', 'w+') as user_history:
            history = {'balance': 0, 'transactions': []}
            json.dump(history, user_history)

    return history


def transaction_to_hold(transaction_id: str, transaction_list: list):

    try:
        with open('hold.json', 'r') as hold_file:
            hold = json.load(hold_file)

        with open('hold.json', 'w') as hold_file:
            hold[transaction_id] = transaction_list
            json.dump(hold, hold_file)

    except (json.JSONDecodeError, FileNotFoundError):
        with open('hold.json', 'w') as hold_file:
            hold = dict()
            hold[transaction_id] = transaction_list
            json.dump(hold, hold_file)

    return hold


def hash_check(file: str):
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def hash_compare(user_id: str):
    if hash_check(f'{user_id}_log.json') == hash_check(f'{user_id}_history_log.json'):
        return True
    else:
        return False


def dump_file(file_name: str, data):
    with open(file_name, 'w') as file:
        json.dump(data, file)


def hold_clear(transaction_id: str):
    with open('hold.json', 'r') as hold_file:
        hold = json.load(hold_file)

    with open('hold.json', 'w') as hold_file:
        del hold[transaction_id]
        json.dump(hold, hold_file)


def transaction(sender_id: str, transaction_sum: int, recipient_id: str):

    if transaction_sum <= 0:
        return

    sender_data = get_user_log(sender_id)
    recipient_data = get_user_log(recipient_id)
    sender_history = get_history_log(sender_id)
    recipient_history = get_history_log(recipient_id)

    transaction_id = str(uuid.uuid4())
    transactions_list = [sender_id, transaction_sum, recipient_id]
    transaction_to_hold(transaction_id, transactions_list)

    if sender_data['balance'] >= transaction_sum:
        if hash_compare(sender_id) and hash_compare(recipient_id):
            sender_data['transactions'].append(transactions_list)
            sender_data['balance'] -= transaction_sum
            recipient_data['transactions'].append(transactions_list)
            recipient_data['balance'] += transaction_sum

            dump_file(f'{sender_id}_log.json', sender_data)
            dump_file(f'{recipient_id}_log.json', recipient_data)
            dump_file(f'{sender_id}_history_log.json', sender_data)
            dump_file(f'{recipient_id}_history_log.json', recipient_data)

            hold_clear(transaction_id)

        else:
            return print('Не совпадают хэши')

    else:
        hold_clear(transaction_id)
        return


# Переводим из банка пользователю
# transaction('bank', сумма, 'Любое имя')
#
# Перевод с одного счет на другой
# transaction('первый пользователь', сумма, 'второй пользователь')


