import argparse
import functools
from collections import namedtuple


class MaxTier(namedtuple(
    'MaxTier', field_names=['additional_down', 'tier', 'min_ratio_seeded']
)):
    def __str__(self):
        f = 'MaxTier(additional_down={:.3f}, tier={}, min_ratio_seeded={:.3f})'
        return f.format(self.additional_down, self.tier, self.min_ratio_seeded)


def additional_down(tracker_tiers, up, down, min_new_fraction_seeded=0):
    """
    Returns three related quantities:
    1. maximum amount of additional data that can be downloaded
    2. required ratio range that this amount corresponds to
    3. minimum fraction seeded acceptable given previous two quantities

    :param tracker_tiers: List of required ratio tiers for the tracker
    :param up: amount of data uploaded in gigabytes
    :param down: amount of data downloaded in gigabytes
    :param min_new_fraction_seeded: min ratio of seeded divided by snatched
    after downloading additional data. Must be between 0 and 1, inclusive
    """
    rr_list = _required_ratio_list(tracker_tiers)

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
        new_fraction_seeded=min_new_fraction_seeded
    )
    func = functools.partial(_additional_down, **func_kwargs)
    add_down = list(map(func, rr_list[i:]))

    # Find required ratio range with highest additional download
    max_add_down = max(add_down)
    inc_i = add_down.index(max_add_down)
    rr = rr_list[i + inc_i]

    # Return another namedtuple
    field_names = ['additional_down', 'tier', 'min_ratio_seeded']
    # MaxTier = namedtuple('MaxTier', field_names=field_names)
    return MaxTier(max_add_down, rr, _min_ratio_seeded(rr, up))


def _required_ratio_list(argument_list):
    field_names = [
        'min_down', 'max_down', 'required_ratio_0', 'required_ratio_100'
    ]
    RequiredRatio = namedtuple('RequiredRatio', field_names=field_names)

    return [RequiredRatio(*args) for args in argument_list]


def _additional_down(required_ratio_obj, up, down, new_fraction_seeded):
    ratio_down = up / _ratio(required_ratio_obj, new_fraction_seeded)
    max_down = min(required_ratio_obj.max_down, ratio_down)
    return max_down - down


def _ratio(required_ratio_obj, new_fraction_seeded):
    calc_rr = required_ratio_obj.required_ratio_0 * (1 - new_fraction_seeded)
    return max(calc_rr, required_ratio_obj.required_ratio_100)


def _min_ratio_seeded(required_ratio_obj, up):
    calc_ratio = up / required_ratio_obj.max_down
    max_ratio = max(calc_ratio, required_ratio_obj.required_ratio_100)
    return max(0, 1 - max_ratio / required_ratio_obj.required_ratio_0)


def get_parser():
    """
    :return: argparse.ArgumentParser
    """
    desc = 'Calculate max additional download'
    p = argparse.ArgumentParser(description=desc)
    p.add_argument('--up', type=_nonnegative_float, required=True)
    p.add_argument('--down', type=_nonnegative_float, required=True)
    p.add_argument(
        '--min_new_fraction_seeded',
        type=_fraction_float,
        required=False,
        default=0
    )

    return p


def _nonnegative_float(value):
    f_val = float(value)

    if f_val < 0:
        msg_fmt = '%s is an invalid nonnegative float value'
        raise argparse.ArgumentTypeError(msg_fmt % value)

    return f_val


def _fraction_float(value):
    f_val = float(value)

    if not 0 <= f_val <= 1:
        msg_fmt = '{} is an invalid fraction between 0 and 1'
        raise argparse.ArgumentTypeError(msg_fmt.format(f_val))

    return f_val