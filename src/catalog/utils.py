
def get_formatted_hour(hours):
    """Return 'hour' properly formatted with respect to number of hours"""
    if (hours % 10) == 1:
        return 'ЧАС'
    elif 1 < hours < 5:
        return 'ЧАСА'
    else:
        return 'ЧАСОВ'
