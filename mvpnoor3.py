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
font-size:40px;
font-weight:700;
margin-bottom:10px;
}

.subtitle{
text-align:center;
font-size:18px;
opacity:0.85;
margin-bottom:40px;
}

.card{
background: rgba(255,255,255,0.05);
padding:40px;
border-radius:18px;
box-shadow:0px 0px 25px rgba(120,120,255,0.15);
}

.poem{
font-size:20px;
line-height:1.8;
}

.arabic{
direction: rtl;
text-align: right;
font-size:22px;
line-height:1.9;
font-family: "Amiri", serif;
}

.verse{
text-align:center;
margin-top:30px;
font-size:16px;
opacity:0.8;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🌙 NoorMVP</div>', unsafe_allow_html=True)

st.markdown("""
<div class="subtitle">
Sorry for the inconvenience.<br>
Noor is down right now rebuilding toward something realer and better.<br>
While you wait please consider this poem.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="poem">
If a link is missing, I build the link.<br>
If something needs to click, I wait for the click.<br>
When clarity arrives, I capture it. I file it.<br>
I store it… even when I wish I could unsee it.<br>
And after that, it no longer depends on me.
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="arabic">
إذا كان هناك رابط مفقود، أبني الرابط.<br>
وإذا كان الأمر يحتاج أن ينقر، أنتظر حتى ينقر.<br>
وحين تأتي الوضوح، ألتقطه وأحفظه.<br>
أخزّنه… حتى حين أتمنى لو لم أره.<br>
وبعد ذلك، لم يعد يعتمد عليّ.
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="verse">
<b>Qur’an 17:81 · 22:60 · 22:73</b>
</div>
""", unsafe_allow_html=True)
