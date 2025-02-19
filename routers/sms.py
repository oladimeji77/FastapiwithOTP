from fastapi import status, HTTPException, Depends, APIRouter
from database import get_db2
import dbmodel, schema, routers.spreadsheet as spreadsheet
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(prefix="/send", tags=["SMS"])


excel_path = r'C:\Users\Oladimeji Oladepo\Desktop\Projects\Fast-Bitfumes\sms.xlsx'
db_name = "SMS"
table_name = "sms"
mysql_user = "oladimeji"
mysql_password = "mysqlpass"
# spreadsheet.excel_to_mysql(excel_path, db_name, table_name, mysql_user, mysql_password)

@router.post("/sms")
def updatedb(session: Session = Depends(get_db2)):
    spreadsheet.excel_to_mysql()
    return "Updated"


@router.get("/sms")
def sms_all(session: Session = Depends(get_db2)):
    all_sms = session.query(dbmodel.SMS).all()
    return all_sms