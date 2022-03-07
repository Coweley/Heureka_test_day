from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, Response, JSONResponse
from typing import Optional
from pydantic import BaseModel
import pymysql
from datetime import datetime




class Shop(BaseModel):
        ownerId: int
        name: str
        url: str
        email: str
        orderPhone: Optional[str] = None
        phone: Optional[str] = None
        importUrl: Optional[str] = None
        status: Optional[str] = None
        deactivationReason: Optional[str] = None
        termsAccepted: bool
        questionnaireRecipient: Optional[str] = None
        questionnaireSender: Optional[str] = None
        certifiedAgreementDate: Optional[datetime] = None
        customerId: str
        createdAt: datetime
        updatedAt: datetime

class Message(BaseModel):
    message: str

app = FastAPI()

@app.get("/ping", response_class=PlainTextResponse)
def pong():
    return "pong"


@app.get("/shops/{id}", responses={404: {"model": Message}})
async def get_shop(id: int):
    connection = pymysql.connect(
        host="172.17.0.1",
        port=3306,
        user="root",
        password="root",
        db="api_testday",
    )
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    with cursor as cursor:
        sql = "SELECT * FROM `Shop` WHERE `id`=%s"
        cursor.execute(sql, id)
        result = cursor.fetchone()
        try:
            result['termsAccepted'] = bool( result['termsAccepted'])
            return result
        except:
            print("Fail")
    if result is None:
        return JSONResponse(status_code=404, content={"detail": "Shop not found"})
