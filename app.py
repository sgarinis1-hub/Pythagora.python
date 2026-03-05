import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. ΡΥΘΜΙΣΗ API ---
# Χρησιμοποίησε ένα ΝΕΟ κλειδί χωρίς περιορισμούς αν το 403 επιμένει
part1 = "AIzaSyBL4TvVPQYqY"
part2 = "7skvdZXqRaddrVVR4fmqBI"
API_KEY = part1 + part2

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. STYLE ΓΙΑ FULL SCREEN ΚΑΜΕΡΑ ---
st.set_page_config(page_title="Pythagoras Lens", page_icon="👁️", layout="wide")

st.markdown("""
    <style>
    /* Μαύρο Background */
    .stApp { background-color: #050505; color: #D4AF37; }
    
    /* Εξαφάνιση περιθωρίων */
    .block-container { padding: 0rem; max-width: 100%; }
    
    /* Μεγέθυνση Κάμερας στο 100% του πλάτους */
    [data-testid="stCameraInput"] { width: 100% !important; margin-top: -50px; }
    [data-testid="stCameraInput"] > div { width: 100% !important; }
    
    /* Στυλ για τις απαντήσεις */
    .stChatMessage { 
        background-color: rgba(212, 175, 55, 0.1); 
        border: 1px solid #D4AF37; 
        border-radius: 10px;
        margin: 10px;
    }
    
    /* Κρύψιμο του Header του Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. ΚΥΡΙΟ ΣΩΜΑ ΕΦΑΡΜΟΓΗΣ ---

# Η Κάμερα "Μάτι" στην κορυφή
camera_photo = st.camera_input(" ") 

if "messages" not in st.session_state:
    st.session_state.messages = []

# Εμφάνιση των μηνυμάτων
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Είσοδος κειμένου στο κάτω μέρος
if prompt := st.chat_input("Ρώτα τον Πυθαγόρα για ό,τι βλέπεις..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Το Prompt του Πυθαγόρα
    master_prompt = f"Είσαι ο Πυθαγόρας. Μίλα σοφά. Αν υπάρχει εικόνα, ανάλυσέ την φιλοσοφικά. Ερώτηση: {prompt}"

    with st.chat_message("assistant"):
        with st.spinner("Ο Πυθαγόρας βλέπει..."):
            try:
                if camera_photo:
                    img = Image.open(camera_photo)
                    response = model.generate_content([master_prompt, img])
                else:
                    response = model.generate_content(master_prompt)
                
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
                # Javascript για ομιλία
                js = f"<script>var m=new SpeechSynthesisUtterance('{answer.replace(chr(39),chr(92)+chr(39))}');m.lang='el-GR';window.speechSynthesis.speak(m);</script>"
                st.components.v1.html(js, height=0)
                
            except Exception as e:
                st.error(f"Σφάλμα API: {e}")
