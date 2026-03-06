import streamlit as st

st.set_page_config(
    page_title="NoorMVP",
    page_icon="🌙",
    layout="centered"
)

st.markdown("""
<style>

.stApp{
    background:
        radial-gradient(1200px 700px at 20% 10%, rgba(120, 70, 255, 0.20), transparent 55%),
        radial-gradient(900px 600px at 85% 25%, rgba(80, 200, 255, 0.10), transparent 60%),
        linear-gradient(180deg, #070910 0%, #0b0b14 100%);
    color: rgba(255,255,255,0.92);
    font-family: serif;
}

main .block-container{
    max-width: 900px;
    padding-top: 3.5rem;
}

/* Title */

.title{
    text-align:center;
    font-size:44px;
    font-weight:800;
}

.moon{
    display:inline-block;
    animation: moonspin 30s linear infinite;
    filter: drop-shadow(0 0 20px rgba(180,140,255,0.5));
}

@keyframes moonspin{
    from{transform:rotate(0deg);}
    to{transform:rotate(360deg);}
}

/* Message text */

.message{
    text-align:center;
    font-size:18px;
    margin-top:35px;
    line-height:1.8;
}

/* Verses */

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
    animation: heartbeat 1.2s ease-in-out infinite;
    text-shadow:0 0 18px rgba(255,255,255,0.25);
}

@keyframes heartbeat{

0%{transform:scale(1);text-shadow:0 0 8px rgba(255,255,255,0.1);}
20%{transform:scale(1.15);text-shadow:0 0 26px rgba(255,255,255,0.6);}
40%{transform:scale(1);}
60%{transform:scale(1.15);text-shadow:0 0 28px rgba(255,255,255,0.7);}
80%{transform:scale(1);}
100%{transform:scale(1);}

}

.dot{
    padding:0 12px;
    opacity:0.4;
}

/* Fly animation */

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
    animation:
        flyx 11s linear infinite alternate,
        flyy 9s linear infinite alternate;
}

@keyframes flyx{
    from{left:10vw;}
    to{left:85vw;}
}

@keyframes flyy{
    from{top:20vh;}
    to{top:80vh;}
}

/* Footer */

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
    opacity:0.65;
    border-top:1px solid rgba(255,255,255,0.08);
    padding-top:18px;
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


Soon, all users will witness—for free—what Noor is capable of uncovering and discovering.


To ease your anticipation, here are some verses to reflect on.

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="verses">
<span class="v-small">22:60</span>
<span class="dot">·</span>
<span class="v-mid">17:81</span>
<span class="dot">·</span>
<span class="v-small">22:73</span>
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
Noor is your AI guide that brings light to your inquiries through the Qur’an.<br>
Noor is preparing to enhance your experience—bringing reflection, context, and evidence to the claims it presents.
</div>
</div>
</div>
""", unsafe_allow_html=True)
