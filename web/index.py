from datetime import datetime

date_time_str = '26/03/2021'

date_time_obj = datetime.strptime(date_time_str, '%d/%m/%Y')


print("The type of the date is now",  type(date_time_obj))
print("The date is", date_time_obj)