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

    def find_missing_sandwich_centers(combo_list):
        missing_combos = defaultdict(list)
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
                            missing_combos[middle_combo].append((a, b))
        return missing_combos

    results = find_missing_sandwich_centers(combo_list)

    if results:
        st.success(f"Found {len(results)} missing sandwich combos!")
        output_lines = []
        for missing, context in sorted(results.items()):
            s1, s2 = context[0]
            st.write(f"**{missing}** ← from {s1} and {s2}")
            output_lines.append(missing)

        st.markdown("### Copyable List of Missing Combos")
        st.text("\n".join(output_lines))

        txt = "\n".join(output_lines)
        st.download_button("Download .txt", txt, file_name="missing_sandwich_combos.txt")

    else:
        st.info("No missing sandwich combos found.")
