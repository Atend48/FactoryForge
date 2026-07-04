from bot.data.base_data_base import User, Factory, AsyncSessionLocal

async def new_user(user_id, username: str, factory_name: str) -> None:
    async with AsyncSessionLocal() as session:
        user = User(id=user_id, username=username)

        factory = Factory(owner=user.id, factory_name=factory_name)

        session.add_all([user, factory])
        await session.commit()