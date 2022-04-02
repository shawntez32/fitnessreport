import psycopg2
import datetime as dt
import pandas as pd

now = dt.datetime.now()
today = dt.date(now.year,now.month,now.day)
day = dt.timedelta(1)
default = dt.timedelta(90)

wkos = []

class Workout:
    def __init__(self,name,wko_type,mus_worked,cardio=False,vol=8,sets=3):
        self.name = name
        self.wko_type = wko_type
        self.muscles = mus_worked
        self.cardio = cardio
        self.vol = vol
        self.sets = sets

squat = Workout('Squat', 'Lower Body', ['Quads','Lower Back', 'Glutes'],cardio=False,vol=12)
bench = Workout('Bench Press','Upper Body',['Chest','Triceps'],cardio=False,vol=10)
deadlift = Workout('Deadlift','Lower Body',['Lower Back','Hamstring'],cardio=False,)
curls = Workout('Curls','Upper Body','Biceps',cardio=False,vol=10)
tri_raise = Workout('Tri-Raise','Upper Body','Triceps',cardio=False,vol=12)
push_ups = Workout('Push-Ups','Upper Body',['Chest','Triceps'],cardio=False,vol=200)
wkos = [squat,bench,deadlift,curls,tri_raise,push_ups]

def register(user,email,dob,pword):
    conn = psycopg2.connect(host = 'ec2-52-22-226-8.compute-1.amazonaws.com',database = 'dach7jo7dkm260',user = 'kcpvqdlgtceuei',password = '46727e8641e115e2e85f7517bc8ad3d8af2d30808815f437e553c9091bf1e5cc',port = '5432')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users WHERE email=%s',(email,))
    row = cur.fetchall()
    if len(row) > 0:
        pass
    else:
        cur.execute('''CREATE TABLE IF NOT EXISTS Users(user_id SERIAL PRIMARY KEY,start TEXT,username TEXT,email TEXT,First TEXT,pword TEXT)''')
        cur.execute('INSERT INTO Users(start,username,email,First,pword) VALUES(%s,%s,%s,%s,%s)',(today,user,email,dob,pword))
        conn.commit()
        conn.close()

def calorie_log(total,id_num):
    conn = psycopg2.connect(
    host = 'ec2-52-22-226-8.compute-1.amazonaws.com',
    database = 'dach7jo7dkm260',
    user = 'kcpvqdlgtceuei',
    password = '46727e8641e115e2e85f7517bc8ad3d8af2d30808815f437e553c9091bf1e5cc',
    port = '5432')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Cal_log(DATE TEXT,Calorie_Intake TEXT,id_num INT)''')
    cur.execute('INSERT INTO Cal_log(DATE,Calorie_Intake,id_num) VALUES(%s,%s,%s)',(today,total,id_num))
    conn.commit()

def wko_log(pct,id_num):
    conn = psycopg2.connect(
    host = 'ec2-52-22-226-8.compute-1.amazonaws.com',
    database = 'dach7jo7dkm260',
    user = 'kcpvqdlgtceuei',
    password = '46727e8641e115e2e85f7517bc8ad3d8af2d30808815f437e553c9091bf1e5cc',
    port = '5432')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Wko_log(DATE TEXT,Wk_pct TEXT,Acc_Grade INT,id_num INT)')
    cur.execute('INSERT INTO Wko_log(DATE,Acc_Grade,Wk_pct,id_num) VALUES(%s,%s,%s,%s)',(date,total,pct,id_num))
    conn.commit()

def calgrade(id_num,days):
    conn = psycopg2.connect(
    host = 'ec2-52-22-226-8.compute-1.amazonaws.com',
    database = 'dach7jo7dkm260',
    user = 'kcpvqdlgtceuei',
    password = '46727e8641e115e2e85f7517bc8ad3d8af2d30808815f437e553c9091bf1e5cc',
    port = '5432')
    cur = conn.cursor()
    cur.execute('SELECT * FROM ProgramGoals WHERE id_num=%s',(id_num))
    rows = cur.fetchall()
    cal_int = int(rows[1])
    goal_cals = cal_int * days
    cur.execute('SELECT * FROM Cal_log WHERE id_num=%s',(id_num,))
    row = cur.fetchall()
    stats = sum(row[1])
    grade = stats / goal_cals
    output = [stats,goal_cals,grade]
    return output



def wkograde(id_num,days):
    conn = psycopg2.connect(
    host = 'ec2-52-22-226-8.compute-1.amazonaws.com',
    database = 'dach7jo7dkm260',
    user = 'kcpvqdlgtceuei',
    password = '46727e8641e115e2e85f7517bc8ad3d8af2d30808815f437e553c9091bf1e5cc',
    port = '5432')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Wko_log WHERE id_num=%s',(id_num))
    row = cur.fetchall()
    list = row[1]
    for e in list:
        e = int(e)
        e += e
    for i in row[2]:
        i = int(i)
        i += i
    points = 100 * days
    acc = i / points
    total = e / points
    totals = [e,points,total,acc]
    return totals



def targets(swt,gwt,gcal,id_num):
    pp = f'{today}-{today + default}'
    conn = psycopg2.connect(
    host = 'ec2-52-22-226-8.compute-1.amazonaws.com',
    database = 'dach7jo7dkm260',
    user = 'kcpvqdlgtceuei',
    password = '46727e8641e115e2e85f7517bc8ad3d8af2d30808815f437e553c9091bf1e5cc',
    port = '5432')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS ProgramGoals(StartingWeight TEXT, GoalIntake TEXT,GoalWeight TEXT,Program_Period TEXT,id_num INT) """)
    cur.execute("INSERT INTO ProgramGoals(StartingWeight,GoalIntake,GoalWeight,Program_Period,id_num) VALUES(%s,%s,%s,%s,%s)",(swt,gcal,gwt,pp,id_num))
    conn.commit()
    conn.close()

def wko_targets(sched,vol,id_num):
    conn = psycopg2.connect(
    host = 'ec2-52-22-226-8.compute-1.amazonaws.com',
    database = 'dach7jo7dkm260',
    user = 'kcpvqdlgtceuei',
    password = '46727e8641e115e2e85f7517bc8ad3d8af2d30808815f437e553c9091bf1e5cc',
    port = '5432')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS WorkoutGoals(Date TEXT,  WkoSched TEXT, WkoVolume TEXT,id_num INT) """)
    cur.execute("INSERT INTO WorkoutGoals(Date,WkoSched,WkoVolume,id_num) VALUES(%s,%s,%s,%s)",(today,sched,vol,id_num))
    conn.commit()
    conn.close()

def track_progress_todate():
    conn = psycopg2.connect(
    host = 'ec2-52-22-226-8.compute-1.amazonaws.com',
    database = 'dach7jo7dkm260',
    user = 'kcpvqdlgtceuei',
    password = '46727e8641e115e2e85f7517bc8ad3d8af2d30808815f437e553c9091bf1e5cc',
    port = '5432')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Goals')
    row = cur.fetchall()
    td_goal = pd.DataFrame(row, columns=['start','today','end','cg','wvg'])
    cals_goal = sum(td_goal['cg'])
    vol_goal = sum(td_goal['wvg'])
    results = [today,cgr,wvgr]
    td_results = pd.DataFrame(results, columns=['Date','Calories','Volume'])
    cals = sum(td_results['Calories'])
    vol = sum(td_results['Volume'])
    cals = cals / cals_goal
    vol = vol / vol / vol_goal
    cal_grade = ''
    vol_grade = ''

def grade(cals):
    if cals >= 0.5999:
        cal_grade = 'F'
    elif cals >= 0.6999 and cals <= 0.7:
        cal_grade = 'D'
    elif cals >= 0.7999 and cals <= 0.8:
        cal_grade = 'C'
    elif cals >= 0.8999 and cals <= 0.9:
        cal_grade = 'B'
    elif cals >= 0.9999 and cals <= 1:
        cal_grade = 'A'
    if vol >= 0.5999:
        vol_grade = 'F'
    elif vol >= 0.6999 and vol <= 0.7:
        vol_grade = 'D'
    elif vol >= 0.7999 and vol <= 0.8:
        vol_grade = 'C'
    elif vol >= 0.8999 and vol <= 0.9:
        vol_grade = 'B'
    elif vol >= 0.9999 and vol <= 1:
        vol_grade = 'A'
