from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "mysql+mysqlconnector://ulawkc6zfgwsech8:lKsE4OVD0LHIiwnGoNW5@b6roiwfu2fkgqmej6rcj-mysql.services.clever-cloud.com:3306/b6roiwfu2fkgqmej6rcj"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()