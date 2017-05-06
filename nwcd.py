from collections import namedtuple
import sys


def additional_down(up, down, new_fraction_seeded=0):
    """
    Returns the maximum amount of additional data that can be downloaded.

    :param up: amount of data uploaded in gigabytes
    :param down: amount of data downloaded in gigabytes
    :param new_fraction_seeded: ratio of seeded divided by snatched after 
    downloading additional data. Must be between 0 and 1, inclusive
    """
    if not 0 <= new_fraction_seeded <= 1:
        msg_fmt = 'Expected 0 <= new_fraction_seeded <= 1 but received: '
        raise ValueError(msg_fmt.format(new_fraction_seeded))

    rr_lst = required_ratio_list()

    # Find current range
    i = 0
    for i, rr in enumerate(rr_lst):
        if rr.min_down < down <= rr.max_down:
            break


def required_ratio_list():
    field_names = [
        'min_down', 'max_down', 'required_ratio_0', 'required_ratio_100'
    ]
    RequiredRatio = namedtuple('RequiredRatio', field_names=field_names)

    args_lst = [
        ( 0, 5, 0, 0),
        ( 5, 10, .15, 0),
        ( 10, 20, .20, 0),
        ( 20, 30, .30, .10),
        ( 30, 40, .40, .15),
        ( 40, 50, .50, .20),
        ( 50, 60, .60, .30),
        ( 60, 80, .60, .40),
        ( 80, 100, .60, .50),
        (100, sys.maxsize, .60, .60),
    ]
    return [RequiredRatio(*args) for args in args_lst]

if __name__ == '__main__':
    pass