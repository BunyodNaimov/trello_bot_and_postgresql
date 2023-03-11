from psycopg2.extras import RealDictCursor
from trello import TrelloManager
from db.conf import connection


def check_chat_id_from_database(chat_id):
    with connection.cursor() as cur:
        cur.execute(f"select chat_id from users where chat_id::TEXT like '{chat_id}%'")
        chat_id_in_database = cur.fetchall()
        return chat_id_in_database


def write_trello_to_database(username, bot_chat_id, full_name):
    members = TrelloManager(username).get_member()
    trello_boards = TrelloManager(username).get_boards()

    with connection.cursor() as cur:
        cur.execute(
            f"insert into members(fullname, trello_username, member_trello_id)"
            f" values('{members.get('fullName')}', '{username}', '{members.get('id')}')"
            f"on conflict(member_trello_id) do update set fullname=excluded.fullname,"
            f"trello_username=excluded.trello_username, member_trello_id=excluded.member_trello_id")

        cur.execute(f"select id from members where member_trello_id='{members.get('id')}'")
        member_id = cur.fetchall()[0][0]

        cur.execute(f"insert into users(chat_id, fullname, username, member_id)"
                    f"values('{bot_chat_id}', '{full_name}', '{username}', '{member_id}')"
                    f"on conflict(chat_id) do update set chat_id=excluded.chat_id, fullname=excluded.fullname,"
                    f"username=excluded.username, member_id=excluded.member_id")

        for i in range(len(trello_boards)):
            cur.execute(f"insert into boards(name, board_trello_id)"
                        f"values('{trello_boards[i].get('name')}', '{trello_boards[i].get('id')}')"
                        f"on conflict(board_trello_id) do update set name=excluded.name,"
                        f" board_trello_id=excluded.board_trello_id")

            lists = TrelloManager(username).get_lists_on_a_board(trello_boards[i].get('id'))
            labels = TrelloManager(username).get_labels_board(trello_boards[i].get('id'))

            for j in range(len(lists)):
                cur.execute(f"select id from boards where board_trello_id='{trello_boards[i].get('id')}'")
                board_id = cur.fetchall()[0][0]
                cur.execute(f"insert into lists(name, list_trello_id, board_id)"
                            f"values('{lists[j].get('name')}', '{lists[j].get('id')}', '{board_id}')"
                            f"on conflict(list_trello_id) do update set name=excluded.name,"
                            f"list_trello_id=excluded.list_trello_id, board_id=excluded.board_id")

                cur.execute(f"select id from lists where list_trello_id='{lists[j].get('id')}'")
                list_id = cur.fetchall()[0][0]

                cards = TrelloManager(username).get_cards_on_a_list(lists[j].get('id'))

                for k in range(len(cards)):
                    cur.execute(f"insert into cards(name, card_trello_id, url, description, lists_id)"
                                f"values('{cards[k].get('name')}', '{cards[k].get('id')}', '{cards[k].get('url')}',"
                                f"'{cards[k].get('desc')}','{list_id}')"
                                f"on conflict(card_trello_id) do update set name=excluded.name,"
                                f"card_trello_id=excluded.card_trello_id, description=excluded.description,"
                                f"lists_id=excluded.lists_id")

                    cur.execute(f"select id from cards where card_trello_id='{cards[k].get('id')}'")
                    card_id = cur.fetchall()[0][0]

                    cur.execute(f"insert into cards_members(card_id, member_id) values ('{card_id}','{member_id}')"
                                f"on conflict(card_id, member_id) do update set card_id=excluded.card_id,"
                                f"member_id=excluded.member_id")

            for n in range(len(labels)):
                if labels[n].get('name'):
                    cur.execute(
                        f"insert into labels(name,label_trello_id,board_id)"
                        f"values ('{labels[n].get('name')}', '{labels[n].get('id')}', '{board_id}')"
                        f"on conflict(label_trello_id) do update set name=excluded.name,"
                        f"label_trello_id=excluded.label_trello_id, board_id=excluded.board_id")

                    cur.execute(f"select id from labels where label_trello_id='{labels[n].get('id')}'")
                    label_id = cur.fetchall()[0][0]

                    cur.execute(
                        f"insert into cards_labels(card_id, labels_id) values ('{card_id}', '{label_id}')"
                        f"on conflict(card_id, labels_id) do update set card_id=excluded.card_id,"
                        f"labels_id=excluded.labels_id")

    with connection.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("select id from boards")
        board_id = cur.fetchall()

        for i in range(len(board_id)):
            cur.execute(f"insert into board_members(board_id, member_id)"
                        f"values('{board_id[i].get('id')}', '{member_id}')"
                        f"on conflict(board_id) do update set board_id=excluded.board_id,"
                        f"member_id=excluded.member_id")

        connection.commit()


def get_boards():
    with connection.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("select name, id from boards")
        return cur.fetchall()


def get_lists(board_id):
    with connection.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(f"select name, id from lists where board_id={board_id}")
        return cur.fetchall()


def get_cards(list_id):
    with connection.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(f"select name, id, url from cards where lists_id={list_id}")
        return cur.fetchall()


def check_size(board_id):
    check = get_lists(board_id)
    return len(check)


def update_database(bot_chat_id, full_name):
    with connection.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(f"select username from users where chat_id={bot_chat_id}")
        username = cur.fetchall()[0].get("username")

    write_trello_to_database(username, bot_chat_id, full_name)
    return "Updated"

