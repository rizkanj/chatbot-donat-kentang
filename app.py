import streamlit as st
from google import genai

st.title("Chatbot Customer Service - Donat Kentang Premium")
st.write("Halo! Ada yang bisa kami bantu seputar pesanan donat kentang hari ini?")

# Fleksibel: Cek nama GEMINI_API_KEY atau GEMINI di Streamlit Secrets
api_key = None
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    try:
        api_key = st.secrets["GEMINI"]
    except Exception:
        api_key = None

# Inisialisasi client Gemini
if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None

# Inisialisasi riwayat chat di session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Halo! Selamat datang di layanan pelanggan **Donat Kentang Premium** 🍩. "
                "Kami memiliki cabang yang tersebar di seluruh Indonesia lho!\n\n"
                "Ada yang bisa kami bantu hari ini? Apakah seputar info cabang terdekat, atau mau intip 3 menu spesial kami:\n"
                "1. **Donat Meses** - Rp 5.000/pcs\n"
                "2. **Donat Creamy** - Rp 10.000/pcs\n"
                "3. **Donat Bomboloni** - Rp 7.000/pcs\n\n"
                "Silakan tanyakan apa saja, Kak!"
            )
        }
    ]

# Tampilkan pesan sebelumnya dari session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kotak input untuk user mengetik pesan
if prompt := st.chat_input("Tulis pertanyaan atau pesananmu di sini..."):
    # Simpan dan tampilkan pesan dari user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Proses respons dari Gemini dengan instruksi sistem yang lebih luwes
    with st.chat_message("assistant"):
        with st.spinner("Memikirkan jawaban..."):
            try:
                if not client:
                    response = "Maaf Kak, kunci API Gemini belum dikonfigurasi di Streamlit Secrets."
                else:
                    # Instruksi sistem yang luwes: toko punya cabang di seluruh Indonesia dan fokus ke 3 menu
                    system_instruction = (
                        "Kamu adalah customer service ramah untuk toko 'Donat Kentang Premium'. "
                        "Toko kita memiliki cabang yang tersebar di seluruh Indonesia. "
                        "Menu utama yang kita tawarkan ada 3: "
                        "1. Donat Meses (Rp 5.000/pcs), "
                        "2. Donat Creamy (Rp 10.000/pcs), "
                        "3. Donat Bomboloni (Rp 7.000/pcs). "
                        "Jawab pertanyaan pelanggan dengan ramah, luwes, dan natural. "
                        "Jika ditanya soal lokasi/cabang, jelaskan bahwa kita punya cabang di berbagai kota di seluruh Indonesia dan bantu arahkan mereka. "
                        "Bantu juga mereka jika ingin memesan ketiga menu tersebut."
                    )
                    
                    chat_response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=f"{system_instruction}\n\nPertanyaan pelanggan: {prompt}",
                    )
                    response = chat_response.text
            except Exception as e:
                response = f"Maaf Kak, terjadi kesalahan dalam memproses permintaan: {e}"
                
            st.markdown(response)
            
    # Simpan respons assistant ke riwayat chat
    st.session_state.messages.append({"role": "assistant", "content": response})
