import streamlit as st
import sqlite3
import pandas as pd
import sqlite3

# Função para garantir que o banco e a tabela existam na nuvem
def setup_database():
    conn = sqlite3.connect('monitoria.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS monitorias 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, disciplina TEXT, monitor TEXT, data TEXT, local TEXT)''')
    conn.commit()
    conn.close()

# Executa a criação assim que o app inicia
setup_database()
# Configuração da Página
st.set_page_config(page_title="Sistema de Monitoria UniRuy", layout="centered")

def check_login(user, pwd):
    return user == "admin" and pwd == "1234" # Simplicidade RAD

# --- INTERFACE DE LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔐 Login - Monitoria UniRuy")
    user = st.text_input("Usuário")
    pwd = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if check_login(user, pwd):
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Credenciais inválidas")
else:
    # --- ÁREA LOGADA ---
    st.sidebar.title("Navegação")
    menu = st.sidebar.radio("Ir para:", ["Dashboard", "Cadastrar Monitoria", "Gerenciar/Excluir", "Relatório"])

    conn = sqlite3.connect('monitoria.db')
    c = conn.cursor()

    if menu == "Dashboard":
        st.title("📚 RF1: Visualizar Horários")
        df = pd.read_sql_query("SELECT * FROM monitorias", conn)
        st.table(df)

    elif menu == "Cadastrar Monitoria":
        st.title("➕ RF2: Cadastrar (Create)")
        disciplina = st.text_input("Nome da Disciplina")
        monitor = st.text_input("Nome do Monitor")
        data = st.date_input("Data da Sessão")
        local = st.selectbox("Local", ["Laboratório A", "Auditório", "Sala 202"])
        
        if st.button("Salvar"):
            c.execute("INSERT INTO monitorias (disciplina, monitor, data, local) VALUES (?,?,?,?)", 
                      (disciplina, monitor, str(data), local))
            conn.commit()
            st.success("Monitoria agendada!")

    elif menu == "Gerenciar/Excluir":
        st.title("⚙️ RF3: Gerenciar (Delete/Update)")
        df = pd.read_sql_query("SELECT * FROM monitorias", conn)
        selected_id = st.selectbox("Selecione o ID para remover", df['id'])
        if st.button("Remover Registro"):
            c.execute(f"DELETE FROM monitorias WHERE id={selected_id}")
            conn.commit()
            st.warning(f"Registro {selected_id} removido.")

    elif menu == "Relatório":
        st.title("📊 RF4: Relatório Opcional")
        df = pd.read_sql_query("SELECT * FROM monitorias", conn)
        st.write(f"Total de monitorias agendadas: {len(df)}")
        st.bar_chart(df['disciplina'].value_counts())

    if st.sidebar.button("Sair"):
        st.session_state['logged_in'] = False
        st.rerun()
