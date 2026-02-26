st.markdown(
    """
    <style>
    body, .main, .block-container {
        background-color: #000000 !important;
        color: #ffffff !important;
    }

    .stButton>button {
        background-color: #FFD700;
        color: black;
        font-weight: bold;
    }

    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 10px;
    }

    .header-row {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
    }

    .spinning-moon {
        font-size: 50px;
        animation: spin 5s linear infinite;
        margin-right: 10px;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .noor {
        font-family: 'Arial Black', sans-serif;
        font-size: 60px;
        font-weight: 900;
        color: #FFD700;
        margin: 0;
    }

    .mvp {
        font-family: 'Arial Black', sans-serif;
        font-size: 60px;
        font-weight: 900;
        color: #CCCCCC;
        margin-left: 5px;
    }

    .caption {
        font-family: Verdana, sans-serif;
        font-size: 14px;
        color: #AAAAAA;
        text-transform: uppercase;
        margin-top: -5px;
    }

    .ai-guide {
        font-family: Verdana, sans-serif;
        font-size: 16px;
        font-weight: 600;
        color: #FFD700;
        margin-top: 5px;
        text-align: center;
    }
    </style>

    <div class="header-container">
        <div class="header-row">
            <div class="spinning-moon">🌙</div>
            <div>
                <span class="noor">Noor</span><span class="mvp">MVP</span>
            </div>
        </div>
        <div class="caption">REMEMBRANCE, YOUR MOST VALUABLE PRAYER</div>
        <div class="ai-guide">Noor is your AI guide, bringing <strong>LIGHT</strong> to your inquiries through the Quran.</div>
    </div>
    """,
    unsafe_allow_html=True
)
