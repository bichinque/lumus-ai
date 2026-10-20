import streamlit as st
from google import genai
from datetime import datetime

# ==========================================
# CONFIGURAÇÃO
# ==========================================

st.set_page_config(
    page_title="Lumus AI | Estúdio Criativo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

MODELO_IA = "gemini-3.5-flash-lite"

TIPOS_CONTEUDO = [
    "Legenda para Instagram",
    "Roteiro para Reels",
    "Calendário de conteúdo",
    "Campanha promocional",
    "Proposta comercial",
    "Mensagem de prospecção",
    "Texto em espanhol"
]

TONS_COMUNICACAO = [
    "Natural e direto",
    "Profissional",
    "Criativo e descontraído",
    "Comercial e persuasivo"
]

# ==========================================
# ESTADO DA APLICAÇÃO
# ==========================================

if "historico" not in st.session_state:
    st.session_state.historico = []

if "conteudo_atual" not in st.session_state:
    st.session_state.conteudo_atual = ""

if "pagina" not in st.session_state:
    st.session_state.pagina = "Criar conteúdo"

if "cliente" not in st.session_state:
    st.session_state.cliente = ""

if "segmento" not in st.session_state:
    st.session_state.segmento = ""

if "objetivo" not in st.session_state:
    st.session_state.objetivo = ""

if "editor_conteudo" not in st.session_state:
    st.session_state.editor_conteudo = ""

if "tipo_conteudo" not in st.session_state:
    st.session_state.tipo_conteudo = TIPOS_CONTEUDO[0]

if "tom" not in st.session_state:
    st.session_state.tom = TONS_COMUNICACAO[0]

if "briefing_salvo" not in st.session_state:
    st.session_state.briefing_salvo = {}

# ==========================================
# CLIENTE GEMINI
# ==========================================

@st.cache_resource
def obter_cliente_gemini(chave):
    """Reutiliza o cliente da API durante a sessão."""
    return genai.Client(api_key=chave)


def obter_chave_api():
    """Obtém a chave configurada nos Secrets do Streamlit."""
    try:
        chave = st.secrets.get("GEMINI_API_KEY", "").strip()
    except Exception:
        chave = ""

    if not chave:
        raise ValueError(
            "A chave GEMINI_API_KEY não está configurada. "
            "Adicione-a em Settings > Secrets no Streamlit."
        )

    return chave


# ==========================================
# GERAÇÃO DE CONTEÚDO COM STREAMING
# ==========================================

def gerar_conteudo_stream(tipo, cliente, segmento, objetivo, tom):
    """
    Gera conteúdo em partes para exibir a resposta
    progressivamente na interface.
    """

    chave = obter_chave_api()
    client = obter_cliente_gemini(chave)

    prompt = f"""
Você é a Lumus AI, assistente de marketing da Lumus Marketing.

Sua especialidade é estratégia de conteúdo, redes sociais,
copywriting, campanhas comerciais e comunicação de marcas.

Crie um conteúdo original, estratégico, natural e profissional.

BRIEFING:
Tipo de conteúdo: {tipo}
Cliente: {cliente or "Não informado"}
Segmento: {segmento or "Não informado"}
Objetivo: {objetivo}
Tom de comunicação: {tom}

REGRAS:
- Escreva em português brasileiro, exceto quando outro idioma
  for solicitado.
- Evite clichês, frases genéricas e linguagem artificial.
- Não invente preços, datas, descontos ou informações comerciais.
- Entregue um conteúdo pronto para revisão e utilização.
- Não faça introduções desnecessárias.
- Não explique seu processo de criação.
- Seja objetivo sem perder a qualidade criativa.
- Considere o segmento e o público da marca.

ORIENTAÇÕES POR FORMATO:
- Legenda: entregue um texto pronto para publicação.
- Reels: inclua gancho inicial, desenvolvimento e chamada para ação.
- Calendário: organize temas, formatos e sugestões de publicação.
- Campanha: apresente conceito, mensagem e chamada para ação.
- Proposta comercial: utilize linguagem profissional e convincente.
- Prospecção: escreva uma mensagem natural, curta e personalizada.
- Espanhol: escreva em espanhol natural e correto.

Entregue somente o conteúdo solicitado.
"""

    resposta = client.models.generate_content_stream(
        model=MODELO_IA,
        contents=prompt,
        config={
            "temperature": 0.7,
            "max_output_tokens": 900
        }
    )

    recebeu_texto = False

    for parte in resposta:
        texto = getattr(parte, "text", None)

        if texto:
            recebeu_texto = True
            yield texto

    if not recebeu_texto:
        raise ValueError(
            "A IA não retornou texto. Tente novamente."
        )


def gerar_conteudo(tipo, cliente, segmento, objetivo, tom):
    """
    Versão tradicional que retorna o conteúdo completo.
    Utilizada quando não é necessário streaming.
    """
    return "".join(
        gerar_conteudo_stream(
            tipo, cliente, segmento, objetivo, tom
        )
    )


# ==========================================
# HISTÓRICO
# ==========================================

def adicionar_historico(
    tipo, cliente, segmento, objetivo, tom, conteudo
):
    st.session_state.historico.insert(0, {
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "tipo": tipo,
        "cliente": cliente or "Sem cliente",
        "segmento": segmento or "Não informado",
        "objetivo": objetivo,
        "tom": tom,
        "conteudo": conteudo
    })

    # Evita que o histórico da sessão cresça indefinidamente.
    st.session_state.historico = (
        st.session_state.historico[:50]
    )


# ==========================================
# NOVA CRIAÇÃO
# ==========================================

def preparar_nova_criacao():
    """Limpa o formulário sem apagar o histórico."""
    st.session_state.pagina = "Criar conteúdo"
    st.session_state.navegacao = "Criar conteúdo"

    st.session_state.conteudo_atual = ""
    st.session_state.editor_conteudo = ""
    st.session_state.briefing_salvo = {}

    st.session_state.cliente = ""
    st.session_state.segmento = ""
    st.session_state.objetivo = ""

    st.session_state.tipo_conteudo = TIPOS_CONTEUDO[0]
    st.session_state.tom = TONS_COMUNICACAO[0]


# ==========================================
# DESIGN
# ==========================================

st.markdown("""
<style>
@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap'
);

.stApp {
    background:
        radial-gradient(
            ellipse at 90% 0%,
            rgba(180, 0, 35, 0.16),
            transparent 38%
        ),
        #090a0e;
    color: #f5f5f7;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1350px;
    padding: 2.2rem 2rem 4rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3 {
    color: #ffffff !important;
}

p, label {
    color: #d1d5df;
}

section[data-testid="stSidebar"] {
    background: #0d0f14;
    border-right: 1px solid #292d38;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 25px;
}

.brand-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 48px;
    height: 48px;
    border-radius: 14px;
    background: linear-gradient(135deg, #ff3048, #a90020);
    color: white;
    font-size: 24px;
    font-weight: 900;
    box-shadow: 0 5px 25px #ff243b20;
}

.brand-name {
    color: white;
    font-size: 28px;
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
    transition: 0.2s ease;
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

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #2a2e39;
    border-radius: 16px;
}

[data-testid="stCaptionContainer"] {
    color: #9299aa;
}

[data-testid="stChatMessage"] {
    background: #10131a;
    border: 1px solid #292d38;
    border-radius: 14px;
}

.footer {
    color: #686f7f;
    font-size: 11px;
    text-align: center;
    padding-top: 35px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# MENU LATERAL
# ==========================================

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

    st.markdown(
        '<div class="eyebrow">MENU PRINCIPAL</div>',
        unsafe_allow_html=True
    )

    if "navegacao" not in st.session_state:
        st.session_state.navegacao = st.session_state.pagina

    st.radio(
        "Navegação",
        [
            "Criar conteúdo",
            "Assistente IA",
            "Histórico",
            "Sobre a Lumus AI"
        ],
        key="navegacao",
        label_visibility="collapsed"
    )

    st.session_state.pagina = st.session_state.navegacao

    st.divider()

    st.button(
        "＋ Nova criação",
        key="botao_nova_criacao",
        use_container_width=True,
        on_click=preparar_nova_criacao
    )

    st.divider()

    st.markdown("**Sua central de marketing**")
    st.caption(
        "Crie, revise e organize conteúdos para seus clientes."
    )

    st.markdown(
        '<div class="muted">LUMUS AI · VERSÃO 3.0</div>',
        unsafe_allow_html=True
    )


# ==========================================
# CABEÇALHO
# ==========================================

st.markdown("""
<div class="brand">
    <div class="brand-icon">L.</div>
    <div>
        <div class="brand-name">LUMUS <span>AI</span></div>
        <div class="muted">Seu estúdio de inteligência criativa.</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# PÁGINA: CRIAR CONTEÚDO
# ==========================================

if st.session_state.pagina == "Criar conteúdo":

    st.markdown(
        '<div class="eyebrow">'
        'INTELIGÊNCIA ARTIFICIAL PARA MARKETING'
        '</div>',
        unsafe_allow_html=True
    )

    st.title("O que vamos criar hoje?")
    st.caption(
        "Transforme ideias em conteúdos estratégicos para marcas."
    )

    st.write("")

    col_form, col_resultado = st.columns(
        [1, 1],
        gap="large"
    )

    with col_form:
        with st.container(border=True):
            st.subheader("✦ Briefing criativo")
            st.caption("Personalize o conteúdo para cada cliente.")

            tipo = st.selectbox(
                "Tipo de conteúdo",
                TIPOS_CONTEUDO,
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
                placeholder=(
                    "Descreva a campanha, produto, "
                    "serviço ou objetivo..."
                ),
                height=145,
                key="objetivo"
            )

            tom = st.selectbox(
                "Tom de comunicação",
                TONS_COMUNICACAO,
                key="tom"
            )

            gerar = st.button(
                "✦ Gerar conteúdo",
                use_container_width=True,
                type="primary"
            )

    if gerar:
        if not objetivo.strip():
            st.warning(
                "Preencha o objetivo antes de gerar o conteúdo."
            )
        else:
            try:
                st.session_state.conteudo_atual = ""
                st.session_state.editor_conteudo = ""

                st.session_state.briefing_salvo = {
                    "tipo": tipo,
                    "cliente": cliente,
                    "segmento": segmento,
                    "objetivo": objetivo,
                    "tom": tom
                }

                with col_resultado:
                    with st.container(border=True):
                        st.subheader("✧ Estúdio de criação")
                        st.caption(
                            "A resposta aparecerá conforme for gerada."
                        )

                        st.markdown(
                            '<div class="eyebrow">'
                            'GERANDO CONTEÚDO'
                            '</div>',
                            unsafe_allow_html=True
                        )

                        conteudo = st.write_stream(
                            gerar_conteudo_stream(
                                tipo,
                                cliente,
                                segmento,
                                objetivo,
                                tom
                            )
                        )

                if not conteudo or not conteudo.strip():
                    raise ValueError(
                        "A IA não retornou conteúdo. Tente novamente."
                    )

                st.session_state.conteudo_atual = conteudo
                st.session_state.editor_conteudo = conteudo

                adicionar_historico(
                    tipo,
                    cliente,
                    segmento,
                    objetivo,
                    tom,
                    conteudo
                )

                st.rerun()

            except Exception as erro:
                st.error(
                    "Não foi possível gerar o conteúdo. "
                    "Verifique sua chave da API e tente novamente."
                )
                st.caption(f"Detalhes técnicos: {erro}")

    with col_resultado:
        if st.session_state.conteudo_atual:
            with st.container(border=True):
                st.subheader("✧ Estúdio de criação")
                st.caption("Revise, edite, copie ou baixe o resultado.")

                st.markdown(
                    '<div class="eyebrow">CONTEÚDO GERADO</div>',
                    unsafe_allow_html=True
                )

                conteudo_final = st.text_area(
                    "Edite seu conteúdo",
                    key="editor_conteudo",
                    height=320
                )

                st.download_button(
                    "↓ Baixar conteúdo (.txt)",
                    data=conteudo_final,
                    file_name="conteudo_lumus.txt",
                    mime="text/plain",
                    use_container_width=True
                )

                st.code(conteudo_final, language=None)

        elif not gerar:
            with st.container(border=True):
                st.subheader("✧ Estúdio de criação")
                st.caption("Revise, edite ou baixe seu conteúdo.")

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
                    <div style="font-size: 42px; color: #ff3048;">
                        ✦
                    </div>
                    <div style="
                        font-size: 17px;
                        color: #f5f5f7;
                        font-weight: 700;
                        margin: 12px 0;
                    ">
                        Sua próxima grande ideia começa aqui.
                    </div>
                    <div style="font-size: 13px;">
                        Preencha o briefing e gere seu conteúdo.
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ==========================================
# PÁGINA: ASSISTENTE IA
# ==========================================

elif st.session_state.pagina == "Assistente IA":

    st.markdown(
        '<div class="eyebrow">ASSISTENTE DE MARKETING</div>',
        unsafe_allow_html=True
    )

    st.title("Converse com a Lumus AI")
    st.caption(
        "Peça ideias, estratégias, legendas, roteiros e sugestões "
        "para o seu trabalho."
    )

    if "mensagens_chat" not in st.session_state:
        st.session_state.mensagens_chat = []

    if st.button("Nova conversa", key="limpar_chat"):
        st.session_state.mensagens_chat = []
        st.rerun()

    # Exibe as mensagens existentes.
    for mensagem in st.session_state.mensagens_chat:
        with st.chat_message(mensagem["role"]):
            st.markdown(mensagem["content"])

    pedido = st.chat_input(
        "Como posso ajudar com seu marketing?"
    )

    if pedido:
        st.session_state.mensagens_chat.append({
            "role": "user",
            "content": pedido
        })

        with st.chat_message("user"):
            st.markdown(pedido)

        # Envia apenas as mensagens mais recentes para reduzir
        # o volume de contexto processado.
        mensagens_recentes = (
            st.session_state.mensagens_chat[-6:]
        )

        transcript = []

        for mensagem in mensagens_recentes:
            papel = (
                "CLIENTE"
                if mensagem["role"] == "user"
                else "LUMUS AI"
            )
            transcript.append(
                f"{papel}: {mensagem['content']}"
            )

        prompt_chat = f"""
Você é a Lumus AI, assistente de marketing da Lumus Marketing.

Responda em português brasileiro, com naturalidade,
criatividade e objetividade.

Ajude com:
- Estratégias de marketing e posicionamento.
- Conteúdos para redes sociais.
- Legendas e roteiros de Reels.
- Prospecção comercial e mensagens de WhatsApp.
- Ideias de campanhas e calendários editoriais.
- Branding, copywriting e comunicação.
- Propostas comerciais para clientes.

REGRAS:
- Entregue textos prontos para uso quando solicitados.
- Evite introduções desnecessárias.
- Não invente informações comerciais.
- Considere o contexto recente da conversa.
- Faça perguntas somente quando forem realmente necessárias.
- Não repita toda a conversa na resposta.

CONVERSA RECENTE:
{chr(10).join(transcript)}

Responda à última mensagem do cliente.
"""

        try:
            client = obter_cliente_gemini(obter_chave_api())

            with st.chat_message("assistant"):
                resposta_completa = st.write_stream(
                    (
                        parte.text
                        for parte in client.models.generate_content_stream(
                            model=MODELO_IA,
                            contents=prompt_chat,
                            config={
                                "temperature": 0.7,
                                "max_output_tokens": 700
                            }
                        )
                        if getattr(parte, "text", None)
                    )
                )

            if resposta_completa:
                st.session_state.mensagens_chat.append({
                    "role": "assistant",
                    "content": resposta_completa
                })

                adicionar_historico(
                    "Conversa com a Lumus AI",
                    "",
                    "Marketing",
                    pedido,
                    "Conversacional",
                    resposta_completa
                )
            else:
                st.error(
                    "A IA não retornou texto. Tente novamente."
                )

        except Exception as erro:
            # Remove a mensagem do usuário que falhou ao processar.
            if (
                st.session_state.mensagens_chat
                and st.session_state.mensagens_chat[-1]["role"] == "user"
            ):
                st.session_state.mensagens_chat.pop()

            st.error(
                "Não foi possível obter uma resposta. "
                "Confira a configuração da API e tente novamente."
            )
            st.caption(f"Detalhes técnicos: {erro}")


# ==========================================
# PÁGINA: HISTÓRICO
# ==========================================

elif st.session_state.pagina == "Histórico":

    st.title("Histórico de criações")
    st.caption("Consulte os conteúdos gerados nesta sessão.")

    historico = st.session_state.historico

    if not historico:
        st.info(
            "Ainda não há conteúdos no histórico. "
            "Crie seu primeiro conteúdo para começar."
        )
    else:
        st.write(
            f"**{len(historico)} conteúdo(s) nesta sessão**"
        )

        for i, item in enumerate(historico):
            titulo = (
                f"{item['tipo']} · "
                f"{item['cliente']} · "
                f"{item['data']}"
            )

            with st.expander(titulo):
                st.caption(
                    f"Segmento: {item['segmento']} | "
                    f"Tom: {item['tom']}"
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

                if st.button(
                    "Usar como base para nova criação",
                    key=f"reutilizar_{i}"
                ):
                    st.session_state.pagina = "Criar conteúdo"
                    st.session_state.navegacao = "Criar conteúdo"

                    st.session_state.cliente = (
                        ""
                        if item["cliente"] == "Sem cliente"
                        else item["cliente"]
                    )

                    st.session_state.segmento = (
                        ""
                        if item["segmento"] == "Não informado"
                        else item["segmento"]
                    )

                    st.session_state.objetivo = item["objetivo"]

                    if item["tipo"] in TIPOS_CONTEUDO:
                        st.session_state.tipo_conteudo = item["tipo"]
                    else:
                        st.session_state.tipo_conteudo = (
                            TIPOS_CONTEUDO[0]
                        )

                    if item["tom"] in TONS_COMUNICACAO:
                        st.session_state.tom = item["tom"]
                    else:
                        st.session_state.tom = TONS_COMUNICACAO[0]

                    st.session_state.conteudo_atual = ""
                    st.session_state.editor_conteudo = ""

                    st.rerun()

        st.divider()

        if st.button("Limpar histórico desta sessão"):
            st.session_state.historico = []
            st.session_state.conteudo_atual = ""
            st.session_state.editor_conteudo = ""
            st.rerun()


# ==========================================
# PÁGINA: SOBRE
# ==========================================

elif st.session_state.pagina == "Sobre a Lumus AI":

    st.title("Sobre a Lumus AI")

    st.markdown("""
A **Lumus AI** é uma ferramenta criativa da Lumus Marketing,
desenvolvida para auxiliar na produção de conteúdo e na rotina
de comunicação dos clientes.

### Ferramentas disponíveis

- Legendas para Instagram
- Roteiros para Reels
- Calendários de conteúdo
- Campanhas promocionais
- Propostas comerciais
- Mensagens de prospecção
- Textos em espanhol
- Assistente conversacional de marketing

### Como utilizar

1. Escolha o tipo de conteúdo ou abra o Assistente IA.
2. Informe o cliente e o objetivo, quando necessário.
3. Selecione o tom de comunicação.
4. Gere, revise, copie ou baixe o resultado.

### Importante

Os conteúdos gerados por IA devem ser revisados antes da publicação.
Confirme preços, datas, condições e demais informações comerciais.
""")

    st.divider()

    st.markdown("**LUMUS MARKETING**")
    st.caption("Criatividade com estratégia.")


# ==========================================
# RODAPÉ
# ==========================================

st.markdown("""
<div class="footer">
    LUMUS AI · CRIATIVIDADE COM ESTRATÉGIA
</div>
""", unsafe_allow_html=True)
