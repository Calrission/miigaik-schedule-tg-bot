from aiogram.types import Message


def get_buttons_text_message(message: Message) -> list[str]:
    return [buttons[0].text for buttons in message.reply_markup.inline_keyboard]
