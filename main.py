import random
import smtplib
import datetime as dt
import pandas
from dotenv import load_dotenv
import os


def send_email(to_email, body):
    load_dotenv()
    my_email = os.getenv("my_email")
    password = os.getenv("password")
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=to_email,
            msg=f"Subject: Happy Birthday!\n\n  {body}")


# 1. Update the birthdays.csv
def update_birthdays():
    new_dict = {
        "name": ["Aaron", "Tori", "Bentley", "Tucker", "Minnie Mouse"],
        "email": ["aboyles05@gmail.com", "aboyles05@gmail.com", "aboyles05@gmail.com", "aboyles05@gmail.com",
                  "aboyles05@gmail.com"],
        "year": [1990, 1994, 2016, 2016, 2019],
        "month": [10, 9, 1, 2, 12],
        "day": [15, 25, 6, 14, 29]
    }
    new_frame = pandas.DataFrame(new_dict)
    new_frame.to_csv("birthdays.csv", mode="a", index=False, header=False)


# 2. Check if today matches a birthday in the birthdays.csv
data = pandas.read_csv("birthdays.csv")
now = dt.datetime.now()
month = now.month
day = now.day
current_birthdays = data[(data["month"] == month) & (data["day"] == day)]
birthday_dict = {data_row["name"]: data_row.email for (index, data_row) in current_birthdays.iterrows()}
PLACEHOLDER = "[NAME]"
for person in birthday_dict:
    # create birthday letters
    random_num = random.randint(1, 3)
    with open(f"letter_templates/letter_{random_num}.txt") as letter:
        letter_content = letter.read()
        birthday_letter = letter_content.replace(PLACEHOLDER, person)
    # Send the letter generated in step 3 to that person's email address.
    send_email(to_email=birthday_dict.get(person), body=birthday_letter)

