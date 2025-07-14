import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_email_alert(product_data, threshold):
    # Email configuration (use environment variables)
    sender_email = os.getenv("EMAIL_USER")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    print(sender_email)
    print(receiver_email)
    print(password)
    
    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = f"Price Alert: {product_data['title']}"
    
    body = f"""
    Price Alert!
    
    Product: {product_data['title']}
    Current Price: ${product_data['price']}
    Your Threshold: ${threshold}
    
    Link: {product_data['url']}
    """
    
    message.attach(MIMEText(body, "plain"))
    
    # Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email alert sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage
# if __name__ == "__main__":
#     # This would normally be called from tracker.py when alert is triggered
#     test_product = {
#         'title': 'Test Product',
#         'price': 250.00,
#         'url': 'https://example.com/product',
#         'date': '2023-01-01'
#     }
#     send_email_alert(test_product, 300.00)