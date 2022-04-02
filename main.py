import datetime as dt
import pandas as pd
import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty,ListProperty
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.dropdown import DropDown
from fit_report_back import *

class Current_User:
    def __init__(self,uname,fname,id_num):
        self.uname = uname
        self.fname = fname
        self.id_num = id_num

class ProgressReport(Screen):
    pass

class WorkoutGrades(Screen):
    pass

class CalorieGrades(Screen):
    pass

class UserPage(Screen):
    pass

class DailyLogCal(Screen):
    pass

class DailyLogWko(Screen):
    pass

class SwingPage(Screen):
    pass

class Login(Screen):
    pass

class Register(Screen):
    pass

class SetGoals(Screen):
    pass

class SetWkoGoals(Screen):
    pass

class Manager(ScreenManager):
    pass

class FitnessReportApp(App):
    timeframe_list = ['Today','This Week','This Month','Program']
    boole = ['YES','NO','REST']
    username = ''
    id_num = ''
    days = ''
    daily_cal_goals = StringProperty('')
    wko_schedule = ListProperty(['Sun,Tues,Thur','Sun,Tues,Fri','Sun,Wed,Fri','Sun,Wed,Sat','Mon,Tues,Thur','Mon,Tues,Fri','Mon,Wed,Fri','Mon,Wed,Sat'])
    duration = StringProperty(['RR: 3-5','RR: 8-10','RR: 12-15','Cardio: 15min','Cardio: 30min','Cardio: 45min','Cardio: 60min','Cardio: 1.5hours'])
    routine_type = ListProperty(['Cardio','Weightlifting','Cardio/Weightlifting'])

    def set_targets(self,swt,gwt,gcal):
        targets(swt,gwt,gcal,self.id_num)

    def passkey(self):
        var = str(self.root.uname.text) + str(self.root.pword.text)
        conn = psycopg2.connect(
        host = 'ec2-52-22-226-8.compute-1.amazonaws.com',
        database = 'dach7jo7dkm260',
        user = 'kcpvqdlgtceuei',
        password = '46727e8641e115e2e85f7517bc8ad3d8af2d30808815f437e553c9091bf1e5cc',
        port = '5432')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Users WHERE email=%s',(self.root.uname.text,))
        row = cur.fetchall()
        conn.close()
        list = []
        for e in row:
            x = str(e[3]) + str(e[5])
            if var == x:
                self.id_num = int(e[0])
                self.username = e[4]
                x = dt.datetime.strptime(e[1], '%Y-%m-%d')
                y = dt.date(x.year,x.month,x.day)
                z = today - y
                self.days = int(z.days)
                self.root.current = "userpage"
                print(self.id_num)

    def make_dict(self,wko_days,reps):
        wko_dict = {'workout-days':wko_days,'rep-range':rep}
        x = f'{wko_dict}'
        return str(x)

    def wko_target(self,wko_days,reps):
        sched = make_dict(wko_days,reps)
        wko_targets(sched,reps,self.id_num)


    def dailycal(self):
        meals = [self.root.m1.text,self.root.m2.text,self.root.m3.text,self.root.m4.text,self.root.m5.text,self.root.m6.text]
        for e in meals:
            try:
                e = int(e)
            except:
                e = 0
            e += e
        total = e
        calorie_log(total,self.id_num)

    def dailywko(self,spinner,two):
        x = 0
        y = 0
        if spinner.text == 'YES':
            x = 1
        elif spinner.text == 'REST':
            x = 1
        elif spinner.text == 'NO':
            pass
        else:
            pass
        y = int(two.text) / 2
        num = (x * 50) + y
        wko_log(num,self.id_num)

    def calorie_grade(self):
        x = cal_grade(self.id_num,self.days)
        self.root.goalcals.text = x[1]
        self.root.totalcals.text = x[0]
        r = x[2]
        s = grade(r)
        self.root.calsgrade.text = s

    def workout_grade(self):
        x = wkograde(self.id_num,self.days)
        self.root.wko_acc.text = x[3]
        self.root.wko_vol.text = x[0]
        r = x[2]
        s = grade(r)
        self.root.wkosgrade.text = s


    def disp(self):
        self.root.user.text = f"Welcome back {self.username}!"

    def reg(self,a1,a2,a3,a4):
        register(a1,a2,a3,a4)
        self.root.current = 'login'

    def build(self):
        kv = Builder.load_file("fitness.kv")
        self.title = 'Fitness Report'
        return kv

if __name__ == "__main__":
    FitnessReportApp().run()
