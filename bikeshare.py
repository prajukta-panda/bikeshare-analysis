import pandas as pd
import time

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}


def get_filters():
    """Get valid user input for city, month, and day."""
    print("\nHello! Let's explore some US bikeshare data!\n")

    cities = ['chicago', 'new york city', 'washington']
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days = ['monday', 'tuesday', 'wednesday', 'thursday',
            'friday', 'saturday', 'sunday', 'all']

    while True:
        city = input("Enter city: ").lower().strip()
        if city in cities:
            break
        print("Invalid city. Try again.")

    while True:
        month = input("Enter month (Jan–Jun or 'all'): ").lower().strip()
        if month in months:
            break
        print("Invalid month. Try again.")

    while True:
        day = input("Enter day (Mon–Sun or 'all'): ").lower().strip()
        if day in days:
            break
        print("Invalid day. Try again.")

    return city, month, day


def load_data(city, month, day):
    """Load data for the specified city and apply filters."""
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month_index = ['january', 'february', 'march',
                       'april', 'may', 'june'].index(month) + 1
        df = df[df['month'] == month_index]

    if day != 'all':
        df = df[df['day'].str.lower() == day]

    return df


def time_stats(df):
    """Display statistics on most frequent times of travel."""
    if df.empty:
        print("\nNo data available for time statistics.\n")
        return

    print("\nCalculating Most Frequent Times...\n")
    start_time = time.time()

    print("Most Common Month:", df['month'].mode()[0])
    print("Most Common Day:", df['day'].mode()[0])
    print("Most Common Hour:", df['hour'].mode()[0])

    print(f"Completed in {time.time() - start_time:.2f} seconds.\n")


def station_stats(df):
    """Display statistics on most popular stations and trip."""
    if df.empty:
        print("\nNo data available for station statistics.\n")
        return

    print("\nCalculating Most Popular Stations...\n")

    print("Most Common Start Station:", df['Start Station'].mode()[0])
    print("Most Common End Station:", df['End Station'].mode()[0])

    df['trip'] = df['Start Station'] + " -> " + df['End Station']
    print("Most Common Trip:", df['trip'].mode()[0])


def trip_duration_stats(df):
    """Display statistics on total and average trip duration."""
    if df.empty:
        print("\nNo data available for trip duration.\n")
        return

    print("\nCalculating Trip Duration...\n")

    print("Total Travel Time:", df['Trip Duration'].sum())
    print("Average Travel Time:", df['Trip Duration'].mean())


def user_stats(df):
    """Display statistics on bikeshare users."""
    if df.empty:
        print("\nNo data available for user statistics.\n")
        return

    print("\nCalculating User Stats...\n")

    print("User Types:\n", df['User Type'].value_counts())

    if 'Gender' in df.columns:
        print("\nGender:\n", df['Gender'].value_counts())
    else:
        print("\nGender data not available.")

    if 'Birth Year' in df.columns:
        print("\nEarliest Year:", int(df['Birth Year'].min()))
        print("Most Recent Year:", int(df['Birth Year'].max()))
        print("Most Common Year:", int(df['Birth Year'].mode()[0]))
    else:
        print("\nBirth year data not available.")


def display_raw_data(df):
    """Display raw data in chunks of five rows."""
    start = 0

    while True:
        show = input("\nDo you want to see raw data? (yes/no): ").lower().strip()
        if show != 'yes':
            break

        if df.empty:
            print("No data to display.")
            break

        print(df.iloc[start:start + 5])
        start += 5


def main():
    """Run the bikeshare data analysis program."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print("\nNo data available for selected filters. Try again.\n")
            continue

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input("\nWould you like to restart? (yes/no): ").lower().strip()
        if restart != 'yes':
            print("\nGoodbye!\n")
            break


if __name__ == "__main__":
    main()