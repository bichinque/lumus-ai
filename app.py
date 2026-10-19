
import streamlit as st
from google import genai
from datetime import datetime

st.set_page_config(
    page_title="Lumus AI | Estúdio Criativo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# ESTADO DA APLICAÇÃO
# =========================

if "historico" not in st.session_state:
    st.session_state.historico = []

if "conteudo_atual" not in st.session_state:
    st.session_state.conteudo_atual = ""

if "pagina" not in st.session_state:
    st.session_state.pagina = "Criar conteúdo"

if "briefing_salvo" not in st.session_state:
    st.session_state.briefing_salvo = {}

if "cliente" not in st.session_state:
    st.session_state.cliente = ""

if "segmento" not in st.session_state:
    st.session_state.segmento = ""

if "objetivo" not in st.session_state:
    st.session_state.objetivo = ""

# =========================
# IDENTIDADE VISUAL
# =========================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 90% 0%,
        rgba(180,0,35,0.16), transparent 38%),
        #090a0e;
    color: #f5f5f7;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1250px;
    padding: 2.2rem 2rem 4rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3 {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] {
    background: #0d0f14;
    border-right: 1px solid #292d38;
}

section[data-testid="stSidebar"] .stRadio label {
    color: #e7e9ef;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 30px;
}

.brand-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: linear-gradient(135deg, #ff3048, #a90020);
    color: white;
    font-size: 25px;
    font-weight: 900;
    box-shadow: 0 5px 25px #ff243b20;
}

.brand-name {
    color: white;
    font-size: 29px;
    font-weight: 900;
    letter-spacing: -1px;
}

.brand-name span {
    color: #ff3048;
}

.muted {
    color: #9299aa;
    font-size: 13px;
}

.eyebrow {
    color: #ff596d;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

.panel {
    background: #11131a;
    border: 1px solid #2a2e39;
    border-radius: 16px;
    padding: 20px;
}

.stTextInput label,
.stTextArea label,
.stSelectbox label {
    color: #e1e4eb !important;
    font-weight: 600 !important;
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background-color: #10131a;
    color: white;
    border: 1px solid #303543;
    border-radius: 10px;
}

.stButton > button {
    background: linear-gradient(110deg, #ff3048, #c90024);
    color: white;
    border: none;
    border-radius: 10px;
    min-height: 44px;
    font-weight: 700;
}

.stButton > button:hover {
    background: linear-gradient(110deg, #ff465b, #e5002b);
    color: white;
    border: none;
}

.stDownloadButton > button {
    background: #191c25;
    color: white;
    border: 1px solid #383d4b;
    border-radius: 10px;
}

hr {
    border-color: #292d38;
}

.footer {
    color: #686f7f;
    font-size: 11px;
    text-align: center;
    padding-top: 35px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# FUNÇÕES
# =========================

def nova_criacao():
    st.session_state.conteudo_atual = ""
    st.session_state.cliente = ""
    st.session_state.segmento = ""
    st.session_state.objetivo = ""
    st.session_state.briefing_salvo = {}
    st.session_state.pagina = "Criar conteúdo"


def gerar_conteudo(tipo, cliente, segmento, objetivo, tom):
    chave = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=chave)

    prompt = f"""
Você é a Lumus AI, assistente de marketing da agência Lumus Marketing.

Crie conteúdo original, estratégico e pronto para revisão.

TIPO: {tipo}
CLIENTE: {cliente or "Não informado"}
SEGMENTO: {segmento or "Não informado"}
OBJETIVO: {objetivo}
TOM: {tom}

INSTRUÇÕES:
- Escreva em português brasileiro, salvo quando outro idioma for solicitado.
- Use linguagem natural, humana, específica e profissional.
- Evite clichês e frases genéricas.
- Não invente preços, datas, condições ou características.
- Para Reels, inclua gancho, desenvolvimento e chamada para ação.
- Para legendas, entregue um texto pronto para publicar.
- Para calendários, organize por dia, formato e tema.
- Não explique o processo: entregue o conteúdo solicitado.
"""

    resposta = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return resposta.text or "A IA não retornou conteúdo. Tente novamente."


def registrar_historico(tipo, cliente, segmento, objetivo, tom, conteudo):
    registro = {
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "tipo": tipo,
        "cliente": cliente or "Sem cliente",
        "segmento": segmento or "Não informado",
        "objetivo": objetivo,
        "tom": tom,
        "conteudo": conteudo
    }

    st.session_state.historico.insert(0, registro)

# =========================
# MENU LATERAL
# =========================

with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-icon">L.</div>
        <div>
            <div class="brand-name">LUMUS <span>AI</span></div>
            <div class="muted">Estúdio criativo</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="eyebrow">MENU PRINCIPAL</div>',
                unsafe_allow_html=True)

    pagina = st.radio(
        "Navegação",
        ["Criar conteúdo", "Histórico", "Sobre a Lumus AI"],
        label_visibility="collapsed",
        key="navegacao"
    )

    st.session_state.pagina = pagina

    st.divider()

    st.markdown("**Sua central de marketing**")
    st.caption("Crie, revise e organize conteúdos para seus clientes.")

    if st.button("＋ Nova criação", use_container_width=True):
        nova_criacao()
        st.rerun()

    st.divider()

    st.caption("LUMUS AI · VERSÃO 2.0")

# =========================
# CABEÇALHO PRINCIPAL
# =========================

st.markdown("""
<div class="brand">
    <div class="brand-icon">L.</div>
    <div>
        <div class="brand-name">LUMUS <span>AI</span></div>
        <div class="muted">Seu estúdio de inteligência criativa.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# PÁGINA: CRIAR CONTEÚDO
# =========================

if pagina == "Criar conteúdo":

    st.markdown(
        '<div class="eyebrow">INTELIGÊNCIA ARTIFICIAL PARA MARKETING</div>',
        unsafe_allow_html=True
    )

    st.title("O que vamos criar hoje?")
    st.markdown(
        '<div class="muted">Transforme ideias em conteúdos estratégicos para marcas.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col_form, col_resultado = st.columns([1, 1], gap="large")

    with col_form:
        with st.container(border=True):
            st.subheader("✦ Briefing criativo")
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
                ],
                key="tipo_conteudo"
            )

            cliente = st.text_input(
                "Nome do cliente",
                placeholder="Ex.: Honda Motospeed",
                key="cliente"
            )

            segmento = st.text_input(
                "Segmento do negócio",
                placeholder="Ex.: concessionária de motocicletas",
                key="segmento"
            )

            objetivo = st.text_area(
                "O que você quer comunicar?",
                placeholder="Descreva a campanha, produto, serviço ou objetivo...",
                height=145,
                key="objetivo"
            )

            tom = st.selectbox(
                "Tom de comunicação",
                [
                    "Natural e direto",
                    "Profissional",
                    "Criativo e descontraído",
                    "Comercial e persuasivo"
                ],
                key="tom"
            )

            gerar = st.button(
                "✦ Gerar conteúdo",
                use_container_width=True
            )

    if gerar:
        if not objetivo.strip():
            st.warning("Preencha o objetivo antes de gerar o conteúdo.")
        else:
            try:
                with st.spinner("A Lumus AI está criando seu conteúdo..."):
                    conteudo = gerar_conteudo(
                        tipo, cliente, segmento, objetivo, tom
                    )

                st.session_state.conteudo_atual = conteudo
                st.session_state.briefing_salvo = {
                    "tipo": tipo,
                    "cliente": cliente,
                    "segmento": segmento,
                    "objetivo": objetivo,
                    "tom": tom
                }

                registrar_historico(
                    tipo, cliente, segmento, objetivo, tom, conteudo
                )

                st.rerun()

            except Exception as erro:
                st.error(f"Não foi possível gerar o conteúdo: {erro}")

    with col_resultado:
        with st.container(border=True):
            st.subheader("✧ Estúdio de criação")
            st.caption("Revise, copie ou baixe o resultado.")

            if st.session_state.conteudo_atual:
                st.markdown(
                    '<div class="eyebrow">CONTEÚDO GERADO</div>',
                    unsafe_allow_html=True
                )

                st.text_area(
                    "Edite seu conteúdo",
                    key="editor_conteudo",
                    height=320
                )

                conteudo_final = st.session_state.editor_conteudo

                st.download_button(
                    "↓ Baixar conteúdo (.txt)",
                    data=conteudo_final,
                    file_name="conteudo_lumus.txt",
                    mime="text/plain",
                    use_container_width=True
                )

                st.caption(
                    "Para copiar: use o ícone de copiar no bloco abaixo."
                )

                st.code(conteudo_final, language=None)

            else:
                st.markdown("""
                <div style="
                    min-height: 300px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                    color: #9299aa;
                ">
                    <div style="font-size: 42px; color: #ff3048;">✦</div>
                    <div style="font-size: 17px; color: #f5f5f7;
                                font-weight: 700; margin: 12px 0;">
                        Sua próxima grande ideia começa aqui.
                    </div>
                    <div style="font-size: 13px;">
                        Preencha o briefing e gere seu conteúdo.
                    </div>
                </div>
                """, unsafe_allow_html=True)

# =========================
# PÁGINA: HISTÓRICO
# =========================

elif pagina == "Histórico":

    st.title("Histórico de criações")
    st.caption("Consulte conteúdos gerados nesta sessão.")

    historico = st.session_state.historico

    if not historico:
        st.info(
            "Ainda não há conteúdos no histórico. "
            "Crie seu primeiro conteúdo para começar."
        )
    else:
        st.write(f"**{len(historico)} conteúdo(s) nesta sessão**")

        for i, item in enumerate(historico):
            titulo = f"{item['tipo']} · {item['cliente']} · {item['data']}"

            with st.expander(titulo):
                st.caption(
                    f"Segmento: {item['segmento']} | Tom: {item['tom']}"
                )

                st.write("**Objetivo informado**")
                st.write(item["objetivo"])

                st.write("**Conteúdo**")
                st.code(item["conteudo"], language=None)

                st.download_button(
                    "Baixar este conteúdo",
                    data=item["conteudo"],
                    file_name=f"lumus_historico_{i + 1}.txt",
                    mime="text/plain",
                    key=f"download_historico_{i}"
                )

        st.divider()

        if st.button("Limpar histórico desta sessão"):
            st.session_state.historico = []
            st.session_state.conteudo_atual = ""
            st.rerun()

# =========================
# PÁGINA: SOBRE
# =========================

elif pagina == "Sobre a Lumus AI":

    st.title("Sobre a Lumus AI")

    st.markdown("""
    A **Lumus AI** é uma ferramenta de apoio criativo da Lumus Marketing,
    criada para facilitar a produção de conteúdo e acelerar tarefas
    do dia a dia de marketing.

    ### Ferramentas disponíveis

    - Legendas para Instagram
    - Roteiros para Reels
    - Calendários de conteúdo
    - Campanhas promocionais
    - Propostas comerciais
    - Mensagens de prospecção
    - Textos em espanhol

    ### Como utilizar

    1. Escolha o tipo de conteúdo.
    2. Informe o cliente e o objetivo.
    3. Selecione o tom de comunicação.
    4. Gere, revise e baixe o resultado.

    ### Importante

    Os conteúdos gerados por IA devem ser revisados antes da publicação.
    Confirme informações, preços, datas e condições comerciais.
    """)

# =========================
# RODAPÉ
# =========================

st.markdown("""
<div class="footer">
    LUMUS AI · CRIATIVIDADE COM ESTRATÉGIA
</div>
""", unsafe_allow_html=True)
