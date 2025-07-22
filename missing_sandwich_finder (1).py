import streamlit as st
from collections import defaultdict
import pandas as pd

st.title("Missing Sandwich Combo Finder")

st.markdown("""
Paste a list of 5-digit combos below (one per line or comma-separated). This app will find all missing
combinations that are 'sandwiched' between two others:
- **Center traps**: where two combos differ by ±2 in one digit and the middle is missing.
- **Forward traps**: where two consecutive steps exist and the next is missing.
- **Backward traps**: where two consecutive steps exist and the prior is missing.
""")

user_input = st.text_area("Paste your combos here:", height=300)

if user_input:
    raw_lines = user_input.replace(',', '\n').split('\n')
    combo_list = [line.strip() for line in raw_lines if line.strip().isdigit() and len(line.strip()) == 5]
    combo_set = set(combo_list)

    def find_center_traps(combo_list):
        traps = defaultdict(list)
        for a in combo_list:
            for b in combo_list:
                if a >= b:
                    continue
                diffs = [(i, int(a[i]), int(b[i])) for i in range(5) if a[i] != b[i]]
                if len(diffs) == 1:
                    i, da, db = diffs[0]
                    if abs(da - db) == 2:
                        mid_digit = str((da + db) // 2)
                        middle = list(a)
                        middle[i] = mid_digit
                        middle_combo = ''.join(middle)
                        if middle_combo not in combo_set:
                            traps[middle_combo].append((a, b))
        return traps

    def find_forward_traps(combo_list):
        traps = defaultdict(list)
        for combo in combo_list:
            digits = list(combo)
            for i in range(5):
                d = int(digits[i])
                if d <= 7:
                    step1 = digits.copy()
                    step2 = digits.copy()
                    step1[i] = str(d + 1)
                    step2[i] = str(d + 2)
                    combo1 = ''.join(step1)
                    combo2 = ''.join(step2)
                    if combo1 in combo_set and combo2 not in combo_set:
                        traps[combo2].append((combo, combo1))
        return traps

    def find_backward_traps(combo_list):
        traps = defaultdict(list)
        for combo in combo_list:
            digits = list(combo)
            for i in range(5):
                d = int(digits[i])
                if d >= 2:
                    step1 = digits.copy()
                    step2 = digits.copy()
                    step1[i] = str(d - 1)
                    step2[i] = str(d - 2)
                    combo1 = ''.join(step1)
                    combo2 = ''.join(step2)
                    if combo1 in combo_set and combo2 not in combo_set:
                        traps[combo2].append((combo1, combo))
        return traps

    center_results = find_center_traps(combo_list)
    forward_results = find_forward_traps(combo_list)
    backward_results = find_backward_traps(combo_list)

    total = len(center_results) + len(forward_results) + len(backward_results)
    st.success(f"Found {total} missing sandwich combos! ({len(center_results)} center, {len(forward_results)} forward, {len(backward_results)} backward)")

    if center_results:
        st.markdown("### Center Traps")
        for missing, sources in sorted(center_results.items()):
            s1, s2 = sources[0]
            st.write(f"**{missing}** ← from {s1} and {s2}")

    if forward_results:
        st.markdown("### Forward Traps")
        for missing, sources in sorted(forward_results.items()):
            s1, s2 = sources[0]
            st.write(f"**{missing}** ← from {s1} and {s2}")

    if backward_results:
        st.markdown("### Backward Traps")
        for missing, sources in sorted(backward_results.items()):
            s1, s2 = sources[0]
            st.write(f"**{missing}** ← from {s1} and {s2}")

    all_missing = list(center_results.keys()) + list(forward_results.keys()) + list(backward_results.keys())
    if all_missing:
        st.markdown("### Copyable List of All Missing Combos")
        st.text("\n".join(sorted(all_missing)))

        txt = "\n".join(sorted(all_missing))
        st.download_button("Download .txt", txt, file_name="missing_sandwich_combos.txt")
    else:
        st.info("No missing sandwich combos found.")
