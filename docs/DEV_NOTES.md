# Developer Notes & Constraints

## PowerShell Command Chaining
- **ERROR TO AVOID**: Do NOT use the ampersand `&` (l'espeluette) to chain commands in PowerShell.
- **CORRECT SYNTAX**: Use the semicolon `;` to separate commands.
  - ❌ Incorrect: `taskkill /F /IM python.exe & streamlit run app.py`
  - ✅ Correct: `taskkill /F /IM python.exe ; streamlit run app.py`

## Streamlit Interaction
- **Widget State**: Do not attempt to modify `st.session_state` for a widget (like a checkbox) *after* it has been instantiated in the same script run. This causes a `StreamlitAPIException`.
