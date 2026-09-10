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
                "Kami memiliki cabang yang tersebar di seluruh Indonesia, termasuk di Kota Tangerang lho!\n\n"
                "Ada yang bisa kami bantu hari ini? Apakah seputar info cabang terdekat, atau mau intip 3 menu spesial kami:\n"
                "1. **Donat Meses** - Rp 5.000/pcs\n"
                "2. **Donat Creamy** - Rp 10.000/pcs\n"
                "3. **Donat Bomboloni** - Rp 7.000/pcs\n\n"
                "Silakan tanyakan apa saja, Kak!"
            )
        }
    ]

# Tampilkan pesan sebelumnya dari session state secara berurutan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kotak input untuk user mengetik pesan
if prompt := st.chat_input("Tulis pertanyaan atau pesananmu di sini..."):
    # 1. Simpan dan tampilkan pesan dari user terlebih dahulu
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Proses respons dari Gemini dengan membawa riwayat percakapan
    with st.chat_message("assistant"):
        with st.spinner("Memikirkan jawaban..."):
            try:
                if not client:
                    response = "Maaf Kak, kunci API Gemini belum dikonfigurasi di Streamlit Secrets."
                else:
                    system_instruction = (
                        "Kamu adalah customer service ramah untuk toko 'Donat Kentang Premium'. "
                        "Toko kita memiliki cabang yang tersebar di seluruh Indonesia (termasuk Kota Tangerang). "
                        "Menu utama yang kita tawarkan ada 3: "
                        "1. Donat Meses (Rp 5.000/pcs), "
                        "2. Donat Creamy (Rp 10.000/pcs), "
                        "3. Donat Bomboloni (Rp 7.000/pcs). "
                        "Jawab pertanyaan pelanggan dengan ramah, luwes, dan ingat konteks percakapan sebelumnya. "
                        "Jangan mengulang-ngulang salam pembuka jika sudah disapa sebelumnya."
                    )

                    # Ubah format riwayat pesan agar bisa dibaca oleh client.chats
                    # (menggabungkan system instruction dengan history chat)
                    formatted_history = []
                    for msg in st.session_state.messages[:-1]: # Ambil riwayat sebelum pesan terakhir
                        role_mapping = "user" if msg["role"] == "user" else "model"
                        formatted_history.append({
                            "role": role_mapping,
                            "parts": [{"text": msg["content"]}]
                        })

                    # Mulai sesi chat dengan history yang tersimpan
                    chat = client.chats.create(
                        model='gemini-3.6-flash',
                        history=formatted_history,
                        config={"system_instruction": system_instruction}
                    )

                    # Kirim pesan terbaru dari user
                    chat_response = chat.send_message(prompt)
                    response = chat_response.text

            except Exception as e:
                response = f"Maaf Kak, terjadi kesalahan dalam memproses permintaan: {e}"
                
            st.markdown(response)
            
    # 3. Simpan respons assistant ke riwayat chat
    st.session_state.messages.append({"role": "assistant", "content": response})
