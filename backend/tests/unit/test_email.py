from users.email import send_message_by_email
from unittest.mock import patch
from email import message_from_string
from email.header import decode_header, make_header


def test_send_message_by_email():

    with patch.dict("os.environ", {
        "SMTP_EMAIL": "reservas@example.com",
        "SMTP_PASSWORD": "password_de_prueba"
    }):
        with patch("users.email.smtplib.SMTP") as mock_smtp:

            send_message_by_email(
                user_email="juan@example.com",
                subject="Confirmación de correo",
                message="Su correo ha sido confirmado"
            )

            mock_smtp.assert_called_once_with(
                "smtp.gmail.com", 587
            )

            servidor = mock_smtp.return_value.__enter__.return_value

            servidor.starttls.assert_called_once()

            servidor.login.assert_called_once_with(
                "reservas@example.com",
                "password_de_prueba"
            )

            servidor.sendmail.assert_called_once()

            args = servidor.sendmail.call_args.args

            assert args[0] == "reservas@example.com"
            assert args[1] == "juan@example.com"
            
            mensaje = message_from_string(args[2])
            
            asunto = str(make_header(decode_header(mensaje["Subject"])))

            assert asunto == "Confirmación de correo"

            cuerpo = mensaje.get_payload(0).get_payload(decode=True).decode("utf-8")

            assert cuerpo == "Su correo ha sido confirmado"