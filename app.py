import streamlit as st

st.title("Chatbot Customer Service - Donat Kentang Premium")
st.write("Halo! Ada yang bisa kami bantu seputar pesanan donat kentang hari ini?")

# Inisialisasi riwayat chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan pesan sebelumnya
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kotak input untuk user mengetik pesan
if prompt := st.chat_input("Tulis pertanyaanmu di sini..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bagian respons dari LLM
    response = f"Halo Kak! Terima kasih sudah bertanya. Untuk menu Donat Kentang Premium kami..."
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
