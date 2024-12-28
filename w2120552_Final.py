#Author: W Y M Perera
#Date: 20/12/2024
#Student ID: W2120552


import csv
from graphics import *


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
            MultiCSVProcessor().process_files() #calls main function (because it needs to loop) if user inputs "Y"
            return 
        elif option == "N":
            print("End of run") #prints message if user inputs "N"
            return
        else:
            print('Please enter "Y" or "N" ') #error message when input is not "Y" or "N"



# Task B: Processed Outcomes
def process_csv_data(file_path, date): #function to process csv file

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
            temp_time_hanley = 0
            temp_time_elm = 0 #variable to help count the number of vehicles passing through Hanley Highway/Westway in an hour
            temp_vehicles_hanley_per_hour = 0 #temporary variable to hold vehicles passing through Hanley Highway/Westway in the hour
            temp_vehicles_elm_per_hour = 0
            list_max_per_hour_hanley = [] #list of vehicles passing through Hanley Highway/Westway on a hourly basis
            list_max_per_hour_elm = []
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
                    if int_time_of_day == temp_time_elm: #if the temp time is equal to he current time of the day, 
                        temp_vehicles_elm_per_hour += 1 #adds 1 to vehicles passing through Hanley Highway/Westway in that hour
                    else:
                        temp_time_elm = int(row["timeOfDay"][:2]) #if the temp time is not equal to he current time of the day,
                        list_max_per_hour_elm.append(temp_vehicles_elm_per_hour) #appends the number of vehicles to this list  
                        temp_vehicles_elm_per_hour = 1 #resets the counter to 1 
                else:
                    if int_time_of_day == temp_time_hanley: #if the temp time is equal to he current time of the day, 
                        temp_vehicles_hanley_per_hour += 1 #adds 1 to vehicles passing through Hanley Highway/Westway in that hour
                    else:
                        temp_time_hanley = int(row["timeOfDay"][:2]) #if the temp time is not equal to he current time of the day,
                        list_max_per_hour_hanley.append(temp_vehicles_hanley_per_hour) #appends the number of vehicles to this list  
                        temp_vehicles_hanley_per_hour = 1 #resets the counter to 1

                
                
                
            list_max_per_hour_hanley.append(temp_vehicles_hanley_per_hour) #appending 23rd hour
            list_max_per_hour_elm.append(temp_vehicles_elm_per_hour) #appending 23rd hour
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
                len(hours_of_rain), #15
            ]

        display_outcomes(outcomes) #calling function to display values in the shell
        save_results_to_file(outcomes) #calling the function to save results to file
        traffic_data = {
            "Elm Avenue/Rabbit Road": list_max_per_hour_elm,
            "Hanley Highway/Westway": list_max_per_hour_hanley
        }
        app = HistogramApp(traffic_data, date)
        app.run()
        

    except FileNotFoundError:
         print(f"{file_path} file not found.") #sends error message if file is not found
         
         

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


# Task D: Histogram Display
class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.width = 1250 #width of the window
        self.height = 500 #height of the window
        self.color = [color_rgb(255,0,0),color_rgb(0,0,255)] 


    def setup_window(self):
        """
        Sets up the graphics.py window and canvas for the histogram.
        """
        self.window = GraphWin("Histogram",self.width,self.height) #setting up the window

        #setting up the heading 
        heading = Text(Point(300,25), f"Histrogram of Vehicle Frequency per Hour ({self.date})") 
        heading.setStyle("bold")
        heading.setSize(14)
        heading.draw(self.window)
        

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """

        #drawing the x axis line
        x_axis = Line(Point(50,self.height-65), Point(self.width-55, self.height-65))
        x_axis.draw(self.window)

        #naming the x axis
        x_name = Text(Point(625,self.height-25), "Hours 00:00 to 24:00")
        x_name.setStyle("bold")
        x_name.setSize(11)
        x_name.draw(self.window)

        #marking the x coordinates on the x axis
        for hour in range(24):
            x_label = Text(Point(80+(hour*47), self.height-50), f"{hour:02}")
            x_label.setSize(9)
            x_label.draw(self.window)

        #getting the junction names from the traffic data dictionary
        junctions = list(self.traffic_data.keys()) 

        #getting the highest data value between both lists of data in traffic data dictionary 
        highest_volume = 0  
        for data in self.traffic_data.values():
            if max(data) > highest_volume:
                highest_volume = max(data)

        junction_name = 1
        
        for juncion in junctions:

            data = self.traffic_data[juncion]
            width = 20 #width of the bars

            if junction_name == 1:
                for i in range(len(data)):
                    
                    #getting x and y coordinates of Elm Avenue/Rabbit Road bars
                    x1 = 50+((i*47)+11)
                    x2 = x1 + width
                    y1 = self.height - 65
                    y2 = y1 - (data[i]/highest_volume)*280

                    #drawing the bars of Elm Avenue/Rabbit Road
                    bar = Rectangle(Point(x1,y1),Point(x2,y2))
                    bar.setFill(self.color[0])
                    bar.draw(self.window)

                    #labeling the Elm Avenue/Rabbit Road bars
                    bar_label = Text(Point((x1+x2)/2,y2-5),f"{data[i]}")
                    bar_label.setSize(7)
                    bar_label.setFill(self.color[0])
                    bar_label.setStyle("bold")
                    bar_label.draw(self.window)

            else:

                for i in range(len(data)):

                    #getting x and y coordinates of Hanley Highway/Westway bars
                    x1 = (50+width)+((i*47)+11)
                    x2 = x1 + width
                    y1 = self.height - 65
                    y2 = y1 - (data[i]/highest_volume)*280

                    #drawing the bars of Hanley Highway/Westway
                    bar = Rectangle(Point(x1,y1),Point(x2,y2))
                    bar.setFill(self.color[1])
                    bar.draw(self.window)

                    #labeling the Hanley Highway/Westway bars
                    bar_label = Text(Point((x1+x2)/2,y2-5),f"{data[i]}")
                    bar_label.setSize(7)
                    bar_label.setFill(self.color[1])
                    bar_label.setStyle("bold")
                    bar_label.draw(self.window)

            junction_name +=1        


    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        legend_w_and_h = 15 #height and width of legend boxes

        #legend of Elm Avenue/Rabbit Road
        legend_elm= Rectangle(Point(65,65),Point(65+legend_w_and_h, 65-legend_w_and_h))
        legend_elm.setFill(self.color[0])
        legend_elm.draw(self.window)

        legend_label_elm=Text(Point(175,60), "Elm Avenue/Rabbit Road")
        legend_label_elm.draw(self.window)
        
        #legend of Hanley Highway/Westway
        legend_hanley= Rectangle(Point(65,85),Point(65+legend_w_and_h, 85-legend_w_and_h))
        legend_hanley.setFill(self.color[1])
        legend_hanley.draw(self.window)

        legend_label_hanley=Text(Point(175,80), "Hanley Highway/Westway")
        legend_label_hanley.draw(self.window)


    def run(self):
        """
        Runs the graphics.py main loop to display the histogram.
        """
        self.setup_window()
        self.draw_histogram() 
        self.add_legend()
        
        #try to avoid the close error that occurs with getMouse
        try: 
            self.window.getMouse()
        except Exception:
            pass
        finally:
            self.window.close()


# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.day = 0
        self.month = 0
        self.year = 0
        self.file_path = 0
        self.date = 0


    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        process_csv_data(file_path, self.date) 
        

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.day = 0
        self.month = 0
        self.year = 0
        self.file_path = 0
        self.date = 0
        

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        validate_continue_input() 
        

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        self.clear_previous_data()
        self.day, self.month, self.year = validate_date_input() #get the day, month and year to globle variables
        self.day = str(self.day).zfill(2) #convert day to string and make it in 00 format
        self.month = str(self.month).zfill(2) #convert month to string and make it 00 format
        self.year = str(self.year) #convert year to string
        self.file_path = f"traffic_data{self.day}{self.month}{self.year}.csv" #make the file path
        self.date = f"{self.day}/{self.month}/{self.year}"
        self.load_csv_file(self.file_path)
        self.handle_user_interaction()
        

MultiCSVProcessor().process_files() #calling the main function 



