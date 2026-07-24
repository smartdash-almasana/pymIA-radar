from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import settings

engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def init_db() -> None:
    from app.models import (
        assessment,
        assessment_v2,
        assessment_v3,
        approved_opportunity_v1,
        conversation,
        conversation_participant,
        discovery,
        engagement,
        presumptive_candidate,
        public_actor,
        qualification,
        review,
    )

    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
