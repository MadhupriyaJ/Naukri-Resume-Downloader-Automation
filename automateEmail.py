import imaplib
import email
from email.header import decode_header
import os

# Account credentials
USERNAME = "kalidas19021993@gmail.com"  # Replace with your email
PASSWORD = "jhxk czqj wafy bimz"          # Replace with your password
IMAP_SERVER = "imap.gmail.com"      # IMAP server for Gmail, update for other providers

# Directory to save attachments
SAVE_DIR = "attachments"

# Ensure the save directory exists
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def clean_filename(filename):
    """Cleans up a filename to avoid invalid characters."""
    return "".join(c for c in filename if c.isalnum() or c in (" ", ".", "_")).strip()

def download_email_attachments():
    try:
        # Connect to the server and log in
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(USERNAME, PASSWORD)
        print("Logged in successfully!")

        # Select the mailbox you want to use (INBOX)
        mail.select("inbox")

        # Search for all emails
        status, messages = mail.search(None, 'ALL')
        if status != "OK":
            print("No messages found!")
            return

        # Convert messages to a list of email IDs
        email_ids = messages[0].split()

        print(f"Found {len(email_ids)} emails. Starting to process...")

        # Loop through the email IDs
        for i, email_id in enumerate(email_ids):
            # Fetch the email by ID
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            if status != "OK":
                print(f"Failed to fetch email ID: {email_id}")
                continue

            # Parse the email content
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # Decode email subject
                        subject = subject.decode(encoding if encoding else "utf-8")
                    print(f"Processing email: {subject}")

                    # Iterate through email parts
                    for part in msg.walk():
                        # Check if the content is an attachment
                        if part.get_content_maintype() == "multipart":
                            continue
                        if part.get("Content-Disposition") is None:
                            continue

                        # Get the filename of the attachment
                        filename = part.get_filename()
                        if filename:
                            filename = clean_filename(filename)
                            filepath = os.path.join(SAVE_DIR, filename)

                            # Save the attachment
                            with open(filepath, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            print(f"Downloaded: {filename}")

        # Logout
        mail.logout()
        print("Finished processing emails and logged out.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    download_email_attachments()