from motor import motor_asyncio as mm


class Channel:
    def __init__(self, uri, database_name):
        self._client = mm.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.channel = self.db.channel
        self.users = self.db.users


    async def is_channel_exist(self, channel_id):
        channel = await self.get_channel_info(channel_id)
        return True if channel else False


    async def num_channels(self):
        count = await self.channel.count_documents({})
        return count


    async def new_channel(self, channel_id, admin_id):
        channel = {
            'channel_id': channel_id,
            'admin_id': admin_id,
            'buttons': None,
            'caption': None,
            'position': 'below',
            'sticker_id': None,
            'webpage_preview': False,
            'edit_mode': 'media'
        }
        await self.channel.insert_one(channel)
        return channel


    async def delete_channel(self, channel_id):
        await self.channel.delete_many({'channel_id': int(channel_id)})


    async def get_channel_info(self, channel_id):
        channel = await self.channel.find_one({"channel_id": channel_id})
        if channel:
            return True, channel
        return False, channel


    async def set_caption(self, channel_id, caption):
        await self.channel.update_one({'channel_id': channel_id}, {'$set': {'caption': caption}})


    async def get_caption(self, channel_id):
        channel = await self.channel.find_one({"channel_id": channel_id})
        return channel.get('caption', None)


    async def set_buttons(self, channel_id, buttons):
        await self.channel.update_one({'channel_id': channel_id}, {'$set': {'buttons': buttons}})


    async def get_buttons(self, channel_id):
        channel = await self.channel.find_one({"channel_id": channel_id})
        return channel.get('buttons', None)


    async def set_position(self, channel_id, position):
        await self.channel.update_one({'channel_id': channel_id}, {'$set': {'position': position}})


    async def get_position(self, channel_id):
        channel = await self.channel.find_one({"channel_id": channel_id})
        return channel.get('position', 'below')


    async def set_sticker(self, channel_id, sticker):
        await self.channel.update_one({'channel_id': channel_id}, {'$set': {'sticker_id': sticker}})
        

    async def get_sticker(self, channel_id):
        channel = await self.channel.find_one({"channel_id": channel_id})
        return channel.get('sticker_id', None)


    async def toggle_webpage_preview(self, channel_id, value):
        sts = True if value else False
        await self.channel.update_one({'channel_id': channel_id}, {'$set': {'webpage_preview': sts}})


    async def get_webpage_preview(self, channel_id):
        channel = await self.channel.find_one({"channel_id": channel_id})
        return channel.get('webpage_preview', False)
        

    async def set_edit_mode(self, channel_id, edit_mode):
        await self.channel.update_one({'channel_id': channel_id}, {'$set': {'edit_mode': edit_mode}})


    async def get_edit_mode(self, channel_id):
        channel = await self.channel.find_one({"channel_id": channel_id})
        return channel.get('edit_mode', 'media')
