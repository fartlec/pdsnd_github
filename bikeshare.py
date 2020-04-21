import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june']
DAY_DATA = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hi there! Let\'s dive into US bikeshare datas \n')
    # get user input for city (chicago, new york city, washington).
    city = input('Please enter a city among Chicago, New York City and Washington: ').lower()
    print()
    if (city == 'new york') or (city == 'ny'):
        city = 'new york city'
    elif city == 'dc':
        city = 'washington'
    while (city not in CITY_DATA.keys()): 
         try:
            city = input('Please enter a valid city: ').lower()
         except :
            print('\nno input taken\n')
            break
    # ask user if filter by month
    while True:
        filter_by_month = input('Would you like to filter by month? ').lower()
        print()
        
        # filter data for month: yes, no, check for valid answer
        if (filter_by_month == 'yes') or (filter_by_month == 'y'):
            
            #get user input for month (all, january, february, ... , june)
            month = input('Please enter a month between January and June: ').lower()
            print()
            # month not valid
            while month not in MONTH_DATA:
                try:
                    month = input('Please enter a valid month: ').lower()
                except :
                    print('\nno input taken\n')
                    break
                    
        # get data from all months
        elif (filter_by_month == 'no') or (filter_by_month == 'n'):
            month = 'all'
        else:
            # wrong input, start again 
            print('Not a valid input, please retry')
            continue
            
        break    
        
    # ask user if filter by day       
    while True:
        filter_by_day = input('Would you like to filter by day? ').lower()
        print()
        
        # filter data for day: yes, no, check for valid answer 
        if (filter_by_day == 'yes') or (filter_by_day == 'y'):
            
            # get user input for day of week (all, monday, tuesday, ... sunday)
            day = input('Please enter a day of the week: ').lower()
            print()
        # if input wrong start again    
            while day not in DAY_DATA:
                try:
                    day = input('Please enter a valid day of the week: ').lower()
                except :
                    print('\nno input taken\n')
                    break
       
        # get data from all days            
        elif (filter_by_day == 'no') or (filter_by_day == 'n'):
            day = 'all'
        else:
            
            # wrong input, start again 
            filter_by_day = input('Not a valid input, please retry')
            continue
        break        
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
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])
   
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        
        # use the index of the months list to get the corresponding int
        month = MONTH_DATA.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

# calculates time in which bikes are most rented
def time_data(df):
    
    # calculates month in which bikes are most rented
   
   
    most_rented_month_n = df['month'].mode()[0]
    most_rented_month = MONTH_DATA[most_rented_month_n-1].title()
    
    print('\nMonth in which bikes are most rented: {} \n'.format(most_rented_month))

    # calculates day of the week in which bikes are most rented
    most_rented_day = df['day_of_week'].mode()[0]
    
    print('Day of the week in which bikes are most rented: {} \n'.format(most_rented_day))

    # calculates hour of the day in which bikes are most rented
    most_rented_hour = df['hour'].mode()[0]
    print('Hour of the day in which bikes are most rented: {} \n'.format(most_rented_hour))

# stats about the users
def users_data(df):
          
    #number and percentage of user types
    types = df.groupby('User Type',as_index=False).count()
    print('There are {} types of users, {}s and {}s \n'.format(len(types), types['User Type'][0], types['User Type'][1]))
    percentage_customers = (types['Start Station'][0] * 100) / (types['Start Station'][0] + types['Start Station'][1])
    percentage_subscribers = (types['Start Station'][1] * 100) / (types['Start Station'][0] + types['Start Station'][1])
    print('{}s ({}) are {}% of the total \n'.format(types['User Type'][0], types['Start Station'][0], percentage_customers))
    print('{}s ({}) are {}% of the total \n'.format(types['User Type'][1], types['Start Station'][1], percentage_subscribers))   
    
   
    # number and percentage of genders
    if 'Gender' not in df:
        print('Sorry, no gender data for this selection\n')
    else: 
        gender = df.groupby('Gender', as_index=False).count()
        percentage_females = (gender['Start Station'][0] * 100) / (gender['Start Station'][0] + gender['Start Station'][1])
        percentage_males = (gender['Start Station'][1] * 100) / (gender['Start Station'][0] + gender['Start Station'][1])
        print('{}s ({}) are {}% of the total \n'.format(gender['Gender'][0], gender['Start Station'][0], percentage_females))
        print('{}s ({}) are {}% of the total \n'.format(gender['Gender'][1], gender['Start Station'][1], percentage_males))
          
    # count birth year
    if 'Birth Year' not in df:
        print('Sorry, no data about birth year of users for this selection\n ')
    else:
        birth_year_count = df.groupby('Birth Year')['Birth Year'].count()
        total = df['Birth Year'].count()
        early_year=int(df['Birth Year'].max())
        late_year=int(df['Birth Year'].min())
        print('The youngest user is born in {}, the eldest is born in {} \n'.format(early_year, late_year))
        # birth year of people who uses bikesharing the most
        sort_years_most = birth_year_count.sort_values(ascending=False)
        birth_year_most = str(int(sort_years_most.index[0]))
        percentage_birth_most = (sort_years_most.iloc[0] * 100) / total
        print('People born in {} use the bikesharing the most, represent {}% of the total \n'.format(birth_year_most, percentage_birth_most))

# stats abount the rides         
def rides_data(df): 
    
    total = df['Start Station'].nunique()
          
    # most common start station
    start_count = df.groupby('Start Station')['Start Station'].count()
    most_start = df['Start Station'].mode()[0]
    sort_start = start_count.sort_values(ascending=False)
    percentage_most_start = sort_start[0]/total
    print('The most common start station is {}, {}% of the total \n'.format(most_start, percentage_most_start))
    
    # most common end station
    end_count = df.groupby('End Station')['End Station'].count()
    most_end = df['End Station'].mode()[0]
    sort_end = end_count.sort_values(ascending=False)
    percentage_most_end = sort_end[0]/total
    print('The most common end station is {}, {}% of the total \n'.format(most_end, percentage_most_end))
    
    # most popular ride 
    ride_count = df.groupby(['Start Station', 'End Station'])['Start Time'].count()
    sort_ride = ride_count.sort_values(ascending=False)
    print('The most popular trip is {} - {} \n'.format(str(sort_ride.index[0][0]), str(sort_ride.index[0][1])))
    
    # shortest trip duration
    trip_count = df.groupby('Trip Duration')['Trip Duration'].count()
    sort_trip_short = trip_count.sort_values(ascending=True)
    short_trip = int(sort_trip_short.index[0])
    m, s = divmod(short_trip, 60)
    h, m = divmod(m, 60)
    print('The shortest trip duration is of {} hours, {} minutes and {} seconds\n'.format(h, m, s))
    
    
    #average trip duration
    avg_trip_dur = int(df['Trip Duration'].mean())
    m, s = divmod(avg_trip_dur, 60)
    h, m = divmod(m, 60)
    print('The average trip duration is of {} hours, {} minutes and {} seconds'.format(h, m, s))


def raw_data(df):
""" Ask user if he would like to see raw data too
    raw data are displayed by 5 rows. then ask user to show 5 more rows
    input : y, yes, yea, yep
    return : 5 rows of raw data
    """
    index=0
    user_input='y'
    while user_input in ['yes','y','yep','yea'] and index+5 < df.shape[0]:
        user_input = input('Would you like to display 5 rows of raw data? ').lower()
        print(df.iloc[index:index+5])
        index += 5    
    
def main():
  """ Ask user which data he is interested in among rides
        users, time or raw data, shows them, then asks if he would
        like to see more
    input : r, u, t, raw
    return : time, rides, user data or raw data
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print('What data are you interested in?')
        choice = input('Please type r for rides, u for users, t for time or raw for raw data: ').lower()
        print()
        while True:
            if choice == 'r':
                rides_data(df)
            elif choice == 'u':
                users_data(df)
            elif choice == 't':
                time_data(df)
            elif choice == 'raw':
                raw_data(df)
            else:
                print('Please type the correct letter')
                continue
            break
        
        restart = input('\nWould you like to see more data (y/n)?').lower()
        if restart != 'yes' and restart != 'y':
            break

if __name__ == "__main__":
    main()
    
