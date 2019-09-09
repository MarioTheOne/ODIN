import json


class BitcoinJsonReader(object):
    """description of class"""

    def __init__(self):
        self._block = None
        self._json_block_file = None

    def get_json_block(self):
        return self._block

    def read_block_file(self, block_json_file_path):
        self._json_block_file = open(block_json_file_path)
        self._block = json.load(self._json_block_file)

    def get_json_transaction_list(self):
        return self._block['data']

    def is_confirmed_transaction(self, json_transaction):
        return json_transaction['confirmations'] > 0

    def is_coinbase_transaction(self, json_transaction):
        return json_transaction['is_coinbase']

    def close_block_file(self):
        self._json_block_file.close()