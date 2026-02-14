from datetime import datetime

moscow_times_date = "Wednesday, October 2, 2002"
moscow_times_format = "%A, %B %d, %Y"
datetime_moscow = datetime.strptime(moscow_times_date, moscow_times_format)
print(f"The Moscow Times: {datetime_moscow}")

guardian_date = "Friday, 11.10.13"
guardian_format = "%A, %d.%m.%y"
datetime_guardian = datetime.strptime(guardian_date, guardian_format)
print(f"The Guardian: {datetime_guardian}")

daily_news_date = "Thursday, 18 August 1977"
daily_news_format = "%A, %d %B %Y"
datetime_daily_news = datetime.strptime(daily_news_date, daily_news_format)
print(f"Daily News: {datetime_daily_news}")