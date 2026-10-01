
from Usuario import Usuario
class UsuarioService:
    def __init__(self,dao):
        self.dao=dao
    def cadastrar_usuario(self, nome, email,senha):
        self.dao.inserir
        #RV01 -- Validação do nome
        #O nome não poderá ser None,vazio ou composto exclusivamente
        #Mensagem: Nome não pode estar em branco.
        if nome is None or nome.strip() =="":
            raise ValueError("Nome não pode estar em branco.")
        '''RV02 -- Validação da senha
        A senha deverá conter, no mínimo, 8 caracteres.
        Mensagem de erro:
        A senha deve conter pelo menos 8 caracteres.'''
        if len(senha) < 8:
            raise ValueError("Nome não pode estar em branco.")
        '''RV03 O e-mail deverá ser informado e conter o caractere @.
        Mensagem de erro:
        E-mail inválido.'''
        if email is None or "@" not in email:
            raise ValueError("E-mail inválido.")
        '''RV04 -- A senha não poderá ser igual ao e-mail informado.
        Mensagem de erro:
        A senha deve ser diferente do e-mail.'''
        if (email == senha):
            raise ValueError("A senha deve ser diferente de e-mail.")
        '''RV05 -- Não poderá existir outro usuário cadastrado com o mesmo e-mail.
        Mensagem de erro:
        E-mail 'EMAIL' já está cadastrado.'''
        
        
        jaTemEmail =self.dao.buscar_por_email(email)
        if jaTemEmail is not None:
            raise ValueError(f'E-mail \'{email}\' já está cadastrado.')
        
        #Criar um objeto da classe Usuario com os dados informados
        usuario = Usuario(nome,email ,senha)
        #Persisteir o novo por meio de UsuarioDAO.inserir(). 
        usuarioComId = self.dao.inserir(usuario)
        #Retonrar o objteo Usuario cadastrado, comtendo o identificador gerado
        return usuarioComId