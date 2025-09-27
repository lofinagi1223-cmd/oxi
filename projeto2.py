import streamlit as st
from merger import PDFMerger
import Database

# Inicializa a tabela no banco
Database.create_table()

st.set_page_config(page_title="Mesclar PDFs", page_icon="📑")

# Estado inicial
if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


# ----------------- Login -----------------
def login():
    st.title("🔑 Login")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Entrar"):
            if Database.verify_user(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["page"] = "app"
                st.rerun()
            else:
                st.error("❌ Usuário ou senha incorretos")

    with col2:
        if st.button("Registrar"):
            st.session_state["page"] = "register"
            st.rerun()


# ----------------- Registro -----------------
def register():
    st.title("📝 Registrar novo usuário")

    username = st.text_input("Novo usuário")
    email = st.text_input("Email")
    password = st.text_input("Nova senha", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Salvar"):
            if Database.add_user(username, email, password):
                st.success("✅ Usuário registrado com sucesso! Faça login.")
                st.session_state["page"] = "login"
                st.rerun()
            else:
                st.error("⚠️ Usuário ou email já existem, tente outro.")

    with col2:
        if st.button("Voltar"):
            st.session_state["page"] = "login"
            st.rerun()


# ----------------- App -----------------
def app():
    st.title("✨ Mesclar PDFs Online")

    arquivos_enviados = st.file_uploader(
        label="Envie os PDFs que deseja mesclar",
        type="pdf",
        accept_multiple_files=True
    )

    if arquivos_enviados:
        pdf_merger = PDFMerger()
        pdf_merger.add_files(arquivos_enviados)
        output_file = pdf_merger.save()

        st.success("✅ PDF mesclado com sucesso!")
        with open(output_file, "rb") as f:
            st.download_button(
                "📥 Baixar PDF Mesclado",
                f,
                file_name="PDF_Mesclado.pdf",
                mime="application/pdf"
            )

    st.subheader("📂 Arraste ou selecione os arquivos acima ☝")

    if st.button("Sair"):
        st.session_state["logged_in"] = False
        st.session_state["page"] = "login"
        st.rerun()


# ----------------- Router -----------------
if st.session_state["page"] == "login":
    login()
elif st.session_state["page"] == "register":
    register()
elif st.session_state["page"] == "app" and st.session_state["logged_in"]:
    app()
