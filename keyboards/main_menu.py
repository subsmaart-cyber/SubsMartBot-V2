from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🛒 Products"),
                KeyboardButton(text="👛 Wallet"),
            ],
            [
                KeyboardButton(text="👤 Profile"),
                KeyboardButton(text="🎁 Referral"),
            ],
            [
                KeyboardButton(text="⭐ Reviews"),
                KeyboardButton(text="📞 Support"),
            ],
        ],
        resize_keyboard=True
    )
