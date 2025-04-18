import sqlite3
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

def migrate_database():
    # Conectar ao banco de dados
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        # 1. Renomear coluna 'senha' para 'senha_hash' se existir
        cursor.execute("PRAGMA table_info(usuarios)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'senha' in columns and 'senha_hash' not in columns:
            print("Migrando coluna de senhas...")
            cursor.execute('''
                ALTER TABLE usuarios RENAME COLUMN senha TO senha_hash
            ''')
            conn.commit()
            
            # 2. Atualizar todas as senhas para hashes bcrypt
            cursor.execute('SELECT id, senha_hash FROM usuarios')
            usuarios = cursor.fetchall()
            
            for usuario_id, senha in usuarios:
                if not senha.startswith('$2b$'):  # Verifica se já não é um hash
                    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    cursor.execute('''
                        UPDATE usuarios SET senha_hash = ? WHERE id = ?
                    ''', (senha_hash, usuario_id))
            
            conn.commit()
            print("Senhas migradas para bcrypt com sucesso!")
        
        # 3. Criar índices se não existirem
        print("Verificando índices...")
        indices = [
            ('idx_usuarios_nome', 'usuarios(nome)'),
            ('idx_usuarios_email', 'usuarios(email)'),
            ('idx_clientes_nome', 'clientes(nome)'),
            ('idx_clientes_telefone', 'clientes(telefone)'),
            ('idx_equipamentos_cliente', 'equipamentos(cliente_id)'),
            ('idx_equipamentos_serie', 'equipamentos(serie)'),
            ('idx_equipamentos_codigo', 'equipamentos(codigo_barras)'),
            ('idx_ordens_equipamento', 'ordens(equipamento_id)'),
            ('idx_ordens_usuario', 'ordens(usuario_id)'),
            ('idx_ordens_status', 'ordens(status)'),
            ('idx_ordens_data', 'ordens(data_criacao)'),
            ('idx_servicos_ordem', 'servicos_tecnicos(ordem_id)')
        ]
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        existing_indices = [idx[0] for idx in cursor.fetchall()]
        
        for idx_name, idx_def in indices:
            if idx_name not in existing_indices:
                cursor.execute(f'CREATE INDEX {idx_name} ON {idx_def}')
                print(f"Índice {idx_name} criado")
        
        conn.commit()
        print("Migração concluída com sucesso!")
        
    except Exception as e:
        print(f"Erro durante a migração: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    print("Iniciando migração do banco de dados...")
    migrate_database()
