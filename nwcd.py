import sys

from tracker import additional_down, get_parser


def nwcd_required_ratio_args():
    return [
        (0, 5, 0, 0),
        (5, 10, 0.15, 0),
        (10, 20, 0.20, 0),
        (20, 30, 0.30, 0.10),
        (30, 40, 0.40, 0.15),
        (40, 50, 0.50, 0.20),
        (50, 60, 0.60, 0.30),
        (60, 80, 0.60, 0.40),
        (80, 100, 0.60, 0.50),
        (100, sys.maxsize, 0.60, 0.60),
    ]


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    results = additional_down(
        tracker_tiers=nwcd_required_ratio_args(),
        up=args.up,
        down=args.down,
        min_new_fraction_seeded=args.min_new_fraction_seeded,
    )

    print(results)
