import streamlit as st
from google import genai

st.title("Chatbot Customer Service - Donat Kentang Premium")
st.write("Halo! Ada yang bisa kami bantu seputar pesanan donat kentang hari ini?")

# Konfigurasi Client Gemini (Pastikan API Key sudah disetel di environment atau secrets)
# client = genai.Client(api_key="MASUKKAN_API_KEY_KAMU_DISINI")

# Inisialisasi riwayat chat
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

    # --- BAGIAN INTEGRASI LLM YANG KURANG ---
    with st.chat_message("assistant"):
        with st.spinner("Memikirkan jawaban..."):
            try:
                # Contoh pemanggilan model Gemini menggunakan client resmi
                client = genai.Client() # Atau masukkan API key langsung
                
                # Mengirim riwayat percakapan atau prompt langsung ke model gemini-2.5-flash
                # (Pastikan model yang dipakai sesuai dengan materi yang diajarkan)
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
