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
    overflow: hidden;
}

main .block-container{
    max-width: 900px;
    padding-top: 3.2rem;
    padding-bottom: 2rem;
}

.title{
    text-align: center;
    font-size: 44px;
    font-weight: 800;
    margin-top: 10px;
    letter-spacing: 0.3px;
}

.moon{
    display: inline-block;
    filter: drop-shadow(0 0 18px rgba(180, 140, 255, 0.40));
    text-shadow: 0 0 22px rgba(180, 140, 255, 0.40);
    animation: moonspin 26s linear infinite;
    transform-origin: center center;
}

@keyframes moonspin{
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.message{
    text-align: center;
    font-size: 18px;
    opacity: 0.92;
    margin-top: 22px;
    line-height: 1.7;
}

.verses{
    text-align: center;
    margin-top: 68px;
    user-select: none;
}

.v-small{
    font-size: 26px;
    opacity: 0.82;
    letter-spacing: 3px;
}

.v-mid{
    font-size: 44px;
    font-weight: 900;
    opacity: 1;
    letter-spacing: 3px;
    display: inline-block;
    padding: 0 12px;
    text-shadow: 0 0 18px rgba(255,255,255,0.10);
}

.dot{
    font-size: 26px;
    opacity: 0.45;
    padding: 0 12px;
}

/* Bouncing fly */
.fly-wrap{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    overflow: hidden;
    z-index: 20;
}

.fly{
    position: absolute;
    top: 20vh;
    left: 12vw;
    font-size: 13px;
    opacity: 0.78;
    animation:
        fly-x 11s linear infinite alternate,
        fly-y 8s linear infinite alternate,
        fly-tilt 0.9s ease-in-out infinite alternate;
}

@keyframes fly-x{
    from { left: 8vw; }
    to   { left: 88vw; }
}

@keyframes fly-y{
    from { top: 22vh; }
    to   { top: 78vh; }
}

@keyframes fly-tilt{
    from { transform: rotate(-18deg) scale(1); }
    to   { transform: rotate(16deg) scale(1.04); }
}

.footer-wrap{
    margin-top: 140px;
    display: flex;
    justify-content: center;
}

.footer{
    display: flex;
    align-items: flex-start;
    gap: 12px;
    max-width: 720px;
    color: rgba(255,255,255,0.68);
    font-size: 14px;
    line-height: 1.6;
    text-align: left;
    border-top: 1px solid rgba(255,255,255,0.08);
    padding-top: 18px;
}

.spinner{
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255,255,255,0.18);
    border-top: 2px solid rgba(255,255,255,0.75);
    border-radius: 50%;
    animation: spin 1.15s linear infinite;
    margin-top: 2px;
    flex-shrink: 0;
}

@keyframes spin{
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* Slight responsiveness */
@media (max-width: 700px){
    .title{ font-size: 38px; }
    .message{ font-size: 17px; }
    .v-small{ font-size: 22px; }
    .v-mid{ font-size: 38px; }
    .dot{ font-size: 22px; padding: 0 8px; }
    .footer{ font-size: 13px; }
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title"><span class="moon">🌙</span> NoorMVP</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="message">
Please be patient as Noor reprograms itself after several recurring errors.<br>
Try again soon to witness, for free, what Noor is capable of uncovering & discovering. Please consider reflecting on the verses below while you wait! 
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="verses">
    <span class="v-small">17:81</span>
    <span class="dot">·</span>
    <span class="v-mid">22:60</span>
    <span class="dot">·</span>
    <span class="v-small">22:73</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="fly-wrap">
    <div class="fly">🪰</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer-wrap">
    <div class="footer">
        <div class="spinner"></div>
        <div>
            Noor is your AI guide that brings light to your inquiries through the Qur’an.<br>
            Noor is preparing to enhance your experience—bringing reflection, context, and evidence to the claims it presents.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
