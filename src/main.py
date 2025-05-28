from fastapi import FastAPI, HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from Data.database import get_db,engine,Base
from Services.MailService import background_email_adder,get_last_email_id
import asyncio
from Setup.MailSetup import initialize_gmail
from Data.DataCrud import retrieve_from_mail,retrieve_mail_by_id
from Dto.ApiResponseDto import ApiResponseDto
from contextlib import asynccontextmanager

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    initialize_gmail()

    global last_seen_id
    last_seen_id = await get_last_email_id()
    task =  asyncio.create_task(background_email_adder())
    print("Background task started.")
    yield
    task.cancel()
    print("Shutting down...")
app=FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return ApiResponseDto(
        status="success",
        message="Welcome to the Mail Fetcher API",
        data=None
    )


@app.get("/mail")
async def get_mail(db: Session = Depends(get_db)):
    try:
        mails = retrieve_from_mail(db)
        return ApiResponseDto(
            status="success",
            message="Mail retrieved successfully",
            data=mails
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/mail/{id}")
async def get_mail_by_id(id: str, db: Session = Depends(get_db)):
    try:
        mail = retrieve_mail_by_id(db, id)
        if not mail:
            raise HTTPException(status_code=404, detail="Mail not found")
        return ApiResponseDto(
            status="success",
            message="Mail retrieved successfully",
            data=mail
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return ApiResponseDto(
        status="error",
        message=exc.detail,
        data=None
    )
@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    return ApiResponseDto(
        status="error",
        message=str(exc),
        data=None
    )