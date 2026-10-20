from peewee import *
from .config import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PORT
)


slowpoke_database = PostgresqlDatabase(
        POSTGRES_DB,
        user = POSTGRES_USER,
        password = POSTGRES_PASSWORD,
        host = POSTGRES_HOST,
        port = POSTGRES_PORT
    )


class BaseModel(Model):

    class Meta:
        database = slowpoke_database


class User(BaseModel):

    class Meta:
        table_name = "users"

    user = IntegerField(primary_key=True)
    user_name = TextField()
    user_email = TextField()


class Ticket(BaseModel):

    class Meta:
        table_name = "ticket"

    ticket = IntegerField(primary_key=True)
    ticket_title = TextField()
    ticket_description = TextField()


class Enrolled(BaseModel):

    class Meta:
        table_name = "enrolled"

    ticket = ForeignKeyField(Ticket, backref="ticket_enrollment")
    enrolled_requester = ForeignKeyField(User, backref="enrolled_requester", null=True)
    enrolled_technician = ForeignKeyField(User, backref="enrolled_technician", null=True)
    enrolled_team = TextField(null=True)


class Followup(BaseModel):

    class Meta:
        table_name = "followup"

    ticket = ForeignKeyField(Ticket, backref="ticket_followup")
    followup = IntegerField(primary_key=True)
    followup_user = ForeignKeyField(User, backref="followup_user")
    followup_content = TextField()


class Solution(BaseModel):

    class Meta:
        table_name = "solution"

    ticket = ForeignKeyField(Ticket, backref="ticket_solution")
    solution = IntegerField(primary_key=True)
    solution_content = TextField()
