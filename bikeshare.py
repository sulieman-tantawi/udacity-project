import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    # This script explores bikeshare data
    print('Hello! Let\'s explore some US bikeshare data!')
    
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n").strip().lower()
        if city in CITY_DATA.keys():
            break
        else:
            print("Invalid input. Please make sure to enter either Chicago, New York City, or Washington.")

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Which month? January, February, March, April, May, June, or type 'all' for no filter:\n").strip().lower()
        if month in months:
            break
        else:
            print("Invalid input. Please enter a valid month from the list or 'all'.")

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or type 'all':\n").strip().lower()
        if day in days:
            break
        else:
            print("Invalid input. Please enter a valid day of the week or 'all'.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month_num = df['month'].mode()[0]
    months_names = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month_name = months_names[popular_month_num - 1]
    print(f"Most Common Month: {popular_month_name}")

    popular_day = df['day_of_week'].mode()[0]
    print(f"Most Common Day of Week: {popular_day}")

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {popular_hour}:00")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    print(f"Most Commonly Used Start Station: {popular_start_station}")

    popular_end_station = df['End Station'].mode()[0]
    print(f"Most Commonly Used End Station: {popular_end_station}")

    df['Trip Route'] = df['Start Station'] + " -> " + df['End Station']
    popular_route = df['Trip Route'].mode()[0]
    print(f"Most Frequent Trip Route: {popular_route}")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_travel_time} seconds (approx. {round(total_travel_time/3600, 2)} hours)")

    mean_travel_time = df['Trip Duration'].mean()
    print(f"Average Travel Time: {round(mean_travel_time, 2)} seconds")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print("Counts of User Types:\n", user_types.to_string())

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of Gender:\n", gender_counts.to_string())
    else:
        print("\nGender data is not available for this city.")

    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print(f"\nEarliest Birth Year: {earliest_year}")
        print(f"Most Recent Birth Year: {most_recent_year}")
        print(f"Most Common Birth Year: {most_common_year}")
    else:
        print("\nBirth Year data is not available for this city.")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def display_raw_data(df):
    while True:
        view_data = input('\nWould you like to view 5 rows of raw trip data? Enter "yes" or "no":\n').strip().lower()
        if view_data in ['yes', 'no']:
            break
        else:
            print("Invalid input. Please explicitly enter 'yes' or 'no'.")

    start_loc = 0
    
    while view_data == 'yes':
        if start_loc < len(df):
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            
            while True:
                view_data = input('\nDo you wish to continue viewing the next 5 rows? Enter "yes" or "no":\n').strip().lower()
                if view_data in ['yes', 'no']:
                    break
                else:
                    print("Invalid input. Please explicitly enter 'yes' or 'no'.")
        else:
            print("\nYou have reached the end of the dataset.")
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        display_raw_data(df)

        while True:
            restart = input('\nWould you like to restart? Enter "yes" or "no":\n').strip().lower()
            if restart in ['yes', 'no']:
                break
            else:
                print("Invalid input. Please explicitly enter 'yes' or 'no'.")
                
        if restart == 'no':
            print("Exiting program. Thank you!")
            break

if __name__ == "__main__":
    main()