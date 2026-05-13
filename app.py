import streamlit as st
import sqlite3
import pandas as pd

# 1. FUNÇÃO PARA CRIAR O BANCO (Essencial para funcionar na Nuvem)
def init_db():
    conn = sqlite3.connect('monitoria.db')
    c = conn.cursor()
    # Cria a tabela se ela não existir
    c.execute('''CREATE TABLE IF NOT EXISTS monitorias 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  disciplina TEXT, 
                  monitor TEXT, 
                  data TEXT, 
                  local TEXT)''')
    conn.commit()
    conn.close()

# Inicializa o banco de dados
init_db()

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sistema de Monitoria UniRuy", layout="centered")

# --- LÓGICA DE LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔐 Login - Monitoria UniRuy")
    user = st.text_input("Usuário (Dica: admin)")
    pwd = st.text_input("Senha (Dica: 1234)", type="password")
    if st.button("Entrar"):
        if user == "admin" and pwd == "1234":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Credenciais inválidas")
else:
    # --- ÁREA LOGADA (NAVEGAÇÃO) ---
    st.sidebar.title("Navegação")
    menu = st.sidebar.radio("Ir para:", ["Dashboard", "Cadastrar Monitoria", "Gerenciar/Excluir", "Relatório"])

    if menu == "Cadastrar Monitoria":
        st.title("➕ RF2: Cadastrar Nova Monitoria")
        
        # Campos para adicionar informações
        with st.form("form_cadastro"):
            disciplina = st.text_input("Nome da Disciplina")
            monitor = st.text_input("Nome do Monitor")
            data = st.date_input("Data da Sessão")
            local = st.selectbox("Local", ["Laboratório A", "Auditório", "Sala 202", "Remoto"])
            
            enviar = st.form_submit_button("Salvar Informações")
            
            if enviar:
                if disciplina and monitor:
                    conn = sqlite3.connect('monitoria.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO monitorias (disciplina, monitor, data, local) VALUES (?,?,?,?)", 
                              (disciplina, monitor, str(data), local))
                    conn.commit()
                    conn.close()
                    st.success("Informações adicionadas com sucesso!")
                else:
                    st.warning("Por favor, preencha todos os campos.")

    elif menu == "Dashboard":
        st.title("📚 RF1: Monitorias Agendadas")
        conn = sqlite3.connect('monitoria.db')
        df = pd.read_sql_query("SELECT * FROM monitorias", conn)
        conn.close()
        if df.empty:
            st.info("Nenhuma informação cadastrada ainda.")
        else:
            st.dataframe(df, use_container_width=True)

    # ... (outros menus como Relatório e Excluir seguem a mesma lógica)
