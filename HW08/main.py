from datetime import date, timedelta, datetime


def get_birthdays_per_week(users):
    today = date.today()
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    birthdays_per_week = {day: [] for day in weekdays}
    if users == []:
        return {}
    for user in users:
        name = user['name']
        birthday = user['birthday']
        this_year_birthday = birthday.replace(year=today.year)
        if this_year_birthday < today:
            this_year_birthday = this_year_birthday.replace(year=today.year + 1)
        if today <= this_year_birthday <= today + timedelta(days=7):
            day_name = weekdays[this_year_birthday.weekday()]
            if day_name in ['Saturday', 'Sunday']:
                day_name = 'Monday'
            birthdays_per_week[day_name].append(name)
    return {day: names for day, names in birthdays_per_week.items() if names}



if __name__ == '__main__':
    users = [
        {'name': 'Sasha', 'birthday': date(2023, 11, 9)},
        {'name': 'Alex', 'birthday': date(2023, 11, 11)},
        {'name': 'Oleksander', 'birthday': date(2023, 11, 12)},
        {'name': 'Shura', 'birthday': date(2023, 11, 13)},
        {'name': 'AlexSashka', 'birthday': date(2023, 11, 6)},
        {'name': 'Saniok', 'birthday': date(2023, 11, 7)},
        {'name': 'Shyrik', 'birthday': date(2023, 11, 8)},
        {'name': 'Sashka', 'birthday': date(2023, 11, 10)}
    ]
    result = get_birthdays_per_week(users)
    
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
   


