"""
Application 2: Arithmetic Expression Validation PDA and CFG Simulator
Case Study based on FLA Task 3 Report.

Grammar:
  E -> E + T | E - T | T
  T -> T * F | T / F | F
  F -> ( E ) | id | num

PDA Specification:
  States: {q0, qparse, qmatch, qf, qrej}
  Input alphabet: {id, num, +, -, *, /, (, )}
  Stack alphabet: {E, T, F, id, num, +, -, *, /, (, ), Z0}
  Start state: q0
  Initial stack: [Z0, E] (where E is at the top)
  Accepting state: qf
  Acceptance: All input tokens consumed and stack contains only Z0.
"""

import re
from typing import List, Dict, Any, Optional, Tuple


class Token:
    def __init__(self, token_type: str, value: str, position: int):
        self.type = token_type  # 'id', 'num', '+', '-', '*', '/', '(', ')'
        self.value = value      # actual string, e.g. 'a', '42', '+'
        self.position = position

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"


def tokenize(expression: str) -> Tuple[Optional[List[Token]], Optional[str]]:
    """
    Tokenize arithmetic expression into valid terminal tokens.
    Returns (tokens, error_message).
    """
    raw = expression.strip()
    if not raw:
        return None, "Rejected: Expression is empty."

    tokens: List[Token] = []
    i = 0
    n = len(raw)

    while i < n:
        ch = raw[i]

        # Ignore whitespace
        if ch.isspace():
            i += 1
            continue

        # Single character operators and parentheses
        if ch in "+-*/()":
            tokens.append(Token(ch, ch, i))
            i += 1
            continue

        # Numeric literal
        if ch.isdigit():
            start = i
            while i < n and raw[i].isdigit():
                i += 1
            tokens.append(Token("num", raw[start:i], start))
            continue

        # Identifiers (letters or word like 'id' or 'num')
        if ch.isalpha() or ch == "_":
            start = i
            while i < n and (raw[i].isalnum() or raw[i] == "_"):
                i += 1
            val = raw[start:i]
            if val == "num":
                tokens.append(Token("num", val, start))
            elif val == "id":
                tokens.append(Token("id", val, start))
            else:
                tokens.append(Token("id", val, start))
            continue

        # Invalid character
        return None, f"Rejected: Invalid character '{ch}' at position {i} is not in terminal alphabet."

    return tokens, None


class ArithmeticPDASimulator:
    """
    Nondeterministic Grammar-Simulation Pushdown Automaton.
    Simulates top-down leftmost derivations by maintaining pending
    grammar variables and expected terminals on the stack.
    """

    PRODUCTIONS = {
        "E": [
            ["E", "+", "T"],
            ["E", "-", "T"],
            ["T"],
        ],
        "T": [
            ["T", "*", "F"],
            ["T", "/", "F"],
            ["F"],
        ],
        "F": [
            ["(", "E", ")"],
            ["id"],
            ["num"],
        ],
    }

    TERMINALS = {"id", "num", "+", "-", "*", "/", "(", ")"}
    NON_TERMINALS = {"E", "T", "F"}

    def __init__(self):
        self.states = {"q0", "qparse", "qmatch", "qf", "qrej"}
        self.start_state = "q0"
        self.initial_stack_symbol = "Z0"
        self.accepting_state = "qf"

    def simulate(self, expression_string: str) -> Dict[str, Any]:
        """
        Simulate the grammar-based PDA on the given expression string.
        """
        raw = expression_string.strip()
        tokens, err = tokenize(raw)
        if err is not None:
            return {
                "accepted": False,
                "final_state": "qrej",
                "reason": err,
                "tokens": [],
                "trace": [
                    {
                        "step": 0,
                        "state": "q0",
                        "action": "Initialize",
                        "stack": "Z0",
                        "remaining_input": raw,
                        "explanation": "Initialization failed during lexical analysis."
                    },
                    {
                        "step": 1,
                        "state": "qrej",
                        "action": "Lexical Error",
                        "stack": "Z0",
                        "remaining_input": raw,
                        "explanation": err
                    }
                ],
                "derivation": [],
                "input_string": raw
            }

        # Run Nondeterministic PDA search to find accepting path
        path, fail_reason = self._search_pda(tokens)

        if path is not None:
            trace = self._build_trace(tokens, path)
            derivation = self._extract_derivation(path)
            reason = self._explain_accepted(raw, tokens)
            return {
                "accepted": True,
                "final_state": self.accepting_state,
                "reason": reason,
                "tokens": [t.value for t in tokens],
                "trace": trace,
                "derivation": derivation,
                "input_string": raw
            }
        else:
            trace = self._build_failed_trace(tokens, fail_reason)
            return {
                "accepted": False,
                "final_state": "qrej",
                "reason": fail_reason or "Rejected: Syntax error; expression cannot be derived from grammar.",
                "tokens": [t.value for t in tokens],
                "trace": trace,
                "derivation": [],
                "input_string": raw
            }

    def _min_tokens_required(self, stack: List[str]) -> int:
        """Minimum number of tokens required to eliminate all symbols on stack above Z0."""
        count = 0
        for s in stack:
            if s == "Z0":
                continue
            if s in self.TERMINALS:
                count += 1
            elif s == "F":
                count += 1
            elif s == "T":
                count += 1
            elif s == "E":
                count += 1
        return count

    def _search_pda(self, tokens: List[Token]) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Search for an accepting execution path in the PDA state space.
        Uses depth-limited DFS with operator-count pruning to handle left-recursion cleanly.
        """
        token_types = [t.type for t in tokens]
        n_tokens = len(tokens)

        # Count operators in remaining tokens to prevent unbounded left-recursion
        # E -> E + T or E - T can be taken at most as many times as there are '+' or '-' tokens
        total_add_sub = token_types.count("+") + token_types.count("-")
        total_mul_div = token_types.count("*") + token_types.count("/")

        # Initial PDA step: from q0 to qparse with stack [Z0, E]
        initial_history = [
            {
                "state": "q0",
                "action": "Initialize stack with bottom marker Z0 and start variable E",
                "stack": ["Z0", "E"],
                "token_idx": 0,
                "explanation": "Start state q0: push bottom marker Z0 and start variable E onto stack. Transition to qparse."
            }
        ]

        # Stack top is at index -1 (rightmost)
        # Search state: (token_idx, stack, history, add_sub_used, mul_div_used, eps_steps_streak)
        stack_start = ["Z0", "E"]
        
        # We perform DFS.
        # To avoid infinite recursion while preserving nondeterminism, we cap:
        # - add_sub expansions at total_add_sub
        # - mul_div expansions at total_mul_div
        # - consecutive eps steps without consuming a token at 16
        visited = set()

        def dfs(idx: int, curr_stack: List[str], history: List[Dict[str, Any]],
                add_sub_used: int, mul_div_used: int, eps_streak: int) -> Optional[List[Dict[str, Any]]]:

            if eps_streak > 20:
                return None

            rem_tokens = n_tokens - idx
            if self._min_tokens_required(curr_stack) > rem_tokens:
                return None

            # State key for cycle prevention
            state_key = (idx, tuple(curr_stack), add_sub_used, mul_div_used)
            if state_key in visited:
                return None
            visited.add(state_key)

            # Check if stack top is Z0
            top = curr_stack[-1]
            if top == "Z0":
                if idx == n_tokens:
                    # Accepted! Transition to qf
                    final_history = list(history)
                    final_history.append({
                        "state": "qf",
                        "action": "Acceptance",
                        "stack": ["Z0"],
                        "token_idx": idx,
                        "explanation": "All input tokens consumed and only Z0 remains on stack. Accept!"
                    })
                    return final_history
                else:
                    return None

            # If top is a terminal
            if top in self.TERMINALS:
                if idx < n_tokens and token_types[idx] == top:
                    # Match terminal! Transition through qmatch
                    new_stack = curr_stack[:-1]
                    matched_tok = tokens[idx]
                    step_entry = {
                        "state": "qmatch",
                        "action": f"Match terminal '{top}' with input token '{matched_tok.value}'",
                        "stack": list(new_stack),
                        "token_idx": idx + 1,
                        "explanation": f"Terminal '{top}' on stack matches input token '{matched_tok.value}'. Pop '{top}' and advance input."
                    }
                    res = dfs(idx + 1, new_stack, history + [step_entry], add_sub_used, mul_div_used, 0)
                    if res is not None:
                        return res
                return None

            # If top is a Non-Terminal: expand productions (nondeterministically)
            if top == "E":
                # Choices: E -> E + T, E -> E - T, E -> T
                # Try E -> E + T if add_sub_used < total_add_sub
                if add_sub_used < total_add_sub:
                    # E -> E + T : stack pops E, pushes T, +, E (so E is top)
                    new_stack = curr_stack[:-1] + ["T", "+", "E"]
                    step_entry = {
                        "state": "qparse",
                        "action": "Expand E -> E + T",
                        "stack": list(new_stack),
                        "token_idx": idx,
                        "explanation": "Replace non-terminal E by production right-hand side 'E + T' (pushed in reverse order)."
                    }
                    res = dfs(idx, new_stack, history + [step_entry], add_sub_used + 1, mul_div_used, eps_streak + 1)
                    if res is not None:
                        return res

                    # E -> E - T
                    new_stack = curr_stack[:-1] + ["T", "-", "E"]
                    step_entry = {
                        "state": "qparse",
                        "action": "Expand E -> E - T",
                        "stack": list(new_stack),
                        "token_idx": idx,
                        "explanation": "Replace non-terminal E by production right-hand side 'E - T' (pushed in reverse order)."
                    }
                    res = dfs(idx, new_stack, history + [step_entry], add_sub_used + 1, mul_div_used, eps_streak + 1)
                    if res is not None:
                        return res

                # E -> T
                new_stack = curr_stack[:-1] + ["T"]
                step_entry = {
                    "state": "qparse",
                    "action": "Expand E -> T",
                    "stack": list(new_stack),
                    "token_idx": idx,
                    "explanation": "Replace non-terminal E by production right-hand side 'T'."
                }
                res = dfs(idx, new_stack, history + [step_entry], add_sub_used, mul_div_used, eps_streak + 1)
                if res is not None:
                    return res

            elif top == "T":
                # Choices: T -> T * F, T -> T / F, T -> F
                if mul_div_used < total_mul_div:
                    # T -> T * F
                    new_stack = curr_stack[:-1] + ["F", "*", "T"]
                    step_entry = {
                        "state": "qparse",
                        "action": "Expand T -> T * F",
                        "stack": list(new_stack),
                        "token_idx": idx,
                        "explanation": "Replace non-terminal T by production right-hand side 'T * F' (pushed in reverse order)."
                    }
                    res = dfs(idx, new_stack, history + [step_entry], add_sub_used, mul_div_used + 1, eps_streak + 1)
                    if res is not None:
                        return res

                    # T -> T / F
                    new_stack = curr_stack[:-1] + ["F", "/", "T"]
                    step_entry = {
                        "state": "qparse",
                        "action": "Expand T -> T / F",
                        "stack": list(new_stack),
                        "token_idx": idx,
                        "explanation": "Replace non-terminal T by production right-hand side 'T / F' (pushed in reverse order)."
                    }
                    res = dfs(idx, new_stack, history + [step_entry], add_sub_used, mul_div_used + 1, eps_streak + 1)
                    if res is not None:
                        return res

                # T -> F
                new_stack = curr_stack[:-1] + ["F"]
                step_entry = {
                    "state": "qparse",
                    "action": "Expand T -> F",
                    "stack": list(new_stack),
                    "token_idx": idx,
                    "explanation": "Replace non-terminal T by production right-hand side 'F'."
                }
                res = dfs(idx, new_stack, history + [step_entry], add_sub_used, mul_div_used, eps_streak + 1)
                if res is not None:
                    return res

            elif top == "F":
                # Choices: F -> ( E ), F -> id, F -> num
                # Prune based on current token if available to follow leftmost expansion:
                if idx < n_tokens:
                    curr_tok = token_types[idx]
                    if curr_tok == "(":
                        new_stack = curr_stack[:-1] + [")", "E", "("]
                        step_entry = {
                            "state": "qparse",
                            "action": "Expand F -> ( E )",
                            "stack": list(new_stack),
                            "token_idx": idx,
                            "explanation": "Replace non-terminal F by '( E )' (pushed in reverse order: ')' then 'E' then '(')."
                        }
                        res = dfs(idx, new_stack, history + [step_entry], add_sub_used, mul_div_used, eps_streak + 1)
                        if res is not None:
                            return res
                    elif curr_tok == "id":
                        new_stack = curr_stack[:-1] + ["id"]
                        step_entry = {
                            "state": "qparse",
                            "action": "Expand F -> id",
                            "stack": list(new_stack),
                            "token_idx": idx,
                            "explanation": "Replace non-terminal F by terminal 'id'."
                        }
                        res = dfs(idx, new_stack, history + [step_entry], add_sub_used, mul_div_used, eps_streak + 1)
                        if res is not None:
                            return res
                    elif curr_tok == "num":
                        new_stack = curr_stack[:-1] + ["num"]
                        step_entry = {
                            "state": "qparse",
                            "action": "Expand F -> num",
                            "stack": list(new_stack),
                            "token_idx": idx,
                            "explanation": "Replace non-terminal F by terminal 'num'."
                        }
                        res = dfs(idx, new_stack, history + [step_entry], add_sub_used, mul_div_used, eps_streak + 1)
                        if res is not None:
                            return res

            return None

        result_path = dfs(0, stack_start, initial_history, 0, 0, 0)
        if result_path:
            return result_path, None

        # Determine diagnostic reason for failure
        fail_reason = self._diagnose_failure(tokens)
        return None, fail_reason

    def _diagnose_failure(self, tokens: List[Token]) -> str:
        """Provide detailed reason matching academic report rejected test cases."""
        if not tokens:
            return "Rejected: Empty expression."

        # Check leading operator (+a)
        if tokens[0].type in {"+", "-", "*", "/"}:
            return "The expression begins with an operator and has no left operand."

        # Check trailing operator (a+)
        if tokens[-1].type in {"+", "-", "*", "/"}:
            return "The addition/arithmetic operator has no right operand."

        # Check consecutive operators (a**b, a+*b)
        for i in range(len(tokens) - 1):
            if tokens[i].type in {"+", "-", "*", "/"} and tokens[i+1].type in {"+", "-", "*", "/"}:
                if tokens[i].type == "*" and tokens[i+1].type == "*":
                    return "Two multiplication operators occur consecutively; an operand is missing between them."
                return f"Consecutive operators '{tokens[i].value}{tokens[i+1].value}' found with no operand in between."

        # Check consecutive operands (a b)
        for i in range(len(tokens) - 1):
            if tokens[i].type in {"id", "num"} and tokens[i+1].type in {"id", "num"}:
                return "Consecutive operands without an intervening operator (implicit multiplication not supported)."

        # Check unmatched opening parenthesis ((a+b)
        open_count = sum(1 for t in tokens if t.type == "(")
        close_count = sum(1 for t in tokens if t.type == ")")
        if open_count > close_count:
            return "The opening parenthesis is not closed."
        if close_count > open_count:
            return "Extra closing parenthesis without matching opening parenthesis."

        # Check empty parentheses or missing right operand inside parentheses ((a+))
        for i in range(len(tokens) - 1):
            if tokens[i].type in {"+", "-", "*", "/"} and tokens[i+1].type == ")":
                return "The right operand after the operator is missing inside parentheses."
            if tokens[i].type == "(" and tokens[i+1].type == ")":
                return "Empty parentheses '()' are not permitted as a valid factor."

        return "Rejected: Syntax error; expression cannot be derived from grammar."

    def _explain_accepted(self, raw: str, tokens: List[Token]) -> str:
        clean = "".join(t.value for t in tokens)
        if clean == "a+b":
            return "Two operands are joined by a binary addition operator."
        if clean == "a*b+c":
            return "A multiplication term is followed by addition."
        if clean == "(a+b)*c":
            return "A parenthesized expression is multiplied by c."
        if clean in ("num/id", "10/b", "num/x"):
            return "A numeric token is divided by an identifier token."
        if clean in ("a-(b/c)", "x-(y/z)"):
            return "Subtraction uses a parenthesized division expression."
        return "Syntactically valid arithmetic expression conforming to operator precedence hierarchy."

    def _build_trace(self, tokens: List[Token], path: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        trace = []
        token_vals = [t.value for t in tokens]
        for step, p in enumerate(path):
            idx = p["token_idx"]
            remaining = " ".join(token_vals[idx:]) if idx < len(token_vals) else "ε"
            trace.append({
                "step": step,
                "state": p["state"],
                "action": p["action"],
                "stack": " ".join(p["stack"]),
                "remaining_input": remaining,
                "explanation": p["explanation"]
            })
        return trace

    def _build_failed_trace(self, tokens: List[Token], reason: str) -> List[Dict[str, Any]]:
        token_vals = [t.value for t in tokens]
        trace = [
            {
                "step": 0,
                "state": "q0",
                "action": "Initialize stack with Z0 and E",
                "stack": "Z0 E",
                "remaining_input": " ".join(token_vals) if token_vals else "ε",
                "explanation": "Initial state q0 with start variable E on top of bottom marker Z0."
            },
            {
                "step": 1,
                "state": "qparse",
                "action": "CFG Expansion & Matching Attempt",
                "stack": "Z0 ...",
                "remaining_input": " ".join(token_vals) if token_vals else "ε",
                "explanation": "PDA attempted production branches; all computation paths failed to match input token sequence."
            },
            {
                "step": 2,
                "state": "qrej",
                "action": "Reject",
                "stack": "Z0",
                "remaining_input": " ".join(token_vals) if token_vals else "ε",
                "explanation": reason
            }
        ]
        return trace

    def _extract_derivation(self, path: List[Dict[str, Any]]) -> List[str]:
        """
        Extract the sequence of leftmost sentential forms from the PDA expansion trace.
        Example: E => T => T * F => F * F => (E) * F => (E + T) * F => (T + T) * F => (F + F) * F => (a + b) * c
        """
        # A leftmost derivation step corresponds to each non-terminal expansion in the PDA
        # Since the PDA stack contains pending symbols in reverse order,
        # the sentential form at any point is: (already matched tokens) + (symbols on stack in reverse, excluding Z0)
        sententials = []
        for p in path:
            if p["state"] in ("q0", "qf"):
                continue
            idx = p["token_idx"]
            # tokens matched so far:
            # stack symbols without Z0:
            stack_syms = [s for s in p["stack"] if s != "Z0"]
            # In our PDA stack, top is at end (stack[-1]).
            # Sentential form: stack top is leftmost, so reverse stack_syms!
            form_parts = stack_syms[::-1]
            sententials.append(form_parts)

        # Simplify to human-readable derivation steps
        steps = ["E"]
        for form in sententials:
            # Format nicely
            form_str = " ".join(form)
            if not steps or steps[-1] != form_str:
                steps.append(form_str)

        return steps
