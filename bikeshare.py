import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # adapted from here: https://python-forum.io/thread-9200.html
    while True:
        city = input("Enter the name of the city you want to inspect\n(\"chicago\", \"new york city\" or \"washington\"): ").lower()
        if city in CITY_DATA:
            print("You chose:", city)
            break
        else:
            print("\nInvalid city name\n")

    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    # Cheat Sheet page 8 and https://stackoverflow.com/questions/21082037/when-making-a-very-simple-multiple-choice-story-in-python-can-i-call-a-line-to
    # In hindsight maybe it would've been better to implement lists of the months/days
    while True:
        timeframe = input("For which timeframe do you want to filter for?\n(Enter \"month\", \"day\", \"all\" or \"none\"): ").lower()
        if timeframe == 'month':
            month = input("For which month do you want to filter for?\n(Enter \"january\", \"february\", \"march\", \"april\" or \"june\"): ").lower()
            day = 'all'
            print("You've filtered for:", month)
            break
        elif timeframe == 'day':
            month = 'all'
            day = input("For which day do you want to filter for?\n(Enter \"monday\", \"tuesday\", \"wednesday\", \"thursday\", \"friday\", \"saturday\" or \"sunday\"): ").lower()
            print("You've filtered for:", day)
            break
        elif timeframe == 'all':
            month = input("For which month do you want to filter for?\n(Enter \"january\", \"february\", \"march\", \"april\" or \"june\"): ").lower()
            day = input("For which day do you want to filter for?\n(Enter \"monday\", \"tuesday\", \"wednesday\", \"thursday\", \"friday\", \"saturday\" or \"sunday\"): ").lower()
            print("You've filtered for:", month, "and", day)
            break
        elif timeframe == 'none':
            month = 'all'
            day = 'all'
            print("Data will not be filtered for a specific timeframe")
            break
        else:
            input("Check your spelling and type in again!\n(Enter \"month\", \"day\", \"all\" or \"none\"): ").lower()
            break
    print('You have filtered for:', city, month, day)
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #This part is taken from; Practice Solution #3: Loading and Filtering Data
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # display the most common day of week
    popular_weekday = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_startstation = df['Start Station'].mode()[0]
    print('Most Popular "Start Station":', popular_startstation)

    # display most commonly used end station
    popular_endstation = df['End Station'].mode()[0]
    print('Most Popular "End Station":', popular_endstation)

    # display most frequent combination of start station and end station trip
    # https://knowledge.udacity.com/questions/263877 + https://knowledge.udacity.com/questions/169734 (adding delimeter)
    df['Start / End Combined'] = df['Start Station'] + ' + ' + df['End Station']
    popular_stationcombination = df['Start / End Combined'].mode()[0]
    print('Most Frequently Combined Start/End Stations:', popular_stationcombination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # Loading Data into a pandas DataFrame; Example 12
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Practice Problem #2: Display a Breakdown of User Types
    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print(user_type_count)

    # Display counts of gender
    # https://knowledge.udacity.com/questions/474771
    # cheatsheet page 14; failing silently for KeyError
    try:
        gender_count = df['Gender'].value_counts()
        print(gender_count)
        # Display earliest, most recent, and most common year of birth
        # https://knowledge.udacity.com/questions/86491
        earliest_YOB = df['Birth Year'].min()
        recent_YOB = df['Birth Year'].max()
        common_YOB = df['Birth Year'].mode()[0]
    except KeyError:
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # Asking user if they want to see 5 rows of raw data incrementally; https://knowledge.udacity.com/questions/26261
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?").lower()
    if view_data in ('yes'):
        start_loc = 0
        while True:
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            view_more_data = input("Do you wish to continue?: ").lower()
            if view_more_data not in ('yes'):
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
