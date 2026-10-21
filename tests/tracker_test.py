import argparse
import itertools
import sys

import pytest

from nwcd import nwcd_required_ratio_args
from ptp import ptp_required_ratio_args
from tracker import MaxTier, additional_down, get_parser


@pytest.mark.parametrize("tiers", [nwcd_required_ratio_args, ptp_required_ratio_args])
def test_tiers_are_contiguous_and_rise(tiers):
    rows = tiers()
    assert rows[0][0] == 0
    assert rows[-1][1] == sys.maxsize
    for (_, prev_max, prev_rr0, _), (cur_min, _, cur_rr0, _) in itertools.pairwise(
        rows
    ):
        assert cur_min == prev_max
        assert cur_rr0 >= prev_rr0


def test_additional_down_picks_tier_with_most_room():
    result = additional_down(ptp_required_ratio_args(), up=30, down=50)
    assert result.additional_down == pytest.approx(25)
    assert result.tier.min_down == 60 and result.tier.max_down == 80
    assert result.min_ratio_seeded == pytest.approx(0)


def test_seeding_lowers_required_ratio():
    result = additional_down(
        nwcd_required_ratio_args(), up=30, down=50, min_new_fraction_seeded=0.5
    )
    assert result.additional_down == pytest.approx(25)
    assert (result.tier.min_down, result.tier.max_down) == (60, 80)
    assert result.min_ratio_seeded == pytest.approx(1 / 3)


@pytest.mark.xfail(raises=ZeroDivisionError, strict=True, reason="0% ratio tier")
def test_download_in_first_tier():
    additional_down(ptp_required_ratio_args(), up=1, down=5)


def test_max_tier_str():
    tier = MaxTier(1.23456, "t", 0.5)
    assert str(tier) == "MaxTier(additional_down=1.235, tier=t, min_ratio_seeded=0.500)"


def test_parser_defaults_and_validation(capsys):
    parser = get_parser()
    args = parser.parse_args(["--up", "1.5", "--down", "2"])
    assert (args.up, args.down, args.min_new_fraction_seeded) == (1.5, 2.0, 0)
    for bad in (
        ["--up", "-1", "--down", "2"],
        ["--up", "1", "--down", "2", "--min_new_fraction_seeded", "1.5"],
    ):
        with pytest.raises(SystemExit):
            parser.parse_args(bad)
    assert "invalid" in capsys.readouterr().err
    with pytest.raises(argparse.ArgumentTypeError):
        parser._option_string_actions["--up"].type("-1")
