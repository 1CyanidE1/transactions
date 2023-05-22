import json
import uuid
import hashlib


def hash_check(file: str):
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class Account:

    def __init__(self, id: str):

        self.id = id

    class Transaction:

        def __init__(self):

            self.id = str(uuid.uuid4())
            self.log = None
            self._history = None

        def get_user_log(self, user_id: str):

            try:
                with open(f'{user_id}_log.json', 'r') as user_data:
                    self.log = json.load(user_data)

            except FileNotFoundError:
                with open(f'{user_id}_log.json', 'w+') as user_data:
                    self.log = {'balance': 0, 'transactions': []}
                    json.dump(self.log, user_data)

            return self.log

        def get_history_log(self, user_id):

            try:
                with open(f'{self.id}_history_log.json', 'r') as user_history:
                    self._history = json.load(user_history)

            except FileNotFoundError:
                with open(f'{self.id}_history_log.json', 'w+') as user_history:
                    self._history = {'balance': 0, 'transactions': []}
                    json.dump(self._history, user_history)

            return self._history

        def _transaction_to_hold(self, transaction_list: list):

            try:
                with open('hold.json', 'r') as hold_file:
                    hold = json.load(hold_file)

                with open('hold.json', 'w') as hold_file:
                    hold[self.id] = transaction_list
                    json.dump(hold, hold_file)

            except (json.JSONDecodeError, FileNotFoundError):
                with open('hold.json', 'w') as hold_file:
                    hold = dict()
                    hold[self.id] = transaction_list
                    json.dump(hold, hold_file)

            return hold

        def _hash_compare(self):
            if hash_check(f'{self.id') == hash_check(f'{user_id}_history_log.json'):
                return True
            else:
                return False


