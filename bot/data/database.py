from sqlalchemy import select

from bot.data.models import User, Factory, AsyncSessionLocal

async def new_user(user_id, username: str, factory_name: str) -> None:
    async with AsyncSessionLocal() as session:
        user = User(id=user_id, username=username)

        factory = Factory(owner=user.id, factory_name=factory_name)

        session.add_all([user, factory])
        await session.commit()


async def user_exists(user_id) -> bool:
    async with AsyncSessionLocal() as session:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)

        user = result.scalar_one_or_none()

        return user is not None

async def get_user_name(user_id) -> str:
    async with AsyncSessionLocal() as session:
        query = select(User.username).where(User.id == user_id)
        result = await session.scalar(query)
        return result

async def get_factory_name(user_id) -> str:
    async with AsyncSessionLocal() as session:
        return await session.scalar(select(Factory.factory_name).where(Factory.owner == user_id))


async def get_factory_by_owner(user_id: int) -> Factory | None:
    async with AsyncSessionLocal() as session:
        query = select(Factory).where(Factory.owner == user_id)
        result = await session.execute(query)

        return result.scalar_one_or_none()

async def update_factory(user_id: int, **kwargs) -> Factory | None:
    async with AsyncSessionLocal() as session:
        query = select(Factory).where(Factory.owner == user_id)
        result = await session.execute(query)
        factory = result.scalar_one_or_none()

        if factory:
            for key, value in kwargs.items():
                if hasattr(factory, key):
                    setattr(factory, key, value)

            await session.commit()
            await session.refresh(factory)
            return factory
        return None

async def check_moneys(user_id, price: int) -> bool | None:
    factory = await get_factory_by_owner(user_id=user_id)

    if not factory:
        return None

    if factory.moneys < price:
        return False

    return True