
import streamlit as st
from google import genai

st.set_page_config(
    page_title="Lumus AI",
    page_icon="⚡",
    layout="centered"
)


st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at top right,
        rgba(150, 0, 20, 0.16), transparent 45%),
        #090a0e;
    color: #f5f5f7;
}

.block-container {
    max-width: 1150px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}

h1 {
    font-size: 2.7rem !important;
    font-weight: 800 !important;
    letter-spacing: -1.5px;
    color: #ffffff !important;
}

h2, h3 {
    color: #ffffff !important;
}

p, label, .stMarkdown {
    color: #d1d5df;
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background-color: #141720;
    color: #ffffff;
    border: 1px solid #303543;
    border-radius: 10px;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #f3263d;
    box-shadow: 0 0 0 1px #f3263d;
}

.stButton > button {
    background: linear-gradient(110deg, #ff243b, #c90024);
    color: #ffffff;
    border: none;
    border-radius: 10px;
    min-height: 48px;
    font-weight: 700;
    width: 100%;
}

.stButton > button:hover {
    background: linear-gradient(110deg, #ff4659, #e5002b);
    box-shadow: 0 0 22px rgba(255, 36, 59, 0.22);
    color: white;
}

hr {
    border-color: #292d38;
}

.stAlert {
    border-radius: 12px;
}

[data-testid="stCaptionContainer"] {
    color: #9299aa;
}

section[data-testid="stSidebar"] {
    background-color: #0d0f14;
    border-right: 1px solid #262a34;
}
</style>
""", unsafe_allow_html=True)


st.title("LUMUS AI")
st.caption("Marketing inteligente para marcas que querem crescer.")

st.divider()

tipo = st.selectbox(
    "O que vamos criar?",
    [
        "Legenda para Instagram",
        "Roteiro para Reels",
        "Calendário de conteúdo",
        "Campanha promocional",
        "Proposta comercial",
        "Mensagem de prospecção",
        "Texto em espanhol"
    ]
)

cliente = st.text_input("Nome do cliente")
segmento = st.text_input("Segmento do negócio")

objetivo = st.text_area(
    "O que você quer comunicar?",
    placeholder="Descreva a campanha, produto ou objetivo."
)

tom = st.selectbox(
    "Tom de comunicação",
    [
        "Natural e direto",
        "Profissional",
        "Criativo e descontraído",
        "Comercial e persuasivo"
    ]
)

if st.button("Gerar conteúdo"):
    if not objetivo.strip():
        st.warning("Descreva o que você deseja criar.")
    else:
        try:
            chave = st.secrets["GEMINI_API_KEY"]
            client = genai.Client(api_key=chave)

            prompt = f"""
Você é a Lumus AI, assistente de marketing
da agência Lumus Marketing.

Crie um conteúdo original e profissional.

Tipo: {tipo}
Cliente: {cliente or "Não informado"}
Segmento: {segmento or "Não informado"}
Objetivo: {objetivo}
Tom: {tom}

Escreva em português brasileiro, salvo
quando outro idioma for solicitado.
Evite clichês e não invente informações.
Entregue um resultado pronto para revisão.
Para Reels, inclua gancho, desenvolvimento
e chamada para ação.
"""

            with st.spinner("Criando seu conteúdo..."):
                resposta = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

            st.subheader("Conteúdo gerado")
            st.write(resposta.text)

            st.download_button(
                "Baixar conteúdo",
                data=resposta.text or "",
                file_name="conteudo_lumus.txt",
                mime="text/plain"
            )

        
        except Exception as erro:
            st.error(f"Erro ao gerar conteúdo: {erro}")

