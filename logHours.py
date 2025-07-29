from datetime import datetime
import os

# Function to calculate the time difference between two hours
def calculate_difference_between_hours(start_hour: datetime, end_hour:datetime):
    format = "%H:%M"
    h1 = datetime.strptime(start_hour, format)
    h2 = datetime.strptime(end_hour, format)
    return h2 - h1

def calculate_day(file_name_of_day):
    print(file_name_of_day)
    return 1

def calculate_week(file_name_of_week):
    print(file_name_of_week)
    return 1

def analyze_time(file_name_to_analyze: str):
    # Make sure the file has one extra line
    with open(file_name_to_analyze, 'rb+') as file_descriptor:
        #Add newline if there is none
        file_descriptor.seek(-1, os.SEEK_END)
        if file_descriptor.read(1) != b"\n":
            file_descriptor.write(b"\n")

    # Read file and process lines
    results = {}
    descriptions = {}
    previous_hour = ""
    results = datetime.strptime("00:00", "%H:%M")
    with open(file_name_to_analyze, 'r+', encoding="utf8") as file_descriptor:
        for line in file_descriptor:
            description_aux = ""
            parts = line.strip().split()
            hours = []
            inside_parenthesis = 0
            for i in parts:
                if inside_parenthesis == 1:
                    if i[-1] == ')':
                        inside_parenthesis = 0
                        description_aux += " " + i[:-1]
                    else:
                        description_aux += " " + i
                elif i[0].isdigit() == True:
                    hours.append(i)
                elif i[0] == '(':
                    if i[-1] == ')':
                        description_aux = i[1:-1]
                    else:
                        description_aux = i[1:]
                        inside_parenthesis = 1
                else:
                    name_task = i
        
            if len(hours) == 1:
                hours.insert(0, previous_hour)

            previous_hour = hours[1]

            difference = calculate_difference_between_hours(hours[0], hours[1])
            results += difference
            if name_task in results:
                results[name_task] += difference
            else:
                results[name_task] = difference

            if (description_aux == ""):
                description_aux = "non-specified"

            if name_task not in descriptions:
                descriptions[name_task] = {}

            if description_aux in descriptions[name_task]:
                descriptions[name_task][description_aux] += difference.seconds
            else:
                descriptions[name_task][description_aux] = difference.seconds
    
    # Show results
    for name_task, difference in results.items():
        print(f"{name_task}: {difference}\n".encode("utf8"))
        if name_task in descriptions:
            for i in descriptions[name_task]:
                    print((f"   + {i}: {int(descriptions[name_task][i] / 3600)}h {int((descriptions[name_task][i] % 3600) / 60)}min\n".encode("utf8")))

    print(f"Total hours: {str(results.hour + ((results.day - 1) * 24))}h {str(results.minute)}mins")

    # Guardar los results en una lista
    lista_results = [(name_task, difference) for name_task, difference in results.items()]