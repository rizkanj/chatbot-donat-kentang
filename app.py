GIMANA FULL NYA?
import streamlit as st
from google import genai

st.title("Chatbot Customer Service - Donat Kentang Premium")
st.write("Halo! Ada yang bisa kami bantu seputar pesanan donat kentang hari ini?")

# Mengambil GEMINI_API_KEY dari Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    client = None

# Inisialisasi riwayat chat di session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan pesan sebelumnya dari session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kotak input untuk user mengetik pesan
if prompt := st.chat_input("Tulis pertanyaanmu di sini..."):
    # Simpan dan tampilkan pesan dari user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Proses respons dari Gemini
    with st.chat_message("assistant"):
        with st.spinner("Memikirkan jawaban..."):
            try:
                if not client:
                    response = "Maaf Kak, GEMINI_API_KEY belum dikonfigurasi di Streamlit Secrets."
                else:
                    chat_response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                    )
                    response = chat_response.text
            except Exception as e:
                response = f"Maaf Kak, terjadi kesalahan dalam memproses permintaan: {e}"
                
            st.markdown(response)
            
    # Simpan respons assistant ke riwayat chat
    st.session_state.messages.append({"role": "assistant", "content": response})
