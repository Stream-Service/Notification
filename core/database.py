from core.config import setting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

Base_model=declarative_base()
 
database_url=setting.get_db_url()

engine=create_engine(database_url,echo=True)
sessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

