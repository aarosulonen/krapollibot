from csv_util import read_poll_answers
from datetime import datetime, timedelta


def get_poll_answers_by_chat(chat_id):
    data = read_poll_answers()
    answers_by_poll = {} 
    
    for row in data:
        if row[0] == str(chat_id):
            poll_id = row[1]
            chosen_option = int(row[2])
            answer_timestamp = row[3]
            
            if poll_id not in answers_by_poll:
                answers_by_poll[poll_id] = []
            
            answers_by_poll[poll_id].append((chosen_option, answer_timestamp))
    
    return answers_by_poll

def calculate_average_first_non_zero(chat_id):
    answers_by_poll = get_poll_answers_by_chat(chat_id)
    first_non_zero_answers = []

    for id, answer_data in answers_by_poll.items():
      for option, timestamp in answer_data:
        if option != 0:
            first_non_zero_answers.append(answer_data[0][0])
            break

    if first_non_zero_answers:
        average = sum(first_non_zero_answers) / len(first_non_zero_answers)
        return round(average, 2)
    else:
        return None

def calculate_average_time_first_non_zero(chat_id):
    answers_by_poll = get_poll_answers_by_chat(chat_id)
    first_non_zero_times = []

    for poll_id, answers in answers_by_poll.items():
        for chosen_option, answer_timestamp in answers:
            if chosen_option != 0 and answer_timestamp != "null":
                timestamp = datetime.strptime(answer_timestamp, '%Y-%m-%d %H:%M:%S')
                time_in_seconds = timestamp.hour * 3600 + timestamp.minute * 60 + timestamp.second
                first_non_zero_times.append(time_in_seconds)
                break

    if first_non_zero_times:
        average_seconds = sum(first_non_zero_times) / len(first_non_zero_times)

        average_time = str(timedelta(seconds=int(average_seconds)))
        return average_time
    else:
        return None
      
def calculate_average_option_for_user(chat_id, user_id, username=None):
    data = read_poll_answers()
    total_option_value = 0
    count = 0

    for row in data:
        if row[0] == str(chat_id) and row[5] == str(user_id):  # Use user_id instead of username
            chosen_option = int(row[2])
            if chosen_option != 0:
                total_option_value += chosen_option
                count += 1

    if count > 0:
        average_option = total_option_value / count
        return (average_option, count)
    else:
        return (None, None)

#The last time a number 5 was answered
def last_5_krapula(chat_id):
    data = list(reversed(read_poll_answers()))
    
    for row in data:
        if row[0] == str(chat_id) and row[2] == "5":
            return (row[3], row[4])
    return (None, None)
    
def calculate_score_streak(chat_id, user_id, username=None):
    data = read_poll_answers()
    relevant_rows = [
        row for row in data
        if row[0] == str(chat_id) and row[5] == str(user_id) and int(row[2]) != 0 and row[3] != "null"
    ]
    
    dates = []
    for row in relevant_rows:
        date_str = row[3]
        current_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').date()
        if current_date not in dates:
            dates.append(current_date)

    dates.sort()
    
    if not dates:
        return (None, None)
    
    longest_streak = 1
    current_streak = 1
    best_segment = [dates[0]]
    current_segment = [dates[0]]

    for i in range(1, len(dates)):
        if (dates[i] - dates[i - 1]).days == 1:
            current_streak += 1
            current_segment.append(dates[i])
        else:
            if current_streak > longest_streak:
                longest_streak = current_streak
                best_segment = current_segment
            current_streak = 1
            current_segment = [dates[i]]

    if current_streak > longest_streak:
        longest_streak = current_streak
        best_segment = current_segment

    best_segment_str = [d.isoformat() for d in best_segment]

    return (longest_streak, best_segment_str)