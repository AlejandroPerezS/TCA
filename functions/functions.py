def convert_to_am_pm(time_float):
    hours = int(time_float)
    minutes = int((time_float - hours) * 60)
    period = 'AM' if hours < 12 else 'PM'
    if hours > 12:
        hours -= 12
    elif hours == 0:
        hours = 12
    return f"{hours:02}:{minutes:02} {period}"