import asyncio
import logging
from app.handlers import *
from app.database import *
from app.utils import *


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )

    try:
        dp.include_routers(search_del.router, add_object.router)
        await bot.delete_webhook(drop_pending_updates=True)
        await db_commands.db_start()
        await dp.start_polling(bot)

    finally:
        await bot.session.close()
        db_commands.con.close()

if __name__ == '__main__':
    asyncio.run(start())
