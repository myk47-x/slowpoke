from src.config.models import Ticket, Enrolled, Followup, Solution, User
import peewee

def notify( category: str, ticket_id: int ):
    Technician = User.alias()
    Requester = User.alias()
    Updater = User.alias()

    match category:
        case "ticket":
            query = Ticket.select().where(Ticket.ticket == ticket_id)

        case "enrollment":
            query = Ticket.select().inner_join(Enrolled).join(Users * 2)

        case "followup":
            query = Ticket.select(Ticket.ticket.alias("ticket_id"),
                                  Ticket.ticket_title,
                                  Followup.followup_content,
                                  Requester.user_email.alias("requester_user_email"),
                                  Updater.user_name.alias("followup_user_name"),
                                  Updater.user_email.alias("followup_user_email"),
                                  Technician.user_email.alias("assigned_user_email"),
                                  ).join(Followup).where(
                Ticket.ticket == ticket_id).dicts()

            for i in query:
                print(i)

        case "solution" :
            query = Ticket.select().inner_join(Solution).join(Users)

