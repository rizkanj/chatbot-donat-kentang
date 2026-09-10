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
                "Halo! Selamat datang di layanan pelanggan Donat Kentang Premium. 🍩\n\n"
                "Berikut adalah 3 menu utama kami:\n"
                "1. **Donat Meses** - Rp 5.000/pcs\n"
                "   *(Donat lembut dengan taburan meses dan berbagai pilihan topping)*\n"
                "2. **Donat Creamy** - Rp 10.000/pcs\n"
                "   *(Donat lembut dengan isian krim yang manis, creamy, dan lumer di mulut)*\n"
                "3. **Donat Bomboloni** - Rp 7.000/pcs\n"
                "   *(Donat lembut tanpa lubang dengan isian krim yang melimpah)*\n\n"
                "Ada yang bisa saya bantu terkait pemesanan menu di atas, Kak?"
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

    # Proses respons dari Gemini dengan instruksi sistem agar fokus ke 3 menu tersebut
    with st.chat_message("assistant"):
        with st.spinner("Memikirkan jawaban..."):
            try:
                if not client:
                    response = "Maaf Kak, kunci API Gemini belum dikonfigurasi di Streamlit Secrets."
                else:
                    # Instruksi sistem agar bot bertindak sebagai CS Donat Kentang dengan 3 menu spesifik
                    system_instruction = (
                        "Kamu adalah customer service ramah untuk toko 'Donat Kentang Premium'. "
                        "Kamu HANYA menjual dan membahas 3 menu berikut:\n"
                        "1. Donat Meses (Rp 5.000/pcs) - camilan lembut dengan taburan meses.\n"
                        "2. Donat Creamy (Rp 10.000/pcs) - donat dengan isian krim lumer.\n"
                        "3. Donat Bomboloni (Rp 7.000/pcs) - donat tanpa lubang dengan isian krim melimpah.\n"
                        "Jika pelanggan bertanya di luar menu ini, arahkan dengan sopan kembali ke 3 menu tersebut. "
                        "Bantu mereka mencatat pesanan, jumlah, atau menjawab pertanyaan seputar menu ini."
                    )
                    
                    # Mengirim prompt beserta konteks sistem menggunakan model gemini-2.5-flash
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
