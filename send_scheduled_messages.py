import os
import glob
import subprocess
from datetime import datetime
from dateutil import parser
import shutil
import re
from dotenv import dotenv_values

DOTENV_SETTINGS_PATH = "./SETTINGS.txt"
env_vars = dotenv_values(DOTENV_SETTINGS_PATH)


MAX_OVERTIME_MINS = int(env_vars["MAX_OVERTIME_MINS"])

DEBUG_TEXTING = env_vars["DEBUG_TEXTING"] == "True"

SCHEDULED_TEXTS_DIRECTORY = env_vars["SCHEDULED_TEXTS_DIRECTORY"]

# get only files starting with 'text' and ending in .txt or .md in the notes directory
TEXT_FILENAME_PATTERN = re.compile(r"^text.*\.(txt|md)$", re.IGNORECASE)
SEND_IMESSAGE_SCRIPT_PATH = "./send_imessage.applescript"
SEND_SMS_SCRIPT_PATH = "./send_sms.applescript"


def parse_human_datetime(human_datetime):
    if human_datetime == "now" or human_datetime == "asap":
        return datetime.now()
    return parser.parse(human_datetime)


def get_date_from_filename(filename):
    last_dot_index = filename.rfind(".")
    filename_without_extension = (
        filename[:last_dot_index] if last_dot_index != -1 else filename
    )
    parts = filename_without_extension.split(" ", 2)
    return " ".join(parts[2:])


def parse_datetime_from_filename(filename):
    human_datetime = get_date_from_filename(filename).lower()

    t = parse_human_datetime(human_datetime)

    return t


def file_ready_to_be_sent(filename):
    t = parse_datetime_from_filename(filename)
    now = datetime.now()
    dt_mins = abs((t - now).total_seconds() / 60)
    # t is earlier than now, and the diff
    return t < now and dt_mins <= MAX_OVERTIME_MINS


def move_file_to_sent_directory(file_path):
    dest_dir = f"{SCHEDULED_TEXTS_DIRECTORY}/sent"
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    shutil.move(file_path, dest_dir)


def parse_recipient_from_filename(filename):
    return filename.split()[1].lower()


def get_recipient_number_from_filename(contact_name):
    try:
        return env_vars[contact_name].lower()
    except KeyError:
        raise ValueError(
            f"Error: contact name '{contact_name}' not declared in settings file."
        )


def is_sms_recipient(recipient):
    return recipient.split("_")[0] == "sms"


def send_message(file):
    contact_name = parse_recipient_from_filename(file.name)
    recipient = get_recipient_number_from_filename(contact_name)
    message = file.read()
    if DEBUG_TEXTING:
        print(f"DEBUG TEXTING MODE: Would send {recipient}: {message}")
        move_file_to_sent_directory(file.name)
        return

    if is_sms_recipient(contact_name):
        try:
            subprocess.run(
                ["osascript", SEND_SMS_SCRIPT_PATH, recipient, message], check=True
            )
            move_file_to_sent_directory(file.name)
        except subprocess.CalledProcessError as e:
            print("error sending SMS:", e)
    else:
        try:
            subprocess.run(
                ["osascript", SEND_IMESSAGE_SCRIPT_PATH, recipient, message], check=True
            )
            move_file_to_sent_directory(file.name)
        except subprocess.CalledProcessError as e:
            print("error sending iMessage:", e)


def send_messages(directory):
    files = []
    for file_path in glob.glob(os.path.join(directory, "*")):
        filename = os.path.basename(file_path)
        if TEXT_FILENAME_PATTERN.match(filename) and file_ready_to_be_sent(filename):
            with open(file_path, "r", encoding="utf-8") as file:
                send_message(file)

    return files


if __name__ == "__main__":
    send_messages(SCHEDULED_TEXTS_DIRECTORY)
