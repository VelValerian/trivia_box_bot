from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.utils import *
from app.database import *
from app.keyboards import *


router = Router()


@router.message(F.text == "Add")
async def cmd_add(message: Message, state: FSMContext):
    await message.answer("Write Name",
                         reply_markup=keyboard_reply.back_keyboard)
    await state.set_state(AddForm.name)


@router.message(AddForm.name)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddForm.note)
    await message.answer("Write Note", reply_markup=keyboard_reply.back_keyboard)


@router.message(AddForm.note)
async def form_note(message: Message, state: FSMContext):
    await state.update_data(note=message.text)
    await state.set_state(AddForm.tag)
    await message.answer("Write Tag", reply_markup=keyboard_reply.back_keyboard)


@router.message(AddForm.tag)
async def form_tag(message: Message, state: FSMContext):
    await state.update_data(tag=message.text.lower())
    await state.set_state(AddForm.photo)
    await message.answer("Загрузите фото.", reply_markup=keyboard_reply.back_keyboard)


@router.message(AddForm.photo, F.photo)
async def form_photo(message: Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    data = await state.get_data()
    print(message.from_user.id, data, photo_file_id)
    await state.clear()

    await db_commands.db_add(message.from_user.id, data['name'], data['note'], data['tag'], photo_file_id)
    await message.answer(f"Вы успешно добавили {data['name']}", reply_markup=keyboard_reply.begin_keyboard)


@router.message(AddForm.photo, ~F.photo)
async def incorrect_photo(message: Message, state: FSMContext):
    await message.answer("Отправь фото!")

