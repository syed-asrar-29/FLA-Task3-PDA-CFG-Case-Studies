"""
Application 3: Palindrome Recognition Nondeterministic PDA and CFG Simulator
Case Study based on FLA Task 3 Report.

Alphabet: Σ = { 'a', 'b' }
Stack Alphabet: Γ = { Z0, 'a', 'b' }
States: {qstart, qpush, qmatch, qf, qrej}
CFG:
  S -> aSa | bSb | a | b | ε

PDA Behavior:
  1. qstart: Initial state with bottom marker Z0. Transitions to qpush via ε.
  2. qpush: Read and push symbols onto stack.
     Nondeterministically guesses the midpoint:
     - Even-length midpoint guess: ε-transition to qmatch without consuming input.
     - Odd-length midpoint guess: reads 1 symbol (the central character) without pushing, transitions to qmatch.
  3. qmatch: Compare remaining input symbols against top of stack and pop.
  4. qf: Reached when all input is consumed and stack contains only Z0.
"""

from typing import List, Dict, Any, Optional, Tuple


class PalindromePDA:
    """
    Nondeterministic Pushdown Automaton for Palindrome Recognition over {a, b}.
    Explicitly simulates nondeterministic branch exploration.
    """

    def __init__(self):
        self.states = {"qstart", "qpush", "qmatch", "qf", "qrej"}
        self.input_alphabet = {"a", "b"}
        self.stack_alphabet = {"Z0", "a", "b"}
        self.start_state = "qstart"
        self.initial_stack_symbol = "Z0"
        self.accepting_state = "qf"

    def simulate(self, input_string: str) -> Dict[str, Any]:
        """
        Simulate all nondeterministic execution branches of the PDA.
        Returns detailed branch exploration and the trace of the accepted path
        (or best diagnostic trace if rejected).
        """
        if input_string == "" or input_string.strip() in ("ε", "epsilon", "EPSILON"):
            tokens = []
            display_input = "ε"
        else:
            tokens = list(input_string)
            display_input = input_string

        # Alphabet check
        for idx, ch in enumerate(tokens):
            if ch not in self.input_alphabet:
                return {
                    "accepted": False,
                    "final_state": "qrej",
                    "reason": f"Rejected: Invalid character '{ch}' at position {idx+1}. Alphabet Σ is restricted to {{'a', 'b'}}.",
                    "branches": [],
                    "trace": [
                        {
                            "step": 0,
                            "state": "qstart",
                            "input_action": "Start",
                            "stack": "Z0",
                            "explanation": "Initial bottom marker."
                        },
                        {
                            "step": 1,
                            "state": "qrej",
                            "input_action": f"Invalid '{ch}'",
                            "stack": "Z0",
                            "explanation": f"Character '{ch}' is not in alphabet Σ = {{'a', 'b'}}."
                        }
                    ],
                    "derivation": [],
                    "input_string": display_input
                }

        # Explore all possible midpoint guess branches
        n = len(tokens)
        all_branches: List[Dict[str, Any]] = []
        accepted_branch: Optional[Dict[str, Any]] = None

        # 1. Even-length midpoint guesses at position k in [0..n]
        # Push tokens[0..k-1], guess even midpoint at k, match tokens[k..n-1]
        for k in range(n + 1):
            branch_info = self._simulate_branch(tokens, midpoint_type="even", midpoint_pos=k)
            all_branches.append(branch_info)
            if branch_info["accepted"] and accepted_branch is None:
                accepted_branch = branch_info

        # 2. Odd-length midpoint guesses at position k in [0..n-1]
        # Push tokens[0..k-1], consume tokens[k] as center, match tokens[k+1..n-1]
        for k in range(n):
            branch_info = self._simulate_branch(tokens, midpoint_type="odd", midpoint_pos=k)
            all_branches.append(branch_info)
            if branch_info["accepted"] and accepted_branch is None:
                accepted_branch = branch_info

        if accepted_branch:
            reason = self._explain_accepted(display_input, n)
            derivation = self.get_cfg_derivation(tokens)
            return {
                "accepted": True,
                "final_state": self.accepting_state,
                "reason": reason,
                "branches": all_branches,
                "trace": accepted_branch["trace"],
                "derivation": derivation,
                "winning_branch": {
                    "type": accepted_branch["midpoint_type"],
                    "position": accepted_branch["midpoint_pos"],
                    "description": accepted_branch["description"]
                },
                "input_string": display_input
            }
        else:
            # Pick the most illustrative failed branch (the midpoint closest to n/2)
            best_failed_trace = self._get_best_failed_trace(all_branches, n)
            reason = self._explain_rejected(display_input)
            return {
                "accepted": False,
                "final_state": "qrej",
                "reason": reason,
                "branches": all_branches,
                "trace": best_failed_trace,
                "derivation": [],
                "winning_branch": None,
                "input_string": display_input
            }

    def _simulate_branch(self, tokens: List[str], midpoint_type: str, midpoint_pos: int) -> Dict[str, Any]:
        """
        Simulate one specific nondeterministic branch choice.
        """
        n = len(tokens)
        stack = [self.initial_stack_symbol]
        trace = []
        step = 0

        # Step 0: qstart
        trace.append({
            "step": step,
            "state": "qstart",
            "input_action": "Start",
            "stack": " ".join(stack),
            "explanation": "Initial bottom marker."
        })

        # Phase 1: Push phase up to midpoint_pos
        current_state = "qpush"
        for i in range(midpoint_pos):
            step += 1
            sym = tokens[i]
            stack.append(sym)
            trace.append({
                "step": step,
                "state": "qpush",
                "input_action": f"Read {sym}; push {sym}",
                "stack": " ".join(stack),
                "explanation": f"Store symbol '{sym}' (index {i+1}) on stack."
            })

        # Phase 2: Midpoint transition
        match_start_idx = midpoint_pos
        if midpoint_type == "even":
            step += 1
            current_state = "qmatch"
            trace.append({
                "step": step,
                "state": "qmatch",
                "input_action": "Guess even midpoint (ε-transition)",
                "stack": " ".join(stack),
                "explanation": "Switch to matching phase without consuming input (even-length center)."
            })
            match_start_idx = midpoint_pos

        elif midpoint_type == "odd":
            step += 1
            current_state = "qmatch"
            center_sym = tokens[midpoint_pos]
            trace.append({
                "step": step,
                "state": "qmatch",
                "input_action": f"Read {center_sym}; guess odd midpoint",
                "stack": " ".join(stack),
                "explanation": f"Consume middle symbol '{center_sym}' without pushing it; switch to matching phase."
            })
            match_start_idx = midpoint_pos + 1

        # Phase 3: Match phase
        branch_failed = False
        fail_msg = ""
        for i in range(match_start_idx, n):
            step += 1
            sym = tokens[i]
            if len(stack) <= 1:
                # Stack underflow (only Z0 remains, but input still left)
                branch_failed = True
                fail_msg = f"Premature stack exhaustion: read '{sym}' while stack has only Z0."
                trace.append({
                    "step": step,
                    "state": "qrej",
                    "input_action": f"Read {sym}; underflow",
                    "stack": " ".join(stack),
                    "explanation": fail_msg
                })
                break

            top = stack[-1]
            if top == sym:
                stack.pop()
                trace.append({
                    "step": step,
                    "state": "qmatch",
                    "input_action": f"Read {sym}; match and pop",
                    "stack": " ".join(stack),
                    "explanation": f"The input {sym} matches the stack top {top}."
                })
            else:
                branch_failed = True
                fail_msg = f"Mismatch: input '{sym}' does not match stack top '{top}'."
                trace.append({
                    "step": step,
                    "state": "qrej",
                    "input_action": f"Read {sym}; mismatch with top '{top}'",
                    "stack": " ".join(stack),
                    "explanation": fail_msg
                })
                break

        # Phase 4: Acceptance check
        if not branch_failed:
            step += 1
            if stack == [self.initial_stack_symbol]:
                current_state = "qf"
                trace.append({
                    "step": step,
                    "state": "qf",
                    "input_action": "End of input",
                    "stack": " ".join(stack),
                    "explanation": "Input consumed and stack restored to bottom marker: accept."
                })
                return {
                    "accepted": True,
                    "midpoint_type": midpoint_type,
                    "midpoint_pos": midpoint_pos,
                    "description": f"Guessed {midpoint_type} midpoint at position {midpoint_pos}",
                    "trace": trace,
                    "final_stack": list(stack)
                }
            else:
                fail_msg = f"Input ended but stack retained unmatched symbols: {' '.join(stack)}."
                trace.append({
                    "step": step,
                    "state": "qrej",
                    "input_action": "End of input",
                    "stack": " ".join(stack),
                    "explanation": fail_msg
                })

        return {
            "accepted": False,
            "midpoint_type": midpoint_type,
            "midpoint_pos": midpoint_pos,
            "description": f"Guessed {midpoint_type} midpoint at position {midpoint_pos} ({fail_msg})",
            "trace": trace,
            "final_stack": list(stack),
            "fail_reason": fail_msg
        }

    def _get_best_failed_trace(self, branches: List[Dict[str, Any]], n: int) -> List[Dict[str, Any]]:
        """Pick the most natural midpoint branch to display for a rejected string."""
        target_pos = n // 2
        preferred_type = "even" if n % 2 == 0 else "odd"
        for b in branches:
            if b["midpoint_pos"] == target_pos and b["midpoint_type"] == preferred_type:
                return b["trace"]
        return branches[0]["trace"] if branches else []

    def _explain_accepted(self, text: str, length: int) -> str:
        if text in ("ε", ""):
            return "The empty string is equal to its reverse."
        if length == 1:
            return "A one-symbol string is a palindrome."
        if text == "abba":
            return "The reverse of abba is abba (even-length palindrome)."
        if text == "aba":
            return "The reverse of aba is aba (odd-length palindrome with center 'b')."
        if text == "baab":
            return "The reverse of baab is baab (even-length palindrome)."
        if length % 2 == 0:
            return f"String is symmetric around even midpoint; reverse of '{text}' is '{text}'."
        else:
            return f"String is symmetric around odd center; reverse of '{text}' is '{text}'."

    def _explain_rejected(self, text: str) -> str:
        rev = text[::-1]
        return f"Its reverse is {rev}, which is different from original string {text}."

    @staticmethod
    def get_cfg_derivation(tokens: List[str]) -> List[str]:
        """
        Generate leftmost CFG derivation for a palindrome string over {a, b}.
        Grammar: S -> aSa | bSb | a | b | ε
        Example for abba: S => aSa => abSba => abεba => abba
        Example for aba:  S => aSa => aba
        """
        if not tokens:
            return ["S", "ε"]

        n = len(tokens)
        # Check if actually palindrome
        if tokens != tokens[::-1]:
            return ["String is not a palindrome; no derivation exists."]

        steps = ["S"]
        prefix = ""
        suffix = ""

        # Outer recursive steps
        left = 0
        right = n - 1
        while left < right:
            char = tokens[left]
            prefix += char
            suffix = char + suffix
            steps.append(f"{prefix}S{suffix}")
            left += 1
            right -= 1

        # Center step
        if left == right:
            # Odd length center: S -> a or S -> b
            center_char = tokens[left]
            steps.append(f"{prefix}{center_char}{suffix}")
        else:
            # Even length center: S -> ε
            steps.append(f"{prefix}ε{suffix}")
            steps.append(f"{prefix}{suffix}" if prefix else "ε")

        # Clean consecutive duplicates
        cleaned = []
        for s in steps:
            if not cleaned or cleaned[-1] != s:
                cleaned.append(s)
        return cleaned
