from datetime import datetime, date, time

STANDARD_HOURS = 8
HALF_DAY_HOURS = 4


def parse_time(t):
    if t is None:
        return None
    if isinstance(t, time):
        return t
    return datetime.strptime(t, "%H:%M").time()


def calculate_attendance(check_in, check_out):
    if not check_in or not check_out:
        return 0, 0, STANDARD_HOURS, "ABSENT", None, None

    check_in = parse_time(check_in)
    check_out = parse_time(check_out)

    diff_seconds = (
        datetime.combine(date.today(), check_out)
        - datetime.combine(date.today(), check_in)
    ).total_seconds()

    if diff_seconds <= 0:
        return 0, 0, STANDARD_HOURS, "ABSENT", check_in, check_out

    diff = diff_seconds / 3600

    if diff >= STANDARD_HOURS:
        status = "PRESENT"
    elif diff >= HALF_DAY_HOURS:
        status = "HALF"
    else:
        status = "ABSENT"

    overtime = max(0, diff - STANDARD_HOURS)
    undertime = max(0, STANDARD_HOURS - diff)

    return round(diff, 2), round(overtime, 2), round(undertime, 2), status, check_in, check_out
