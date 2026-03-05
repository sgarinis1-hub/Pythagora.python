import streamlit as st
import google.generativeai as genai

# Ρύθμιση Gemini
# Χρησιμοποίησε το API Key σου
genai.configure(api_key="ΤΟ_API_KEY_ΣΟΥ")
model = genai.GenerativeModel('gemini-1.5-flash')

# Λειτουργία API: Αν η HTML στείλει ερώτηση μέσω URL
query_params = st.query_params
if "q" in query_params:
    user_query = query_params["q"]
    prompt = f"Είσαι ο Πυθαγόρας ο Σάμιος. Απάντησε σοφά και σύντομα: {user_query}"
    response = model.generate_content(prompt)
    st.write(response.text) # Αυτό επιστρέφει την απάντηση στην HTML
    st.stop() 

# Εμφάνιση για εσένα (Admin panel)
st.title("🏛️ Pythagoras Brain Server")
st.info("Ο server είναι Online. Η HTML σελίδα μπορεί πλέον να του στέλνει ερωτήσεις.")
