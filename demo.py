import streamlit as st
st.write("Hello, I am Anushmita")
s = st.text_input("Enter your name:")
if s:
    st.write(f"Hi {s}, nice to meet you!")
