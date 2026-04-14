import pandas as pd
import time

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks user to specify a city, month, and day.
    Returns:
        (city, month, day)
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    # city input
    while True:
        city = input("Choose city (Chicago, New York City, Washington): ").lower()
        if city in CITY_DATA:
            break
        print("Invalid city. Try again.")

    # month input
    while True:
        month = input("Choose month (Jan–Jun or 'all'): ").lower()
        if month in ['january','february','march','april','may','june','all']:
            break
        print("Invalid month. Try again.")

    # day input
    while True:
        day = input("Choose day (Monday–Sunday or 'all'): ").lower()
        if day in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']:
            break
        print("Invalid day. Try again.")

    return city, month, day


def load_data(city, month, day):
    """
    Loads data and applies filters.
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month
    if month != 'all':
        month_index = ['january','february','march','april','may','june'].index(month) + 1
        df = df[df['month'] == month_index]

    # filter by day
    if day != 'all':
        df = df[df['day'].str.lower() == day]

    return df


def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print("Most Common Month:", df['month'].mode()[0])
    print("Most Common Day:", df['day'].mode()[0])
    print("Most Common Start Hour:", df['hour'].mode()[0])

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")


def station_stats(df):
    print('\nCalculating The Most Popular Stations...\n')

    print("Most Common Start Station:", df['Start Station'].mode()[0])
    print("Most Common End Station:", df['End Station'].mode()[0])

    df['trip'] = df['Start Station'] + " -> " + df['End Station']
    print("Most Common Trip:", df['trip'].mode()[0])


def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')

    print("Total Travel Time:", df['Trip Duration'].sum())
    print("Average Travel Time:", df['Trip Duration'].mean())


def user_stats(df):
    print('\nCalculating User Stats...\n')

    print("User Types:\n", df['User Type'].value_counts())

    if 'Gender' in df.columns:
        print("\nGender:\n", df['Gender'].value_counts())

    if 'Birth Year' in df.columns:
        print("\nEarliest Birth Year:", int(df['Birth Year'].min()))
        print("Most Recent Birth Year:", int(df['Birth Year'].max()))
        print("Most Common Birth Year:", int(df['Birth Year'].mode()[0]))


def display_raw_data(df):
    """
    Show raw data in chunks of 5 rows
    """
    start = 0
    while True:
        show = input("\nDo you want to see raw data? (yes/no): ").lower()
        if show != 'yes':
            break
        print(df.iloc[start:start+5])
        start += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? (yes/no): ')
        if restart.lower() != 'yes':
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()