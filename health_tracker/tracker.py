import csv
import mysql.connector
from health_tracker.user import User

class HealthTracker:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        try:
            with open('logins.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    users.append(User(row[0], row[1]))  # Assuming login file has username and password
        except FileNotFoundError:
            print("logins.csv not found.")
        return users

    def admin_actions(self):
        print('ADMIN::editing')
        print('What Changes would you like to make?')
        print('1 to add food to the menu')
        print('2 to remove food from the menu')
        print('3 to add a new physical activity')
        print('4 to check student details')
        option = input('>>>')
        while option not in ['1', '2', '3', '4']:
            option = input('Please refrain from entering any value but 1, 2, 3, or 4: ')
        if option == '1':
            self.add_food_to_menu()
        elif option == '2':
            self.remove_food_from_menu()
        elif option == '3':
            self.add_phy_activity()
        elif option == '4':
            self.show_student_details()

    def add_food_to_menu(self):
        with mysql.connector.connect(
                host='localhost',
                user='root',
                password='pass123',
                port='3306',
                database='school'
        ) as my_connector:
            my_cursor = my_connector.cursor()
            my_cursor.execute('SELECT * FROM food')
            foods = my_cursor.fetchall()
            food_names = [food[1] for food in foods]

            food_to_be_added_name = input('Enter name of food that is to be added >>>').strip()
            if not food_to_be_added_name:
                print('Food name cannot be empty.')
                return

            if food_to_be_added_name in food_names:
                food_to_be_added_id = next(food[0] for food in foods if food[1] == food_to_be_added_name)
                my_cursor.execute("UPDATE food SET is_served = 1 WHERE food_id = %s", (food_to_be_added_id,))
                my_connector.commit()
                print(
                    f'{food_to_be_added_name} already exists in our system. It has been successfully added to the menu.')
            else:
                food_to_be_added_calorie_count = int(
                    input('Enter the number of calories per portion of food that is to be added >>>'))
                my_cursor.execute(
                    "INSERT INTO food (food_id, food_name, calorie_consumed, is_served) VALUES (%s, %s, %s, %s)",
                    (len(foods) + 1, food_to_be_added_name, food_to_be_added_calorie_count, 1))
                my_connector.commit()
                print(f'{food_to_be_added_name} was successfully added to the menu!')

    def remove_food_from_menu(self):
        with mysql.connector.connect(
                host='localhost',
                user='root',
                password='pass123',
                port='3306',
                database='school'
        ) as my_connector:
            my_cursor = my_connector.cursor()
            my_cursor.execute('SELECT * FROM food')
            foods = my_cursor.fetchall()
            food_in_menu = [food[1] for food in foods if food[3] == 1]

            if food_in_menu:
                print('The list of foods in the menu are:')
                for food in food_in_menu:
                    print(food)

                food_to_be_removed_name = input(
                    'Enter name of food that is to be deleted from the above list >>>').strip()
                while food_to_be_removed_name not in food_in_menu:
                    food_to_be_removed_name = input(
                        'Please refrain from entering a food name that was not mentioned in the list above >>>').strip()

                food_to_be_removed_id = next(food[0] for food in foods if food[1] == food_to_be_removed_name)
                my_cursor.execute("UPDATE food SET is_served = 0 WHERE food_id = %s", (food_to_be_removed_id,))
                my_connector.commit()
                print(f'{food_to_be_removed_name} was successfully deleted from the menu!')
            else:
                print('The food menu is empty right now. Please try again later when required.')

    def add_phy_activity(self):
        with mysql.connector.connect(
                host='localhost',
                user='root',
                password='pass123',
                port='3306',
                database='school'
        ) as my_connector:
            my_cursor = my_connector.cursor()
            my_cursor.execute('SELECT * FROM phy_activity')
            activities = my_cursor.fetchall()

            phy_activity_to_be_added_name = input('Enter the name of the new physical activity >>>').strip()
            if not phy_activity_to_be_added_name:
                print('Physical activity name cannot be empty.')
                return

            if any(phy_activity_to_be_added_name == activity[1] for activity in activities):
                print(f'{phy_activity_to_be_added_name} already exists in our system. Please try again when required.')
            else:
                phy_activity_to_be_added_calorie_burnt = int(input(
                    f'Enter the number of calories burnt for every hour of {phy_activity_to_be_added_name} executed >>>'))
                my_cursor.execute(
                    "INSERT INTO phy_activity (activity_id, activity_name, calorie_burnt) VALUES (%s, %s, %s)",
                    (len(activities) + 1, phy_activity_to_be_added_name, phy_activity_to_be_added_calorie_burnt))
                my_connector.commit()
                print(f'{phy_activity_to_be_added_name} was successfully added!')

    def show_student_details(self):
        with mysql.connector.connect(
                host='localhost',
                user='root',
                password='pass123',
                port='3306',
                database='school'
        ) as my_connector:
            my_cursor = my_connector.cursor()
            my_cursor.execute('SELECT admission_no FROM students')
            admission_nos = [i[0] for i in my_cursor.fetchall()]

            admission_no = input('Enter admission number of the student whose details are required >>>')
            while True:
                try:
                    admission_no = int(admission_no)
                    if admission_no in admission_nos:
                        break
                    else:
                        raise ValueError
                except ValueError:
                    admission_no = input('Please refrain from entering an invalid admission number >>>')

            my_cursor.execute('SELECT * FROM students WHERE admission_no = %s', (admission_no,))
            student_details = my_cursor.fetchone()
            print('The details of the student:')
            print('Admission number:', student_details[0])
            print('Roll number:', student_details[1])
            print('Name:', student_details[2])
            print('Grade:', student_details[3])
            print('Age:', student_details[4])
            print('Gender:', student_details[5])
            print('Date of Birth:', student_details[6])
            print('Mother tongue:', student_details[7])
            print('Nationality:', student_details[8])
            print('Phone number:', student_details[9])
