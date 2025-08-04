#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path
import sys
import os

# Function to calculate the time difference between two hours
def calculate_difference_between_hours(start_hour: datetime, end_hour:datetime):
    format = "%H:%M"
    h1 = datetime.strptime(start_hour, format)
    h2 = datetime.strptime(end_hour, format)
    return h2 - h1

def calculate_day(file_name_of_day):
    # If file doesn't exist create it and that's it
    if (os.path.isfile(file_name_of_day) == False):
        print("File of that day doesn't exist, creating one ...")
        with open(file_name_of_day, 'x') as file_descriptor:
            file_descriptor.write("\n")
        print("File created:", file_name_of_day)
        return 1
    
    # If file exists analyze it
    analyze_time(file_name_of_day)
    return 1

def calculate_week():
    sourceDir = Path("./")

    aux_week_file_name = "esta_semana.txt"
    with open(aux_week_file_name, "w") as aux_week_file:
        for file_path in sourceDir.glob("*-*-*.txt"):
            print(file_path)
            with open(file_path, "r") as infile:
                aux_week_file.write(infile.read())
    
    calculate_day(aux_week_file_name)

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
    result = datetime.strptime("00:00", "%H:%M")
    with open(file_name_to_analyze, 'r', encoding="utf8") as file_descriptor:
        for index, line in enumerate(file_descriptor):
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

            # If there's only one hour at that line, use the finish hour of the previous line
            if len(hours) == 1:
                hours.insert(0, previous_hour)
            
            # If there's no hour at that line, there's an error
            elif len(hours) == 0:
                print("Error on file:", file_name_to_analyze)
                print("On line:", file_name_to_analyze)

            previous_hour = hours[1]

            difference = calculate_difference_between_hours(hours[0], hours[1])
            result += difference
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
        print(f"{name_task}: {difference}")
        if name_task in descriptions:
            for i in descriptions[name_task]:
                    print((f"   + {i}: {int(descriptions[name_task][i] / 3600)}h {int((descriptions[name_task][i] % 3600) / 60)}min"))

    print(f"Total hours: {str(result.hour + ((result.day - 1) * 24))}h {str(result.minute)}mins")

    # Guardar los results en una lista
    lista_results = [(name_task, difference) for name_task, difference in results.items()]

def main():
    try:
        # Calculate day operation
        calculate_day_command = "-cd"
        if ((calculate_day_command in sys.argv) or ("--calculate-day" in sys.argv)):
            calculate_day_command_index = sys.argv.index(calculate_day_command)
            # If no file of the day given, then use the filename of that day
            if (len(sys.argv) == calculate_day_command_index + 1):
                calculate_day(datetime.now().strftime("%d-%m-%Y.txt"))
            else:
                calculate_day(sys.argv[calculate_day_command_index + 1])
            
        # Calculate week operation
        calculate_week_command = "-cw"
        if ((calculate_week_command in sys.argv) or ("--calculate-week" in sys.argv)):
            calculate_week()
    except:
        print("Error at processing request")

if __name__ == "__main__":
    main()