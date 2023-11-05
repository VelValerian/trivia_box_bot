from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.utils import *
from app.database import *
from app.keyboards import keyboard_reply


@dp.message(CommandStart())
async def cmd_start(message: Message):
    # await db_commands.db_start()
    await message.answer(f"Hi {message.from_user.username} "
                         "\n\nI'm a simple Bot that can store trivias in library."
                         "\nYou can store books or simple things that interest you.",
                         reply_markup=keyboard_reply.start_keyboard)
    await message.delete()


@dp.message(F.text == "Help")
async def cmd_help(message: Message):
    await message.answer("\nYou can Add, Edit and Delete trivias that will you stored in the bot's library."
                         "\nIt is also possible to search throug trivia box for an already stored stuff.",
                         reply_markup=keyboard_reply.start_keyboard)
    await message.delete()


@dp.message(F.text.in_({"Begin", "Back"}))
async def cmd_search(message: Message, state: FSMContext):
    await message.answer("Let's Start", reply_markup=keyboard_reply.begin_keyboard)
    a = await state.get_data()
    await state.clear()
    await message.delete()


@dp.message(F.text == "Edite")
async def cmd_search(message: Message):
    await message.answer("Select button you need", reply_markup=keyboard_reply.edit_keyboard)
    await message.delete()


@dp.message(F.text == "Search Tag List")
async def cmd_search_tag_list(message: Message):
    tags_list = await db_commands.db_tag_list(message.from_user.id)
    if not tags_list:
        await message.answer(f"You don't have tags in library!",
                             reply_markup=keyboard_reply.begin_keyboard)
        await message.delete()
    else:
        await message.answer(f"Write tag of object from list you want search:"
                             f"\n\n{', '.join(tags_list)} ",
                             reply_markup=keyboard_reply.search_tag_keyboard)
        await message.delete()


@dp.message(F.text == "Delete")
async def cmd_delete(message: Message, state: FSMContext):
    await message.answer("Write tag of object to delete."
                         "\nPress 'Tag List' button to receive all tags",
                         reply_markup=keyboard_reply.delete_tag_keyboard)
    await state.set_state(SearchDelForm.tag)
    await state.update_data(tag='delete')
    await message.delete()


@dp.message(F.text == "Delete Tag List")
async def cmd_search_tag_list(message: Message):
        tags_list = await db_commands.db_tag_list(message.from_user.id)
        if not tags_list:
            await message.answer(f"You don't have tags in library!",
                                 reply_markup=keyboard_reply.begin_keyboard)
            await message.delete()
        else:
            await message.answer(f"Write tag of object from list you want delete:"
                                 f"\n\n{', '.join(tags_list)} ",
                                 reply_markup=keyboard_reply.delete_tag_keyboard)
        await message.delete()


