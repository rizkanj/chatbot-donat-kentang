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

    # 2. Proses respons dari Gemini
    with st.chat_message("assistant"):
        with st.spinner("Memikirkan jawaban..."):
            try:
                if not client:
                    response = "Maaf Kak, kunci API Gemini belum dikonfigurasi di Streamlit Secrets."
                else:
                    # Susun riwayat chat dan sisipkan instruksi karakter CS di awal
                    contents_payload = [
                        (
                            "Aturan peran: Kamu adalah customer service ramah untuk toko 'Donat Kentang Premium'. "
                            "Toko kita memiliki cabang di seluruh Indonesia (termasuk Tangerang). "
                            "Menu utama kita hanya ada 3: Donat Meses (Rp 5.000/pcs), Donat Creamy (Rp 10.000/pcs), "
                            "dan Donat Bomboloni (Rp 7.000/pcs). Jawablah dengan ramah, luwes, dan ingat konteks sebelumnya."
                        )
                    ]
                    
                    # Masukkan seluruh riwayat obrolan sebelumnya
                    for msg in st.session_state.messages:
                        prefix = "User: " if msg["role"] == "user" else "Assistant: "
                        contents_payload.append(prefix + msg["content"])

                    # Kirim payload lengkap ke model
                    chat_response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=contents_payload,
                    )
                    response = chat_response.text

            except Exception as e:
                response = f"Maaf Kak, terjadi kesalahan dalam memproses permintaan: {e}"
                
            st.markdown(response)
            
    # 3. Simpan respons assistant ke riwayat chat
    st.session_state.messages.append({"role": "assistant", "content": response})
