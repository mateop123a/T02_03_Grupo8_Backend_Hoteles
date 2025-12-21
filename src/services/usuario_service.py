import re

def validacionCorreo(correo):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, correo):
        raise ValueError("El correo electronico no es valido")
    
def registrarUsuario(usuario, repository):

    if not usuario.get("nombre"):
        raise ValueError("El nombre es un campo obligatorio")

    if not usuario.get("correo"):
        raise ValueError("El correo es un campo obligatorio")
    
    validacionCorreo(usuario["correo"])

    if repository.existeCorreo(usuario["correo"]):
        raise ValueError("El correo ya ha sido registrado")
    
    repository.save(usuario)
    return {"mensaje" : "Usuario registrado correctamente"}