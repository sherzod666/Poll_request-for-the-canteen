from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

choose_lang = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ru🇷🇺'),
            KeyboardButton(text='Uz🇺🇿')
        ]
    ],
    resize_keyboard=True
)

provide_a_rus_review = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Оставить отзыв'), KeyboardButton(text='Отмена')
        ]
    ], resize_keyboard=True
)

provide_an_uzb_review = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Fikr qoldiring'), KeyboardButton(text='Bekor qilish')
        ]
    ], resize_keyboard=True
)

rus_assessment_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отлично')
        ],
        [
            KeyboardButton(text='Хорошо'),
            KeyboardButton(text='Удовлетворительно')
        ],
        [
            KeyboardButton(text='Очень плохо'),
            KeyboardButton(text='Плохо')
        ]
    ], resize_keyboard=True
)

uzb_assessment_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ajoyib')
        ],
        [
            KeyboardButton(text='Yaxshi'),
            KeyboardButton(text='Qoniqarli')
        ],
        [
            KeyboardButton(text='Juda yomon'),
            KeyboardButton(text='Yomon')
        ]
    ], resize_keyboard=True
)

afilliate_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='A1 - Nurofshon(eski/старый)'),
            KeyboardButton(text='A4 - Lunacharski')
        ],
        [
            KeyboardButton(text='A5 - Shimoliy/Северный'),
            KeyboardButton(text='A6 - Kadisheva')
        ],
        [
            KeyboardButton(text='A7 - Taraqiyot'),
            KeyboardButton(text='A8 - Depo')
        ]
    ], resize_keyboard=True
)