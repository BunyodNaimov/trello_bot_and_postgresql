import requests
import json

from environs import Env

env = Env()
env.read_env()


class TrelloManager:
    KEY = env("TRELLO_KEY")
    TOKEN = env("TRELLO_TOKEN")

    def __init__(self, username):
        self.username = username

    @staticmethod
    def base_headers():
        return {
            "Accept": "application/json"
        }

    def credentials(self):
        return {
            "key": self.KEY,
            "token": self.TOKEN
        }

    def get_member(self):
        url = f"https://api.trello.com/1/members/{self.username}"

        response = requests.request(
            "GET",
            url,
            headers=self.base_headers(),
            params=self.credentials()
        )
        if response.status_code == 200:
            return json.loads(response.text)

    def get_boards(self):
        url = f"https://api.trello.com/1/members/{self.username}/boards"

        response = requests.request(
            "GET",
            url,
            headers=self.base_headers(),
            params=self.credentials()
        )
        if response.status_code == 200:
            return json.loads(response.text)

    def get_lists_on_a_board(self, board_id):
        url = f"https://api.trello.com/1/boards/{board_id}/lists"

        response = requests.request(
            "GET",
            url,
            headers=self.base_headers(),
            params=self.credentials()
        )
        if response.status_code == 200:
            return json.loads(response.text)

    def get_cards_on_a_list(self, list_id):
        url = f"https://api.trello.com/1/lists/{list_id}/cards"

        response = requests.request(
            "GET",
            url,
            headers=self.base_headers(),
            params=self.credentials()
        )
        if response.status_code == 200:
            # for i in json.loads(response.text):
            #     print(i)
            return json.loads(response.text)

    def get_board_members(self, board_id):

        url = f"https://api.trello.com/1/boards/{board_id}/memberships"

        response = requests.request(
            "GET",
            url,
            headers=self.base_headers(),
            params=self.credentials()
        )

        if response.status_code == 200:
            return json.loads(response.text)

    def get_labels_board(self, board_id):
        url = f"https://api.trello.com/1/boards/{board_id}/labels"

        response = requests.request(
            "GET",
            url,
            params=self.credentials()
        )

        if response.status_code == 200:
            return json.loads(response.text)
