import argparse
from collections import namedtuple
import functools
import sys


def additional_down(up, down, new_fraction_seeded=0):
    """
    Returns two related quantities:
    1. the maximum amount of additional data that can be downloaded
    2. the required ratio range that this amount corresponds to

    :param up: amount of data uploaded in gigabytes
    :param down: amount of data downloaded in gigabytes
    :param new_fraction_seeded: ratio of seeded divided by snatched after 
    downloading additional data. Must be between 0 and 1, inclusive
    """
    if not 0 <= new_fraction_seeded <= 1:
        msg_fmt = 'Expected 0 <= new_fraction_seeded <= 1 but received: '
        raise ValueError(msg_fmt.format(new_fraction_seeded))

    rr_list = required_ratio_list()

    # Find current required ratio range
    i = 0
    for i, rr in enumerate(rr_list):
        if rr.min_down < down <= rr.max_down:
            break

    # For current required ratio range and higher, calculate maximum amount of
    # data that can be downloaded
    func_kwargs = dict(
        up=up,
        down=down,
        new_fraction_seeded=new_fraction_seeded
    )
    func = functools.partial(_additional_down, **func_kwargs)
    add_down = list(map(func, rr_list[i:]))

    # Find required ratio range with highest additional download and return
    max_add_down = max(add_down)
    inc_i = add_down.index(max_add_down)
    return max_add_down, rr_list[i + inc_i]


def _additional_down(required_ratio_obj, up, down, new_fraction_seeded):
    ratio_down = up / _ratio(required_ratio_obj, new_fraction_seeded)
    max_down = min(required_ratio_obj.max_down, ratio_down)
    return max_down - down


def _ratio(required_ratio_obj, new_fraction_seeded):
    calc_rr = required_ratio_obj.required_ratio_0 * (1 - new_fraction_seeded)
    return max(calc_rr, required_ratio_obj.required_ratio_100)


def required_ratio_list():
    field_names = [
        'min_down', 'max_down', 'required_ratio_0', 'required_ratio_100'
    ]
    RequiredRatio = namedtuple('RequiredRatio', field_names=field_names)

    args_lst = [
        (0, 5, 0, 0),
        (5, 10, .15, 0),
        (10, 20, .20, 0),
        (20, 30, .30, .10),
        (30, 40, .40, .15),
        (40, 50, .50, .20),
        (50, 60, .60, .30),
        (60, 80, .60, .40),
        (80, 100, .60, .50),
        (100, sys.maxsize, .60, .60),
    ]
    return [RequiredRatio(*args) for args in args_lst]

if __name__ == '__main__':
    desc = 'Calculate max additional download'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--up', type=float, required=True)
    parser.add_argument('--down', type=float, required=True)
    parser.add_argument('--new_fraction_seeded', type=float, required=True)

    args = parser.parse_args()

    print(additional_down(args.up, args.down, args.new_fraction_seeded))
