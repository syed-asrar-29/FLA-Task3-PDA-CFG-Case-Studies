"""
PDA AND CFG SIMULATOR
Case Study-Based Analysis and Design Using PDA and CFG
Formal Language and Automata (FLA) Task 3

Educational Streamlit application for B.Tech academic demonstration.
"""

import os
import streamlit as st
import pandas as pd

from automata.balanced_parentheses import BalancedParenthesesPDA
from automata.arithmetic_parser import ArithmeticPDASimulator
from automata.palindrome_pda import PalindromePDA

# Configure Streamlit page
st.set_page_config(
    page_title="PDA and CFG Simulator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper function to load grammar file
def load_grammar_file(filename: str) -> str:
    path = os.path.join(os.path.dirname(__file__), "grammars", filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Grammar file not found."


def render_header():
    st.title("PDA AND CFG SIMULATOR")
    st.caption(
        "**CASE STUDY-BASED ANALYSIS AND DESIGN USING PDA AND CFG**  \n"
        "A study of balanced parentheses, arithmetic-expression validation and palindrome recognition  \n"
        "*Course:* Formal Language and Automata (21CSC301T) | B.Tech Computer Science and Artificial Intelligence"
    )
    st.divider()


def section_balanced_parentheses():
    st.header("1. Balanced Parentheses")
    st.markdown(
        r"""
        **Objective:** Determine whether every opening parenthesis `'('` has a corresponding closing parenthesis `')'` in the correct order.  
        **Alphabet:** $\Sigma = \{ '(', ')' \}$  
        **Language:** $L = \{ w \in \Sigma^* \mid w \text{ is properly balanced} \}$ (Empty string $\varepsilon$ is accepted)
        """
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("CFG Productions")
        grammar_text = load_grammar_file("balanced_parentheses.txt")
        st.code(grammar_text, language="text")

    with col2:
        st.subheader("PDA Formal Model")
        st.markdown(
            r"""
            - **States:** $Q = \{q, q_f, q_{rej}\}$
            - **Input Alphabet:** $\Sigma = \{ '(', ')' \}$
            - **Stack Alphabet:** $\Gamma = \{ Z_0, X \}$
            - **Start State:** $q$
            - **Initial Stack Symbol:** $Z_0$
            - **Accepting State:** $q_f$
            - **Acceptance Condition:** All input consumed and stack contains only $Z_0$.
            """
        )

    st.subheader("PDA Transition Diagram")
    diagram_path = os.path.join(os.path.dirname(__file__), "diagrams", "balanced_parentheses_pda.png")
    if os.path.exists(diagram_path):
        st.image(diagram_path, caption="Deterministic PDA for Balanced Parentheses", use_container_width=True)

    st.subheader("Interactive Simulation")
    example_options = [
        "Custom Input...",
        "() (Accepted: One matched pair)",
        "(()) (Accepted: Nested pair)",
        "()() (Accepted: Adjacent pairs)",
        "(()()) (Accepted: Nested and adjacent)",
        "ε (Accepted: Empty string)",
        "( (Rejected: Unmatched opening)",
        ") (Rejected: Immediate underflow)",
        "(() (Rejected: Missing closing)",
        "()) (Rejected: Extra closing)",
        "())( (Rejected: Premature underflow)",
    ]
    selected_example = st.selectbox("Load Example from Report:", example_options, key="bp_select")

    default_val = "(()())"
    if selected_example != "Custom Input...":
        default_val = selected_example.split(" ")[0]
        if default_val == "ε":
            default_val = "ε"

    user_input = st.text_input("Enter Parentheses String (or leave empty / type 'ε' for empty string):",
                               value=default_val, key="bp_input")

    if st.button("Run Simulation", key="bp_run"):
        pda = BalancedParenthesesPDA()
        result = pda.simulate(user_input)

        if result["accepted"]:
            st.success(f"**STATUS: ACCEPTED** (Final State: `{result['final_state']}`)")
        else:
            st.error(f"**STATUS: REJECTED** (Final State: `{result['final_state']}`)")

        st.info(f"**Theoretical Reason:** {result['reason']}")

        # Execution table
        st.subheader("Step-by-Step Stack Trace")
        df = pd.DataFrame(result["trace"])
        df.rename(columns={
            "step": "Step",
            "state": "State",
            "input_read": "Input Read",
            "stack": "Stack (bottom → top)",
            "explanation": "Explanation / Action"
        }, inplace=True)
        st.dataframe(df, use_container_width=True)

        # CFG Derivation
        if result["accepted"]:
            st.subheader("CFG Leftmost Derivation")
            deriv = BalancedParenthesesPDA.get_cfg_derivation(user_input)
            st.code("  ⇒  ".join(deriv), language="text")

    st.subheader("Report Reference Test Cases")
    ref_data = [
        {"String": "()", "Result": "ACCEPTED", "Reason": "One opening and one closing parenthesis match."},
        {"String": "(())", "Result": "ACCEPTED", "Reason": "The inner pair closes before the outer pair."},
        {"String": "()()", "Result": "ACCEPTED", "Reason": "Two balanced groups appear consecutively."},
        {"String": "(()())", "Result": "ACCEPTED", "Reason": "All nested and adjacent pairs are matched in order."},
        {"String": "ε", "Result": "ACCEPTED", "Reason": "The empty string contains no unmatched parentheses."},
        {"String": "(", "Result": "REJECTED", "Reason": "An opening parenthesis remains unmatched at the end."},
        {"String": ")", "Result": "REJECTED", "Reason": "A closing parenthesis appears when the stack contains only Z0."},
        {"String": "(()", "Result": "REJECTED", "Reason": "One opening parenthesis remains unmatched."},
        {"String": "())", "Result": "REJECTED", "Reason": "The third symbol is an extra closing parenthesis."},
        {"String": "())(", "Result": "REJECTED", "Reason": "A closing parenthesis occurs with no matching opening."},
    ]
    st.table(pd.DataFrame(ref_data))


def section_arithmetic_expressions():
    st.header("2. Arithmetic Expression Validation")
    st.markdown(
        r"""
        **Objective:** Validate arithmetic expressions using a context-free grammar and a grammar-simulation PDA.  
        **Terminals:** $\{ id, num, +, -, *, /, (, ) \}$  
        **Precedence:** Multiplication and division bind tighter than addition and subtraction. Unary minus and implicit multiplication are not supported.
        """
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("CFG Productions (Operator Precedence Hierarchy)")
        grammar_text = load_grammar_file("arithmetic_expression.txt")
        st.code(grammar_text, language="text")

    with col2:
        st.subheader("PDA Formal Model (CFG-Simulation)")
        st.markdown(
            r"""
            - **States:** $Q = \{q_0, q_{parse}, q_{match}, q_f, q_{rej}\}$
            - **Input Alphabet:** $\Sigma = \{ id, num, +, -, *, /, (, ) \}$
            - **Stack Alphabet:** $\Gamma = \{ E, T, F, id, num, +, -, *, /, (, ), Z_0 \}$
            - **Start State:** $q_0$ with initial stack $Z_0\ E$
            - **Accepting State:** $q_f$
            - **Simulation Logic:**
              1. Non-terminals on top are expanded using CFG productions (reversed on stack).
              2. Terminals on top are matched against input tokens and consumed.
              3. Accepts when all input is consumed and only $Z_0$ remains.
            """
        )

    st.subheader("PDA Transition Diagram")
    diagram_path = os.path.join(os.path.dirname(__file__), "diagrams", "arithmetic_expression_pda.png")
    if os.path.exists(diagram_path):
        st.image(diagram_path, caption="Grammar-Simulation PDA for Arithmetic Expressions", use_container_width=True)

    st.subheader("Interactive Simulation")
    example_options = [
        "Custom Input...",
        "a+b (Accepted: Binary addition)",
        "a*b+c (Accepted: Multiplication followed by addition)",
        "(a+b)*c (Accepted: Grouped addition multiplied by factor)",
        "num/id (Accepted: Number divided by identifier)",
        "a-(b/c) (Accepted: Subtraction with parenthesized division)",
        "+a (Rejected: Leading operator without left operand)",
        "a+ (Rejected: Trailing operator without right operand)",
        "a**b (Rejected: Consecutive multiplication operators)",
        "(a+b (Rejected: Unclosed opening parenthesis)",
        "a b (Rejected: Missing operator between operands)",
        "a+*b (Rejected: Consecutive operator sequence)",
        "(a+) (Rejected: Missing operand inside parenthesis)",
    ]
    selected_example = st.selectbox("Load Example from Report:", example_options, key="arith_select")

    default_val = "(a+b)*c"
    if selected_example != "Custom Input...":
        default_val = selected_example.split(" ")[0]

    user_input = st.text_input("Enter Arithmetic Expression:", value=default_val, key="arith_input")

    if st.button("Run Simulation", key="arith_run"):
        sim = ArithmeticPDASimulator()
        result = sim.simulate(user_input)

        if result["accepted"]:
            st.success(f"**STATUS: ACCEPTED** (Final State: `{result['final_state']}`)")
        else:
            st.error(f"**STATUS: REJECTED** (Final State: `{result['final_state']}`)")

        st.info(f"**Theoretical Reason:** {result['reason']}")

        # Step-by-step trace
        st.subheader("PDA Stack & Transition Trace")
        df = pd.DataFrame(result["trace"])
        df.rename(columns={
            "step": "Step",
            "state": "State",
            "action": "PDA Action",
            "stack": "Stack (bottom → top)",
            "remaining_input": "Remaining Tokens",
            "explanation": "Explanation"
        }, inplace=True)
        st.dataframe(df, use_container_width=True)

        # CFG Derivation
        if result["accepted"] and result["derivation"]:
            st.subheader("Grammar Derivation Steps")
            st.code("  ⇒  \n".join(result["derivation"]), language="text")

    st.subheader("Report Reference Test Cases")
    ref_data = [
        {"Expression": "a+b", "Result": "ACCEPTED", "Reason": "Two operands are joined by a binary addition operator."},
        {"Expression": "a*b+c", "Result": "ACCEPTED", "Reason": "A multiplication term is followed by addition."},
        {"Expression": "(a+b)*c", "Result": "ACCEPTED", "Reason": "A parenthesized expression is multiplied by c."},
        {"Expression": "num/id", "Result": "ACCEPTED", "Reason": "A numeric token is divided by an identifier token."},
        {"Expression": "a-(b/c)", "Result": "ACCEPTED", "Reason": "Subtraction uses a parenthesized division expression."},
        {"Expression": "+a", "Result": "REJECTED", "Reason": "The expression begins with an operator and has no left operand."},
        {"Expression": "a+", "Result": "REJECTED", "Reason": "The addition operator has no right operand."},
        {"Expression": "a**b", "Result": "REJECTED", "Reason": "Two multiplication operators occur consecutively."},
        {"Expression": "(a+b", "Result": "REJECTED", "Reason": "The opening parenthesis is not closed."},
        {"Expression": "a b", "Result": "REJECTED", "Reason": "Consecutive operands without intervening operator."},
        {"Expression": "a+*b", "Result": "REJECTED", "Reason": "Consecutive operators found with no operand."},
    ]
    st.table(pd.DataFrame(ref_data))


def section_palindrome_recognition():
    st.header("3. Palindrome Recognition")
    st.markdown(
        r"""
        **Objective:** Recognize palindromes over the alphabet $\{a, b\}$.  
        **Alphabet:** $\Sigma = \{ a, b \}$  
        **Language:** $L = \{ w \in \{a,b\}^* \mid w = w^R \}$ (Includes even and odd lengths, plus $\varepsilon$)  
        **PDA Mechanism:** Nondeterministic midpoint guessing with push and match phases.
        """
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("CFG Productions")
        grammar_text = load_grammar_file("palindrome.txt")
        st.code(grammar_text, language="text")

    with col2:
        st.subheader("Nondeterministic PDA Model")
        st.markdown(
            r"""
            - **States:** $Q = \{q_{start}, q_{push}, q_{match}, q_f, q_{rej}\}$
            - **Stack Alphabet:** $\Gamma = \{ Z_0, a, b \}$
            - **Nondeterministic Midpoint Transitions:**
              - *Even Midpoint:* $\delta(q_{push}, \varepsilon, X) \to \{(q_{match}, X)\}$ without consuming input.
              - *Odd Midpoint:* $\delta(q_{push}, c, X) \to \{(q_{match}, X)\}$ consuming middle character $c \in \{a, b\}$.
            - **Matching Phase:** $\delta(q_{match}, a, a) \to \{(q_{match}, \varepsilon)\}$ and $\delta(q_{match}, b, b) \to \{(q_{match}, \varepsilon)\}$.
            - **Acceptance:** Reaching $q_f$ with stack containing only $Z_0$ when input is exhausted.
            """
        )

    st.subheader("PDA Transition Diagram")
    diagram_path = os.path.join(os.path.dirname(__file__), "diagrams", "palindrome_pda.png")
    if os.path.exists(diagram_path):
        st.image(diagram_path, caption="Nondeterministic PDA for Palindrome Recognition", use_container_width=True)

    st.subheader("Interactive Simulation")
    example_options = [
        "Custom Input...",
        "ε (Accepted: Empty string palindrome)",
        "a (Accepted: Single character odd palindrome)",
        "b (Accepted: Single character odd palindrome)",
        "aa (Accepted: Even-length palindrome)",
        "aba (Accepted: Odd-length palindrome, center 'b')",
        "abba (Accepted: Even-length palindrome)",
        "baab (Accepted: Even-length palindrome)",
        "ab (Rejected: Reverse is ba)",
        "aab (Rejected: Reverse is baa)",
        "abb (Rejected: Reverse is bba)",
        "abab (Rejected: Reverse is baba)",
        "aabb (Rejected: Reverse is bbaa)",
    ]
    selected_example = st.selectbox("Load Example from Report:", example_options, key="pal_select")

    default_val = "abba"
    if selected_example != "Custom Input...":
        default_val = selected_example.split(" ")[0]

    user_input = st.text_input("Enter String over {a, b} (or 'ε' / empty for ε):",
                               value=default_val, key="pal_input")

    if st.button("Run Simulation", key="pal_run"):
        pda = PalindromePDA()
        result = pda.simulate(user_input)

        if result["accepted"]:
            st.success(f"**STATUS: ACCEPTED** (Final State: `{result['final_state']}`)")
            if result.get("winning_branch"):
                wb = result["winning_branch"]
                st.info(f"**Winning Nondeterministic Path:** {wb['description']}")
        else:
            st.error(f"**STATUS: REJECTED** (Final State: `{result['final_state']}`)")

        st.info(f"**Theoretical Reason:** {result['reason']}")

        # Midpoint Exploration Branches
        st.subheader("Nondeterministic Midpoint Branches Explored")
        branch_rows = []
        for b in result.get("branches", []):
            branch_rows.append({
                "Midpoint Guess Type": b["midpoint_type"].upper(),
                "Midpoint Index": b["midpoint_pos"],
                "Branch Description": b["description"],
                "Outcome": "ACCEPTED" if b["accepted"] else "FAILED"
            })
        if branch_rows:
            st.dataframe(pd.DataFrame(branch_rows), use_container_width=True)

        # Step-by-step trace
        st.subheader("Stack Trace for Best / Accepted Branch")
        df = pd.DataFrame(result["trace"])
        df.rename(columns={
            "step": "Step",
            "state": "State",
            "input_action": "Input Action",
            "stack": "Stack (bottom → top)",
            "explanation": "Explanation"
        }, inplace=True)
        st.dataframe(df, use_container_width=True)

        # CFG Derivation
        if result["accepted"] and result.get("derivation"):
            st.subheader("CFG Derivation Steps")
            st.code("  ⇒  ".join(result["derivation"]), language="text")

    st.subheader("Report Reference Test Cases")
    ref_data = [
        {"String": "ε", "Result": "ACCEPTED", "Reason": "The empty string is equal to its reverse."},
        {"String": "a", "Result": "ACCEPTED", "Reason": "A one-symbol string is a palindrome."},
        {"String": "abba", "Result": "ACCEPTED", "Reason": "The reverse of abba is abba."},
        {"String": "aba", "Result": "ACCEPTED", "Reason": "The reverse of aba is aba."},
        {"String": "baab", "Result": "ACCEPTED", "Reason": "The reverse of baab is baab."},
        {"String": "ab", "Result": "REJECTED", "Reason": "Its reverse is ba, which is different."},
        {"String": "aab", "Result": "REJECTED", "Reason": "Its reverse is baa."},
        {"String": "abb", "Result": "REJECTED", "Reason": "Its reverse is bba."},
        {"String": "abab", "Result": "REJECTED", "Reason": "Its reverse is baba."},
        {"String": "aabb", "Result": "REJECTED", "Reason": "Its reverse is bbaa."},
    ]
    st.table(pd.DataFrame(ref_data))


def section_overview_and_comparison():
    st.header("4. Theoretical Background & Comparative Analysis")
    st.markdown(
        """
        ### Why Finite Automata (DFA/NFA) Are Insufficient
        A finite automaton has a fixed finite number of states and no auxiliary memory.
        It cannot recognize non-regular context-free languages that require unbounded counting or matching:
        - **Balanced Parentheses:** The nesting depth can grow arbitrarily large. A finite automaton cannot count an unbounded number of unmatched opening parentheses.
        - **Arithmetic Expressions:** Expressions have hierarchical recursive structure and nested parentheses, requiring pending operator/operand contexts to be remembered.
        - **Palindromes:** The automaton must remember an arbitrarily long first half of the string and verify it in reverse order against the second half.
        """
    )

    st.subheader("Comparison of the Three Case Studies (From Task 3 Report Table 6.1)")
    comp_data = [
        {
            "Feature": "Alphabet / Input",
            "Balanced Parentheses": "'(' and ')'",
            "Arithmetic Expressions": "id, num, +, -, *, /, (, )",
            "Palindromes": "a and b"
        },
        {
            "Feature": "Main Structure",
            "Balanced Parentheses": "Nested matching delimiters",
            "Arithmetic Expressions": "Hierarchical operator and factor structure",
            "Palindromes": "Symmetry around a midpoint"
        },
        {
            "Feature": "CFG",
            "Balanced Parentheses": "S → (S)S | ε",
            "Arithmetic Expressions": "E / T / F precedence grammar",
            "Palindromes": "S → aSa | bSb | a | b | ε"
        },
        {
            "Feature": "Stack Purpose",
            "Balanced Parentheses": "Remember unmatched opening brackets",
            "Arithmetic Expressions": "Store pending grammar symbols and expected terminals",
            "Palindromes": "Store first half for reverse comparison"
        },
        {
            "Feature": "PDA Behaviour",
            "Balanced Parentheses": "Deterministic push/pop",
            "Arithmetic Expressions": "General CFG-simulation PDA (nondeterministic choices)",
            "Palindromes": "Nondeterministic midpoint guess"
        },
        {
            "Feature": "Acceptance Condition",
            "Balanced Parentheses": "Input consumed; only Z0 remains",
            "Arithmetic Expressions": "Input consumed; grammar stack cleared (only Z0 remains)",
            "Palindromes": "Input consumed; only Z0 remains in qf"
        }
    ]
    st.table(pd.DataFrame(comp_data))


def main():
    render_header()

    menu = st.sidebar.radio(
        "Select Application / Section:",
        [
            "1. Balanced Parentheses",
            "2. Arithmetic Expression Validation",
            "3. Palindrome Recognition",
            "4. Theoretical Background & Comparison",
        ]
    )

    if menu.startswith("1."):
        section_balanced_parentheses()
    elif menu.startswith("2."):
        section_arithmetic_expressions()
    elif menu.startswith("3."):
        section_palindrome_recognition()
    elif menu.startswith("4."):
        section_overview_and_comparison()


if __name__ == "__main__":
    main()
