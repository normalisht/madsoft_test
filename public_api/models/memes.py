import datetime as dt
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from core.db import Base


class Meme(Base):
    filename: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(512), nullable=True)
    image_url: Mapped[str] = mapped_column(String(2096), nullable=True)
    expires_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
