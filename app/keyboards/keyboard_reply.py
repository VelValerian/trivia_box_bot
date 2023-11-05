from aiogram.types import ReplyKeyboardMarkup
from app.keyboards.buttons_reply import *

start_keyboard = ReplyKeyboardMarkup(keyboard=start_button, resize_keyboard=True)

begin_keyboard = ReplyKeyboardMarkup(keyboard=begin_button, resize_keyboard=True)

edit_keyboard = ReplyKeyboardMarkup(keyboard=edit_button, resize_keyboard=True)

back_keyboard = ReplyKeyboardMarkup(keyboard=back_button, resize_keyboard=True)

search_tag_keyboard = ReplyKeyboardMarkup(keyboard=search_tag_button, resize_keyboard=True)
search_object_keyboard = ReplyKeyboardMarkup(keyboard=search_object_button, resize_keyboard=True)

delete_tag_keyboard = ReplyKeyboardMarkup(keyboard=delete_tag_button, resize_keyboard=True)
delete_object_keyboard = ReplyKeyboardMarkup(keyboard=delete_object_button, resize_keyboard=True)
