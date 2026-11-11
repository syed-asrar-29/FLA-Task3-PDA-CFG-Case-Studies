"""
Unit tests for Application 1: Balanced Parentheses PDA and CFG.
Based strictly on FLA Task 3 Report case study.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from automata.balanced_parentheses import BalancedParenthesesPDA


@pytest.fixture
def pda():
    return BalancedParenthesesPDA()


def test_accepted_cases_report(pda):
    """Test all accepted examples documented in the Task 3 report."""
    cases = [
        "()",
        "(())",
        "()()",
        "(()())",
        "ε",
        "",
        "((()))",
        "(()(()))",
    ]
    for s in cases:
        result = pda.simulate(s)
        assert result["accepted"] is True, f"Failed on valid string: {s}"
        assert result["final_state"] == "qf"
        assert len(result["trace"]) > 0


def test_rejected_cases_report(pda):
    """Test all rejected examples documented in the Task 3 report."""
    cases = [
        "(",
        ")",
        "(()",
        "())",
        "())(",
        ")(",
        "((())",
        "(()))",
    ]
    for s in cases:
        result = pda.simulate(s)
        assert result["accepted"] is False, f"Should reject invalid string: {s}"
        assert result["final_state"] == "qrej"
        assert len(result["reason"]) > 0


def test_empty_string(pda):
    """Test empty string and epsilon notation."""
    res_empty = pda.simulate("")
    assert res_empty["accepted"] is True
    assert res_empty["final_state"] == "qf"

    res_eps = pda.simulate("ε")
    assert res_eps["accepted"] is True
    assert res_eps["final_state"] == "qf"


def test_invalid_characters(pda):
    """Test inputs with characters outside alphabet Σ = {'(', ')'}."""
    invalid_cases = ["(a)", "()1", " ", "(+)", "()@"]
    for s in invalid_cases:
        res = pda.simulate(s)
        assert res["accepted"] is False
        assert "Invalid character" in res["reason"]


def test_stack_trace_detailed(pda):
    """Verify exact step-by-step stack trace for input (())."""
    res = pda.simulate("(())")
    assert res["accepted"] is True
    trace = res["trace"]
    # Trace should have:
    # Step 0: Start, stack Z0
    # Step 1: (, stack Z0 X
    # Step 2: (, stack Z0 X X
    # Step 3: ), stack Z0 X
    # Step 4: ), stack Z0
    # Step 5: End, stack Z0, state qf
    assert trace[0]["stack"] == "Z0"
    assert trace[1]["stack"] == "Z0 X"
    assert trace[2]["stack"] == "Z0 X X"
    assert trace[3]["stack"] == "Z0 X"
    assert trace[4]["stack"] == "Z0"
    assert trace[5]["stack"] == "Z0"
    assert trace[5]["state"] == "qf"


def test_cfg_derivation():
    """Verify CFG leftmost derivation generation for (()())."""
    deriv = BalancedParenthesesPDA.get_cfg_derivation("(()())")
    assert len(deriv) > 1
    assert deriv[0] == "S"
    assert deriv[-1] == "(()())"
