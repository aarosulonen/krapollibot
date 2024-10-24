import csv

ANSWER_FILE = 'answers_data.csv'

def read_registered_groups(csv_filename='registered_groups.csv'):
    registered_groups = set()
    try:
        with open(csv_filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 1:
                    registered_groups.add(int(row[0]))
    except FileNotFoundError:
        pass
    return registered_groups
  
def write_registered_group(chat_id, csv_filename='registered_groups.csv'):
    registered_groups = read_registered_groups(csv_filename)
    if chat_id not in registered_groups:
        registered_groups.add(chat_id)
        with open(csv_filename, mode='a', newline='') as file: 
            writer = csv.writer(file)
            writer.writerow([chat_id])

def read_last_poll_ids(csv_filename='last_polls.csv'):
    last_polls = {}
    try:
        with open(csv_filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    last_polls[int(row[0])] = int(row[1])
    except FileNotFoundError:
        pass
    return last_polls

def write_last_poll_id(chat_id, message_id, csv_filename='last_polls.csv'):
    last_polls = read_last_poll_ids(csv_filename)
    last_polls[chat_id] = message_id
    
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for chat, msg_id in last_polls.items():
            writer.writerow([chat, msg_id])

def overwrite_registered_groups(groups, csv_filename='registered_groups.csv'):
  with open(csv_filename, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        for group_id in groups:
            csv_writer.writerow([group_id])
            
def store_poll_id_to_chat_id(poll_id, chat_id):
    data = []

    try:
        with open('poll_id_to_chat_id.csv', mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
    except FileNotFoundError:
        pass

    updated = False
    for row in data:
        if row[1] == str(chat_id):
            row[0] = poll_id
            updated = True
            break

    if not updated:
        data.append([poll_id, chat_id])

    with open('poll_id_to_chat_id.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def get_chat_id_from_poll_id(poll_id):
    try:
        with open('poll_id_to_chat_id.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == poll_id:
                    return row[1]
    except FileNotFoundError:
        print("CSV file not found.")
    return None

def store_poll_answer(poll_id, chat_id, chosen_option, answer_timestamp, username):
    data = read_poll_answers()
    
    updated = False
    for row in data:
        if row[0] == str(chat_id) and row[1] == str(poll_id) and row[4] == username:
            row[2] = chosen_option
            row[3] = answer_timestamp  
            updated = True
            break

    if not updated:
        data.append([chat_id, poll_id, chosen_option, answer_timestamp, username])

    with open(ANSWER_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        
def read_poll_answers():
    data = []
    try:
        with open(ANSWER_FILE, mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
    except FileNotFoundError:
        pass
    return list(reversed(data))

def groupid_in_file(group_id, csv_filename='last_polls.csv') -> bool:
    last_polls = read_last_poll_ids(csv_filename)
    return group_id in last_polls

def delete_closed_poll_data(csv_filename='last_polls.csv'):
    with open(csv_filename, mode='w', newline='') as file:
        pass