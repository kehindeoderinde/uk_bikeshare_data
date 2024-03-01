import time
import math
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    city, month, day = None, None, None
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in CITY_DATA:
        print('NOTE: Only the following cities are allowed: chicago, new york city, washington')
        city = input('Enter your city name: ').strip().lower()
        try:
            pass
            
        except (ValueError, KeyboardInterrupt) as e:
            print('An error occured', e)

    # get user input for month (all, january, february, ... , june)
    while month not in MONTHS:
        print('NOTE: Only the first six months of the year formatted as string are allowed e.g. may, february etc. and "all"')
        month = input('Enter month by name or "all": ').strip().lower()
        try:
            pass
            
        except (ValueError, KeyboardInterrupt) as e:
            print('An error occured', e)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in DAYS:
        print('NOTE: Only day of week formatted as string is allowed e.g. monday, friday, wednesday etc.')
        day = input('Enter day of week or "all": ').strip().lower()
        try:
            pass
            
        except (ValueError, KeyboardInterrupt) as e:
            print('An error occured', e)

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
    # Read initial data based on city data key
    df = pd.read_csv(CITY_DATA[city], index_col=[0])
    
    # Configure new fields and filter data results according to day and month
    df.insert(2, 'Hour Of Travel', pd.to_datetime(df['Start Time']).dt.strftime('%H').apply(int))
    df.insert(3, 'Day Of Week', pd.to_datetime(df['Start Time']).dt.strftime('%A').apply(str.title))
    df.insert(4, 'Month', pd.to_datetime(df['Start Time']).dt.strftime('%B').apply(str.title))
    
    if day != 'all':
        df = df[df['Day Of Week'] == day.title()]
        
    if month != 'all':
        df = df[df['Month'] == month.title()]
    
    # Drop Start and End Time after relevant extraction
    df.drop(columns=['Start Time', 'End Time'], axis=1, inplace=True)

    return df


def time_stats(df: pd.DataFrame):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # Tried using  mode and aggregtion to solve the problem to test performance and play with aggregations - Mode is faster for common occurences

    # display the most common month
    # USING MODE
    most_common_month = df['Month'].mode().values
    
    # USING GROUP BY
    # grouped_months = df.groupby('Month')
    # grouped_months_count = grouped_months.agg({'Month': ['count']})    
    # most_common_month = grouped_months_count.idxmax().values
    
    print('The most common travel month is {}'.format(*most_common_month), '\n')

    # display the most common day of week
    # USING MODE
    most_common_dow = df['Day Of Week'].mode().values
    
    # USING GROUP BY
    # grouped_dow = df.groupby('Day Of Week')
    # grouped_dow_count = grouped_dow.agg({'Day Of Week': ['count']})
    # most_common_dow = grouped_dow_count.idxmax().values
    
    print('The most common day of the week travelled is {}'.format(*most_common_dow), '\n')

    # display the most common start hour
    # USING MODE
    most_common_hour = df['Hour Of Travel'].mode().values
    
    # USING GROUP BY
    # grouped_hour = df.groupby('Hour Of Travel')
    # grouped_hour_count = grouped_hour.agg({'Hour Of Travel': ['count']})
    # most_common_hour = grouped_hour_count.idxmax().values
    
    print('The most common start hour of travel is {}'.format(*most_common_hour), '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df: pd.DataFrame):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode().values
    print('The most commonly travelled start station is {}'.format(*most_common_start_station), '\n')
    
    # display most commonly used end station
    most_common_end_station = df['End Station'].mode().values
    print('The most commonly travelled end station is {}'.format(*most_common_end_station), '\n')

    # display most frequent combination of start station and end station trip
    grouped_start_end_station = df.groupby(['Start Station', 'End Station'])
    grouped_start_end_station_count = grouped_start_end_station.agg({'Trip Duration': ['count']})
    most_common_start_end_stations = grouped_start_end_station_count.idxmax().values
    
    
    print('The most commonly travelled start and end station trips are between {}'.format(' and '.join(*most_common_start_end_stations)), '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df: pd.DataFrame):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is {} minutes and {} seconds'.format(math.ceil(total_travel_time // 60), math.ceil(total_travel_time % 60)), '\n')
    


    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('The average travel time is {} minutes and {} seconds'.format(math.ceil(avg_travel_time // 60), math.ceil(avg_travel_time % 60)), '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df: pd.DataFrame):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCalculating User type and count...\n')
    user_type_count = df['User Type'].value_counts().items()
    
    for user_type, count in user_type_count:
        print(f'The user type is {user_type} and there are {count} members')

    # Display counts of gender
    print('\nCalculating User gender and count...\n')
    if 'Gender' in df.keys():
        gender_count = df['Gender'].value_counts().items()
        
        for gender, count in gender_count:
            print(f'The gender is {gender} and there are {count} of them')
    else:
        print('There is no gender data to be analysed here')

    # Display earliest, most recent, and most common year of birth
    
    # Convert Birth Year to int and drop all users without valid birth years
    print('\nCalculating birth year metrics if available in dataset...\n')
    if 'Birth Year' in df.keys():
        print('Dropping rows without valid birth year..\n')
        df.dropna(subset=['Birth Year'], inplace=True)
        df['Birth Year'] = df['Birth Year'].apply(int)

        earliest_birth_year = df['Birth Year'].min()
        print('The earliest birth year of an customer is {}'. format(earliest_birth_year))
        
        most_recent_birth_year = df['Birth Year'].max()
        print('The most recent birth year of an customer is {}'. format(most_recent_birth_year))
        
        most_common_birth_year = df['Birth Year'].mode().values
        print('The most common birth year of an customer is {}'. format(*most_common_birth_year))
    else:
        print('There is no birth year data to be analysed here')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_data(df: pd.DataFrame, num_of_rows=5):
    """Display specific number of rows of dataframe to user upon request"""
    requested_df = pd.DataFrame()
    df_count = df['Month'].count()
    view_data = input(f"Would you like to view {num_of_rows} rows of individual trip data? Enter yes or no?: ").lower()
    if view_data == 'yes':
        start_loc = 0
        while (start_loc <= df_count):
            start_loc += num_of_rows
            print(df.iloc[0: start_loc])
            requested_df = df.iloc[0: start_loc]
            view_display = input(f"Do you want to see next {num_of_rows} rows of individual trip data?: ").lower()
            if view_display == 'no':
                break
    else:
        requested_df = df
                     
    return requested_df


def main():
    '''Main function'''
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        # Prompt user if they want to see rows of data. Default num_of_rows is 5
        df = display_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
