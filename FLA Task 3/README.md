# Case Study-Based Analysis and Design Using PDA and CFG

> **Subtitle:** A study of balanced parentheses, arithmetic-expression validation and palindrome recognition  
> **Course:** Formal Language and Automata (21CSC301T)  
> **Degree:** Bachelor of Technology in Computer Science and Artificial Intelligence (B.Tech CSAI)  
> **Institution:** Amrita Vishwa Vidyapeetham, Bengaluru Campus, School of Computing  
> **Task:** Individual Case Study Report & Interactive Educational Simulator (Task 3)

---

## Table of Contents
1. [Project Introduction](#1-project-introduction)
2. [Objectives](#2-objectives)
3. [Theoretical Background: CFG and PDA](#3-theoretical-background-cfg-and-pda)
4. [Application 1: Balanced Parentheses](#4-application-1-balanced-parentheses)
5. [Application 2: Arithmetic Expression Validation](#5-application-2-arithmetic-expression-validation)
6. [Application 3: Palindrome Recognition](#6-application-3-palindrome-recognition)
7. [Comparative Analysis & Memory Limitations of Finite Automata](#7-comparative-analysis--memory-limitations-of-finite-automata)
8. [PDA State Transition Diagrams](#8-pda-state-transition-diagrams)
9. [Project Folder Structure](#9-project-folder-structure)
10. [Installation Instructions](#10-installation-instructions)
11. [How to Run the Simulator](#11-how-to-run-the-simulator)
12. [How to Execute Test Cases](#12-how-to-execute-test-cases)
13. [Conclusion & References](#13-conclusion--references)

---

## 1. Project Introduction

This project implements an interactive educational simulator demonstrating how **Context-Free Grammars (CFGs)** and **Pushdown Automata (PDAs)** describe and recognize Context-Free Languages (CFLs). The implementation is based directly on the formal models, alphabets, transition functions, derivation rules, and test cases defined in the academic report:

> **"CASE STUDY-BASED ANALYSIS AND DESIGN USING PDA AND CFG"**  
> *A study of balanced parentheses, arithmetic-expression validation and palindrome recognition*

The simulator provides:
- Live CFG productions and leftmost derivation generation.
- Full step-by-step PDA state and stack execution traces.
- Push and pop operations visible at every input symbol.
- Explicit demonstrations of deterministic vs. nondeterministic PDA computation paths.
- Interactive web interface built with **Streamlit**.
- Comprehensive unit test suite with **pytest**.

---

## 2. Objectives

- **Grammar & Derivations:** Model CFG productions with identified non-terminals, terminals, and start variables; generate valid leftmost derivations.
- **PDA State Transitions:** Implement the formal transition function $\delta(q, a, X)$ tracking current state, read symbol, stack pop/push, and target state.
- **Stack Memory Demonstration:** Show how last-in, first-out (LIFO) stack memory handles unbounded delimiter nesting, pending operator structures, and symmetric midpoint reflection.
- **Determinism vs. Nondeterminism:** Highlight the contrast between deterministic recognition (balanced parentheses) and nondeterministic branching (grammar simulation and palindrome midpoint guessing).
- **Academic Verification:** Verify all accepted and rejected test cases against the course report specifications.

---

## 3. Theoretical Background: CFG and PDA

### 3.1 Context-Free Grammar (CFG)
A context-free grammar is defined as a 4-tuple:
$$G = (V, \Sigma, P, S)$$
- $V$: Finite set of variables (non-terminal symbols).
- $\Sigma$: Finite set of terminal symbols ($V \cap \Sigma = \emptyset$).
- $P$: Set of production rules of the form $A \to \alpha$, where $A \in V$ and $\alpha \in (V \cup \Sigma)^*$.
- $S \in V$: The start symbol.

### 3.2 Pushdown Automaton (PDA)
A pushdown automaton is a 7-tuple:
$$M = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)$$
- $Q$: Finite set of states.
- $\Sigma$: Input alphabet.
- $\Gamma$: Stack alphabet.
- $\delta: Q \times (\Sigma \cup \{\varepsilon\}) \times \Gamma \to \mathcal{P}(Q \times \Gamma^*)$: Transition function.
- $q_0 \in Q$: Start state.
- $Z_0 \in \Gamma$: Initial bottom-of-stack marker.
- $F \subseteq Q$: Set of accepting states.

### 3.3 Acceptance Conditions
A PDA may accept by **final state** ($w$ is accepted if the PDA reaches state $q \in F$ after consuming $w$) or by **empty stack** (all symbols cleared). In this project, acceptance requires **all input to be consumed and the stack to contain only the bottom marker $Z_0$** upon reaching the accepting state $q_f$.

---

## 4. Application 1: Balanced Parentheses

### 4.1 Specification
- **Alphabet:** $\Sigma = \{ '(', ')' \}$
- **Language:** $L_1 = \{ w \in \Sigma^* \mid w \text{ is properly balanced} \}$ (includes empty string $\varepsilon$).

### 4.2 Context-Free Grammar
$$S \to (S)S \mid \varepsilon$$
- $S$ is the start variable.
- Production $S \to (S)S$ introduces one matched outer pair and permits a following balanced sequence.
- Production $S \to \varepsilon$ terminates the recursive derivation.

#### Example Leftmost Derivation for `(()())`:
$$S \Rightarrow (S)S \Rightarrow ((S)S)S \Rightarrow (()S)S \Rightarrow (()(S)S)S \Rightarrow (()())S \Rightarrow (()())$$

### 4.3 PDA Design & Deterministic Stack Behaviour
- **States:** $Q = \{q, q_f, q_{rej}\}$
- **Input Alphabet:** $\Sigma = \{ '(', ')' \}$
- **Stack Alphabet:** $\Gamma = \{ Z_0, X \}$
- **Start State:** $q$; **Initial Stack:** $Z_0$; **Accepting State:** $q_f$.
- **Operational Transitions:**
  - On `'('`: push $X$ above the stack top; remain in $q$.
  - On `')'`: if top is $X$, pop $X$; remain in $q$.
  - On `')'` when top is $Z_0$: no valid transition (stack underflow $\to$ reject).
  - End of input: if top is $Z_0$, transition to $q_f$ and accept; if $X$ remains on stack, reject.

### 4.4 Stack Trace for `(())`
| Step | Input Read | Stack (bottom $\to$ top) | State | Explanation |
| :---: | :---: | :---: | :---: | :--- |
| 0 | Start | $Z_0$ | $q$ | Only bottom marker is present. |
| 1 | `(` | $Z_0\ X$ | $q$ | Push $X$ for the first opening parenthesis. |
| 2 | `(` | $Z_0\ X\ X$ | $q$ | Push another $X$ for the nested opening parenthesis. |
| 3 | `)` | $Z_0\ X$ | $q$ | Pop one $X$; inner opening parenthesis matched. |
| 4 | `)` | $Z_0$ | $q$ | Pop remaining $X$; outer opening parenthesis matched. |
| 5 | End | $Z_0$ | $q_f$ | Input consumed and only $Z_0$ remains: **ACCEPT**. |

### 4.5 Test Cases
- **Accepted:** `()`, `(())`, `()()`, `(()())`, `ε`
- **Rejected:** `(`, `)`, `(()`, `())`, `())(`

---

## 5. Application 2: Arithmetic Expression Validation

### 5.1 Specification
- **Terminals:** $\Sigma = \{ id, num, +, -, *, /, (, ) \}$
- **Non-terminals:** $V = \{ E, T, F \}$
- **Start Variable:** $E$
- **Assumptions:** Tokens $id$ and $num$ represent complete lexical entities. Binary operators only; unary operators and implicit multiplication are not permitted. Multiplication and division have higher precedence than addition and subtraction.

### 5.2 Context-Free Grammar
$$\begin{aligned}
E &\to E + T \mid E - T \mid T \\
T &\to T * F \mid T / F \mid F \\
F &\to ( E ) \mid id \mid num
\end{aligned}$$

#### Example Leftmost Derivation for `(a+b)*c`:
$$E \Rightarrow T \Rightarrow T * F \Rightarrow F * F \Rightarrow (E) * F \Rightarrow (E + T) * F \Rightarrow (T + T) * F \Rightarrow (F + F) * F \Rightarrow (a + b) * c$$

### 5.3 Grammar-Simulation PDA Design
- **States:** $Q = \{q_0, q_{parse}, q_{match}, q_f, q_{rej}\}$
- **Stack Alphabet:** $\{ E, T, F, id, num, +, -, *, /, (, ), Z_0 \}$
- **Initial Stack:** $[Z_0, E]$ (start variable $E$ is on top).
- **Simulation Logic:**
  1. **Non-terminal on stack top:** Replace by production RHS pushed in **reverse order** so the leftmost symbol is at the top.
  2. **Terminal on stack top:** Compare with current input token. If matching, pop terminal and consume token ($q_{parse} \leftrightarrow q_{match}$). If not matching, computation path fails.
  3. **Acceptance:** Transition to $q_f$ when all tokens are consumed and only $Z_0$ remains.

### 5.4 Test Cases
- **Accepted:** `a+b`, `a*b+c`, `(a+b)*c`, `num/id`, `a-(b/c)`
- **Rejected:** `+a`, `a+`, `a**b`, `(a+b`, `a b`, `a+*b`, `(a+)`

---

## 6. Application 3: Palindrome Recognition

### 6.1 Specification
- **Alphabet:** $\Sigma = \{ a, b \}$
- **Language:** $L_3 = \{ w \in \{a, b\}^* \mid w = w^R \}$ (contains $\varepsilon$, odd-length, and even-length palindromes).

### 6.2 Context-Free Grammar
$$S \to aSa \mid bSb \mid a \mid b \mid \varepsilon$$
- $S \to aSa \mid bSb$: Recursively places matching outer boundary symbols.
- $S \to a \mid b$: Middle element for odd-length palindromes.
- $S \to \varepsilon$: Empty center for even-length palindromes.

#### Example Leftmost Derivation for `abba`:
$$S \Rightarrow aSa \Rightarrow abSba \Rightarrow ab\varepsilon ba \Rightarrow abba$$

### 6.3 Nondeterministic Midpoint Guessing PDA
Because the PDA reads input sequentially without knowing where the midpoint is, it nondeterministically branches:
- **States:** $Q = \{q_{start}, q_{push}, q_{match}, q_f, q_{rej}\}$
- **Stack Alphabet:** $\Gamma = \{ Z_0, a, b \}$
- **Phase 1 ($q_{push}$):** Push symbols $a$ or $b$ onto the stack.
- **Midpoint Transition ($q_{push} \to q_{match}$):**
  - **Even Midpoint Guess:** $\varepsilon$-transition without consuming input.
  - **Odd Midpoint Guess:** Reads center symbol ($a$ or $b$) without pushing it onto the stack.
- **Phase 2 ($q_{match}$):** Read remaining input symbols and pop matching stack symbols.
- **Acceptance:** Move to $q_f$ when stack contains only $Z_0$ after exhausting input.

### 6.4 Successful Stack Trace for `abba`
| Step | Input Action | Stack (bottom $\to$ top) | State | Explanation |
| :---: | :---: | :---: | :---: | :--- |
| 0 | Start | $Z_0$ | $q_{start}$ | Initial bottom marker. |
| 1 | Read `a`; push `a` | $Z_0\ a$ | $q_{push}$ | Store the first symbol. |
| 2 | Read `b`; push `b` | $Z_0\ a\ b$ | $q_{push}$ | Store the second symbol. |
| 3 | Guess even midpoint | $Z_0\ a\ b$ | $q_{match}$ | Switch to matching phase without consuming input. |
| 4 | Read `b`; match & pop | $Z_0\ a$ | $q_{match}$ | Input `b` matches stack top `b`. |
| 5 | Read `a`; match & pop | $Z_0$ | $q_{match}$ | Input `a` matches stack top `a`. |
| 6 | End of input | $Z_0$ | $q_f$ | Input consumed and stack restored to bottom marker: **ACCEPT**. |

### 6.5 Odd-Length Processing Demonstration (`aba`)
- Push `a` onto stack $\to [Z_0, a]$.
- Read `b`: PDA nondeterministically guesses `b` is the odd-length center, consumes `b` without pushing, and transitions to $q_{match}$.
- Read `a`: Matches stack top `a`, pops `a`, leaving $[Z_0]$.
- End of input: Stack has $Z_0 \to$ **ACCEPT**.

### 6.6 Test Cases
- **Accepted:** `ε`, `a`, `b`, `aa`, `aba`, `abba`, `baab`
- **Rejected:** `ab`, `aab`, `abb`, `abab`, `aabb`

---

## 7. Comparative Analysis & Memory Limitations of Finite Automata

| Feature | Balanced Parentheses | Arithmetic Expressions | Palindromes |
| :--- | :--- | :--- | :--- |
| **Alphabet / Input** | `'('` and `')'` | $id, num, +, -, *, /, (, )$ | $a$ and $b$ |
| **Main Structure** | Nested matching delimiters | Hierarchical operator & factor precedence | Symmetry around midpoint |
| **CFG** | $S \to (S)S \mid \varepsilon$ | $E / T / F$ precedence hierarchy | $S \to aSa \mid bSb \mid a \mid b \mid \varepsilon$ |
| **Stack Purpose** | Count unmatched opening brackets | Store pending variables & expected terminals | Store first half for reverse comparison |
| **PDA Behaviour** | Deterministic push/pop | CFG-simulation PDA (nondeterministic) | Nondeterministic midpoint guessing |
| **Acceptance** | All input consumed; stack $= [Z_0]$ | All tokens matched; stack $= [Z_0]$ | All input consumed; stack $= [Z_0]$ |

### Why Finite Automata (DFA/NFA) Are Insufficient
A Finite Automaton (FA) has a fixed, finite number of states $k$. It cannot count an unbounded number of items:
1. **Parentheses:** For input $(^n )^n$, if $n > k$, the Pigeonhole Principle guarantees the FA must repeat a state, making it impossible to ensure that the number of closing brackets exactly equals the number of opening brackets.
2. **Arithmetic:** Arbitrarily nested expressions $(((\dots)))$ require tracking an unbounded number of open scopes.
3. **Palindromes:** For strings $w w^R$, an FA cannot remember an arbitrary prefix $w$ of length $> k$ to verify the reversed suffix.

The auxiliary **LIFO stack memory** of a Pushdown Automaton removes this finite bound, allowing context-free languages to be recognized.

---

## 8. PDA State Transition Diagrams

The state transition diagrams are located in the `diagrams/` folder:

1. **Balanced Parentheses PDA:**  
   `diagrams/balanced_parentheses_pda.png`
2. **Arithmetic Expression Validation PDA:**  
   `diagrams/arithmetic_expression_pda.png`
3. **Palindrome Recognition PDA:**  
   `diagrams/palindrome_pda.png`

*(To regenerate all diagrams programmatically at any time, run `python diagrams/generate_diagrams.py`)*

---

## 9. Project Folder Structure

```text
PDA-CFG-Task3-Simulator/
│
├── README.md                      # Comprehensive academic documentation
├── requirements.txt               # Minimal Python dependencies
├── app.py                         # Interactive Streamlit application
│
├── automata/                      # Formal Automata & Parser implementations
│   ├── __init__.py                # Package exports
│   ├── balanced_parentheses.py    # Deterministic PDA for Parentheses
│   ├── arithmetic_parser.py       # Grammar-Simulation PDA for Arithmetic
│   └── palindrome_pda.py          # Nondeterministic PDA for Palindromes
│
├── grammars/                      # Context-Free Grammar definitions
│   ├── balanced_parentheses.txt   # S -> (S)S | ε
│   ├── arithmetic_expression.txt  # E/T/F Precedence Grammar
│   └── palindrome.txt             # S -> aSa | bSb | a | b | ε
│
├── diagrams/                      # Generated State Transition Diagrams
│   ├── balanced_parentheses_pda.png
│   ├── arithmetic_expression_pda.png
│   ├── palindrome_pda.png
│   └── generate_diagrams.py       # Diagram generation script (Matplotlib)
│
├── tests/                         # Pytest test suite
│   ├── test_balanced_parentheses.py
│   ├── test_arithmetic.py
│   └── test_palindrome.py
│
└── docs/                          # Academic documentation & original report
    └── Task3_Report.pdf           # Uploaded FLA Task 3 Case Study Report
```

---

## 10. Installation Instructions

### Prerequisites
- Python 3.9+ (Tested on Python 3.14)
- Pip package manager

### Steps
1. Open a terminal / command prompt in the project root directory:
   ```bash
   cd "PDA-CFG-Task3-Simulator"
   ```

2. (Optional) Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux / macOS:
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## 11. How to Run the Simulator

Launch the Streamlit web interface by running:
```bash
streamlit run app.py
```

Once launched:
- The app will automatically open in your web browser at `http://localhost:8501`.
- Use the sidebar navigation to switch between the three case studies or review the comparative analysis.
- Select pre-configured test cases from the report or enter your own custom strings.
- Click **Run Simulation** to view the live execution table, stack traces, and CFG derivations.

---

## 12. How to Execute Test Cases

Run the complete test suite using `pytest`:
```bash
pytest -v
```

To run individual test files:
```bash
pytest tests/test_balanced_parentheses.py -v
pytest tests/test_arithmetic.py -v
pytest tests/test_palindrome.py -v
```

All 20 test cases verify boundary conditions, accepted strings, rejected strings, empty strings ($\varepsilon$), and invalid lexical characters.

---

## 13. Conclusion & References

### Academic Conclusion
This project demonstrates the practical and theoretical foundations of Context-Free Grammars and Pushdown Automata.
- **Delimiters:** Easily checked using deterministic stack counting.
- **Arithmetic:** Requires precedence levels ($E \to T \to F$) naturally validated through top-down CFG expansion and terminal matching.
- **Symmetry:** Requires nondeterminism to explore midpoint guesses in the absence of explicit delimiters.
- **Power of Stack:** Demonstrates why finite automata are fundamentally insufficient for nested or symmetric languages, establishing the theoretical boundary between regular and context-free languages.

### References
1. Course Assignment Guide: *Task 3 – PDA and CFG Case Study Guide*, Formal Language and Automata (21CSC301T), Amrita Vishwa Vidyapeetham, School of Computing.
2. Original Report: `docs/Task3_Report.pdf` (*Case Study-Based Analysis and Design Using PDA and CFG*, November 2026).
3. Michael Sipser, *Introduction to the Theory of Computation*, 3rd Edition, Cengage Learning.
4. John E. Hopcroft, Rajeev Motwani, Jeffrey D. Ullman, *Introduction to Automata Theory, Languages, and Computation*, 3rd Edition, Pearson.
