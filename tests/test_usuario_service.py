import pytest
from src.services.usuario_service import UsuarioService

class FakeUsuarioRepository:
    def __init__(self):
        self.correos = []
        self.usernames = []

    def existe_correo(self, correo):
        return correo in self.correos
    
    def existe_usuario(self, username):
        return username in self.usernames
    
    def save(self, usuario):
        self.correos.append(usuario["correo"])
        self.usernames.append(usuario["username"])
        return usuario
    
    def test_usuario_correcto():
        repo = FakeUsuarioRepository()
        service = UsuarioService(repo)

        usuario = {
            "nombre" : "name",
            "rol" : "Admin",
            "username" : "name123",
            "password" : "123",
            "correo" : "name123@gmail.com"
        }

        result = service.registrar_usuario(usuario)
        assert result["username"] == "name123"
    
    def test_correo_invalido():
        service = UsuarioService(FakeUsuarioRepository())

        usuario = {
            "nombre" : "name",
            "rol" : "Admin",
            "username" : "name123",
            "password" : "123",
            "correo" : "name123@gmail.com"
        }

        with pytest.raises(ValueError):
            service.registrar_usuario(usuario)
    
    def test_rol_invalido():
        service = UsuarioService(FakeUsuarioRepository())

        usuario = {
            "nombre" : "name",
            "rol" : "Admin",
            "username" : "name123",
            "password" : "123",
            "correo" : "name123@gmail.com"
        }

        with pytest.raises(ValueError):
            service.registrar_usuario(usuario)

