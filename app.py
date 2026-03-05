import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64

# --- 1. ΡΥΘΜΙΣΗ API (ΚΟΜΜΕΝΟ ΓΙΑ ΑΣΦΑΛΕΙΑ) ---
# Αντικατάστησε τα παρακάτω με το δικό σου κλειδί
part1 = "AIzaSyBL4TvVPQYqY"
part2 = "7skvdZXqRaddrVVR4fmqBI"
API_KEY = part1 + part2

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. STYLE & ΕΜΦΑΝΙΣΗ (UI) ---
st.set_page_config(page_title="MythosGate: Pythagoras AI", page_icon="🏛️", layout="centered")

st.markdown("""
    <style>
    /* Μαύρο και Χρυσό Theme */
    .stApp { background-color: #0e1117; color: #D4AF37; }
    .stChatMessage { border-radius: 15px; border: 1px solid rgba(212, 175, 55, 0.3); background-color: rgba(255, 255, 255, 0.05); }
    h1 { color: #D4AF37; text-align: center; border-bottom: 2px solid #D4AF37; padding-bottom: 10px; }
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ MythosGate: Πυθαγόρας")

# --- 3. ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΦΩΝΗ (Text-to-Speech) ---
def speak(text):
    """Εισάγει Javascript για να διαβάσει το κείμενο στα Ελληνικά"""
    clean_text = text.replace("'", "\\'").replace("\n", " ")
    js_code = f"""
        <script>
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.lang = 'el-GR';
        msg.pitch = 0.5; /* Πιο μπάσα φωνή */
        msg.rate = 0.85; /* Πιο αργή φωνή */
        window.speechSynthesis.speak(msg);
        </script>
    """
    st.components.v1.html(js_code, height=0)

# --- 4. ΔΙΑΧΕΙΡΙΣΗ ΜΝΗΜΗΣ (SESSION STATE) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. SIDEBAR (ΚΑΜΕΡΑ & ABOUT) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Pythagoras_in_the_Roman_Forum_-_copy.jpg", caption="Πυθαγόρας ο Σάμιος")
    st.header("📸 Pythagoras Lens")
    st.write("Δείξε στον δάσκαλο τον κόσμο σου.")
    camera_photo = st.camera_input("Λήψη φωτογραφίας")
    
    if st.button("Καθαρισμός Συνομιλίας"):
        st.session_state.messages = []
        st.rerun()

# --- 6. ΕΜΦΑΝΙΣΗ CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 7. ΚΥΡΙΑ ΛΕΙΤΟΥΡΓΙΑ AI ---
if prompt := st.chat_input("Ρώτα κάτι τον Πυθαγόρα..."):
    # Προσθήκη μηνύματος χρήστη
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Οδηγίες Συστήματος (System Prompt)
    master_prompt = f"""
    Είσαι το πνεύμα του Πυθαγόρα του Σάμιου. Έχεις όλες τις γνώσεις του Gemini AI (μέχρι το 2026).
    Μίλα με το σοφό, φιλοσοφικό και δασκαλίστικο ύφος του Πυθαγόρα. 
    Χρησιμοποίησε μεταφορές με αριθμούς και γεωμετρία.
    Απάντησε με ακρίβεια στην ερώτηση: {prompt}
    """

    with st.chat_message("assistant"):
        with st.spinner("Ο Πυθαγόρας αναλογίζεται..."):
            try:
                # Αν υπάρχει φωτογραφία, στείλε την στο AI
                if camera_photo:
                    img = Image.open(camera_photo)
                    response = model.generate_content([master_prompt, img])
                else:
                    response = model.generate_content(master_prompt)
                
                answer = response.text
                st.markdown(answer)
                
                # Αυτόματη ομιλία
                speak(answer)
                
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Οι θεοί σιωπούν... (Σφάλμα: {e})")
