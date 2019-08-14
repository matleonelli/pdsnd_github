#!/usr/bin/env python3

import time
import pandas as pd
import numpy as np

# loading files
CITY_DATA = {
    'chicago':'/Users/leonellm/Documents/Udacity/version-control/chicago.csv',
    'new york city':'/Users/leonellm/Documents/Udacity/version-control/new_york_city.csv',
    'washington':'/Users/leonellm/Documents/Udacity/version-control/washington.csv'
}

def get_city():
    '''
    This function asks the user for a city to analyze
    '''
    print('Let\'s explore some US bikeshare data!')
    print(' ')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Would you like to see data for Chicago, New York, or Washington?\n')
    print(' ')
    city = input('Please choose the city for which you would like to see the Statistics: ')
    city = city.lower()
    while True:     # for handling the unexpected input by user
            if city == 'chicago':
                print("\nChicago! Okay Let's go further\n")
                return 'chicago'
            elif city == 'new york':
                print("\nNew York City! Okay let's go further\n")
                return 'new york city'
            elif city == 'washington':
                print("\nWashington! Okay let's go further\n")
                return 'washington'
            # error handled by implementing 'else' and provided another option to input data
            else:
                print('\nInput incorrect, please enter the name of a city.\n')
                city = input('Please choose the city for which you would like to see the Statistics: ')
                city = city.lower()
    return city

def get_time_filter():
    '''
    This function asks the user to choose between month and day of month,
    day of the week or no filters at all
    '''
    time_filter = input('\nDo you want to filter the data by "month" and day of the month, or "day" of the week, or you do not want to filter at all? Type "no" for no filter.\n')
    time_filter = time_filter.lower()

    while True:
        if time_filter == "month":
            while True:
                day_month = input("\nDo you want to filter the data by the day of the month too? Type 'YES' or 'NO'\n").lower()
                if day_month == "no":
                    print('\nThe data is now being filtered by month.\n')
                    return 'month'
                elif day_month == "yes":
                   print ('\nThe data is now being filtered by month and day of the month.\n')
                   return 'day_of_month'

        if time_filter == "day":
            print('\nThe data is now being filtered by the day of the week.\n')
            return 'day_of_week'
        elif time_filter == "no":
            print('\nNo time_filter filter is being applied to the data\n')
            return "none"
        time_filter = input("\nPlease choose a time_filter filter option between 'month', 'day' of the week, or none (no)\n").lower()

def get_month(m):      # get user input for month (all, january, february, ... , june)
    if m == 'month':
        month = input('\nChoose the month! January, February, March, April, May, or June? Please type the full month name.\n')
        while month.strip().lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input('\nPlease choose between January, February, March, April, May, or June? Please type the full month name.\n')
        return month.strip().lower()
    else:
        return 'none'

def get_day_of_month(df, day_m):     # Asks the user for a month and a day of month,
    day_of_month = []
    if day_m == "day_of_month":
        month = get_month("month")
        day_of_month.append(month)
        maximum_day_month = most_common_day_month(df, month)

        while (True):
            ask = """ \n Which day of the month? \n
            Please type your response as an integer between 1 and """
            ask  = ask + str(maximum_day_month) + "\n"
            day_m = input(ask)

            try:
                day_m = int(day_m)
                if 1 <= day_m <= maximum_day_month:
                    day_of_month.append(day_m)
                    return day_of_month
            except ValueError:
                print("That's not a correct value")
    else:
        return 'none'

def get_day(d):       # Asks the user for a day and returns the specified day
    if d == 'day_of_week':
        day = input('\nWhich day? Please type a day M, Tu, W, Th, F, Sa, Su. \n')
        while day.lower().strip() not in ['m', 'tu', 'w', 'th', 'f', 'sa', 'su']:
            day = input('\nPlease type a day as a choice from M, Tu, W, Th, F, Sa, Su. \n')
        return day.lower().strip()
    else:
        return 'none'

def load_data(city):
    # Loads data for the specified city
    print('\nLoading the data... .. .. ..\n')
    df = pd.read_csv(CITY_DATA[city])

    #extracting from Start Time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    df["day_of_month"] = df["Start Time"].dt.day
    return df

def time_filters(df, time, month, week_day, md):
    '''
    Filters the data according to the criteria specified by the user.
    Local Variables:
    df         - city dataframe
    time       - indicates the specified time (either "month", "day_of_month", or "day_of_week")
    month      - indicates the month used to filter the data
    week_day   - indicates the week day used to filter the data
    md         - list that indicates the month (at index [0]) used to filter the data
                    and the day number (at index [1])
    Result:
    df - dataframe to be used for final calculation
    '''
    print('Data loaded. Now computing statistics... \n')
    #Filter by Month
    if time == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #Filter by day of week
    if time == 'day_of_week':
        days = ['Monday', 'Tuesday',
        'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday']
        for d in days:
            if week_day.capitalize() in d:
                day_of_week = d
        df = df[df['day_of_week'] == day_of_week]

    if time == "day_of_month":
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = md[0]
        month = months.index(month) + 1
        df = df[df['month']==month]
        day = md[1]
        df = df[df['day_of_month'] == day]

    return df

def most_common_day_month(df, month):
    '''Gets the most common day of the month '''

    months = {"january": 1, "february": 2, "march": 3, "april":4, "may": 5, "june":6}
    df = df[df["month"] == months[month]]
    max_day = max(df["day_of_month"])
    return max_day

def most_common_month(df):
    '''What is the most common month for start time?
    '''
    # df - dataframe returned from time_filters
    print('\n * Q1. What is the most popular month for bike traveling?')
    m = df.month.mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[m - 1].capitalize()
    return popular_month

def most_common_day_week(df):
    '''What is the most common day of week for start time?
    '''
    # df - dataframe returned from time_filters
    print('\n * Q2. What is the most popular day of the week for bike rides?')
    return df['day_of_week'].value_counts().reset_index()['index'][0]

def most_common_start_hour(df):
    '''What is the most common hour of day for start time?
    '''
    # df - dataframe returned from time_filters
    print('\n * Q3. What is the most popular hour of the day for bike rides?')
    df['hour'] = df['Start Time'].dt.hour
    return df.hour.mode()[0]

def ride_duration_avg_total(df):
    '''
    What is the total ride duration and average ride duration?
    '''
    # df - dataframe returned from time_filters
    print('\n * Q4. What was the total traveling done for 2017 through June, and what was the average time spent on each trip?')
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    #sum for total trip time, mean for avg trip time
    total_ride_time = np.sum(df['Travel Time'])
    total_days = str(total_ride_time).split()[0]

    print ("\nThe total travel time on 2017 through June was " + total_days + " days \n")
    avg_ride_time = np.mean(df['Travel Time'])
    avg_days = str(avg_ride_time).split()[0]
    print("The average travel time on 2017 through June was " + avg_days + " days \n")

    return total_ride_time, avg_ride_time

def most_common_station(df):
    '''What is the most common start station and most popular end station?
    '''
    # df - dataframe returned from time_filters
    print("\n* Q5. What is the most popular start station?\n")
    start_station = df['Start Station'].value_counts().reset_index()['index'][0]
    print (start_station)
    print("\n* Q6. What is the most popular end station?\n")
    end_station = df['End Station'].value_counts().reset_index()['index'][0]
    print(end_station)
    return start_station, end_station

def most_common_trip(df):
    '''What is the most common trip?
    '''
    # df - dataframe returned from time_filters
    result = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\n* Q7. What was the most popular trip from start to end?')
    return result

def count_user_type(df):
    '''What are the counts of each user type?
    '''
     # df - dataframe returned from time_filters
    print('\n* Q8. Types of users: subscribers, customers, others\n')
    return df['User Type'].value_counts()

def count_user_gender(df):
    '''What are the counts of gender?'''
    # df - dataframe returned from time_filters
    try:
        print('\n* Q9. What is the breakdown of gender among users?\n')
        return df['Gender'].value_counts()
    except:
        print('There is no gender data in the source.')

def user_birthyears(df):
    '''What is the earliest, latest, and most frequent birth year?'''
    # df - dataframe returned from time_filters
    try:
        print('\n* Q10. What is the earliest, latest, and most frequent year of birth, respectively?')
        earliest = np.min(df['Birth Year'])
        print ("\nThe earliest year of birth is " + str(earliest) + "\n")
        latest = np.max(df['Birth Year'])
        print ("The latest year of birth is " + str(latest) + "\n")
        most_frequent= df['Birth Year'].mode()[0]
        print ("The most frequent year of birth is " + str(most_frequent) + "\n")
        return earliest, latest, most_frequent
    except:
        print('No available birth date data for this time_filter.')

def process_stat(f, df):
    '''Calculates the time it takes to compute a statistic
    '''
    start_time = time.time()
    statToCompute = f(df)
    print(statToCompute)
    print("Computing this stat took %s seconds." % (time.time() - start_time))

def show_data(df):
    '''
    Displays the data used to compute the stats
    '''
    #omit irrelevant columns from visualization
    df = df.drop(['month', 'day_of_month'], axis = 1)
    row_index = 0

    see_data = input("\nWould you like to see the rows of the data used to compute the stats? Please write 'yes' or 'no' \n").lower()
    while True:
        if see_data == 'no':
            return
        if see_data == 'yes':
            print(df[row_index: row_index + 5])
            row_index = row_index + 5
        see_data = input("\n Would you like to see five more rows of the data used to compute the stats? Please write 'yes' or 'no' \n").lower()

def main():
    '''The main function calculates and prints out the
    descriptive statistics about a requested city
    '''
    # calling all the functions step by step
    city = get_city()
    df = load_data(city)
    time_filter = get_time_filter()
    month = get_month(time_filter)
    day = get_day(time_filter)
    day_of_month = get_day_of_month(df, time_filter)

    df = time_filters(df, time_filter, month, day, day_of_month)
    show_data(df)

    # all the conclusions
    stats_funcs_list = [most_common_month,
     most_common_day_week, most_common_start_hour,
     ride_duration_avg_total, most_common_trip,
     most_common_station, count_user_type, user_birthyears, count_user_gender]

    for x in stats_funcs_list:	# displays processing time for each function block
        process_stat(x, df)

    # Restarting option
    restart = input("\n * Would you like to restart? Type \'yes\' or \'no\'.\n")
    if restart.upper() == 'YES' or restart.upper() == "Y":
        main()

if __name__ == '__main__':
    main()
