import csv
from tkinter import Tk, Label, Button
from functools import partial
import mysql

from health_tracker.tracker import HealthTracker

def validateLogin(username, password):
    item1 = username.get()
    item2 = password.get()
    skip = True
    file_path = r'C:\Users\vedam\PycharmProjects\School_Student_Health_Tracker\logins.csv'
    with open(file_path, 'r', newline='') as file:
        a = csv.reader(file)
        for row in a:
            if skip:
                skip = False
            elif row[0] == item1 and row[1] == item2:
                print('Account found')
                print("username entered:", item1)
                print("password entered:", item2)
                item1 = int(item1)
                loginSuccess(item1)
                return
    print('Account not found or username and password entered incorrectly. Please try again!')

def loginSuccess(item1):
    # Create a new window for actions
    actionWindow = Tk()
    actionWindow.geometry('400x150')
    actionWindow.title('Select Action')

    Label(actionWindow, text=f"Welcome, user {item1}!").grid(row=0, column=1)

    Button(actionWindow, text="Record Food Consumption", command=partial(record_food_consumed, item1)).grid(row=1, column=1)
    Button(actionWindow, text="Record Physical Activity", command=partial(record_phy_activity_executed, item1)).grid(row=2, column=1)
    Button(actionWindow, text="Get Stats Report", command=partial(show_stats, item1)).grid(row=3, column=1)

    actionWindow.mainloop()

def record_food_consumed(roll_no):
    with mysql.connector.connect(
            host='localhost',
            user='root',
            password='pass123',
            port='3306',
            database='school'
    ) as my_connector:
        my_cursor = my_connector.cursor()
        my_cursor.execute('SELECT * FROM food WHERE is_served = 1')
        foods = my_cursor.fetchall()
        food_names = [food[1] for food in foods]

        if food_names:
            print('The foods served in the menu are:')
            for food in food_names:
                print(food)

            food_name = input('Please enter one of the foods mentioned above that you have consumed >>>').strip()
            while food_name not in food_names:
                food_name = input('Please refrain from entering any food that is not on the menu >>>').strip()

            food_id = next(food[0] for food in foods if food[1] == food_name)
            my_cursor.execute('SELECT CAST(SYSDATE() AS Date)')
            date_ = my_cursor.fetchone()[0]
            my_cursor.execute(
                "INSERT INTO food_consumed_records (roll_no, date_, food_id) VALUES (%s, %s, %s)",
                (roll_no, date_, food_id)
            )
            my_connector.commit()
            print('Your food consumption has been recorded successfully!')
        else:
            print('The menu is empty right now. Please try again when there is food to eat.')

def record_phy_activity_executed(roll_no):
    with mysql.connector.connect(
            host='localhost',
            user='root',
            password='pass123',
            port='3306',
            database='school'
    ) as my_connector:
        my_cursor = my_connector.cursor()
        my_cursor.execute('SELECT * FROM phy_activity')
        phy_activities = my_cursor.fetchall()
        phy_activity_names = [phy_activity[1] for phy_activity in phy_activities]
        print('The following are the activities you can do:')
        for phy_activity in phy_activity_names:
            print(phy_activity)

        phy_activity_name = input(
            'Please enter one of the physical activities mentioned above that you have played >>>').strip()
        while phy_activity_name not in phy_activity_names:
            phy_activity_name = input(
                'Please refrain from entering any physical activity that is not mentioned in the list above >>>').strip()

        phy_activity_id = next(
            phy_activity[0] for phy_activity in phy_activities if phy_activity[1] == phy_activity_name)
        my_cursor.execute('SELECT CAST(SYSDATE() AS Date)')
        date_ = my_cursor.fetchone()[0]
        my_cursor.execute(
            "INSERT INTO phyact_executed_records (roll_no, date_, activity_id) VALUES (%s, %s, %s)",
            (roll_no, date_, phy_activity_id)
        )
        my_connector.commit()
        print('Your physical activity has been recorded successfully!')

def show_stats(roll_no):
    import datetime
    with mysql.connector.connect(
            host='localhost',
            user='root',
            password='pass123',
            port='3306',
            database='school'
    ) as my_connector:
        my_cursor = my_connector.cursor()
        my_cursor.execute('SELECT CAST(SYSDATE() AS Date)')
        current_date = my_cursor.fetchone()[0]
        day_differences = [datetime.timedelta(days=i) for i in range(7)]

        # Calculate the last 7 days' dates
        last_7_days = [(current_date - day_diff).strftime('%Y-%m-%d') for day_diff in day_differences]

        # Food consumption stats
        my_cursor.execute('SELECT * FROM food')
        foods = my_cursor.fetchall()
        my_cursor.execute('SELECT * FROM food_consumed_records WHERE roll_no = %s', (roll_no,))
        food_records = my_cursor.fetchall()

        food_final_results = {date: 0 for date in last_7_days}
        for record in food_records:
            if record[1].strftime('%Y-%m-%d') in last_7_days:
                food_id = record[2]
                for food in foods:
                    if food[0] == food_id:
                        food_final_results[record[1].strftime('%Y-%m-%d')] += food[2]

        reached_required_counter = sum(1 for calories in food_final_results.values() if 800 <= calories <= 1200)
        recorded_days = sum(1 for calories in food_final_results.values() if calories > 0)

        if recorded_days <= 3:
            print(f'Food consumption has been recorded for {recorded_days} days.')
            print('Insufficient data to make any calculations. Please try again later.')
        else:
            print(f'In the last 7 days, food consumption has been recorded for {recorded_days} days')
            print('In these days, the number of calories consumed is as follows:')
            for date, calories in food_final_results.items():
                if calories > 0:
                    print(f'{date}: {calories} calories')
            if reached_required_counter >= 5:
                print(f'Out of the {recorded_days} days of recorded data, the requirement was reached for {reached_required_counter} days')
                print('Please continue to follow the same eating habits!')
            else:
                print(f'Out of the {recorded_days} days of recorded data, the requirement was reached for {reached_required_counter} days')
                print('Please try to practice new eating habits!')

        # Physical activity stats
        my_cursor.execute('SELECT * FROM phy_activity')
        phy_activities = my_cursor.fetchall()
        my_cursor.execute('SELECT * FROM phyact_executed_records WHERE roll_no = %s', (roll_no,))
        phyact_records = my_cursor.fetchall()

        phyact_final_results = {date: 0 for date in last_7_days}
        for record in phyact_records:
            if record[1].strftime('%Y-%m-%d') in last_7_days:
                activity_id = record[2]
                for phyact in phy_activities:
                    if phyact[0] == activity_id:
                        phyact_final_results[record[1].strftime('%Y-%m-%d')] += phyact[2]

        reached_required_counter = sum(1 for calories in phyact_final_results.values() if calories >= 400)
        recorded_days = sum(1 for calories in phyact_final_results.values() if calories > 0)

        if recorded_days <= 3:
            print(f'Physical activity executed has been recorded for {recorded_days} days in the last 7 days.')
            print('Insufficient data to make any calculations. Please try again later.')
        else:
            print(f'In the last 7 days, Physical activity executed has been recorded for {recorded_days} days')
            print('In these days, the number of calories burnt is as follows:')
            for date, calories in phyact_final_results.items():
                if calories > 0:
                    print(f'{date}: {calories} calories')
            if reached_required_counter >= 5:
                print(f'Out of the {recorded_days} days of recorded data, the requirement was reached for {reached_required_counter} days')
                print('Please continue to follow the same exercising habits!')
            else:
                print(f'Out of the {recorded_days} days of recorded data, the requirement was reached for {reached_required_counter} days')
                print('Please try to practice new exercising habits!')