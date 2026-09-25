import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

BASE_DIR = Path(__file__).resolve().parent
INDEX_PATH = BASE_DIR / "frontend" / "templates" / "index.html"

RAW_DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@db:5432/app_db"
)

# Enforce asyncpg scheme for async SQLAlchemy engine
if RAW_DB_URL.startswith("postgresql://"):
    DATABASE_URL = RAW_DB_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif RAW_DB_URL.startswith("postgres://"):
    DATABASE_URL = RAW_DB_URL.replace("postgres://", "postgresql+asyncpg://", 1)
else:
    DATABASE_URL = RAW_DB_URL

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class TeamMember(Base):
    __tablename__ = "team_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_name: Mapped[str] = mapped_column(String(100))
    member_name: Mapped[str] = mapped_column(String(100))


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(TeamMember))
        if not result.scalars().first():
            team = "Tech-Titans"
            members = ["Stefan", "Sebastian"]

            session.add_all([
                TeamMember(team_name=team, member_name=name) for name in members
            ])
            await session.commit()
    yield


# Single application instance with initialized lifespan
app = FastAPI(title="Academy API", lifespan=lifespan)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@app.get("/")
async def read_root():
    if not INDEX_PATH.is_file():
        raise HTTPException(status_code=404, detail="Index file not found")
    return FileResponse(INDEX_PATH)


@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}


@app.get("/api/team")
async def get_team(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TeamMember))
    records = result.scalars().all()

    if not records:
        return {"team_name": "N/A", "members": []}

    return {
        "team_name": records[0].team_name,
        "members": [r.member_name for r in records]
    }
