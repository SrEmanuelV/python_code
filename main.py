import tkinter as tk
from tkinter import messagebox
import random
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

# Configuración de la conexión a la base de datos
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abc"
    )

# Función para enviar código de verificación por correo
def enviar_codigo_verificacion(correo, codigo):
    remitente = "emanuelvillalobos546@gmail.com"
    receptor = correo
    asunto = "Código de Verificación"
    mensaje = f"Tu código de verificación es: {codigo}"

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = receptor
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, 'xzkstdyilfsarrdz')  # Contraseña de aplicación
        servidor.sendmail(remitente, receptor, msg.as_string())
        servidor.quit()
        print(f"Correo enviado a {correo}")
    except Exception as e:
        print(f"Error enviando correo: {e}")

# Clase para la aplicación principal
class Aplicacion(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Aplicación con Verificación")
        self.geometry("500x400")
        
        contenedor = tk.Frame(self)
        contenedor.pack(side="top", fill="both", expand=True)
        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for Pantalla in (PantallaRegistro, PantallaLogin, PantallaPrincipal, PantallaOlvideContraseña, PantallaEditarPerfil):
            frame = Pantalla(contenedor, self)
            self.frames[Pantalla] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.mostrar_pantalla(PantallaLogin)

    def mostrar_pantalla(self, pantalla):
        frame = self.frames[pantalla]
        frame.tkraise()

import tkinter as tk
from tkinter import messagebox
import random
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

# Configuración de la conexión a la base de datos
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abc"
    )

# Función para enviar código de verificación por correo
def enviar_codigo_verificacion(correo, codigo):
    remitente = "emanuelvillalobos546@gmail.com"
    receptor = correo
    asunto = "Código de Verificación"
    mensaje = f"Tu código de verificación es: {codigo}"

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = receptor
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, 'xzkstdyilfsarrdz')  # Contraseña de aplicación
        servidor.sendmail(remitente, receptor, msg.as_string())
        servidor.quit()
        print(f"Correo enviado a {correo}")
    except Exception as e:
        print(f"Error enviando correo: {e}")

# Clase para la aplicación principal
class Aplicacion(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Aplicación con Verificación")
        self.geometry("500x400")
        
        contenedor = tk.Frame(self)
        contenedor.pack(side="top", fill="both", expand=True)
        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for Pantalla in (PantallaRegistro, PantallaLogin, PantallaPrincipal, PantallaOlvideContraseña, PantallaEditarPerfil):
            frame = Pantalla(contenedor, self)
            self.frames[Pantalla] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.mostrar_pantalla(PantallaLogin)

    def mostrar_pantalla(self, pantalla):
        frame = self.frames[pantalla]
        frame.tkraise()

# Pantalla de Registro
class PantallaRegistro(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Registro", font=("Helvetica", 18))
        label.pack(pady=10)

        # Entradas para el registro
        tk.Label(self, text="Nombre de Usuario").pack()
        self.entrada_nombre = tk.Entry(self)
        self.entrada_nombre.pack()

        tk.Label(self, text="Correo").pack()
        self.entrada_correo = tk.Entry(self)
        self.entrada_correo.pack()

        tk.Label(self, text="Contraseña").pack()
        self.entrada_contraseña = tk.Entry(self, show="*")
        self.entrada_contraseña.pack()

        # Botón para registrarse
        boton_registrar = tk.Button(self, text="Registrar", command=self.registrar)
        boton_registrar.pack(pady=10)
        
        # Botón para ir al login
        boton_login = tk.Button(self, text="Ya tengo cuenta", command=lambda: controller.mostrar_pantalla(PantallaLogin))
        boton_login.pack()

    # Función para registrar al usuario
    def registrar(self):
        nombre_usuario = self.entrada_nombre.get()
        correo = self.entrada_correo.get()
        contraseña = self.entrada_contraseña.get()
        
        if nombre_usuario and correo and contraseña:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            
            # Verificar si el usuario ya existe
            cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
            usuario_existente = cursor.fetchone()
            
            if usuario_existente:
                messagebox.showwarning("Error", "El correo ya está registrado.")
            else:
                # Generar código de verificación
                self.codigo_verificacion = str(random.randint(100000, 999999))
                
                # Registrar nuevo usuario con el código de verificación y verificado en False
                cursor.execute(
                    "INSERT INTO usuarios (nombre_usuario, correo, contraseña, codigo_verificacion, verificado) VALUES (%s, %s, %s, %s, %s)",
                    (nombre_usuario, correo, contraseña, self.codigo_verificacion, False)
                )
                conexion.commit()
                conexion.close()

                # Enviar el código de verificación por correo
                enviar_codigo_verificacion(correo, self.codigo_verificacion)

                # Mostrar ventana para ingresar el código de verificación
                self.mostrar_ventana_verificacion(correo)
        
        else:
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")

    # Mostrar ventana emergente para ingresar el código de verificación
    def mostrar_ventana_verificacion(self, correo):
        ventana_verificacion = tk.Toplevel(self)
        ventana_verificacion.title("Verificación de cuenta")

        label = tk.Label(ventana_verificacion, text="Ingresa el código de verificación enviado a tu correo")
        label.pack(pady=10)

        entrada_codigo = tk.Entry(ventana_verificacion)
        entrada_codigo.pack()

        # Botón para verificar el código
        boton_verificar = tk.Button(ventana_verificacion, text="Verificar", command=lambda: self.verificar_codigo(entrada_codigo.get(), correo, ventana_verificacion))
        boton_verificar.pack(pady=10)

    # Verificar código ingresado
    def verificar_codigo(self, codigo_ingresado, correo, ventana):
        if codigo_ingresado == self.codigo_verificacion:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Actualizar la base de datos para marcar el usuario como verificado
            cursor.execute("UPDATE usuarios SET verificado = %s WHERE correo = %s", (True, correo))
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Verificación", "Cuenta verificada correctamente.")
            ventana.destroy()  # Cerrar la ventana de verificación
            self.controller.mostrar_pantalla(PantallaLogin)  # Volver al login
        else:
            messagebox.showerror("Error", "Código de verificación incorrecto.")



# Pantalla de Login
class PantallaLogin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Iniciar Sesión", font=("Helvetica", 18))
        label.pack(pady=10)

        tk.Label(self, text="Correo").pack()
        self.entrada_correo = tk.Entry(self)
        self.entrada_correo.pack()

        tk.Label(self, text="Contraseña").pack()
        self.entrada_contraseña = tk.Entry(self, show="*")
        self.entrada_contraseña.pack()

        # Botón para iniciar sesión
        boton_login = tk.Button(self, text="Login", command=self.login)
        boton_login.pack(pady=10)

        # Botón para "Olvidé mi contraseña"
        boton_olvide = tk.Button(self, text="Olvidé mi contraseña", command=lambda: controller.mostrar_pantalla(PantallaOlvideContraseña))
        boton_olvide.pack()

        # Botón para ir a registro
        boton_registrar = tk.Button(self, text="Crear Cuenta", command=lambda: controller.mostrar_pantalla(PantallaRegistro))
        boton_registrar.pack()

    def login(self):
        correo = self.entrada_correo.get()
        contraseña = self.entrada_contraseña.get()
        
        if correo and contraseña:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            
            # Obtener el usuario de la base de datos
            cursor.execute("SELECT * FROM usuarios WHERE correo = %s AND contraseña = %s", (correo, contraseña))
            usuario = cursor.fetchone()
            conexion.close()
            
            if usuario:
                verificado = usuario[5]  # Asumiendo que la columna 5 es 'verificado'
                if verificado:
                    messagebox.showinfo("Login", "Inicio de sesión exitoso.")
                    self.controller.mostrar_pantalla(PantallaPrincipal)
                else:
                    messagebox.showinfo("Verificación", "Tu cuenta no está verificada. Se te pedirá el código de verificación.")
                    self.mostrar_verificacion(correo)
            else:
                messagebox.showwarning("Error", "Correo o contraseña incorrectos.")
        else:
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")

    def mostrar_verificacion(self, correo):
        # Crear una ventana emergente para el código de verificación
        ventana_verificacion = tk.Toplevel(self)
        ventana_verificacion.title("Verificación de cuenta")

        label = tk.Label(ventana_verificacion, text="Ingresa el código de verificación enviado a tu correo")
        label.pack(pady=10)

        entrada_codigo = tk.Entry(ventana_verificacion)
        entrada_codigo.pack()

        # Botón para verificar el código
        boton_verificar = tk.Button(ventana_verificacion, text="Verificar", command=lambda: self.verificar_codigo(entrada_codigo.get(), correo, ventana_verificacion))
        boton_verificar.pack(pady=10)

    def verificar_codigo(self, codigo_ingresado, correo, ventana):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("SELECT codigo_verificacion FROM usuarios WHERE correo = %s", (correo,))
        codigo_correcto = cursor.fetchone()[0]
        conexion.close()

        if codigo_ingresado == codigo_correcto:
            # Código correcto, actualizar la base de datos para marcar el correo como verificado
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("UPDATE usuarios SET verificado = %s WHERE correo = %s", (True, correo))
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Verificación", "Cuenta verificada correctamente.")
            ventana.destroy()  # Cerrar la ventana de verificación
            self.controller.mostrar_pantalla(PantallaPrincipal)
        else:
            messagebox.showerror("Error", "Código de verificación incorrecto.")



# Pantalla Principal
class PantallaPrincipal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Pantalla Principal", font=("Helvetica", 18))
        label.pack(pady=10)

        # Botón para editar perfil
        boton_editar = tk.Button(self, text="Editar Perfil", command=lambda: controller.mostrar_pantalla(PantallaEditarPerfil))
        boton_editar.pack()

# Pantalla "Olvidé mi Contraseña"
class PantallaOlvideContraseña(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Recuperar Contraseña", font=("Helvetica", 18))
        label.pack(pady=10)

        tk.Label(self, text="Correo").pack()
        self.entrada_correo = tk.Entry(self)
        self.entrada_correo.pack()

        boton_enviar_codigo = tk.Button(self, text="Enviar Código", command=self.enviar_codigo)
        boton_enviar_codigo.pack(pady=10)

        self.codigo_generado = None

    def enviar_codigo(self):
        correo = self.entrada_correo.get()
        if correo:
            codigo = str(random.randint(100000, 999999))
            enviar_codigo_verificacion(correo, codigo)
            self.codigo_generado = codigo
            messagebox.showinfo("Código Enviado", "Se ha enviado un código a tu correo.")
            self.mostrar_ingreso_codigo()

    def mostrar_ingreso_codigo(self):
        tk.Label(self, text="Ingrese el código").pack()
        self.entrada_codigo = tk.Entry(self)
        self.entrada_codigo.pack()

        boton_verificar_codigo = tk.Button(self, text="Verificar Código", command=self.verificar_codigo)
        boton_verificar_codigo.pack(pady=10)

    def verificar_codigo(self):
        codigo_ingresado = self.entrada_codigo.get()
        if codigo_ingresado == self.codigo_generado:
            messagebox.showinfo("Verificación", "Código verificado. Ahora puedes cambiar tu contraseña.")
            self.mostrar_cambio_contraseña()
        else:
            messagebox.showerror("Error", "Código incorrecto.")

    def mostrar_cambio_contraseña(self):
        tk.Label(self, text="Nueva Contraseña").pack()
        self.entrada_nueva_contraseña = tk.Entry(self, show="*")
        self.entrada_nueva_contraseña.pack()

        boton_cambiar_contraseña = tk.Button(self, text="Cambiar Contraseña", command=self.cambiar_contraseña)
        boton_cambiar_contraseña.pack(pady=10)

    def cambiar_contraseña(self):
        nueva_contraseña = self.entrada_nueva_contraseña.get()
        correo = self.entrada_correo.get()

        if nueva_contraseña:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Actualizar la contraseña en la base de datos
            cursor.execute("UPDATE usuarios SET contraseña = %s WHERE correo = %s", (nueva_contraseña, correo))
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", "Tu contraseña ha sido actualizada correctamente.")
            self.master.mostrar_pantalla(PantallaLogin)
        else:
            messagebox.showwarning("Error", "Por favor ingresa una nueva contraseña.")

# Pantalla de Edición de Perfil
class PantallaEditarPerfil(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Editar Perfil", font=("Helvetica", 18))
        label.pack(pady=10)

        tk.Label(self, text="Nuevo Nombre de Usuario").pack()
        self.entrada_nuevo_usuario = tk.Entry(self)
        self.entrada_nuevo_usuario.pack()

        tk.Label(self, text="Nuevo Correo").pack()
        self.entrada_nuevo_correo = tk.Entry(self)
        self.entrada_nuevo_correo.pack()

        tk.Label(self, text="Nueva Contraseña").pack()
        self.entrada_nueva_contraseña = tk.Entry(self, show="*")
        self.entrada_nueva_contraseña.pack()

        # Botón para enviar cambios
        boton_guardar = tk.Button(self, text="Guardar Cambios", command=self.guardar_cambios)
        boton_guardar.pack(pady=10)

    def guardar_cambios(self):
        nuevo_usuario = self.entrada_nuevo_usuario.get()
        nuevo_correo = self.entrada_nuevo_correo.get()
        nueva_contraseña = self.entrada_nueva_contraseña.get()

        correo_actual = self.master.frames[PantallaLogin].entrada_correo.get()  # Recuperar el correo del usuario logueado

        if nuevo_usuario or nuevo_correo or nueva_contraseña:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            if nuevo_usuario:
                cursor.execute("UPDATE usuarios SET nombre_usuario = %s WHERE correo = %s", (nuevo_usuario, correo_actual))

            if nuevo_correo:
                # Si se cambia el correo, se envía un código de verificación al nuevo correo
                codigo_verificacion = str(random.randint(100000, 999999))
                enviar_codigo_verificacion(nuevo_correo, codigo_verificacion)
                cursor.execute("UPDATE usuarios SET correo = %s, codigo_verificacion = %s, verificado = %s WHERE correo = %s",
                               (nuevo_correo, codigo_verificacion, False, correo_actual))

            if nueva_contraseña:
                cursor.execute("UPDATE usuarios SET contraseña = %s WHERE correo = %s", (nueva_contraseña, correo_actual))

            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", "Los cambios han sido guardados. Si cambiaste el correo, verifica tu nuevo correo.")
            self.master.mostrar_pantalla(PantallaLogin)
        else:
            messagebox.showwarning("Error", "No se ha realizado ningún cambio.")

# Ejecución de la aplicación
if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()

