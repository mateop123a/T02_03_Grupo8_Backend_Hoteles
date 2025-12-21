import re

class UsuarioService:
    def __init__(self, repository):
        self.repository = repository
        self.roles = ["Administrador", "Recepcionista", "Contador"]

    def validacionCorreo(self, correo):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, correo):
            raise ValueError("El correo electronico no es valido")
    
    def registrarUsuario(self, datos_usuario):
        campos = ["nombre", "rol", "username", "password", "correo"]
        for campo in campos:
            if not datos_usuario.get(campo):
                raise ValueError(f"El campo {campo} es obligatorio")
        
        if datos_usuario["rol"] not in self.roles:
            raise ValueError(f"Rol no valido. Debe ser: {', '.join(self.roles)}")
        self.validacionCorreo(datos_usuario["correo"])

        if self.repository.existeCorreo(datos_usuario["correo"]):
            raise ValueError("Este correo ya ha sido registrado")

        if self.repository.existeUsuario(datos_usuario["username"]):
            raise ValueError("El nombre de usuario ya existe")
        return self.repository.save(datos_usuario)
