import sqlite3

def init_db():
    conn = sqlite3.connect('monitoria.db')
    c = conn.cursor()
    # Criar tabela de usuários para o Login
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
    # Criar tabela de Monitorias (CRUD)
    c.execute('''CREATE TABLE IF NOT EXISTS monitorias 
                 (id INTEGER PRIMARY KEY, disciplina TEXT, monitor TEXT, data TEXT, local TEXT)''')
    
    # Inserir um usuário padrão se não existir
    c.execute("INSERT OR IGNORE INTO users VALUES ('admin', '1234')")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()