#Author: W Y M Perera
#Date: 28/11/2024
#Student ID: 20240091/W2120552


import csv

def is_leap_year(year): #function to check if its a leap year
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) #returns True if its a leap year 

# Task A: Input Validation
def validate_date_input(): #function to get and validate date, month and year

    while True:
        try:
            day = int(input("Please enter the day of the survey in the format dd: ").strip()) #prompts user to input the date
            if day>=1 and day<=31: #checks if the range is right
                break #breaks the loop since both conditions are satisfied 
            else:
                    print("Out of range - values must be in the range 1 and 31.") #error message displayed when the input is out of range
        except ValueError:
            print("Integer required") #error message displayed when the input is not a integer value.

    while True:
        try:
            month = int(input("Please enter the month of the survey in the format MM: ").strip()) #prompts user to input month
            if month>=1 and month<=12: #checks if the range is right
                break #breaks the loop since both conditions are satisfied 
            else:
                print("Out of range - values must be in the range 1 to 12.") #error message displayed when the input is out of range
        except ValueError:
            print("Integer required") #error message displayed when the input is not a integer value.

    while True:
        try:
            year = int(input("Please enter the year of the survey in the format YYYY: ").strip()) #prompts user to input year
            if year>=2000 and year<=2024: #checks if the range is right
                break #breaks the loop since both conditions are satisfied 
            else: 
                print("Out of range - values must range from 2000 and 2024.")  #error message displayed when the input is out of range
        except ValueError: 
            print("Integer required") #error message displayed when the input is not a integer value.

    if month == 2: #validates the day in February
        if is_leap_year(year):
            if day > 29:
                print(f"Invalid day for February in a leap year.") #error for when day is out of range when its a leap year
                validate_date_input() #calls function to get input again
        else:
            if day > 28:
                print("Invalid day for February in a non-leap year.") #error for when day is out of range when its not a leap year
                validate_date_input() #calls function to get input again
    elif month in [4, 6, 9, 11] and day > 30: #checks if day exceeds 30 in 4th, 6th, 9th or 11th months
        print("Invalid day for the selected month.") #error message when day is invalid 
        validate_date_input() #calls function to get input again
        
    return day, month, year #returns the valid values.
 

def validate_continue_input(): #function to select another file and loop until user inputs "N"
    
    while True:
        option = input("Do you want to select another data file for a different date? Y/N > ").strip().upper() #get option from user
        #.strip() removes spaces
        #.upper() converts to uppercase

        if option == "Y": 
            main() #calls main function (because it needs to loop) if user inputs "Y"
            break 
        elif option == "N":
            print("End of run") #prints message if user inputs "N"
            break
        else:
            print('Please enter "Y" or "N" ') #error message when input is not "Y" or "N"



# Task B: Processed Outcomes
def process_csv_data(file_path): #function to process csv file

    try: #try to open the csv file
        with open(file_path, 'r') as file: #opens the csv file with read permissions
            reader = csv.DictReader(file) #uses the csv library to read the csv file as a dictionary and assign to object reader

            total_vehicles = 0 #counter for total vehicles
            total_trucks = 0 #counter for total trucks
            total_ev = 0 #counter for total electric vehicles
            total_two_wheeled_vehicles = 0 #counter for two wheeled vehicles 
            buses_leaving_elm_north = 0 #counter for buses leaving Elm Avenue/Rabbit Road traveling north
            vehicles_not_turning = 0 #counter for vehicles that are not turning 
            total_bicycles = 0 #counter fr total bicycles
            vehicles_over_speed_limit = 0 #counter for vehicles exceeding speed limit
            vehicles_elm = 0 #counter for vehicles leaving Elm Avenue/Rabbit Road 
            vehicles_hanley = 0 #counter for vehicles leaving Hanley Highway/Westway
            total_scooters_elm = 0 #counter for scooters leaving Elm Avenue/Rabbit Road
            temp_time = 0 #variable to help count the number of vehicles passing through Hanley Highway/Westway in an hour
            temp_vehicles_hanley_per_hour = 0 #temporary variable to hold vehicles passing through Hanley Highway/Westway in the hour
            list_max_per_hour_hanley = [] #list of vehicles passing through Hanley Highway/Westway on a hourly basis
            hours_of_rain = set() #set to count hours of rain
            outcomes = [] #list of all processed values
            peak_traffic_hours_hanley_index = []


            for row in reader:
                total_vehicles += 1 #increment for total vehicles 
                if row["VehicleType"] == "Truck":
                    total_trucks += 1 #increment for trucks 
                if row["elctricHybrid"] == "True":
                    total_ev += 1 #increment for electric vehicles
                if row["VehicleType"] == "Bicycle" or row["VehicleType"] == "Motorcycle" or row["VehicleType"] == "Scooter":
                    total_two_wheeled_vehicles += 1 #increment for two wheeled vehicles
                if row["VehicleType"] == "Buss" and row["JunctionName"] == "Elm Avenue/Rabbit Road" and row["travel_Direction_out"] == "N":
                    buses_leaving_elm_north += 1 #increment for busses leaving Elm Avenue/Rabbit Road heading north
                if row["travel_Direction_in"] == row["travel_Direction_out"]:
                    vehicles_not_turning += 1 #increment for vehicles not turning 
                if row["VehicleType"] == "Bicycle":
                    total_bicycles += 1 #increment for bicycles
                if int(row["VehicleSpeed"]) > int(row["JunctionSpeedLimit"]):
                    vehicles_over_speed_limit += 1 #increment for vehicles exceeding speed limit
                if row["JunctionName"] == "Elm Avenue/Rabbit Road":
                    vehicles_elm += 1 #increment for vehicles leaving Elm Avenue/Rabbit Road
                    if row["VehicleType"] == "Scooter":
                        total_scooters_elm += 1 #increment for scooters leaving Elm Avenue/Rabbit Road
                if row["JunctionName"] == "Hanley Highway/Westway":
                    vehicles_hanley += 1 #increment for vehicles leaving Hanley Highway/Westway

                if row["Weather_Conditions"] == "Heavy Rain" or  row["Weather_Conditions"] == "Light Rain": 
                    hours_of_rain.add(int(row["timeOfDay"][:2])) #adds the hour part of timeOfDay as a integer to the hours_of_rain set if rain is in weather conditions.

                int_time_of_day = int(row["timeOfDay"][:2]) #converts the hour part of timeOfDay to integer

                if not row["JunctionName"] == "Hanley Highway/Westway":
                    continue #skips the iteration if the vehicle is not passing through Hanley Highway/Westway
                else:
                    if int_time_of_day == temp_time: #if the temp time is equal to he current time of the day, 
                        temp_vehicles_hanley_per_hour += 1 #adds 1 to vehicles passing through Hanley Highway/Westway in that hour
                    else:
                        temp_time = int(row["timeOfDay"][:2]) #if the temp time is not equal to he current time of the day,
                        list_max_per_hour_hanley.append(temp_vehicles_hanley_per_hour) #appends the number of vehicles to this list  
                        temp_vehicles_hanley_per_hour = 1 #resets the counter to 1 
                

            max_vehicles_per_hour_hanley = max(list_max_per_hour_hanley) #assigns the maximam value in the list to the max_vehicles_per_hour_hanley variable        

            for index, count in enumerate(list_max_per_hour_hanley): #get index and the vehicle count
                if count == max_vehicles_per_hour_hanley: #checks if the vehicle count is equal to max vehicles on hanley
                    peak_traffic_hours_hanley_index.append(index) #appends the index of the value to the index list

            percentage_trucks = (total_trucks/total_vehicles)*100 #calculate percentage of trucks
            avg_bicycles_per_hour = total_bicycles/24 #calulate bicycles per hour
            percentage_scooters_elm = (total_scooters_elm/vehicles_elm)*100 #percentage of scooters passing through Elm Avenue/Rabbit Road
            peak_traffic_hours_hanley = ", ".join(f"{hour:02d}.00 to {hour + 1:02d}.00" for hour in peak_traffic_hours_hanley_index) #convert to the format 00:00 to 01:00

            outcomes = [ #assign processed values to the outcomes list
                file_path, #0
                total_vehicles, #1
                total_trucks, #2
                total_ev, #3
                total_two_wheeled_vehicles, #4
                buses_leaving_elm_north, #5
                vehicles_not_turning, #6
                percentage_trucks, #7
                avg_bicycles_per_hour, #8
                vehicles_over_speed_limit, #9
                vehicles_elm, #10
                vehicles_hanley, #11
                percentage_scooters_elm, #12
                max_vehicles_per_hour_hanley, #13
                peak_traffic_hours_hanley, #14
                len(hours_of_rain) #15
            ]

        display_outcomes(outcomes) #calling function to display values in the shell
        save_results_to_file(outcomes) #calling the function to save results to file
        validate_continue_input() #calling function to select another file

    except FileNotFoundError:
         print(f"{file_path} file not found.") #sends error message if file is not found
         validate_continue_input() #asks the user if they want to select another date after the file not found error.
         

def display_outcomes(outcomes): #function to display outcomes from the csv file

    print(f"""
***************************          
data file selected is {outcomes[0]}
*************************** 
The total number of vehicles recorded for this date is {outcomes[1]}
The total number of trucks recorded for this date is {outcomes[2]}
The total number of electric vehicles for this date is {outcomes[3]}
The total number of two-wheeled vehicles for this date is {outcomes[4]}
The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes[5]}
The total number of Vehicles through both junctions not turning left or right is {outcomes[6]}
The percentage of total vehicles recorded that are trucks for this date is {round(outcomes[7])}%
The average number of Bikes per hour for this date is {round(outcomes[8])}

The total number of Vehicles recorded as over the speed limit for this date is {outcomes[9]}
The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes[10]}
The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes[11]}
{int(outcomes[12])}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters 

The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes[13]}
The most vehicles through Hanley Highway/Westway were recorded between {outcomes[14]}
The number of hours of rain for this date is {outcomes[15]}
""")


# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name="results.txt"): #function to store outcomes from the csv file to the text file, results.txt

    with open(file_name, 'a') as file: #open the file results.txt with append permissions, creates a file is it does not exist

        #assign the output to a varible data to write to file
        data = f"""data file selected is {outcomes[0]} 
The total number of vehicles recorded for this date is {outcomes[1]}
The total number of trucks recorded for this date is {outcomes[2]}
The total number of electric vehicles for this date is {outcomes[3]}
The total number of two-wheeled vehicles for this date is {outcomes[4]}
The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes[5]}
The total number of Vehicles through both junctions not turning left or right is {outcomes[6]}
The percentage of total vehicles recorded that are trucks for this date is {round(outcomes[7])}%
The average number of Bikes per hour for this date is {round(outcomes[8])}

The total number of Vehicles recorded as over the speed limit for this date is {outcomes[9]}
The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes[10]}
The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes[11]}
{int(outcomes[12])}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters 

The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes[13]}
The most vehicles through Hanley Highway/Westway were recorded between {outcomes[14]}
The number of hours of rain for this date is {outcomes[15]}

****************************

"""
        file.write(data) #write to file


def main(): #main function marks the start of the program and to help loop the proram
    day, month, year = validate_date_input() #get the day, month and year to globle variables
    day = str(day).zfill(2) #convert day to string and make it in 00 format
    month = str(month).zfill(2) #convert month to string and make it 00 format
    year = str(year) #convert year to string
    file_path = f"traffic_data{day}{month}{year}.csv" #make the file path
    process_csv_data(file_path) #calling the function to process the csv file


main() #calling the main funtion 