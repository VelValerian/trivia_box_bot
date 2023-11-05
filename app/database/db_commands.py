import sqlite3 as sq3

# Connection to DB
# con = sq3.connect('trivia_box_library.db')
con = sq3.connect('trivia_box_library.db')
# Create connection for work with DB
cur = con.cursor()


async def db_start():
    """ Create if NOT exists TABLETS in DB"""
    cur.execute("CREATE TABLE IF NOT EXISTS things_lib ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "user_tg_id INTEGER, "
                "name TEXT UNIQUE NOT NULL, "
                "note TEXT,"
                "tag TEXT,"
                "photo TEXT)")

    con.commit()


async def db_tag_list(user_tg_id: int) -> list:
    """
    Get list of user tags from DB
    :param user_tg_id: telegram id of user
    :return: Sorted list of user tags
    If list is empty: return None
    """
    cur.execute("SELECT DISTINCT tag FROM things_lib WHERE user_tg_id =?",
                (user_tg_id,))
    x = cur.fetchall()
    a = 0
    lst_tags = []
    for i in x:
        lst_tags.append(x[a][0])
        a += 1
    lst_tags.sort()
    return lst_tags


async def db_id_list(user_id: int, tag: str) -> list:
    """
    Get list of user tags from DB
    :param user_id: telegram id of user
    :param tag: telegram id of user
    :return: Sorted list of id object by tag
    If list is empty: return None
    """
    cur.execute("SELECT DISTINCT id FROM things_lib WHERE user_tg_id =? AND tag =?",
                (user_id, tag.lower()))
    x = cur.fetchall()
    a = 0
    lst_id = []
    for i in x:
        lst_id.append(x[a][0])
        a += 1
    lst_id.sort()
    return lst_id


async def db_value_check(check_list: list, search_value) -> bool:
    """
    Check if a vakue exists in list
    :param check_list: list of values
    :param search_value: value to check
    :return: True if tag exists
    """
    for i in check_list:
        if i == search_value:
            x = True
            return x
    else:
        x = False
        return x


async def db_object_list(user_id: int, tag: str) -> list:
    """
    Get list of user objects from DB
    :param user_id: telegram id of user
    :param tag: tag of objects user search
    :return: Sorted list of user objects
    If list is empty: return None
    """
    cur.execute("SELECT id,name FROM things_lib WHERE user_tg_id =? AND tag =?",
                (user_id, tag.lower()))
    x = cur.fetchall()
    x = dict(x)
    lst_objects = []
    for i, n in x.items():
        lst_objects.append(f"ID:{i} -> {n}")
    return lst_objects


async def db_objects_results(user_id: int, id: int):

    cur.execute(f"SELECT * FROM things_lib WHERE user_tg_id =? AND id =?",
                (user_id, id))
    x = cur.fetchall()
    x = x[0]
    return x


async def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


async def db_delete_object(user_id: int, id: int):
    """
    Delete row from DB
    :param user_id: telegram id of user
    :param id: row id in TABLE
    """
    cur.execute(f"DELETE FROM things_lib WHERE user_tg_id=? AND id=?",
                (user_id, id))
    con.commit()


async def db_add(tg_id, name, note, tag, photo_file_id):
    """
    INSERT new object in DB
    :param tg_id: telegram id of user
    :param name: Name of object
    :param note: Note of object
    :param tag: Tag of object
    :param photo_file_id: telegram id of photo
    """
    cur.execute(f"INSERT INTO things_lib(user_tg_id, name, note, tag, photo) "
                f"VALUES('{tg_id}', '{name}', '{note}', '{tag}', '{photo_file_id}')")

    con.commit()
