from Usuario import Usuario
from UsuarioDAO import UsuarioDAO
from UsuarioService import UsuarioService
import pytest

@pytest.fixture
def usuarioFeliz(scope="session"):
    usuario = Usuario(
        nome  = "Maria do Exemplo",
        email = "maria@exemplo.com",
        senha = "9876543210" )
    return usuario


@pytest.fixture(scope="function")
def usuarioDAO(usuarioFeliz):
    #setup
    usuarioDAO = UsuarioDAO()
    usuarioBanco = usuarioDAO.buscar_por_email(usuarioFeliz.email)
    if(usuarioBanco is not None):
        usuarioDAO.excluir(usuarioBanco.id)
    yield usuarioDAO
    #teardown
    usuarioBanco = usuarioDAO.buscar_por_email(usuarioFeliz.email)
    if(usuarioBanco is not None):
        usuarioDAO.excluir(usuarioBanco.id)
    usuarioDAO.fechar()
def test_caminhoFeliz(usuarioDAO, usuarioFeliz):
    usuarioService = UsuarioService(usuarioDAO)
    usuarioBanco = usuarioService.cadastrar_usuario(
        usuarioFeliz.nome,
        usuarioFeliz.email,
        usuarioFeliz.senha
    )
    assert usuarioBanco.nome  == usuarioFeliz.nome
    assert usuarioBanco.email == usuarioFeliz.email
    assert usuarioBanco.senha == usuarioFeliz.senha
    assert usuarioBanco.id is not None

def test_caminhoFeliz_persistido(usuarioDAO, usuarioFeliz):
    usuarioService = UsuarioService(usuarioDAO)
    usuarioDoServico = usuarioService.cadastrar_usuario(
        usuarioFeliz.nome,
        usuarioFeliz.email,
        usuarioFeliz.senha
    )
    usuarioDoBanco = usuarioDAO.buscar_por_id(usuarioDoServico.id)

    assert usuarioDoBanco.nome  == usuarioFeliz.nome
    assert usuarioDoBanco.email == usuarioFeliz.email
    assert usuarioDoBanco.senha == usuarioFeliz.senha
@pytest.fixture(scope="function")
def usuarioService(usuarioDAO):
    return UsuarioService(usuarioDAO)

@pytest.mark.parametrize("nome", [
    (""),
    (None),
    ("  "),
    (" ")
])
def test_cadastro_RV02_invalido(usuarioService, usuarioFeliz, nome):
    with pytest.raises(ValueError, match="^Nome não pode estar em branco.$"):
        usuarioService.cadastrar_usuario(
        nome,
        usuarioFeliz.email,
        usuarioFeliz.senha)

@pytest.mark.parametrize("email",[
    (None),
    ("www.exemplo.com"),
    (""),
    ("teste#exemplo.com")
])
def teste_cadastro_RV03_invalido(usuarioService, usuarioFeliz, email):
    with pytest.raises(ValueError,
                       match="^E-mail inválido.$"):
        usuarioService.cadastrar_usuario(
            usuarioFeliz.nome, email, usuarioFeliz.senha
        )

def test_cadastro_RV04_invalido(usuarioService, usuarioFeliz):
    with pytest.raises(ValueError, match="^A senha deve ser diferente de e-mail.$"):
        usuarioService.cadastrar_usuario(
            usuarioFeliz.nome,
            usuarioFeliz.email,
            usuarioFeliz.email)

def test_cadastro_RV05(usuarioService, usuarioFeliz):
    usuarioService.cadastrar_usuario(
            usuarioFeliz.nome,
            usuarioFeliz.email,
            usuarioFeliz.senha
    )
    with pytest.raises(ValueError,
        match=f"E-mail '{usuarioFeliz.email}' já está cadastrado."):
            usuarioService.cadastrar_usuario(
            usuarioFeliz.nome,
            usuarioFeliz.email,
            usuarioFeliz.senha
            )
def test_buscar_por_id_RV02_valida(usuarioService, usuarioFeliz):
    usuario = usuarioService.cadastrar_usuario(
        usuarioFeliz.nome,
        usuarioFeliz.email,
        usuarioFeliz.senha)
    usuarioBuscado = usuarioService.buscar_por_id(usuario.id)
    assert usuario.id == usuarioBuscado.id
    assert usuario.nome == usuarioBuscado.nome
    assert usuario.email == usuarioBuscado.email
    assert usuario.senha == usuarioBuscado.senha


def test_excluir_ususario_RF05_valido(usuarioService, usuarioFeliz):
    usuario = usuarioService.cadastrar_usuario(
        usuarioFeliz.nome,
        usuarioFeliz.email,
        usuarioFeliz.senha)
    usuarioService.excluir_usuario(usuario.id)
    with pytest.raises(ValueError,
                       match=f'Usuário com ID {usuario.id} não encontrado.'):
        usuarioService.buscar_por_id(usuario.id)

def test_excluir_ususario_RF05_invalido(usuarioService, usuarioFeliz):
    usuario = usuarioService.cadastrar_usuario(
        usuarioFeliz.nome,
        usuarioFeliz.email,
        usuarioFeliz.senha)
    usuarioService.excluir_usuario(usuario.id)
    with pytest.raises(ValueError,
                       match=f'Usuário não encontrado para exclusão.'):
        usuarioService.excluir_usuario(usuario.id)
@pytest.mark.parametrize("senha", [
    ("12345678"),
    ("123456789"),
    ("1234567890"),
    ("1234567dsjnklfsoijoierreoti")
])
def test_cadastro_RV02(usuarioService, usuarioFeliz, senha):
    usuario = usuarioService.cadastrar_usuario(usuarioFeliz.nome, usuarioFeliz.email, senha)
    assert senha ==  usuario.senha

@pytest.mark.parametrize("senha",[
    (None),
    (""),
    ("1"),
    ("123456"),
    ("1234567")
])
def test_cadastro_invalido(usuarioService, usuarioFeliz, senha):
    with pytest.raises(ValueError,
                        match="^A senha deve conter pelo menos 8 caracteres.$"):
        usuarioService.cadastrar_usuario(
            usuarioFeliz.nome, usuarioFeliz.email,senha)

    
