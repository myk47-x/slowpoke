:wq


notify(client: GlpiClient, category: str, ticket_id: int ):
    match category:
        case "ticket":
            query = Ticket.select().where(Ticket.ticket == ticket_id)

        case "enrollment":
            query = Ticket.select().inner_join(Enrollment).join(Users * 2)

        case: "followup":
            query = Ticket.select().inner_join(Followup).join(Users * 3)

        case "solution" :
            query = Ticket.select().inner_join(Solution).join(Users)

