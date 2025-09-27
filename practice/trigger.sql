CREATE TRIGGER create_ticket_after_registration
AFTER INSERT ON Register_to
FOR EACH ROW
BEGIN
    -- Create a new ticket
    INSERT INTO Tickets (status, qr_code_data)
    VALUES ('issued', CONCAT('QR-', NEW.user_id, '-', NEW.event_id));

    -- Link ticket to the event
    INSERT INTO Generates (event_id, ticket_id)
    VALUES (NEW.event_id, LAST_INSERT_ID());

    -- Link ticket to the user
    INSERT INTO StudentTicket (user_id, ticket_id, booking_date)
    VALUES (NEW.user_id, LAST_INSERT_ID(), NOW());
END;
