"""
Unit tests for Application 3: Palindrome Recognition Nondeterministic PDA and CFG.
Based strictly on FLA Task 3 Report case study.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from automata.palindrome_pda import PalindromePDA


@pytest.fixture
def pda():
    return PalindromePDA()


def test_accepted_cases_report(pda):
    """Test all accepted examples documented in the Task 3 report."""
    cases = [
        "ε",
        "",
        "a",
        "b",
        "aa",
        "aba",
        "abba",
        "baab",
        "bb",
        "aaaa",
        "aabaa",
    ]
    for s in cases:
        res = pda.simulate(s)
        assert res["accepted"] is True, f"Failed on valid palindrome: {s}"
        assert res["final_state"] == "qf"
        assert len(res["trace"]) > 0


def test_rejected_cases_report(pda):
    """Test all rejected examples documented in the Task 3 report."""
    cases = [
        "ab",
        "aab",
        "abb",
        "abab",
        "aabb",
        "ba",
        "bba",
        "aaba",
    ]
    for s in cases:
        res = pda.simulate(s)
        assert res["accepted"] is False, f"Should reject non-palindrome: {s}"
        assert res["final_state"] == "qrej"
        assert len(res["reason"]) > 0


def test_empty_string(pda):
    """Test empty string and epsilon."""
    res_empty = pda.simulate("")
    assert res_empty["accepted"] is True
    assert res_empty["final_state"] == "qf"

    res_eps = pda.simulate("ε")
    assert res_eps["accepted"] is True
    assert res_eps["final_state"] == "qf"


def test_invalid_tokens(pda):
    """Test characters outside alphabet Σ = {'a', 'b'}."""
    invalid_cases = ["abc", "a1a", "a b", "a#a", "c"]
    for s in invalid_cases:
        res = pda.simulate(s)
        assert res["accepted"] is False
        assert "Invalid character" in res["reason"]


def test_even_and_odd_palindromes(pda):
    """Verify even-length vs odd-length midpoint detection."""
    # Even-length: abba
    res_even = pda.simulate("abba")
    assert res_even["accepted"] is True
    assert res_even["winning_branch"]["type"] == "even"
    assert res_even["winning_branch"]["position"] == 2

    # Odd-length: aba
    res_odd = pda.simulate("aba")
    assert res_odd["accepted"] is True
    assert res_odd["winning_branch"]["type"] == "odd"
    assert res_odd["winning_branch"]["position"] == 1


def test_nondeterministic_branch_exploration(pda):
    """Verify that multiple branches are explored nondeterministically."""
    res = pda.simulate("abba")
    assert "branches" in res
    # For length 4: even midpoints at 0,1,2,3,4 (5 branches) + odd midpoints at 0,1,2,3 (4 branches) = 9 branches
    assert len(res["branches"]) == 9


def test_cfg_derivation_palindrome():
    """Verify CFG derivation for abba and aba."""
    deriv_abba = PalindromePDA.get_cfg_derivation(list("abba"))
    assert deriv_abba[0] == "S"
    assert deriv_abba[-1] == "abba"

    deriv_aba = PalindromePDA.get_cfg_derivation(list("aba"))
    assert deriv_aba[0] == "S"
    assert deriv_aba[-1] == "aba"
