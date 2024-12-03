# meta developer: your_username
# meta banner: https://example.com/banner.png
# meta details: Модуль для добавления пользователей в контакты через команду %nikcn

from telethon.tl.functions.contacts import AddContactRequest
from .. import loader, utils

@loader.tds
class SaveAsContactMod(loader.Module):
    """Модуль для добавления контактов через команду %nikcn"""

    strings = {"name": "SaveAsContact"}

    async def client_ready(self, client, db):
        self.client = client

    async def nikcncmd(self, message):
        """Используйте команду: %nikcn {имя} в ответ на сообщение"""
        if not message.is_reply:
            await message.edit("Ответьте на сообщение пользователя, чтобы сохранить его в контакты.")
            return

        args = utils.get_args_raw(message)
        if not args:
            await message.edit("Укажите имя для нового контакта.")
            return

        reply = await message.get_reply_message()
        user = await self.client.get_entity(reply.sender_id)

        try:
            await self.client(
                AddContactRequest(
                    id=user.id,
                    first_name=args,
                    last_name="",
                    phone="",
                    add_phone_privacy_exception=False,
                )
            )
            await message.edit(f"Пользователь {args} успешно добавлен в контакты.")
        except Exception as e:
            await message.edit(f"Не удалось добавить пользователя в контакты: {e}")
