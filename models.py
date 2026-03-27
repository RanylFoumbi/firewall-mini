import ipaddress
from sqlmodel import SQLModel, Field
from pydantic import field_validator


class RuleBase(SQLModel):
    name: str
    source_ip: str
    port: int

    @field_validator('source_ip')
    @classmethod
    def validate_ip(cls, v: str):
        try:
            ipaddress.ip_address(v)
            return v
        except ValueError:
            raise ValueError(f"{v} is not a valid IP address")

    @field_validator('port')
    @classmethod
    def validate_port(cls, v: int):
        if not 1 <= v <= 65535:
            raise ValueError(f"{v} is not a valid port")
        return v


class Rule(RuleBase, table=True):
    id: str = Field(default=None, primary_key=True)


class CreateRule(RuleBase):
    pass