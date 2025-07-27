from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel

router = APIRouter()

# MODELO SQLALCHEMY
class Song(Base):
    __tablename__ = "TBL_SONG"
    ID_SONG = Column(Integer, primary_key=True, index=True)
    SONG_NAME = Column(String(50), nullable=False)
    SONG_PATH = Column(String(255), nullable=False)
    PLAYS = Column(Integer)

# CREAR TABLAS (opcional si ya están creadas)
Base.metadata.create_all(bind=engine)

# ESQUEMAS Pydantic
class SongSchema(BaseModel):
    SONG_NAME: str
    SONG_PATH: str
    PLAYS: int

    class Config:
        orm_mode = True

class SongUpdateSchema(BaseModel):
    SONG_NAME: str | None = None
    SONG_PATH: str | None = None
    PLAYS: int | None = None

    class Config:
        orm_mode = True

# DEPENDENCIA DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ENDPOINTS CRUD
@router.get("/songs")
def get_songs(db: Session = Depends(get_db)):
    return db.query(Song).all()

@router.post("/songs")
def create_song(song: SongSchema, db: Session = Depends(get_db)):
    new_song = Song(**song.dict())
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song

@router.put("/songs/{song_id}")
def update_song(song_id: int, song_data: SongUpdateSchema, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.ID_SONG == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    for field, value in song_data.dict(exclude_unset=True).items():
        setattr(song, field, value)
    db.commit()
    db.refresh(song)
    return song

@router.delete("/songs/{song_id}")
def delete_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.ID_SONG == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    db.delete(song)
    db.commit()
    return {"message": "Canción eliminada correctamente"}