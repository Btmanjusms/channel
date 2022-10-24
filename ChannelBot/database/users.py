from .channel import Channel


class Users(Channel):
    
    async def check_user(self, user_id):
        user = await self.users.find_one({"user_id": user_id})
        if not user:
            new_user = {
                'user_id': user_id,
                'channels': []
            }
            await self.users.insert_one(new_user)


    async def num_users(self):
        await self.users.count_documents({})


    async def add_channel(self, user_id, channel_id):
        user = await self.users.find_one({"user_id": user_id})
        channels = user.get('channels', [])
        channels.append(channel_id)
        await self.users.update_one({'user_id': user_id}, {'$set': {'channels': channels}})


    async def remove_channel(self, user_id, channel_id):
        user = await self.users.find_one({"user_id": user_id})
        channels = user.get('channels', [])
        channels.remove(channel_id)
        await self.users.update_one({'user_id': user_id}, {'$set': {'channels': channels}})


    async def get_channels(self, user_id):
        user = await self.users.find_one({"user_id": user_id})
        channels = user.get('channels', [])
        if len(channels) == 0:
            return False, channels
        return True, channels
