from uuid import uuid4

from fastapi import HTTPException, UploadFile, Form, File
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings
from utils import save_audio, convert_wav_to_mp3

engine = create_engine(f"postgresql+psycopg2://{settings.DB_USER}:"
                       f"{settings.DB_PASSWORD}@{settings.SERVICE_NAME}/{settings.DB_NAME}")
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String)
    access_token = Column(String)


class AudioRecord(Base):
    __tablename__ = "audio_records"

    id = Column(String, primary_key=True)
    user_id = Column(String)
    file_path = Column(String)


class UserCreate(BaseModel):
    name: str


class AudioRecordCreate(BaseModel):
    user_id: str
    access_token: str
    audio_file: UploadFile

    @classmethod
    def as_form(
            cls,
            user_id: str = Form(...),
            access_token: str = Form(...),
            file: UploadFile = File(...)
    ):
        return cls(
            username=user_id,
            password=access_token,
            file=file
        )


def create_user(db: Session, user_data: UserCreate):
    try:
        user_id = str(uuid4())
        access_token = str(uuid4())

        user = User(id=user_id, name=user_data.name, access_token=access_token)

        db.add(user)
        db.commit()
        db.refresh(user)

        return {"user_id": user_id, "access_token": access_token}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def create_record(db: Session, user_id: str, record_data: AudioRecordCreate):
    record_id = str(uuid4())

    file_extension = record_data.audio_file.filename.split(".")[-1]
    if file_extension != "wav":
        raise HTTPException(status_code=400, detail="Audio file must be in WAV format")

    wav_path = save_audio(record_id, record_data.audio_file.file)
    mp3_filename = convert_wav_to_mp3(record_id, wav_path)

    audio_record = AudioRecord(id=record_id, user_id=user_id, file_path=mp3_filename)
    db.add(audio_record)
    db.commit()

    return record_id


def get_record(db: Session, record_id: str, user_id: str):
    try:
        audio_record = db.query(AudioRecord).filter(AudioRecord.id == record_id, AudioRecord.user_id == user_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Audio record not found")

    return audio_record
