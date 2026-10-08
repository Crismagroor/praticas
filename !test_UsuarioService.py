from Usuario import Usuario
from UsuarioDAO import UsuarioDAO
from UsuarioService import UsuarioService
import pytest
def test_caminhoFeliz():
    usuarioDAO = UsuarioDAO(db_name=":memory:")
    usuarioService = UsuarioService(usuarioDAO)
    usuarioCadastrado = usuarioService.cadastrar_usuario(
        "Maria do Exemplo",
        "maria@exemplo.com",
        "4321"
        )
    assert usuarioCadastrado.nome == "Maria do Exemplo"
    assert usuarioCadastrado.email == "maria@exemplo.com"
    assert usuarioCadastrado.senha == "4321"


from unittest.mock import Mock
def test_caminhoFeliz_mock():
    usuarioDAO = Mock()
    usuarioDAO.inserir.return_value =Mock(
        nome  = "Maria do Exemplo",
        email = "maria@exemplo.com",
        senha = "4321",
        id = 1
        )
    usuarioService = UsuarioService(usuarioDAO)
    usuarioCadastrado = usuarioService.cadastrar_usuario(
        "Maria do Exemplo",
        "maria@exemplo.com",
        "4321"
        )
    assert usuarioCadastrado.nome == "Maria do Exemplo"
    assert usuarioCadastrado.email == "maria@exemplo.com"
    assert usuarioCadastrado.senha == "4321"
