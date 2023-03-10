from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton)

from database import get_boards, get_lists, get_cards


def get_inline_boards_btn(action):
    inline_boards_btn = InlineKeyboardMarkup()
    boards = get_boards()
    if len(boards) % 2 == 0:
        last_board = None
    else:
        last_board = boards.pop()
    for i in range(0, len(boards) - 1, 2):
        inline_boards_btn.add(
            InlineKeyboardButton(
                boards[i].get("name"), callback_data=f"{action}_{boards[i].get('id')}"
            ),
            InlineKeyboardButton(
                boards[i + 1].get("name"), callback_data=f"{action}_{boards[i + 1].get('id')}"
            ),
        )
    if last_board:
        inline_boards_btn.add(
            InlineKeyboardButton(last_board.get("name"), callback_data=f"{action}_{last_board.get('id')}")
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


def get_cards_btn(list_id):
    data = get_cards(list_id)
    if not data:
        return 'Task topilmadi!'
    msg = ''
    for i in data:
        msg += f"<a href=\"{i.get('url')}\">{i.get('name')}</a>\n"
    return msg
