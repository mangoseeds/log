from flask import Flask, render_template, request, flash, redirect, url_for, session
import sys

application = Flask(__name__)


#이번 달 날짜 정보 가져오기
from datetime import datetime, timedelta
from dateutil import relativedelta
import calendar

def getCalendar():
    today = datetime.today()
    cal = calendar.Calendar(firstweekday=0) #월요일을 주의 시작으로 설정
    print(f'{today.year}년 {today.month}월')
    calendar_list = cal.monthdatescalendar(today.year, today.month)
     

    #print(calendar_list)
    


#Index 페이지
@application.route("/")
def index():
    return render_template("Home.html")


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8000, debug=True)