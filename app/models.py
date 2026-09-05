from .database import Base
from sqlalchemy import Column, Integer, String, Enum, CheckConstraint, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class Power(Base):
    __tablename__ = "powers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    damage = Column(Integer, server_default="0", nullable=False)
    learned_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    player_id = Column(Integer, ForeignKey("player.id", ondelete="CASCADE"), nullable=False)

    player = relationship("Player")

class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(Enum("Male", "Female", "Undefined", name="gender_enum"), nullable=False)
    age = Column(Integer, server_default="18", nullable=False)
    race = Column(String, server_default="Human", nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    awakened_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

    __table_args__ = (
        CheckConstraint("age >= 18", name="check_player_age"),
    )

class Love(Base):
    __tablename__ = "loves"

    player_id = Column(Integer, ForeignKey("player.id", ondelete="CASCADE"), primary_key=True)
    power_id = Column(Integer, ForeignKey("powers.id", ondelete="CASCADE"), primary_key=True)    