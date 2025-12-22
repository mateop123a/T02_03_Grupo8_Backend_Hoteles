import re

class UsuarioService:
    ROLES_VALIDOS = ["Administrador", "Recepcionista", "Contador"]
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def _validar_correo(self, correo:str):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, correo):
            raise ValueError("El correo electronico no es valido")
    
    def _validar_campos_obligatorios(self, datos_usuario):
        campos = ["nombre", "rol", "username", "password", "correo"]
        for campo in campos:
            if not datos_usuario.get(campo):
                raise ValueError(f"El campo {campo} es obligatorio")
    
    def _validar_rol(self, rol):
        if rol not in self.ROLES_VALIDOS:
            raise ValueError(
                f"Rol no valido. Debe ser: {', '.join(self.ROLES_VALIDOS)}"
            )
        
    def registrar_usuario(self, datos_usuario:dict):
        self._validar_campos_obligatorios(datos_usuario)
        self._validar_rol(datos_usuario["rol"])
        self._validar_correo(datos_usuario["correo"])

        if self.usuario_repository.existe_correo(datos_usuario["correo"]):
            raise ValueError("El correo ya está registrado")
        
        if self.usuario_repository.existe_usuario(datos_usuario["username"]):
            raise ValueError("El nombre de usuario ya existe")
        
        return self.usuario_repository(datos_usuario)