import sqlite3
import os

def read_imessages_for_number(phone_number):
    # Path to the iMessage database
    db_path = os.path.expanduser('~/Library/Messages/chat.db')

    # Connecting to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to select messages from a specific chat
    query = """
    SELECT 
        m.text 
    FROM 
        message m
        JOIN chat_message_join cmj ON m.ROWID = cmj.message_id
        JOIN chat_handle_join chj ON cmj.chat_id = chj.chat_id
        JOIN handle h ON chj.handle_id = h.ROWID 
    WHERE 
        h.id = ? 
        AND 
        m.text IS NOT NULL 
        AND 
        (SELECT count(*) FROM chat_handle_join WHERE chat_id = cmj.chat_id) = 1
        AND
        m.is_from_me = 0
        AND
        m.associated_message_type = 0
    ORDER BY 
        m.date 
    DESC
    LIMIT 3
    """

    try:
        cursor.execute(query, (phone_number,))
        messages = cursor.fetchall()
        message_lst = [message[0] for message in messages][::-1]
        return message_lst
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def read_texts(number):
    return read_imessages_for_number('+' + str(number))
