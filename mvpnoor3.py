import time
import streamlit as st

st.set_page_config(page_title="NoorMVP", page_icon="🌙", layout="centered")

if "verse_index" not in st.session_state:
    st.session_state.verse_index = 0

verse_states = [
    ("22:60", "17:81", "22:73"),
    ("17:81", "22:73", "22:60"),
    ("22:73", "22:60", "17:81"),
]

left_verse, center_verse, right_verse = verse_states[st.session_state.verse_index]

st.markdown("""
<style>

.stApp{
background:
radial-gradient(circle at 20% 10%, rgba(120,70,255,0.20), transparent 55%),
radial-gradient(circle at 85% 25%, rgba(80,200,255,0.10), transparent 60%),
linear-gradient(180deg,#070910,#0b0b14);
color:white;
font-family:serif;
}

.title{
text-align:center;
font-size:44px;
font-weight:800;
margin-top:20px;
}

.moon{
display:inline-block;
animation:moonspin 30s linear infinite;
filter:drop-shadow(0 0 20px rgba(180,140,255,0.6));
}

@keyframes moonspin{
from{transform:rotate(0deg);}
to{transform:rotate(360deg);}
}

.message{
text-align:center;
font-size:18px;
margin-top:30px;
line-height:1.8;
}

.verses{
text-align:center;
margin-top:70px;
letter-spacing:3px;
}

.v-small{
font-size:26px;
opacity:0.8;
}

.v-mid{
font-size:46px;
font-weight:900;
padding:0 12px;
display:inline-block;
animation:heartbeat 1.2s ease-in-out 3;
text-shadow:0 0 18px rgba(255,255,255,0.35);
}

@keyframes heartbeat{
0%{transform:scale(1);}
20%{transform:scale(1.15);}
40%{transform:scale(1);}
60%{transform:scale(1.15);}
80%{transform:scale(1);}
100%{transform:scale(1);}
}

.dot{
padding:0 12px;
opacity:0.4;
}

.sub-verses{
text-align:center;
margin-top:25px;
font-size:18px;
letter-spacing:2px;
opacity:0.6;
}

/* fly */

.flywrap{
position:fixed;
top:0;
left:0;
width:100vw;
height:100vh;
pointer-events:none;
}

.fly{
position:absolute;
font-size:13px;
animation:flyx 11s linear infinite alternate, flyy 9s linear infinite alternate;
}

@keyframes flyx{
from{left:10vw;}
to{left:85vw;}
}

@keyframes flyy{
from{top:20vh;}
to{top:80vh;}
}

/* footer */

.footerwrap{
margin-top:120px;
display:flex;
justify-content:center;
}

.footer{
display:flex;
gap:12px;
max-width:720px;
font-size:14px;
opacity:0.7;
border-top:1px solid rgba(255,255,255,0.1);
padding-top:18px;
line-height:1.6;
}

.spinner{
width:16px;
height:16px;
border:2px solid rgba(255,255,255,0.2);
border-top:2px solid white;
border-radius:50%;
animation:spin 1.2s linear infinite;
}

@keyframes spin{
from{transform:rotate(0deg);}
to{transform:rotate(360deg);}
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title"><span class="moon">🌙</span> NoorMVP</div>', unsafe_allow_html=True)

st.markdown("""
<div class="message">

Please be patient as Noor reprograms itself after several recurring errors.
All users will be able to experience—for free— how Noor uses the Qur'an to uncover, discover, recover. 

To ease your anticipation, here are 3 + 2 verses to reflect on.

</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="verses">
<span class="v-small">{left_verse}</span>
<span class="dot">·</span>
<span class="v-mid">{center_verse}</span>
<span class="dot">·</span>
<span class="v-small">{right_verse}</span>
</div>

<div class="sub-verses">
49:11 · 24:11
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="flywrap">
<div class="fly">🪰</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footerwrap">
<div class="footer">
<div class="spinner"></div>
<div>
Noor is actively reprogramming itself—undertaking the careful work of recalibrating.<br>
Noor is your AI guide that brings darkness to light  using guidance from the Qur’an.
</div>
</div>
</div>
""", unsafe_allow_html=True)

time.sleep(3)
st.session_state.verse_index = (st.session_state.verse_index + 1) % len(verse_states)
st.rerun()
