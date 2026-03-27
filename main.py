from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session
from models import CreateRule
from database import create_db_and_tables, get_session
from service import RuleService, RuleAlreadyExistsError, RuleNotFoundError

app = FastAPI()
rule_service = RuleService()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.on_event("shutdown")
def on_shutdown():
    print("Application shutting down")

@app.get("/")
def get_rules(session: Session = Depends(get_session)):
    return rule_service.get_all_rules(session)


@app.get("/{rule_id}")
def get_rule(rule_id: str, session: Session = Depends(get_session)):
    try:
        return rule_service.get_rule_by_id(session, rule_id)
    except RuleNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/", status_code=201)
def create_rule(data: CreateRule, session: Session = Depends(get_session)):
    try:
        return rule_service.create_rule(session, data)
    except RuleAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.delete("/{rule_id}")
def delete_rule(rule_id: str, session: Session = Depends(get_session)):
    try:
        rule_service.delete_rule(session, rule_id)
        return {"message": "Rule deleted successfully"}
    except RuleNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))