import sys

from tracker import additional_down, get_parser


def ptp_required_ratio_args():
    return [
        (0, 10, 0, 0),
        (10, 20, .15, .15),
        (20, 40, .20, .20),
        (40, 60, .30, .30),
        (60, 80, .40, .40),
        (80, 100, .50, .50),
        (100, sys.maxsize, .60, .60),
    ]


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    print(additional_down(
        tracker_tiers=ptp_required_ratio_args(),
        up=args.up,
        down=args.down,
        new_fraction_seeded=args.new_fraction_seeded)
    )
