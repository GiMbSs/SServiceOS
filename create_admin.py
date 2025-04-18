import sqlite3
import bcrypt
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
DATABASE = 'database.db'
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@example.com')

def init_database(conn):
    """Cria todas as tabelas necessárias se não existirem"""
    cursor = conn.cursor()
    
    # Comandos SQL para criar as tabelas
    sql_commands = [
        '''CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            cargo TEXT NOT NULL,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''',
        '''CREATE INDEX IF NOT EXISTS idx_usuarios_nome ON usuarios(nome)''',
        '''CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email)''',
        '''CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            endereco TEXT NOT NULL,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''',
        '''CREATE INDEX IF NOT EXISTS idx_clientes_nome ON clientes(nome)''',
        '''CREATE INDEX IF NOT EXISTS idx_clientes_telefone ON clientes(telefone)''',
        '''CREATE TABLE IF NOT EXISTS equipamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            serie TEXT,
            estado_equipamento TEXT NOT NULL,
            defeito_relatado TEXT NOT NULL,
            codigo_barras TEXT UNIQUE,
            foto1 TEXT,
            foto2 TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )''',
        '''CREATE INDEX IF NOT EXISTS idx_equipamentos_cliente ON equipamentos(cliente_id)''',
        '''CREATE INDEX IF NOT EXISTS idx_equipamentos_serie ON equipamentos(serie)''',
        '''CREATE INDEX IF NOT EXISTS idx_equipamentos_codigo ON equipamentos(codigo_barras)''',
        '''CREATE TABLE IF NOT EXISTS ordens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipamento_id INTEGER NOT NULL,
            usuario_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            declaracao TEXT,
            relatorio_pecas TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            visivel INTEGER DEFAULT 1,
            FOREIGN KEY (equipamento_id) REFERENCES equipamentos (id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )''',
        '''CREATE INDEX IF NOT EXISTS idx_ordens_equipamento ON ordens(equipamento_id)''',
        '''CREATE INDEX IF NOT EXISTS idx_ordens_usuario ON ordens(usuario_id)''',
        '''CREATE INDEX IF NOT EXISTS idx_ordens_status ON ordens(status)''',
        '''CREATE INDEX IF NOT EXISTS idx_ordens_data ON ordens(data_criacao)''',
        '''CREATE TABLE IF NOT EXISTS servicos_tecnicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ordem_id INTEGER NOT NULL,
            diagnostico TEXT NOT NULL,
            descricao_servico TEXT NOT NULL,
            valor_mao_obra REAL NOT NULL,
            servico_realizado TEXT NOT NULL,
            produtos TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ordem_id) REFERENCES ordens (id)
        )''',
        '''CREATE INDEX IF NOT EXISTS idx_servicos_ordem ON servicos_tecnicos(ordem_id)'''
    ]
    
    for command in sql_commands:
        cursor.execute(command)
    conn.commit()

def create_admin_user():
    # Gerar hash da senha
    password_hash = bcrypt.hashpw(ADMIN_PASSWORD.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    try:
        # Conectar ao banco
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Verificar se já existe admin
        cursor.execute('SELECT id FROM usuarios WHERE nome = ?', (ADMIN_USERNAME,))
        if cursor.fetchone():
            print(f"Usuário admin '{ADMIN_USERNAME}' já existe!")
            return False
            
        # Inserir admin
        cursor.execute('''
            INSERT INTO usuarios (nome, email, senha, cargo)
            VALUES (?, ?, ?, 'Administrador')
        ''', (ADMIN_USERNAME, ADMIN_EMAIL, password_hash))
        
        conn.commit()
        print(f"Usuário admin '{ADMIN_USERNAME}' criado com sucesso!")
        return True
        
    except sqlite3.Error as e:
        print(f"Erro ao criar usuário admin: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # Verificar se o banco existe
    db_exists = os.path.exists(DATABASE)
    
    try:
        conn = sqlite3.connect(DATABASE)
        
        # Se o banco não existia, inicializar as tabelas
        if not db_exists:
            print(f"Criando novo banco de dados em {DATABASE}...")
            init_database(conn)
            print("Banco de dados inicializado com todas as tabelas.")
        
        # Tentar criar o usuário admin
        if create_admin_user():
            print("Setup completo. Você pode agora acessar o sistema com:")
            print(f"Usuário: {ADMIN_USERNAME}")
            print(f"Senha: {ADMIN_PASSWORD}")
        else:
            print("Setup concluído, mas o usuário admin já existia.")
            
    except Exception as e:
        print(f"Erro durante o setup: {e}")
    finally:
        if conn:
            conn.close()
