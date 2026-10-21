from src.config.models import slowpoke_database,User,Ticket,Enrolled,Solution,Followup
import peewee
from src.glpi_client import GlpiClient
from src.load_users import escavate_users
from src.load_tickets import escavate_tickets
from src.load_followups import escavate_followups
from src.load_enrollments import escavate_enrollments

slowpoke_database.connect()
slowpoke_database.create_tables([User, Ticket, Enrolled, Solution, Followup])


with GlpiClient() as client:

    client.authenticate()

    escavate_users(client,{"limit":1000,"sort":"id:asc"})
    escavate_tickets(client,{"limit":2000,"filter":"status.id!=6;is_deleted==false"},True)
    escavate_enrollments(client,{"limit":2000,"filter":"status.id!=6;is_deleted==false"})
    escavate_followups(client,{"limit" : 5000})
