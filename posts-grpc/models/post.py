from typing import Optional

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class PostData(Base):
    __tablename__ = 'posts'

    id: Mapped[str] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column()
    text: Mapped[str] = mapped_column()
    created_at: Mapped[int] = mapped_column(index=True)
    edited_at: Mapped[Optional[int]] = mapped_column()
