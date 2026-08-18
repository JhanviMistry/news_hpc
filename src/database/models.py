from sqlalchemy import Column, Float, Integer, JSON, String

from .connection import Base


class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(String(20), nullable=True)

    title = Column(String, nullable=False)

    source = Column(String(500), nullable=True)

    impact = Column(Float, nullable=False)

    confidence = Column(Float, nullable=False)

    timestamp = Column(Float, nullable=False)

    relevance = Column(Float, nullable=False)

    sentiment_label = Column(String(20), nullable=True)

    sentiment_score = Column(Float, nullable=True)

    entities = Column(JSON, nullable=True)