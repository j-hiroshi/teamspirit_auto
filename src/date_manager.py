import datetime
from dateutil.relativedelta import relativedelta
import jpholiday


class DateManager:

    def __init__(self):
        today = datetime.datetime.today()
        self.business_days = []
        self.year = today.year
        self.month = today.month
        self.day_end = (today + relativedelta(months=+1, day=1, days=-1)).day  # 月末日

    # 営業日のみのリストを作成する
    def create_business_days(self):
        for i in range(1, self.day_end + 1):
            date = datetime.date(self.year, self.month, i)

            if date.weekday() < 5 and not jpholiday.is_holiday(date):
                # 0埋め
                d = "{}-{}-{}".format(
                    str(self.year).zfill(2), str(self.month).zfill(2), str(i).zfill(2)
                )
                self.business_days.append(d)
