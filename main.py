import os
import time
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.exc import NoResultFound, OperationalError

from config import settings
from database import Session, UserCreate, create_user, AudioRecordCreate, User, create_record, get_record, Base, engine

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

while True:
    try:
        conn = engine.connect()
        conn.close()
        break
    except OperationalError:
        time.sleep(1)

Base.metadata.create_all(bind=engine)


@contextmanager
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", tags=['users'])
async def create_user_rest(user_data: UserCreate):
    with get_db() as db:
        result = create_user(db, user_data)
        return result


@app.post("/record", tags=["records"])
async def create_record_rest(record_data: AudioRecordCreate = Depends(AudioRecordCreate)):
    with get_db() as db:

        try:
            user = db.query(User).filter(User.id == record_data.user_id,
                                         User.access_token == record_data.access_token).one()
        except NoResultFound:
            raise HTTPException(status_code=401, detail="Invalid user credentials")

        record_id = create_record(db=db, user_id=user.id, record_data=record_data)

        download_url = f"http://{settings.HOST}:{settings.PORT}/record?record_id={record_id}&user_id={user.id}"
        return {"download_url": download_url}


@app.get("/record", tags=["records"])
def download_audio_record(record_id: str, user_id: str):
    with get_db() as db:
        audio_record = get_record(db=db, user_id=user_id, record_id=record_id)
        mp3_path = f"audio_files/{audio_record.file_path}"

        if not os.path.isfile(mp3_path):
            raise HTTPException(status_code=404, detail="Audio record file not found")

        return FileResponse(path=mp3_path, media_type="application/octet-stream", filename=audio_record.file_path)
