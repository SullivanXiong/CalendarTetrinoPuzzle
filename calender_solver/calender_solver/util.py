from enum import Enum

calender_order = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG",
                  "SEP", "OCT", "NOV", "DEC", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                  11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                  26, 27, 28, 29, 30, 31, "SUN", "MON", "TUE", "WED", "THU",
                  "FRI", "SAT"]

class Month(Enum):
    """
    Enum for the months of the year.
    """
    JAN = 1
    FEB = 2
    MAR = 3
    APR = 4
    MAY = 5
    JUN = 6
    JUL = 7
    AUG = 8
    SEP = 9
    OCT = 10
    NOV = 11
    DEC = 12

class DayOfWeek(Enum):
    """
    Enum for the days of the week.
    """
    SUN = 0
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6

def get_calender_order():
    """
    Get the order of the calendar.
    :return: A list of strings representing the order of the calendar.
    """
    return calender_order
