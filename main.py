import pdf2image
import requests
import os
from config import CHAT_ID, URL_FOR_PHOTO, URL_FOR_BOOK, BOOK_CAPTION, DIRECTORY

# Set directory where the books are stored
os.chdir(DIRECTORY)
Books = [book for book in os.listdir() if book.endswith(".pdf")]

# Send the image function
def send_photo(book, name):
    images = pdf2image.convert_from_path(book, first_page=1, last_page=1)
    image_path = f"{name}_pic.png"
    images[0].save(image_path, "PNG")
    
    # Send the photo to Telegram
    with open(image_path, "rb") as photo:
        response = requests.post(
            URL_FOR_PHOTO,
            data={"chat_id": CHAT_ID, "caption": name},
            files={"photo": photo}
        )

    return response

# Send the book function
def send_document(book, name, id):
    with open(book, "rb") as document:
        response = requests.post(
            URL_FOR_BOOK,
            data={
                "chat_id": CHAT_ID,
                "caption": BOOK_CAPTION,
                "reply_to_message_id": id
            },
            files={"document": document}
        )

    if response.status_code == 200:
        print(f"Successfully sent {name}")
    else:
        print(f"Failed to send the book {name}: {response.json()}")



for book in Books:
    try:
        book_name = os.path.splitext(book)[0]
        photo_res = send_photo(book, book_name)

        if photo_res.status_code == 200:
            id_to_reply = photo_res.json()['result']['message_id']
            send_document(book, book_name, id_to_reply)

        else:
            print(f"Failed to send the image for {book_name}: {photo_res.json()}")

    except Exception as err:
        print(f"An error occurred with book '{book}': {err}")
