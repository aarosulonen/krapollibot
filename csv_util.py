import csv

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