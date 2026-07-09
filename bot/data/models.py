from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import String, ForeignKey, CheckConstraint, BIGINT, Computed
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

DATABASE_URL = "sqlite+aiosqlite:///db.sqlite3"
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    username: Mapped[str] = mapped_column(String(70))


class Factory(Base):
    __tablename__ = "fabrics"

    id: Mapped[int] = mapped_column(primary_key=True)
    factory_name: Mapped[str] = mapped_column(String(70))

    environmental_friendliness: Mapped[float] = mapped_column(
        CheckConstraint("environmental_friendliness < 6.0", name="check_environmental_friendliness"),
        default=0.0
    )
    number_of_workers: Mapped[int] = mapped_column(default=0)
    workers_happiness: Mapped[float] = mapped_column(
        CheckConstraint("workers_happiness < 6.0", name="check_workers_happiness"),
        default=0.0
    )
    quality_of_equipment: Mapped[float] = mapped_column(
        CheckConstraint("quality_of_equipment < 6.0", name="check_quality_of_equipment"),
        default=0.0
    )
    production_per_hour: Mapped[float] = mapped_column(
        Computed("(number_of_workers * 0.5) * (1 + quality_of_equipment * 0.2) * (1 + workers_happiness * 0.1)")
    )
    price: Mapped[float] = mapped_column(
        Computed("50 + (quality_of_equipment * 20) + (environmental_friendliness * 15)")
    )
    number_of_production: Mapped[int] = mapped_column(default=0)
    worker_fatigue: Mapped[int] = mapped_column(
        CheckConstraint("worker_fatigue < 3", name="check_worker_fatigue"),
        default=0
    )

    moneys: Mapped[int] = mapped_column(default=10000)
    expenses_per_hour: Mapped[float] = mapped_column(
        Computed("(number_of_workers * 100) + (environmental_friendliness * 50) + (quality_of_equipment * 30)")
    )
    reputation: Mapped[float] = mapped_column(
        Computed("100 + (environmental_friendliness * 3) + (quality_of_equipment * 2)")
    )
    score: Mapped[float] = mapped_column(
        Computed("(moneys * 0.1) + (reputation * 10) + (quality_of_equipment * 50) + (environmental_friendliness * 40) + (workers_happiness * 30)")
    )

    owner: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
