import streamlit as st

st.set_page_config(
    page_title="NoorMVP",
    page_icon="🌙",
    layout="centered"
)

st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at 20% 20%, #1a1a2e, #0b0b14);
    color: white;
    font-family: serif;
}

.title {
    text-align:center;
    font-size:42px;
    font-weight:700;
    margin-top:40px;
}

.message{
    text-align:center;
    font-size:18px;
    opacity:0.9;
    margin-top:20px;
    line-height:1.6;
}

.verses{
    text-align:center;
    font-size:30px;
    margin-top:60px;
    letter-spacing:4px;
}

.fly{
    position: fixed;
    top: 68%;
    left: 21%;
    font-size:14px;
    opacity:0.7;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🌙 NoorMVP</div>', unsafe_allow_html=True)

st.markdown("""
<div class="message">
Thank you for your patience as Noor, once again, returns to building something real.<br><br>
While you wait, please consider reflecting on these verses:
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="verses">
17:81 · 22:60 · 22:73
</div>
""", unsafe_allow_html=True)

# tiny fly reference to 22:73
st.markdown('<div class="fly">🪰</div>', unsafe_allow_html=True)
