from gmailer import send_confirmation_email

def handle_booking(user_id, msg):
    # Here you’d add the Google Calendar API logic
    print(f"✅ Booking confirmed for {user_id}: {msg}")
    send_confirmation_email("client@example.com", msg)
