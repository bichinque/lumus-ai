
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
    background-color: #101010;
    color: white;
}
.stButton > button {
    background-color: #e32636;
    color: white;
    border-radius: 8px;
    width: 100%;
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
                    model="gemini-2.5-flash",
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

        except Exception:
            st.error(
                "Não foi possível gerar o conteúdo. "
                "Confira a chave da API e tente novamente."
            )
