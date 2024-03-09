# schedule-texts-from-txt
Schedule iMessage texts from `.txt` files on your computer.

![a cute smiling mailbox](./mailbox.png)

# Send your first text
1. Clone this repo to your computer.
3. Verify there is a file in example_scheduled_texts folder named `Text myself now.txt` that has the word "Hello!" in the file body.
4. Open `SETTINGS.txt` and replace the number after `myself=...` to **your phone number**.
5. Open your terminal to this project directory and run these commands in order
   1. `virtualenv venv`
   2. `source activate.sh` 
   3. `pip install -r requirements.txt`
   4. `python send_scheduled_messages.py`
6. ✅ If everything went well, you should receive an iMessage text that says "Hello!" from yourself 

# How it works
The script parses the filename, `Text {person} {datetime}.txt`, to determine who and when to send the text message. 
1. The first word in the filename must be "Text." 
2. The second word, `person` must be the persons identifier. This is set in SETTINGS.txt, e.g., `bob=1234567890` would set `bob`'s phone number to `1234567890`
3. Everything following the name, before the .txt, is considered the `datetime`. Many formats may work for the `datetime`, but this is the only one I have tested extensively: `Month D, YYYY HH:MM(AM|PM)`, for example `March 9, 2024 7:25AM`. You can also use the keyword `now` as a `datetime` to send one immediately.

# Help & Feedback
Please create a GitHub issue if you have feedback or need help. Thanks! 

Made by Reid JS on March 9, 2024
