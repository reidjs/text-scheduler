# schedule-texts-from-txt
Schedule iMessage or SMS texts from `.txt` files from your Mac.

![a cute smiling mailbox](./mailbox.png)

# Send messages
1. Clone this repo to your computer.
2. Open `SETTINGS.txt` and replace the number after `myself=...` to **an iMessage capable phone number**. Replace the number after `sms_myself=...` to any working phone number.
3. Open your terminal to this project directory and run these commands in order
   1. `virtualenv venv`
   2. `source activate.sh` 
   3. `pip install -r requirements.txt`
   4. `python send_scheduled_messages.py`
4. 💬 If everything went well, you should receive an iMessage text that says "Hello from iMessage!", and an SMS text that says "Hello from SMS!"


# How it works
The script parses files in the `scheduled_messages` directory that follow this filename format: `Text {person} {datetime}.txt`. Every file with a `{datetime}` after your system's current datetime will be sent immediately*. You can change this directory in the SETTINGS.txt file. 
1. The first word in the filename must be `Text`.
2. The second word, `{person}` must be the persons identifier. This is set in SETTINGS.txt, e.g., `bob=1234567890` would set `bob`'s phone number to `1234567890`. If `{person}` starts with `sms_` like `sms_bob`, then the text will send via SMS. 
3. Everything following the name, before the .txt, is considered the `{datetime}`. Many formats may work, but this is the only one I have tested: `Month D, YYYY HH:MM(AM|PM)`, for example `March 9, 2024 7:25AM`. You can also use the keyword `now` or `asap` as a `datetime` to send texts immediately.
4. After a message is sent, it will move the message to the `sent` folder in your `scheduled_texts` directory. 

# Help & Feedback
Please create a GitHub issue if you have feedback or need help. Thanks! 

Made by Reid JS on March 9, 2024

*Will only send texts with `{datetime}` less than MAX_OVERTIME_MINS, 30 minutes by default. This is to prevent accidentally sending really old messages. For example, if you had this script running on a cron that failed then restarted a week later, you probably don't want those week-old messages to send. 

