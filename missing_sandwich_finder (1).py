import streamlit as st
from collections import defaultdict
import pandas as pd

st.title("Missing Sandwich Combo Finder")

st.markdown("""
Paste a list of 5-digit combos below (one per line or comma-separated). This app will find all missing
combinations that are 'sandwiched' between two others, differing by ±1 in the same digit position.
""")

user_input = st.text_area("Paste your combos here:", height=300)

if user_input:
    raw_lines = user_input.replace(',', '\n').split('\n')
    combo_list = [line.strip() for line in raw_lines if line.strip().isdigit() and len(line.strip()) == 5]
    combo_set = set(combo_list)

    def find_missing_sandwich_combos(combo_list):
        missing_centers = defaultdict(list)
        for a in combo_list:
            for b in combo_list:
                if a == b:
                    continue

                diff_positions = [k for k in range(5) if a[k] != b[k]]
                if len(diff_positions) == 1:
                    pos = diff_positions[0]
                    da, db = int(a[pos]), int(b[pos])
                    if abs(da - db) == 1:
                        # check in the same direction for the 3rd missing link
                        forward_digit = str(max(da, db) + 1)
                        if int(forward_digit) <= 9:
                            forward = list(a)
                            forward[pos] = forward_digit
                            forward_combo = ''.join(forward)
                            if forward_combo not in combo_set:
                                missing_centers[forward_combo].append((a, b))

                        backward_digit = str(min(da, db) - 1)
                        if int(backward_digit) >= 0:
                            backward = list(a)
                            backward[pos] = backward_digit
                            backward_combo = ''.join(backward)
                            if backward_combo not in combo_set:
                                missing_centers[backward_combo].append((a, b))

        return missing_centers

    results = find_missing_sandwich_combos(combo_list)

    if results:
        st.success(f"Found {len(results)} missing sandwich combos!")
        output_lines = []
        for missing, siblings in sorted(results.items()):
            s1, s2 = siblings[0]
            st.write(f"**{missing}** ← from {s1} and {s2}")
            output_lines.append(missing)

        st.markdown("### Copyable List of Missing Combos")
        st.text("\n".join(output_lines))

        txt = "\n".join(output_lines)
        st.download_button("Download .txt", txt, file_name="missing_sandwich_combos.txt")

    else:
        st.info("No missing sandwich combos found.")
