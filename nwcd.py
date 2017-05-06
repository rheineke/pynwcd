import sys


def max_down(current_up, zero_percent_seeded=True):
    rr = required_ratio(zero_percent_seeded=zero_percent_seeded)


def required_ratio(zero_percent_seeded=True):
    if zero_percent_seeded:
        return _zero_seeded_required_ratio()
    return _100_seeded_required_ratio()


def _zero_seeded_required_ratio():
    return [
        (5, 0),
        (10, .15),
        (20, .20),
        (30, .30),
        (40, .40),
        (50, .50),
        (sys.maxsize, .60),
    ]


def _100_seeded_required_ratio():
    return [
        (20, 0),
        (30, .05),
        (40, .10),
        (50, .20),
        (60, .30),
        (80, .40),
        (100, .50),
        (sys.maxsize, .60),
    ]

if __name__ == '__main__':
    pass