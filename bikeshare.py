import time
import pandas as pd

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
MONTH_ABBR = {
    'jan': 'january',
    'feb': 'february',
    'mar': 'march',
    'apr': 'april',
    'may': 'may',
    'jun': 'june'
}

DAYS = [
    'monday', 'tuesday', 'wednesday',
    'thursday', 'friday', 'saturday',
    'sunday', 'all'
]


def get_filters():
    """Ask user for city, month, and day filters."""
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input(
            '\nChoose a city '
            '(Chicago, New York City, Washington): '
        ).lower().strip()

        if city in CITY_DATA:
            break
        print('Invalid city. Please try again.')

    while True:
        month = input(
            '\nChoose a month '
            '(January to June), month abbreviation '
            '(Jan to Jun), or "all": '
        ).lower().strip()

        if month in MONTH_ABBR:
            month = MONTH_ABBR[month]

        if month in MONTHS:
            break
        print('Invalid month. Please try again.')

    while True:
        day = input(
            '\nChoose a day of week '
            '(Monday to Sunday) or "all": '
        ).lower().strip()

        if day in DAYS:
            break
        print('Invalid day. Please try again.')

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """Load data and apply city, month, and day filters."""
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month_num = MONTHS.index(month) + 1
        df = df[df['month'] == month_num]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Display statistics on the most frequent travel times."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    common_day = df['day_of_week'].mode()[0].title()
    common_hour = df['hour'].mode()[0]

    print('Most Common Month:', MONTHS[common_month - 1].title())
    print('Most Common Day of Week:', common_day)
    print('Most Common Start Hour:', common_hour)

    print(
        '\nThis took {:.2f} seconds.'.format(
            time.time() - start_time
        )
    )
    print('-' * 40)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start = df['Start Station'].mode()[0]
    common_end = df['End Station'].mode()[0]

    df['route'] = df['Start Station'] + ' to ' + df['End Station']
    common_route = df['route'].mode()[0]

    print('Most Common Start Station:', common_start)
    print('Most Common End Station:', common_end)
    print('Most Common Trip:', common_route)

    print(
        '\nThis took {:.2f} seconds.'.format(
            time.time() - start_time
        )
    )
    print('-' * 40)


def trip_duration_stats(df):
    """Display statistics on total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_time = df['Trip Duration'].sum()
    mean_time = df['Trip Duration'].mean()

    print('Total Travel Time:', total_time)
    print('Average Travel Time:', mean_time)

    print(
        '\nThis took {:.2f} seconds.'.format(
            time.time() - start_time
        )
    )
    print('-' * 40)


def user_stats(df):
    """Display statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('User Types:')
    print(df['User Type'].value_counts())

    if 'Gender' in df.columns:
        print('\nGender:')
        print(df['Gender'].value_counts())

    if 'Birth Year' in df.columns:
        print('\nEarliest Birth Year:',
              int(df['Birth Year'].min()))
        print('Most Recent Birth Year:',
              int(df['Birth Year'].max()))
        print('Most Common Birth Year:',
              int(df['Birth Year'].mode()[0]))

    print(
        '\nThis took {:.2f} seconds.'.format(
            time.time() - start_time
        )
    )
    print('-' * 40)


def display_raw_data(df):
    """Display raw data five rows at a time."""
    start = 0

    while True:
        answer = input(
            '\nWould you like to view 5 rows of raw data? '
            'Enter yes or no: '
        ).lower().strip()

        if answer == 'yes':
            print(df.iloc[start:start + 5])
            start += 5

            if start >= len(df):
                print('\nNo more raw data available.')
                break

        elif answer == 'no':
            break

        else:
            print('Please enter only yes or no.')


def main():
    """Run the bikeshare statistics program."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print(
                '\nNo data available for selected filters. '
                'Please try different options.'
            )
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(df)

        restart = input(
            '\nWould you like to restart? '
            'Enter yes or no: '
        ).lower().strip()

        while restart not in ['yes', 'no']:
            restart = input(
                'Please enter only yes or no: '
            ).lower().strip()

        if restart == 'no':
            break


if __name__ == "__main__":
    main()