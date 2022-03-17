import sqlite3
import time
import hashlib
from employee import EMPLOYEE_LIST
from upgrades import UPGRADE_LIST, listToUpgrade

connect = sqlite3.connect("idlejeffbezos.db")
cursor = connect.cursor()

def createProgressTable() -> None:
    """creates the playerProgress table"""
    cursor.execute("CREATE TABLE IF NOT EXISTS playerProgress (username TEXT, hashed_password TEXT, last_save REAL, money REAL, money_per_second REAL, mps_mutliplier REAL, clicking_mps_percent INT, rocks INT, coffees INT, tax_frauds INT)")

def closeDBConnect() -> None:
    cursor.close()
    connect.close()

def makeEmployeeColumns() -> None:
    # count, price, mps_add_multiplier
    for employee in EMPLOYEE_LIST:
        if employee.name == "?":
            continue
        name = employee.name.replace(" ", "_")
        count_name = name + "_count"
        price_name = name + "_price"
        multiplier_name = name + "_mps_add_multiplier"
        cursor.execute(f"ALTER TABLE playerProgress ADD {count_name} INTEGER")
        cursor.execute(f"ALTER TABLE playerProgress ADD {price_name} REAL")
        cursor.execute(f"ALTER TABLE playerProgress ADD {multiplier_name} INTEGER")
    connect.commit()

def signUp(username: str, password: str) -> bool:
    """signs the user into the database. returns whether or not they signed up or not"""

    cursor.execute("SELECT username FROM playerProgress WHERE username = ?", (username,))
    if len(cursor.fetchall()) > 0:
        return False

    hashedpwd = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("INSERT INTO playerProgress (username, hashed_password) VALUES (?, ?)",
                    (username, hashedpwd))
    connect.commit()
    return True

def tryLogin(username: str, password: str) -> bool:
    """tries to login to a previous save. returns whether or not they logged in"""
    if username == "" or password == "":
        return False

    hashedpwd = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute("SELECT username, hashed_password FROM playerProgress WHERE username = ?", (username,))
    found_login = cursor.fetchall()

    if len(found_login) == 0:
        return False
    if hashedpwd != found_login[0][1]:
        return False
    
    return True

def saveProgress(username: str, money: int, money_per_second: float, mps_multiplier: float, clicking_mps_percent: int, available_upgrades: list, waiting_upgrades: list, shown_employees: list) -> None:
    """save all progress to a user"""
    
    cursor.execute("SELECT * from playerProgress WHERE username = ?", (username,))
    user_tuple = cursor.fetchall()[0]
    user_list = [x for x in user_tuple]

    user_list[2] = time.time()
    user_list[3] = money
    user_list[4] = money_per_second
    user_list[5] = mps_multiplier
    user_list[6] = clicking_mps_percent

    rocks, coffees, tax_frauds = 0, 0, 0
    for upgrade in available_upgrades:
        if upgrade.name == "rock":
            rocks += 1
        elif upgrade.name == "coffee":
            coffees += 1
        else:
            tax_frauds += 1
    for upgrade in waiting_upgrades:
        if upgrade.name == "rock":
            rocks += 1
        elif upgrade.name == "coffee":
            coffees += 1
        else:
            tax_frauds += 1

    user_list[7] = rocks
    user_list[8] = coffees
    user_list[9] = tax_frauds

    place = 10
    for i in range(len(shown_employees)):
        user_list[place+(i*3)] = shown_employees[i].count
        user_list[place+(i*3)+1] = shown_employees[i].price
        user_list[place+(i*3)+2] = shown_employees[i].mps_add_multiplier

    cursor.execute("DELETE FROM playerProgress WHERE username = ?", (username,))
    cursor.execute("INSERT INTO playerProgress VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", user_list)
    connect.commit()

    print("successefuly saved progress")

def loadProgresss(username: str) -> tuple:
    """returns all data from a previous save. 
    returns: money, money_per_second, mps_multiplier, clicking_mps_percent, available_upgrades, waiting_upgrades, shown_employees, waiting_employees"""
    cursor.execute("SELECT * from playerProgress WHERE username = ?", (username,))
    user_tuple = cursor.fetchall()[0]
    user_list = [x for x in user_tuple]

    money = user_list[3]
    money_per_second = user_list[4]
    mps_multiplier = user_list[5]
    money += (money_per_second*mps_multiplier) * (time.time() - user_list[2]) # get all money gained whilst logged out

    clicking_mps_percent = user_list[6]

    available_upgrades, waiting_upgrades = [], []
    for i in range(user_list[7]): # rocks
        available_upgrades.append(listToUpgrade(UPGRADE_LIST[0]))
    for i in range(user_list[8]): # coffees
        available_upgrades.append(listToUpgrade(UPGRADE_LIST[1]))
    for i in range(user_list[9]): # tax frauds
        available_upgrades.append(listToUpgrade(UPGRADE_LIST[2]))
    
    if len(available_upgrades) >= 9:
        available_upgrades = available_upgrades[0:9]
        waiting_upgrades = available_upgrades[9::]
    
    place = 10
    shown_employees, waiting_employees = [], []
    hidden = EMPLOYEE_LIST[1]
    EMPLOYEE_LIST.pop(1)
    for i in range(len(EMPLOYEE_LIST)):
        if user_list[place+(i*3)] == None:
            continue
        if user_list[place+(i*3)] > 0:
            shown_employees.append(EMPLOYEE_LIST[i])

        EMPLOYEE_LIST[i].count = user_list[place+(i*3)]
        EMPLOYEE_LIST[i].price = user_list[place+(i*3)+1]
        EMPLOYEE_LIST[i].mps_add_multiplier = user_list[place+(i*3)+2]
        EMPLOYEE_LIST[i].mps_add = EMPLOYEE_LIST[i].mps_adder * EMPLOYEE_LIST[i].count
    if len(shown_employees) < len(EMPLOYEE_LIST):
        waiting_employees = EMPLOYEE_LIST[len(shown_employees)::]
    shown_employees.append(hidden)
    
    return money, money_per_second, mps_multiplier, clicking_mps_percent, available_upgrades, waiting_upgrades, shown_employees, waiting_employees