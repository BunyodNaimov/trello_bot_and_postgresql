def get_fullname(chat_message):
    first_name = chat_message.chat.first_name
    last_name = chat_message.chat.last_name
    return f"{first_name} {last_name}" if last_name else first_name


def get_cards_btn(cards):
    msg = ''
    for index, card in enumerate(cards):
        msg += f"{index + 1}. <a href=\"{card.get('url')}\">{card.get('card_name')}</a>\n"
    return msg
