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

    def find_missing_targets(combo_list):
        missing_combos = defaultdict(list)
        for combo in combo_list:
            digits = list(combo)
            for i in range(5):
                d = int(digits[i])

                # Check for sandwich trap: combo[i-1], combo[i+1] -> want center
                for delta in [-2, 2]:
                    neighbor_digits = digits.copy()
                    neighbor_value = d + delta
                    if 0 <= neighbor_value <= 9:
                        neighbor_digits[i] = str(neighbor_value)
                        neighbor_combo = ''.join(neighbor_digits)

                        # middle value between current and neighbor
                        middle_digit = str((d + neighbor_value) // 2)
                        center_digits = digits.copy()
                        center_digits[i] = middle_digit
                        center_combo = ''.join(center_digits)

                        if neighbor_combo in combo_set and center_combo not in combo_set:
                            missing_combos[center_combo].append((combo, neighbor_combo))

                # If combo is center, make sure ±1 neighbors are present
                for offset in [-1, 1]:
                    neighbor_digits = digits.copy()
                    new_val = d + offset
                    if 0 <= new_val <= 9:
                        neighbor_digits[i] = str(new_val)
                        neighbor_combo = ''.join(neighbor_digits)
                        if neighbor_combo not in combo_set:
                            missing_combos[neighbor_combo].append((combo,))

        return missing_combos

    results = find_missing_targets(combo_list)

    if results:
        st.success(f"Found {len(results)} missing sandwich combos!")
        output_lines = []
        for missing, context in sorted(results.items()):
            example = ' and '.join(context[0])
            st.write(f"**{missing}** ← from {example}")
            output_lines.append(missing)

        st.markdown("### Copyable List of Missing Combos")
        st.text("\n".join(output_lines))

        txt = "\n".join(output_lines)
        st.download_button("Download .txt", txt, file_name="missing_sandwich_combos.txt")

    else:
        st.info("No missing sandwich combos found.")
