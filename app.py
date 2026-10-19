
import streamlit as st
from google import genai

st.set_page_config(
    page_title="Lumus AI | Estúdio Criativo",
    page_icon="⚡",
    layout="wide"
)

# IDENTIDADE VISUAL
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 90% 0%, rgba(180, 0, 35, 0.18), transparent 38%),
        #090a0e;
    color: #f5f5f7;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1200px;
    padding: 2.5rem 2rem 4rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.brand {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 12px;
}

.brand-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 52px;
    height: 52px;
    border-radius: 15px;
    background: linear-gradient(135deg, #ff3048, #a90020);
    color: white;
    font-size: 27px;
    font-weight: 900;
    box-shadow: 0 8px 30px rgba(255, 36, 59, 0.2);
}

.brand-name {
    font-size: 34px;
    font-weight: 900;
    letter-spacing: -1.5px;
    color: white;
    line-height: 1.1;
}

.brand-name span {
    color: #ff3048;
}

.brand-subtitle {
    color: #9299aa;
    font-size: 14px;
    margin-top: 7px;
}

.top-label {
    display: inline-block;
    padding: 7px 12px;
    margin: 24px 0 10px;
    border: 1px solid #3b2029;
    border-radius: 100px;
    background: rgba(255, 36, 59, 0.07);
    color: #ff6677;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}

.section-title {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -0.7px;
    color: white;
    margin: 0 0 8px;
}

.section-subtitle {
    color: #9299aa;
    font-size: 14px;
    margin-bottom: 25px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(19, 21, 29, 0.82);
    border: 1px solid #292d38;
    border-radius: 18px;
}

.stTextInput label,
.stTextArea label,
.stSelectbox label {
    color: #e1e4eb !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background-color: #10131a;
    color: white;
    border: 1px solid #303543;
    border-radius: 10px;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #ff3048;
    box-shadow: 0 0 0 1px #ff3048;
}

.stSelectbox div[data-baseweb="select"] * {
    color: white;
}

.stButton > button {
    background: linear-gradient(110deg, #ff3048, #c90024);
    color: white;
    border: none;
    border-radius: 10px;
    min-height: 46px;
    font-weight: 700;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(110deg, #ff465b, #e5002b);
    color: white;
    box-shadow: 0 0 22px rgba(255, 36, 59, 0.22);
    border: none;
}

.stDownloadButton > button {
    background: #191c25;
    color: white;
    border: 1px solid #383d4b;
    border-radius: 10px;
    min-height: 44px;
}

.stDownloadButton > button:hover {
    border-color: #ff3048;
    color: white;
}

hr {
    border-color: #292d38;
}

[data-testid="stCaptionContainer"] {
    color: #9299aa;
}

.stAlert {
    border-radius: 12px;
}

section[data-testid="stSidebar"] {
    background-color: #0d0f14;
    border-right: 1px solid #262a34;
}

.result-label {
    color: #ff6677;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}

.footer {
    color: #666d7d;
    font-size: 12px;
    text-align: center;
    padding-top: 35px;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1.5rem 1rem 3rem;
    }
    .brand-name {
        font-size: 28px;
    }
}
</style>
""", unsafe_allow_html=True)


# CABEÇALHO
st.markdown("""
<div class="brand">
    <div class="brand-icon">L.</div>
    <div>
        <div class="brand-name">LUMUS <span>AI</span></div>
        <div class="brand-subtitle">
            Seu estúdio de inteligência criativa.
        </div>
    </div>
</div>
<div class="top-label">✦ INTELIGÊNCIA ARTIFICIAL PARA MARKETING</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-title">O que vamos criar hoje?</div>
<div class="section-subtitle">
Transforme suas ideias em conteúdos estratégicos para marcas.
</div>
""", unsafe_allow_html=True)

# FORMULÁRIO E RESULTADO
col_form, col_resultado = st.columns([1, 1], gap="large")

with col_form:
    with st.container(border=True):
        st.markdown("### ✦ Briefing criativo")
        st.caption("Personalize o conteúdo para cada cliente.")

        tipo = st.selectbox(
            "Tipo de conteúdo",
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

        cliente = st.text_input(
            "Nome do cliente",
            placeholder="Ex.: Honda Motospeed"
        )

        segmento = st.text_input(
            "Segmento do negócio",
            placeholder="Ex.: concessionária de motocicletas"
        )

        objetivo = st.text_area(
            "O que você quer comunicar?",
            placeholder="Descreva a campanha, produto, serviço ou objetivo...",
            height=150
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

        gerar = st.button(
            "✦  Gerar conteúdo",
            use_container_width=True
        )

with col_resultado:
    with st.container(border=True):
        st.markdown("### ✧ Estúdio de criação")
        st.caption("Seu conteúdo aparecerá aqui, pronto para revisar.")

        if "conteudo_lumus" not in st.session_state:
            st.session_state.conteudo_lumus = ""

        if gerar:
            if not objetivo.strip():
                st.warning("Preencha o objetivo do conteúdo primeiro.")
            else:
                try:
                    chave = st.secrets["GEMINI_API_KEY"]
                    client = genai.Client(api_key=chave)

                    prompt = f"""
Você é a Lumus AI, assistente especializada em marketing
da agência Lumus Marketing.

Crie conteúdo original, estratégico e pronto para revisão.

TIPO: {tipo}
CLIENTE: {cliente or "Não informado"}
SEGMENTO: {segmento or "Não informado"}
OBJETIVO: {objetivo}
TOM: {tom}

REGRAS:
- Escreva em português brasileiro, exceto quando outro idioma for solicitado.
- Use linguagem natural, humana e específica para o negócio.
- Evite clichês, exageros e frases genéricas.
- Não invente preços, condições, datas ou características.
- Respeite o formato solicitado.
- Para Reels, inclua gancho, desenvolvimento e chamada para ação.
- Para legendas, entregue texto pronto para publicar.
- Não explique o processo: entregue o conteúdo solicitado.
"""

                    with st.spinner("A Lumus AI está criando..."):
                        resposta = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=prompt
                        )

                    st.session_state.conteudo_lumus = (
                        resposta.text or "Não foi gerado conteúdo. Tente novamente."
                    )

                except Exception as erro:
                    st.error(f"Não foi possível gerar o conteúdo: {erro}")

        if st.session_state.conteudo_lumus:
            st.markdown(
                '<div class="result-label">CONTEÚDO GERADO</div>',
                unsafe_allow_html=True
            )

            st.text_area(
                "Revise e edite seu conteúdo",
                key="resultado_editavel",
                value=st.session_state.conteudo_lumus,
                height=300
            )

            conteudo_final = st.session_state.get(
                "resultado_editavel",
                st.session_state.conteudo_lumus
            )

            st.button(
                "📋 Selecionar conteúdo para copiar",
                on_click=None,
                help="Selecione o texto na caixa acima e copie com Ctrl+C."
            )

            st.download_button(
                "↓  Baixar arquivo .txt",
                data=conteudo_final,
                file_name="conteudo_lumus.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.markdown("""
            <div style="
                min-height: 300px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                padding: 20px;
                color: #777f90;
            ">
                <div style="font-size: 42px; margin-bottom: 16px;">✦</div>
                <div style="color: #e1e4eb; font-size: 17px;
                            font-weight: 700; margin-bottom: 8px;">
                    Sua próxima grande ideia começa aqui.
                </div>
                <div style="font-size: 13px;">
                    Preencha o briefing e gere seu conteúdo.
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    LUMUS AI · CRIATIVIDADE COM ESTRATÉGIA
</div>
""", unsafe_allow_html=True)
