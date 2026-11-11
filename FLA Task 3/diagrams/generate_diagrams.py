"""
Generate publication-quality PDA transition diagrams for:
1. Balanced Parentheses PDA
2. Arithmetic Expression Validation PDA
3. Palindrome Recognition PDA

Uses Matplotlib to produce clean, reproducible PNG diagrams.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def create_balanced_parentheses_diagram(output_path: str):
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_xlim(-1, 11)
    ax.set_ylim(-2, 5)
    ax.axis("off")

    # Title
    ax.text(5, 4.4, "Case Study 1: Pushdown Automaton for Balanced Parentheses",
            fontsize=14, weight="bold", ha="center", color="#0F2C59")
    ax.text(5, 4.0, "Alphabet Σ = {'(', ')'}, Stack Alphabet Γ = {Z0, X}, Acceptance by Final State",
            fontsize=10, ha="center", color="#333333", style="italic")

    # Start pointer
    ax.annotate("", xy=(1.2, 1.5), xytext=(0.0, 1.5),
                arrowprops=dict(facecolor="#1E3E62", edgecolor="#1E3E62", width=2, headwidth=8))
    ax.text(0.5, 1.7, "Start", fontsize=11, weight="bold", color="#1E3E62", ha="center")

    # State q (main control state)
    q_circle = plt.Circle((2.5, 1.5), 0.9, facecolor="#EBF4F6", edgecolor="#088395", linewidth=2.5)
    ax.add_patch(q_circle)
    ax.text(2.5, 1.5, "q", fontsize=16, weight="bold", ha="center", va="center", color="#088395")
    ax.text(2.5, 0.25, "(Start State / Processing)", fontsize=9, ha="center", color="#555555")

    # Self-loops on q
    # Push transitions on '('
    ax.annotate("", xy=(2.0, 2.3), xytext=(3.0, 2.3),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-2.5", color="#088395", lw=2))
    ax.text(2.5, 3.5, "( , Z0  ->  X Z0  (Push X)\n( , X   ->  X X   (Push X)\n) , X   ->  ε     (Pop X)",
            fontsize=10, weight="semibold", ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#F0F8FF", edgecolor="#088395", lw=1))

    # Transition q -> qf on ε, Z0 -> Z0
    ax.annotate("", xy=(7.4, 1.5), xytext=(3.5, 1.5),
                arrowprops=dict(facecolor="#0A5C36", edgecolor="#0A5C36", width=2, headwidth=8))
    ax.text(5.45, 1.85, "ε , Z0  ->  Z0", fontsize=11, weight="bold", ha="center", color="#0A5C36")
    ax.text(5.45, 1.2, "(All input consumed,\nonly Z0 on stack)", fontsize=8.5, ha="center", color="#444444")

    # Accepting State qf (Double circle)
    qf_outer = plt.Circle((8.5, 1.5), 0.95, facecolor="#E8F5E9", edgecolor="#2E7D32", linewidth=2.5)
    qf_inner = plt.Circle((8.5, 1.5), 0.8, facecolor="none", edgecolor="#2E7D32", linewidth=1.8)
    ax.add_patch(qf_outer)
    ax.add_patch(qf_inner)
    ax.text(8.5, 1.5, "qf", fontsize=16, weight="bold", ha="center", va="center", color="#2E7D32")
    ax.text(8.5, 0.25, "(Accepting State)", fontsize=9, ha="center", color="#2E7D32", weight="bold")

    # Reject note
    ax.text(5.0, -1.2, "Implicit Reject (qrej): Reading ')' when top is Z0 (underflow) or input ends with X on stack.",
            fontsize=9.5, ha="center", color="#C62828", style="italic",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFEBEE", edgecolor="#EF5350", lw=1))

    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    print(f"Generated: {output_path}")


def create_arithmetic_pda_diagram(output_path: str):
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    ax.set_xlim(-1, 13)
    ax.set_ylim(-2, 7)
    ax.axis("off")

    # Title
    ax.text(6, 6.4, "Case Study 2: Grammar-Simulation Pushdown Automaton for Arithmetic Expressions",
            fontsize=13.5, weight="bold", ha="center", color="#0F2C59")
    ax.text(6, 6.0, "E -> E+T | E-T | T      T -> T*F | T/F | F      F -> (E) | id | num",
            fontsize=10, ha="center", color="#333333", style="italic")

    # Start pointer to q0
    ax.annotate("", xy=(0.8, 3.0), xytext=(-0.2, 3.0),
                arrowprops=dict(facecolor="#1E3E62", edgecolor="#1E3E62", width=2, headwidth=8))
    ax.text(0.3, 3.25, "Start", fontsize=10.5, weight="bold", color="#1E3E62", ha="center")

    # State q0
    q0_circle = plt.Circle((1.7, 3.0), 0.75, facecolor="#EBF4F6", edgecolor="#088395", linewidth=2)
    ax.add_patch(q0_circle)
    ax.text(1.7, 3.0, "q0", fontsize=14, weight="bold", ha="center", va="center", color="#088395")
    ax.text(1.7, 1.9, "Initialize", fontsize=9, ha="center", color="#555555")

    # Transition q0 -> qparse with ε, Z0 -> Z0 E
    ax.annotate("", xy=(4.4, 3.0), xytext=(2.6, 3.0),
                arrowprops=dict(facecolor="#1E3E62", edgecolor="#1E3E62", width=2, headwidth=7))
    ax.text(3.5, 3.3, "ε , Z0 -> Z0 E\n(Push E)", fontsize=9.5, weight="bold", ha="center", color="#1E3E62")

    # State qparse
    qp_circle = plt.Circle((5.3, 3.0), 0.85, facecolor="#E8EAF6", edgecolor="#3F51B5", linewidth=2)
    ax.add_patch(qp_circle)
    ax.text(5.3, 3.0, "qparse", fontsize=13, weight="bold", ha="center", va="center", color="#3F51B5")
    ax.text(5.3, 1.8, "Expand Variables\n(Non-terminals)", fontsize=8.5, ha="center", color="#555555")

    # Production expansion self-loop on qparse
    ax.annotate("", xy=(4.8, 3.8), xytext=(5.8, 3.8),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-2.4", color="#3F51B5", lw=2))
    ax.text(5.3, 5.0, "ε-expansions:\nE -> E+T | E-T | T\nT -> T*F | T/F | F\nF -> (E) | id | num",
            fontsize=8.5, weight="semibold", ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#EDE7F6", edgecolor="#7E57C2", lw=1))

    # Transition qparse -> qmatch on token match
    ax.annotate("", xy=(7.9, 3.4), xytext=(6.3, 3.4),
                arrowprops=dict(facecolor="#00796B", edgecolor="#00796B", width=1.8, headwidth=7))
    ax.text(7.1, 3.7, "t , t -> ε\n(Match token)", fontsize=9, weight="bold", ha="center", color="#00796B")

    # Transition qmatch back to qparse on ε
    ax.annotate("", xy=(6.2, 2.6), xytext=(8.0, 2.6),
                arrowprops=dict(facecolor="#00796B", edgecolor="#00796B", width=1.8, headwidth=7))
    ax.text(7.1, 2.1, "ε (Continue)", fontsize=8.5, ha="center", color="#00796B")

    # State qmatch
    qm_circle = plt.Circle((8.9, 3.0), 0.85, facecolor="#E0F2F1", edgecolor="#00796B", linewidth=2)
    ax.add_patch(qm_circle)
    ax.text(8.9, 3.0, "qmatch", fontsize=13, weight="bold", ha="center", va="center", color="#00796B")
    ax.text(8.9, 1.8, "Terminal Match\n& Advance Input", fontsize=8.5, ha="center", color="#555555")

    # Transition qparse -> qf on ε, Z0 -> Z0
    # Arc below
    ax.annotate("", xy=(11.3, 2.4), xytext=(5.5, 2.1),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.3", color="#2E7D32", lw=2))
    ax.text(8.5, 0.4, "ε , Z0 -> Z0  (All tokens consumed; stack cleared)",
            fontsize=9.5, weight="bold", ha="center", color="#2E7D32",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#E8F5E9", edgecolor="#2E7D32", lw=0.8))

    # State qf (Double circle)
    qf_outer = plt.Circle((11.9, 3.0), 0.85, facecolor="#E8F5E9", edgecolor="#2E7D32", linewidth=2.5)
    qf_inner = plt.Circle((11.9, 3.0), 0.7, facecolor="none", edgecolor="#2E7D32", linewidth=1.8)
    ax.add_patch(qf_outer)
    ax.add_patch(qf_inner)
    ax.text(11.9, 3.0, "qf", fontsize=15, weight="bold", ha="center", va="center", color="#2E7D32")
    ax.text(11.9, 1.8, "(Accepting State)", fontsize=8.5, ha="center", color="#2E7D32", weight="bold")

    # Footnote
    ax.text(6.0, -1.3,
            "Nondeterministic CFG Simulation: The PDA nondeterministically chooses production branches.\n"
            "Stack stores pending variables and expected terminals (reversed). Accepted when all tokens match and stack returns to Z0.",
            fontsize=8.5, ha="center", color="#333333", style="italic")

    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    print(f"Generated: {output_path}")


def create_palindrome_pda_diagram(output_path: str):
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
    ax.set_xlim(-1, 11)
    ax.set_ylim(-2, 6)
    ax.axis("off")

    # Title
    ax.text(5, 5.4, "Case Study 3: Nondeterministic Pushdown Automaton for Palindromes",
            fontsize=13.5, weight="bold", ha="center", color="#0F2C59")
    ax.text(5, 5.0, "Alphabet Σ = {'a', 'b'}, Stack Alphabet Γ = {Z0, 'a', 'b'}, CFG: S -> aSa | bSb | a | b | ε",
            fontsize=9.5, ha="center", color="#333333", style="italic")

    # Start pointer to qstart
    ax.annotate("", xy=(0.8, 2.5), xytext=(-0.2, 2.5),
                arrowprops=dict(facecolor="#1E3E62", edgecolor="#1E3E62", width=2, headwidth=8))
    ax.text(0.3, 2.75, "Start", fontsize=10.5, weight="bold", color="#1E3E62", ha="center")

    # State qstart
    qs = plt.Circle((1.5, 2.5), 0.7, facecolor="#EBF4F6", edgecolor="#088395", linewidth=2)
    ax.add_patch(qs)
    ax.text(1.5, 2.5, "qstart", fontsize=12, weight="bold", ha="center", va="center", color="#088395")
    ax.text(1.5, 1.5, "Initial", fontsize=9, ha="center", color="#555555")

    # Transition qstart -> qpush on ε, Z0 -> Z0
    ax.annotate("", xy=(3.3, 2.5), xytext=(2.3, 2.5),
                arrowprops=dict(facecolor="#1E3E62", edgecolor="#1E3E62", width=2, headwidth=7))
    ax.text(2.8, 2.8, "ε , Z0 -> Z0", fontsize=9, weight="bold", ha="center", color="#1E3E62")

    # State qpush
    qp = plt.Circle((4.2, 2.5), 0.8, facecolor="#EDE7F6", edgecolor="#5E35B1", linewidth=2)
    ax.add_patch(qp)
    ax.text(4.2, 2.5, "qpush", fontsize=13, weight="bold", ha="center", va="center", color="#5E35B1")
    ax.text(4.2, 1.4, "Push Phase\n(Store 1st half)", fontsize=8.5, ha="center", color="#555555")

    # Self loops on qpush
    ax.annotate("", xy=(3.8, 3.3), xytext=(4.6, 3.3),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-2.3", color="#5E35B1", lw=1.8))
    ax.text(4.2, 4.3, "a , X -> a X  (Push a)\nb , X -> b X  (Push b)",
            fontsize=8.5, weight="semibold", ha="center",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#F3E5F5", edgecolor="#5E35B1", lw=0.8))

    # Midpoint Guess Transitions from qpush to qmatch
    # 1. Even midpoint (top arc)
    ax.annotate("", xy=(6.4, 2.9), xytext=(5.1, 2.9),
                arrowprops=dict(facecolor="#C2185B", edgecolor="#C2185B", width=1.8, headwidth=7))
    ax.text(5.75, 3.25, "ε , X -> X\n(Even guess)", fontsize=8.5, weight="bold", ha="center", color="#C2185B")

    # 2. Odd midpoint (bottom arc)
    ax.annotate("", xy=(6.4, 2.1), xytext=(5.1, 2.1),
                arrowprops=dict(facecolor="#D81B60", edgecolor="#D81B60", width=1.8, headwidth=7))
    ax.text(5.75, 1.45, "a, X -> X\nb, X -> X\n(Odd center)", fontsize=8, weight="bold", ha="center", color="#D81B60")

    # State qmatch
    qm = plt.Circle((7.3, 2.5), 0.8, facecolor="#E0F2F1", edgecolor="#00897B", linewidth=2)
    ax.add_patch(qm)
    ax.text(7.3, 2.5, "qmatch", fontsize=13, weight="bold", ha="center", va="center", color="#00897B")
    ax.text(7.3, 1.4, "Match Phase\n(Pop & compare)", fontsize=8.5, ha="center", color="#555555")

    # Self loops on qmatch
    ax.annotate("", xy=(6.9, 3.3), xytext=(7.7, 3.3),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-2.3", color="#00897B", lw=1.8))
    ax.text(7.3, 4.3, "a , a -> ε  (Pop a)\nb , b -> ε  (Pop b)",
            fontsize=8.5, weight="semibold", ha="center",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#E0F2F1", edgecolor="#00897B", lw=0.8))

    # Transition qmatch -> qf
    ax.annotate("", xy=(9.1, 2.5), xytext=(8.2, 2.5),
                arrowprops=dict(facecolor="#2E7D32", edgecolor="#2E7D32", width=2, headwidth=7))
    ax.text(8.65, 2.8, "ε , Z0 -> Z0", fontsize=9, weight="bold", ha="center", color="#2E7D32")

    # State qf (Double circle)
    qf_outer = plt.Circle((9.8, 2.5), 0.75, facecolor="#E8F5E9", edgecolor="#2E7D32", linewidth=2.5)
    qf_inner = plt.Circle((9.8, 2.5), 0.6, facecolor="none", edgecolor="#2E7D32", linewidth=1.8)
    ax.add_patch(qf_outer)
    ax.add_patch(qf_inner)
    ax.text(9.8, 2.5, "qf", fontsize=14, weight="bold", ha="center", va="center", color="#2E7D32")
    ax.text(9.8, 1.4, "(Accept)", fontsize=8.5, ha="center", color="#2E7D32", weight="bold")

    # Footnote
    ax.text(5.0, -1.2,
            "Nondeterministic branching: At each symbol, the PDA can either stay in qpush or guess that the midpoint has arrived.\n"
            "An even midpoint is guessed via ε-transition; an odd midpoint is guessed by reading and discarding the center symbol.",
            fontsize=8.5, ha="center", color="#333333", style="italic")

    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    print(f"Generated: {output_path}")


def main():
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "diagrams"))
    os.makedirs(out_dir, exist_ok=True)
    create_balanced_parentheses_diagram(os.path.join(out_dir, "balanced_parentheses_pda.png"))
    create_arithmetic_pda_diagram(os.path.join(out_dir, "arithmetic_expression_pda.png"))
    create_palindrome_pda_diagram(os.path.join(out_dir, "palindrome_pda.png"))


if __name__ == "__main__":
    main()
