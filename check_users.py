import sqlite3
import sys

def check_user_passwords():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Verificar estrutura da tabela
        cursor.execute("PRAGMA table_info(usuarios)")
        columns = [col[1] for col in cursor.fetchall()]
        print("Colunas da tabela usuarios:", columns)
        
        # Verificar usuários e hashes
        cursor.execute("SELECT id, nome, senha FROM usuarios")
        users = cursor.fetchall()
        
        print("\nUsuários encontrados:")
        for user in users:
            print(f"ID: {user[0]}, Nome: {user[1]}, Hash: {user[2][:20]}... (tamanho: {len(user[2])})")
            
    except Exception as e:
        print(f"Erro ao verificar usuários: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    check_user_passwords()
