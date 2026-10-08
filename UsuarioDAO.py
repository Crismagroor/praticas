import sqlite3
from Usuario import Usuario

class UsuarioDAO:
    def __init__(self, db_name="usuarios.db"):
        self.conn = sqlite3.connect(db_name)
        self._criar_tabela()

    def _criar_tabela(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def inserir(self, usuario):
        try:
            cur = self.conn.cursor()
            cur.execute('''
                INSERT INTO usuarios (nome, email, senha)
                VALUES (?, ?, ?)
            ''', (usuario.nome, usuario.email, usuario.senha))
            self.conn.commit()
            usuario.id = cur.lastrowid
            return usuario
        except sqlite3.IntegrityError as e:
            raise ValueError("Erro ao inserir usuário: e-mail duplicado.") from e

    def buscar_por_id(self, id):
        cur = self.conn.cursor()
        cur.execute('SELECT id, nome, email, senha FROM usuarios WHERE id = ?', (id,))
        row = cur.fetchone()
        return Usuario(*row[1:], id=row[0]) if row else None

    def buscar_por_email(self, email):
        cur = self.conn.cursor()
        cur.execute('SELECT id, nome, email, senha FROM usuarios WHERE email = ?', (email,))
        row = cur.fetchone()
        return Usuario(*row[1:], id=row[0]) if row else None

    def listar_todos(self):
        cur = self.conn.cursor()
        cur.execute('SELECT id, nome, email, senha FROM usuarios')
        return [Usuario(id=row[0], nome=row[1], email=row[2], senha=row[3]) for row in cur.fetchall()]

    def atualizar(self, usuario):
        cur = self.conn.cursor()
        cur.execute('''
            UPDATE usuarios
            SET nome = ?, email = ?, senha = ?
            WHERE id = ?
        ''', (usuario.nome, usuario.email, usuario.senha, usuario.id))
        self.conn.commit()
        if cur.rowcount == 0:
            raise ValueError("Usuário não encontrado para atualização.")

    def excluir(self, id):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM usuarios WHERE id = ?', (id,))
        self.conn.commit()
        if cur.rowcount == 0:
            raise ValueError("Usuário não encontrado para exclusão.")

    def fechar(self):
        self.conn.close()