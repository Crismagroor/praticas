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
def test_cadastro_nome_invalido(usuarioService, usuarioFeliz, nome):
    with pytest.raises(ValueError, match="^Nome não pode estar em branco.$"):
        usuarioService.cadastrar_usuario(
        nome,
        usuarioFeliz.email,
        usuarioFeliz.senha)

def test_cadastro_RV05(usuarioService, usuarioFeliz):
    usuarioService.cadastrar_usuario(
        "nome",
        "tests@aaa",
        "34324234234"
    )
    with pytest.raises(ValueError,
        match=f"E-mail {usuarioFeliz.email} 'teste@aaa' já está cadastrado."):
            usuarioService.cadastrar_usuario(
            usuarioFeliz.nome,
            usuarioFeliz.email,
            usuarioFeliz.senha
            )
