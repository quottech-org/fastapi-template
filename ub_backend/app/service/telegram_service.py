import asyncio
from aiogram import Bot, Dispatcher, exceptions
from ub_backend.app.model.full_order import FullOrder
from ub_backend.core.config import app_config
from ub_backend.core.logger import logger

class TelegramService:
    def __init__(self):
        self._bot = Bot(token=app_config.telegram.bot_token)
        self._dp = Dispatcher(self._bot)

    async def send_message(self, user_id: int, text: str, disable_notification: bool = False) -> bool:
        try:
            await self._bot.send_message(user_id, text, disable_notification=disable_notification)
        except exceptions.BotBlocked:
            logger.error(f"Target [ID:{user_id}]: blocked by user")
        except exceptions.ChatNotFound:
            logger.error(f"Target [ID:{user_id}]: invalid user ID")
        except exceptions.RetryAfter as e:
            logger.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
            await asyncio.sleep(e.timeout)
            return await self._bot.send_message(user_id, text)  # Recursive call
        except exceptions.UserDeactivated:
            logger.error(f"Target [ID:{user_id}]: user is deactivated")
        except exceptions.TelegramAPIError:
            logger.exception(f"Target [ID:{user_id}]: failed")
        else:
            logger.info(f"Target [ID:{user_id}]: success")
            return True
        return False

    async def send_order_alert(self, full_order: FullOrder):
        msg = f"order_id: {full_order.order.id}" + "\n" + f"TOTAL $: {full_order.total_price_usd}" + "\n---\ncart:\n"
        for i in full_order.goods:
            msg += "\t" + f'{i.title} - {i.price_usd}$' + "\n"
        msg += "---\n" + f"client_tel: {full_order.client.phone_number}"

        for chat_id in app_config.telegram.alert_order_create_chats:
            await self.send_message(chat_id, text=msg)
            
telegram_service = TelegramService()
