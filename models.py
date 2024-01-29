from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Integer, String, ForeignKey, UUID
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from database import Base


# https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html
class BaseInfoMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    notes: Mapped[Optional[str]]


class User(BaseInfoMixin, Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(50), index=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    hashed_password: Mapped[str]
    user_uuid: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4)
    is_active: Mapped[bool] = mapped_column(default=True)
    verified_at: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=True)

    tokens = relationship('UserRefreshToken', back_populates='user')

    def __repr__(self) -> str:
        return f'User {self.name} -> #{self.id}'


class UserRefreshToken(BaseInfoMixin, Base):
    __tablename__ = 'refresh_tokens'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    refresh_key: Mapped[str]
    expires_at: Mapped[datetime]

    user = relationship('User', back_populates='tokens')


class Product(BaseInfoMixin, Base):
    __tablename__ = 'products'

    title: Mapped[str]
    price: Mapped[float]
    image_url: Mapped[str] = mapped_column(default='', nullable=True)
    image_file: Mapped[str] = mapped_column(default='', nullable=True)
