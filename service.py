import uuid
from sqlmodel import Session, select
from models import Rule, CreateRule


class RuleAlreadyExistsError(Exception):
    pass


class RuleNotFoundError(Exception):
    pass


class RuleService:

    def create_rule(self, session: Session, data: CreateRule) -> Rule:
        statement = select(Rule).where(
            Rule.source_ip == data.source_ip,
            Rule.port == data.port
        )
        existing = session.exec(statement).first()
        if existing:
            raise RuleAlreadyExistsError(
                f"Rule with source IP {data.source_ip} and port {data.port} already exists"
            )

        new_rule = Rule(id=str(uuid.uuid4()), **data.model_dump())
        session.add(new_rule)
        session.commit()
        session.refresh(new_rule)
        return new_rule

    def get_all_rules(self, session: Session) -> list[Rule]:
        return session.exec(select(Rule)).all()

    def get_rule_by_id(self, session: Session, rule_id: str) -> Rule:
        rule = session.get(Rule, rule_id)
        if not rule:
            raise RuleNotFoundError(f"Rule with ID {rule_id} not found")
        return rule

    def delete_rule(self, session: Session, rule_id: str) -> None:
        rule = session.get(Rule, rule_id)
        if not rule:
            raise RuleNotFoundError(f"Rule with ID {rule_id} not found")
        session.delete(rule)
        session.commit()