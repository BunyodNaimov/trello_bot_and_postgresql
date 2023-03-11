from psycopg2.extras import RealDictCursor
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton)

from db import connection, queries


def get_inline_boards_btn(user_id, action):
    inline_boards_btn = InlineKeyboardMarkup()
    with connection.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(queries.GET_USER_BOARDS, (user_id,))
        boards = cur.fetchall()
    if len(boards) % 2 == 0:
        last_board = None
    else:
        last_board = boards.pop()
    for i in range(0, len(boards) - 1, 2):
        inline_boards_btn.add(
            InlineKeyboardButton(
                boards[i].get("name"), callback_data=f"{action}_{boards[i].get('board_id')}"
            ),
            InlineKeyboardButton(
                boards[i + 1].get("name"), callback_data=f"{action}_{boards[i + 1].get('board_id')}"
            ),
        )
    if last_board:
        inline_boards_btn.add(
            InlineKeyboardButton(last_board.get("name"), callback_data=f"{action}_{last_board.get('board_id')}")
        )
    return inline_boards_btn


def get_inline_lists_btn(board_id, action):
    lists_inline_btn = InlineKeyboardMarkup()
    lists = get_lists(board_id)
    # if len(lists) == 0:
    #     lists_inline_btn.add(InlineKeyboardButton("Mavjud emas!", callback_data=f'{action}_0'))
    if len(lists) % 2 == 0:
        last_list = None
    else:
        last_list = lists.pop()
    for i in range(0, len(lists) - 1, 2):
        lists_inline_btn.add(
            InlineKeyboardButton(
                lists[i].get("name"),
                callback_data=f'{action}_{lists[i].get("id")}'
            ),
            InlineKeyboardButton(
                lists[i + 1].get("name"),
                callback_data=f'{action}_{lists[i + 1].get("id")}'
            )
        )
    if last_list:
        lists_inline_btn.add(
            InlineKeyboardButton(
                last_list.get("name"),
                callback_data=f'{action}_{last_list.get("id")}'
            )
        )
    return lists_inline_btn


