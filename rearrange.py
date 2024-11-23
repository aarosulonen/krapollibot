import csv
from datetime import datetime

def sort_csv():
  # Read the CSV file
  with open('answers_data.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

  # Separate null and non-null entries
  null_entries = []
  non_null_entries = []
  
  for row in data:
    if row[3] == 'null':
      null_entries.append(row)
    else:
      non_null_entries.append(row)

  # Sort non-null entries by timestamp
  def get_timestamp(row):
    try:
      return datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
    except:
      return datetime.min

  sorted_non_null = sorted(non_null_entries, key=get_timestamp)
  
  # Combine reversed nulls with sorted non-null entries
  sorted_data = null_entries[::-1] + sorted_non_null

  # Write the sorted data back to the file
  with open('answers_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(sorted_data)

if __name__ == '__main__':
  sort_csv()