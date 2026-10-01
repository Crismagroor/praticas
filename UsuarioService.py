
from Usuario import Usuario
class UsuarioService:
    def __init__(self,dao):
        self.dao=dao
    def cadastrar_usuario(self, nome, email,senha):
        self.dao.inserir
        #Criar um objeto da classe Usuario com os dados informados
        usuario = Usuario(nome,email ,senha)
        #Persisteir o novo por meio de UsuarioDAO.inserir(). 
        usuarioComId = self.dao.inserir(usuario)
        #Retonrar o objteo Usuario cadastrado, comtendo o identificador
        return usuarioComId