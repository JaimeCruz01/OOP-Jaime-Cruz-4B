mensajes = []
comentarios = []
class user:
    def __init__(self, correo, contraseña, telefono, nombre):
        self.correo = correo
        self._contraseña = contraseña
        self.telefono = telefono
        self.nombre = nombre

    def enviar(self, receptor, texto):
        print("Texto enviado")
        mensaje = dm(self.nombre, receptor, texto)
        mensajes.append(mensaje)

    def verchat(self, receptor):
        for mensaje in mensajes:
            if (mensaje.emisor == self.nombre and mensaje.receptor == receptor) or (mensaje.emisor == receptor and mensaje.receptor == self.nombre):
                print(f"{mensaje.emisor} a {mensaje.receptor}: {mensaje.texto}")

    def postear(self, post):
        self.post = post
        post.mostrar()

    def comentar(self, usuario, comentario, post):
        print(f"El usuario {usuario} comenta {comentario} en el post {post.descripcion}")

class post:
    def __init__(self, usuario, comentarios, likes, descripcion):
        self.usuario = usuario
        self.comentarios = comentarios
        self.likes = likes
        self.descripcion = descripcion
    def mostrar(self):
        print(f"Post de {self.usuario}: {self.descripcion} con {self.likes} likes y {self.comentarios} comentarios")

class comentario:
    def __init__(self, usuario, comentarios, likes, texto, id_post):
        self.usuario = usuario
        self.comentarios = comentarios
        self.likes = likes
        self.texto = texto
        self.id_post = id_post
    def modificar(self, nuevo_texto):
        self.texto = nuevo_texto

class dm:
    def __init__(self, emisor, receptor, texto):
        self.emisor = emisor
        self.receptor = receptor
        self.texto = texto

    def modificar(self, nuevo_texto):
        self.texto = nuevo_texto

usuario1 = user("Jaie", "1234", "1234567890", "Jaie")
usuario2 = user("Omar", "1234", "1234567890", "Omar")
posteo = post(usuario1.nombre, "Hola", "31", "holaa")

usuario1.postear(posteo)
usuario2.comentar(usuario2.nombre, "Muy bueno", posteo)