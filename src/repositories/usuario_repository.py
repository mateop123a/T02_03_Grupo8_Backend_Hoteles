class UsuarioRepository:
    def __init__(self):
        self.usuarios = []

    def existeCorreo(self, correo):
        return any(u["correo"] == correo for u in self.usuarios)
    
    def existeUsuario(self, username):
        return any(u["username"] == username for u in self.usuarios)
    
    def save(self, usuario):
        usuario["usuario_id"] = len(self.usuarios) + 1
        self.usuarios.append(usuario)
        return usuario