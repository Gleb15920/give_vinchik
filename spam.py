from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from collections import defaultdict
from time import time
import give_vinchik.app.keybords as kb

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, logger, limit=1, period=1):
        super().__init__()
        self.limit = limit  # Максимум сообщений
        self.period = period  # Период в секундах
        self.user_messages = defaultdict(list)
        self.logger = logger

    async def __call__(
        self,
        handler,
        event: TelegramObject,
        data: dict,
    ):
        state = data.get("state")
        if not isinstance(event, Message):
            return await handler(event, data)

        user_id = event.from_user.id
        current_time = time()

        self.user_messages[user_id] = [
            t for t in self.user_messages[user_id] if current_time - t < self.period
        ]

        self.user_messages[user_id].append(current_time)

        if len(self.user_messages[user_id]) > self.limit:
            self.logger.warning(f"Пользователь {user_id} превысил лимит сообщений: {self.limit} за {self.period} сек")
            await event.answer("Слишком много сообщений! Подождите немного.",
                               reply_markup=kb.registred_user,
                               resize_keyboard=True
                               )
            await state.clear()
            return

        return await handler(event, data)
