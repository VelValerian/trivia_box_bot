from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.utils import *
from app.database import *
from app.keyboards import *


router = Router()


@router.message(F.text == "Search")
async def cmd_search(message: Message, state: FSMContext):
    await message.answer("Write tag of object to search."
                         "\nPress 'Tag List' button to receive all tags",
                         reply_markup=keyboard_reply.search_tag_keyboard)
    await state.set_state(SearchDelForm.tag)
    await state.update_data(tag='search')
    await message.delete()


@router.message(SearchDelForm.tag)
async def search_del_tag_result(message: Message, state: FSMContext):
    state_value = await state.get_data()
    #  Search part of function
    if state_value['tag'] == 'search':
        tags_list = await db_commands.db_tag_list(message.from_user.id)

        if not tags_list:
            await message.answer(f"You don't have tags in library!",
                                 reply_markup=keyboard_reply.begin_keyboard)
        else:
            tag_check = await db_commands.db_value_check(tags_list, message.text.lower())

            if tag_check:
                object_list = await db_commands.db_object_list(message.from_user.id, message.text.lower())
                separator = '\n'
                await message.answer(f"Write ID of object from list you want search:"
                                     f"\n\n{separator.join(object_list)} ",
                                     reply_markup=keyboard_reply.search_object_keyboard)
                await state.set_state(SearchDelForm.object)
                await state.update_data(object='search')
                await state.update_data(msg=message.text)


            else:
                await message.answer(f"<b>{message.text}</b> \nYou don't have this tag in library!"
                                     f"\nPlease check 'Search Tag List'",
                                     reply_markup=keyboard_reply.search_tag_keyboard)
    #  Delete part of function
    else:
        tags_list = await db_commands.db_tag_list(message.from_user.id)

        if not tags_list:
            await message.answer(f"You don't have tags in library!",
                                 reply_markup=keyboard_reply.begin_keyboard)
        else:
            tag_check = await db_commands.db_value_check(tags_list, message.text.lower())

            if tag_check:
                object_list = await db_commands.db_object_list(message.from_user.id, message.text.lower())
                separator = '\n'
                await message.answer(f"Write ID of object from list you want delete:"
                                     f"\n\n{separator.join(object_list)} ",
                                     reply_markup=keyboard_reply.delete_object_keyboard)
                await state.set_state(SearchDelForm.object)
                await state.update_data(object='delete')
                await state.update_data(msg=message.text)

            else:
                await message.answer(f"<b>{message.text}</b> \nYou don't have this tag in library!"
                                     f"\nPlease check 'Delete Tag List'",
                                     reply_markup=keyboard_reply.delete_tag_keyboard)


@router.message(SearchDelForm.object)
async def search_del_object_result(message: Message, state: FSMContext):
    state_value = await state.get_data()

    if state_value['object'] == 'search':
        msg = await db_commands.is_number(message.text)

        if msg:
            id_list = await db_commands.db_id_list(message.from_user.id, state_value['msg'])
            id_check = await db_commands.db_value_check(id_list, int(message.text))

            if id_check:
                object_results = await db_commands.db_objects_results(message.from_user.id, int(message.text))
                name = object_results[2]
                note = object_results[3]
                tag = object_results[4]
                photo_tg_id = object_results[5]

                if photo_tg_id == 'None':
                    await message.answer(f"Name: {name}\nNote: {note}\nTag: {tag}\nDon't have photo",
                                         reply_markup=keyboard_reply.search_object_keyboard)
                    await state.clear()
                else:
                    await message.answer_photo(photo_tg_id,
                                               f"Name: {name}\nNote: {note}\nTag: {tag}",
                                               reply_markup=keyboard_reply.search_object_keyboard)
                    await state.clear()
            else:
                await message.answer('Please write only number ID of object you searched'
                                     '\n\nOr start search from begin by pressing Search button',
                                     reply_markup=keyboard_reply.search_object_keyboard)
        else:
            await message.answer('Please write only number ID of object you searched'
                                 '\n\nOr start search from begin by pressing Search button',
                                 reply_markup=keyboard_reply.search_object_keyboard)
        #  Delete part of function
    else:
        msg = await db_commands.is_number(message.text)

        if msg:
            id_list = await db_commands.db_id_list(message.from_user.id, state_value['msg'])
            id_check = await db_commands.db_value_check(id_list, int(message.text))

            if id_check:
                object_results = await db_commands.db_objects_results(message.from_user.id, int(message.text))
                name = object_results[2]
                note = object_results[3]
                tag = object_results[4]

                await message.answer(f"Successful delete:\n\nName: {name}\nNote: {note}\nTag: {tag}\n",
                                     reply_markup=keyboard_reply.delete_object_keyboard)
                await db_commands.db_delete_object(message.from_user.id, int(message.text))
                await state.clear()
            else:
                await message.answer('Please write only number ID of object want delete'
                                     '\n\nOr start search from begin by pressing Delete button',
                                     reply_markup=keyboard_reply.delete_object_keyboard)
        else:
            await message.answer('Please write only number ID of object want delete'
                                 '\n\nOr start search from begin by pressing Delete button',
                                 reply_markup=keyboard_reply.delete_object_keyboard)
