import subprocess

def send_imessage(phone_number, message):
    apple_script = f'''
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{phone_number}" of targetService
        send "{message}" to targetBuddy
    end tell
    '''

    subprocess.run(["osascript", "-e", apple_script])


def send_sms(phone_number, message):
    apple_script = f'''
    tell application "Messages"
        set targetService to 1st service whose service type = SMS
        set targetBuddy to buddy "{phone_number}" of targetService
        send "{message}" to targetBuddy
    end tell
    '''

    subprocess.run(["osascript", "-e", apple_script])
