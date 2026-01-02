from fastapi import FastAPI
from notifications_template.routes import router as noti_router
from database_template.template import router as db_router
 
from core.database import engine,Base_model

Base_model.metadata.create_all(bind=engine)



app=FastAPI()
app.include_router(noti_router)
app.include_router(db_router)

@app.get("/")
def root():
    return {"Connection":"Successful"}