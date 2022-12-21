import datetime

chartTimeOptions={
        "1d": "Today",
        "PWeek": "This Week",
        "LWeek": "Last 2 Weeks",
        "PMonth": "This Month",
        "PQuarter": "This Quarter",
        "PYear": "This Year",
        "P5Year": "Last 5 Years",
        "Forever": "Forever",
    }
    

def get_relative_date(dateOption):
       
    today = datetime.date.today()

    days_past_monday  = 0 - today.weekday()
    PWeekDate = (today + datetime.timedelta(days_past_monday))
    LWeekDate = (today + datetime.timedelta(days_past_monday-7))
    PMonthDate = datetime.date(today.year,today.month,1)
    if today.month in [1,2,3]:
        PQuarterStartMonth = 1
    elif today.month in [4,5,6]:
        PQuarterStartMonth = 4
    elif today.month in [7,8,9]:
        PQuarterStartMonth = 7
    elif today.month in [10,11,12]:
        PQuarterStartMonth = 10
    PQuarterDate = datetime.date(today.year,PQuarterStartMonth,1)
    PYearDate = datetime.date(today.year,1,1)
    P5YearDate = datetime.date(today.year-5,1,1)

    if dateOption== "1d":
        return today
    elif dateOption=="PWeek":
        return PWeekDate
    elif dateOption=="LWeek":
        return LWeekDate
    elif dateOption=="PMonth": 
        return PMonthDate
    elif dateOption=="PQuarter": 
        return PQuarterDate
    elif dateOption=="PYear": 
        return PYearDate
    elif dateOption=="P5Year":
        return P5YearDate
    elif dateOption=="Forever":
        return None
    else:
        return None
