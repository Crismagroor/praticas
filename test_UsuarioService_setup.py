from Usuario import Usuario
from UsuarioDAO import UsuarioDAO
from UsuarioService import UsuarioService
import pytest

@pytest.fixture
def usuarioFeliz():
    usuario = Usuario(
        nome  = "Maria do Exemplo",
        email = "maria@exemplo.com",
        senha = "4321" )
    return usuario


@pytest.fixture
def usuarioDAO():
    #setup
    usuarioDAO = UsuarioDAO()
    yield usuarioDAO
    #teardown
    usuarioDAO.fechar()
def test_caminhoFeliz(usuarioDAO, usuarioFeliz):
    usuarioService = UsuarioService(usuarioDAO)
    usuarioaBanco = usuarioService.cadastrar_usuario(
        usuarioFeliz.nome,
        usuarioFeliz.email,
        usuarioFeliz.senha
    )
    assert usuarioaBanco.nome == usuarioFeliz.nome
    assert usuarioaBanco.email == usuarioFeliz.email
    assert usuarioaBanco.senha == usuarioFeliz.senha
    assert usuarioaBanco.id is not None
