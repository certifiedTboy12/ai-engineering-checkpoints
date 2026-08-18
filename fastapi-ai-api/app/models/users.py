import uuid
from typing import TYPE_CHECKING
from sqlalchemy import String
from datetime import datetime
from app.config.dbconfig import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from app.models.conversations import Conversation


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    first_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    password: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    otp: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    otp_expiry: Mapped[datetime | None] = mapped_column(
        nullable=True
    )

    is_verified: Mapped[bool] = mapped_column(
        default=False,
        nullable=False
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation",
        back_populates="user",
        cascade="all, delete-orphan"
    )