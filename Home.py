import streamlit as st

st.title("make voice with aws polly")
a = st.select_slider("Pick a size", ["S", "M", "L"])
st.write(a)