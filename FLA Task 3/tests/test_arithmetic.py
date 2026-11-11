"""
Unit tests for Application 2: Arithmetic Expression Validation PDA and CFG.
Based strictly on FLA Task 3 Report case study.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from automata.arithmetic_parser import ArithmeticPDASimulator, tokenize


@pytest.fixture
def sim():
    return ArithmeticPDASimulator()


def test_accepted_cases_report(sim):
    """Test all accepted examples documented in the Task 3 report."""
    cases = [
        "a+b",
        "a*b+c",
        "(a+b)*c",
        "num/id",
        "a-(b/c)",
        "x+y-z",
        "a*b*c",
        "id",
        "num",
        "(a)",
        "((a+b))",
    ]
    for expr in cases:
        res = sim.simulate(expr)
        assert res["accepted"] is True, f"Failed on valid expression: {expr}. Reason: {res['reason']}"
        assert res["final_state"] == "qf"
        assert len(res["trace"]) > 0


def test_rejected_cases_report(sim):
    """Test all rejected examples documented in the Task 3 report."""
    cases = [
        ("+a", "begins with an operator"),
        ("a+", "has no right operand"),
        ("a**b", "consecutive"),
        ("(a+b", "opening parenthesis is not closed"),
        ("a b", "Consecutive operands"),
        ("a+*b", "Consecutive operators"),
        ("(a+)", "right operand"),
    ]
    for expr, keyword in cases:
        res = sim.simulate(expr)
        assert res["accepted"] is False, f"Should reject invalid expression: {expr}"
        assert res["final_state"] == "qrej"
        assert keyword.lower() in res["reason"].lower(), f"Expected keyword '{keyword}' in '{res['reason']}'"


def test_empty_expression(sim):
    """Test empty string and whitespace-only expression."""
    res_empty = sim.simulate("")
    assert res_empty["accepted"] is False
    assert "empty" in res_empty["reason"].lower()

    res_ws = sim.simulate("   ")
    assert res_ws["accepted"] is False


def test_invalid_tokens(sim):
    """Test expressions containing invalid lexical tokens."""
    invalid_cases = ["a $ b", "a @ b", "a # b", "a & b", "a % b"]
    for expr in invalid_cases:
        res = sim.simulate(expr)
        assert res["accepted"] is False
        assert "Invalid character" in res["reason"]


def test_nested_expressions(sim):
    """Test deeply nested arithmetic expressions."""
    res = sim.simulate("((a+b)*(c-(d/e)))")
    assert res["accepted"] is True
    assert res["final_state"] == "qf"


def test_derivation_generation(sim):
    """Verify derivation is produced for (a+b)*c."""
    res = sim.simulate("(a+b)*c")
    assert res["accepted"] is True
    deriv = res["derivation"]
    assert len(deriv) > 0
    assert deriv[0] == "E"


def test_tokenization_whitespace_tolerance():
    """Verify whitespace handling."""
    tokens, err = tokenize("  a   +   b  *   c  ")
    assert err is None
    assert [t.value for t in tokens] == ["a", "+", "b", "*", "c"]
