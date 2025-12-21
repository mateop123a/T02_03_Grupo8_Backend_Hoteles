class UsuarioRepository:
    def __init__(self):
        self.usuarios = []

    def existeCorreo(self, correo):
        return any(u["correo"] == correo for u in self.usuarios)
    
    def save(self, usuario):
        self.usuarios.append(usuario)