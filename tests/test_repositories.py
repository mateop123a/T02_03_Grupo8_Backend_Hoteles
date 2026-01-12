from src.repositories.usuario_repository import UsuarioRepository


class TestUsuarioRepository:

    def setup_method(self):
        self.repo = UsuarioRepository()

    def test_save_usuario(self):
        usuario = {
            "username": "astro",
            "correo": "astro@test.com"
        }

        saved = self.repo.save(usuario)

        assert saved["usuario_id"] == 1
        assert saved["username"] == "astro"
        assert saved["correo"] == "astro@test.com"
        assert len(self.repo.usuarios) == 1

    def test_existe_correo_true(self):
        self.repo.save({
            "username": "user1",
            "correo": "user1@test.com"
        })

        assert self.repo.existeCorreo("user1@test.com") is True

    def test_existe_correo_false(self):
        assert self.repo.existeCorreo("noexiste@test.com") is False

    def test_existe_usuario_true(self):
        self.repo.save({
            "username": "user2",
            "correo": "user2@test.com"
        })

        assert self.repo.existeUsuario("user2") is True

    def test_existe_usuario_false(self):
        assert self.repo.existeUsuario("noexiste") is False
