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
        self.geometry("600x500")
        
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



import tkinter as tk
from tkinter import messagebox
import smtplib
import random

# Clase para la pantalla de inicio de sesión
class PantallaLogin(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Título
        label_titulo = tk.Label(self, text="Inicio de sesión", font=("Arial", 16))
        label_titulo.pack(pady=20)

        # Etiqueta y campo de entrada para el correo
        label_correo = tk.Label(self, text="Correo electrónico:")
        label_correo.pack(pady=5)
        self.entrada_correo = tk.Entry(self, width=30)
        self.entrada_correo.pack(pady=5)

        # Etiqueta y campo de entrada para la contraseña
        label_contraseña = tk.Label(self, text="Contraseña:")
        label_contraseña.pack(pady=5)
        self.entrada_contraseña = tk.Entry(self, show="*", width=30)  # show="*" oculta la contraseña
        self.entrada_contraseña.pack(pady=5)

        # Botón para iniciar sesión
        boton_login = tk.Button(self, text="Iniciar sesión", command=self.login)
        boton_login.pack(pady=10)

        # Botón para crear cuenta
        boton_registro = tk.Button(self, text="Crear cuenta", command=self.ir_a_registro)
        boton_registro.pack(pady=5)

        # Botón para recuperar contraseña
        boton_olvide = tk.Button(self, text="¿Olvidaste tu contraseña?", command=self.recuperar_contraseña)
        boton_olvide.pack(pady=10)

    # Método para manejar el inicio de sesión
    def login(self):
        correo = self.entrada_correo.get()
        contraseña = self.entrada_contraseña.get()

        if correo and contraseña:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE correo = %s AND contraseña = %s", (correo, contraseña))
            usuario = cursor.fetchone()
            conexion.close()

            if usuario:
                nombre_usuario = usuario[1]
                verificado = usuario[5]
                if verificado:
                    self.controller.correo_usuario_actual = correo  # Guardamos el correo del usuario actual
                    self.controller.frames[PantallaPrincipal].actualizar_bienvenida(nombre_usuario)
                    self.controller.mostrar_pantalla(PantallaPrincipal)
                else:
                    messagebox.showinfo("Verificación", "Tu cuenta no está verificada.")
                    self.mostrar_verificacion(correo)
            else:
                messagebox.showwarning("Error", "Correo o contraseña incorrectos.")
        else:
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")

    # Método para ir a la pantalla de registro
    def ir_a_registro(self):
        self.controller.mostrar_pantalla(PantallaRegistro)

    # Método para manejar la recuperación de contraseña
    def recuperar_contraseña(self):
        correo = self.entrada_correo.get()

        if correo:
            # Verificar si el correo existe en la base de datos
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
            usuario = cursor.fetchone()
            conexion.close()

            if usuario:
                # Generar un código de verificación y enviarlo por correo
                codigo_verificacion = str(random.randint(100000, 999999))
                self.enviar_codigo_verificacion(correo, codigo_verificacion)

                # Mostrar ventana emergente para ingresar el código y restablecer la contraseña
                self.mostrar_ventana_recuperacion(correo, codigo_verificacion)
            else:
                messagebox.showerror("Error", "El correo no está registrado.")
        else:
            messagebox.showwarning("Error", "Por favor, ingresa tu correo.")

    # Método para mostrar la ventana de recuperación de contraseña
    def mostrar_ventana_recuperacion(self, correo, codigo_verificacion):
        ventana_recuperacion = tk.Toplevel(self)
        ventana_recuperacion.title("Recuperar Contraseña")

        label = tk.Label(ventana_recuperacion, text="Ingresa el código de verificación enviado a tu correo")
        label.pack(pady=10)

        entrada_codigo = tk.Entry(ventana_recuperacion)
        entrada_codigo.pack()

        label_nueva_contraseña = tk.Label(ventana_recuperacion, text="Nueva contraseña:")
        label_nueva_contraseña.pack(pady=10)

        entrada_nueva_contraseña = tk.Entry(ventana_recuperacion, show="*")
        entrada_nueva_contraseña.pack()

        boton_restaurar = tk.Button(ventana_recuperacion, text="Restaurar contraseña",
                                    command=lambda: self.restablecer_contraseña(entrada_codigo.get(), codigo_verificacion,
                                                                                correo, entrada_nueva_contraseña.get(),
                                                                                ventana_recuperacion))
        boton_restaurar.pack(pady=10)

    # Método para restablecer la contraseña
    def restablecer_contraseña(self, codigo_ingresado, codigo_correcto, correo, nueva_contraseña, ventana):
        if codigo_ingresado == codigo_correcto and nueva_contraseña:
            # Actualizar la contraseña en la base de datos
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("UPDATE usuarios SET contraseña = %s WHERE correo = %s", (nueva_contraseña, correo))
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", "Contraseña restablecida correctamente.")
            ventana.destroy()  # Cerrar la ventana de recuperación
        else:
            messagebox.showerror("Error", "Código incorrecto o contraseña vacía.")

    def enviar_codigo_verificacion(self, correo, codigo):
        try:
            servidor = smtplib.SMTP("smtp.gmail.com", 587)
            servidor.starttls()
            servidor.login("emanuelvillalobos546@gmail.com", "xzkstdyilfsarrdz")
            
            # Codificar el mensaje en UTF-8
            mensaje = f"Tu código de verificación es: {codigo}".encode('utf-8')
            
            servidor.sendmail("emanuelvillalobos546@gmail.com", correo, mensaje)
            servidor.quit()
            messagebox.showinfo("Correo enviado", f"Se ha enviado un código de verificación a {correo}.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el correo. {str(e)}")

# Pantalla Principal
class PantallaPrincipal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label_bienvenida = tk.Label(self, text="", font=("Helvetica", 18))
        self.label_bienvenida.pack(pady=10)

        # Botón para editar perfil
        boton_editar = tk.Button(self, text="Editar Perfil", command=lambda: controller.mostrar_pantalla(PantallaEditarPerfil))
        boton_editar.pack()

        # Método para actualizar el saludo con el nombre del usuario
    def actualizar_bienvenida(self, nombre_usuario):
        self.label_bienvenida.config(text=f"Bienvenido {nombre_usuario}")

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
# Pantalla Editar Perfil (sólo cambio de contraseña)
class PantallaEditarPerfil(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Etiqueta para título
        label = tk.Label(self, text="Cambiar Contraseña", font=("Helvetica", 18))
        label.pack(pady=10)

        # Entrada para contraseña actual
        tk.Label(self, text="Contraseña actual").pack()
        self.entrada_contraseña_actual = tk.Entry(self, show="*")
        self.entrada_contraseña_actual.pack()

        # Entrada para nueva contraseña
        tk.Label(self, text="Nueva contraseña").pack()
        self.entrada_nueva_contraseña = tk.Entry(self, show="*")
        self.entrada_nueva_contraseña.pack()

        # Botón para cambiar contraseña
        boton_cambiar = tk.Button(self, text="Cambiar Contraseña", command=self.cambiar_contraseña)
        boton_cambiar.pack(pady=10)

    # Método para cambiar contraseña
    def cambiar_contraseña(self):
        contraseña_actual = self.entrada_contraseña_actual.get()
        nueva_contraseña = self.entrada_nueva_contraseña.get()

        if contraseña_actual and nueva_contraseña:
            # Obtenemos el correo del usuario actual desde la sesión o base de datos
            correo_usuario = self.controller.correo_usuario_actual

            # Conectamos a la base de datos y verificamos la contraseña actual
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("SELECT contraseña FROM usuarios WHERE correo = %s", (correo_usuario,))
            resultado = cursor.fetchone()

            if resultado and resultado[0] == contraseña_actual:
                # Actualizamos la contraseña en la base de datos
                cursor.execute("UPDATE usuarios SET contraseña = %s WHERE correo = %s", (nueva_contraseña, correo_usuario))
                conexion.commit()
                conexion.close()

                # Enviar correo de confirmación
                self.enviar_correo_confirmacion(correo_usuario)

                messagebox.showinfo("Éxito", "Tu contraseña ha sido cambiada exitosamente.")
                self.controller.mostrar_pantalla(PantallaPrincipal)
            else:
                messagebox.showwarning("Error", "La contraseña actual no es correcta.")
        else:
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")

    # Método para enviar correo de confirmación
    def enviar_correo_confirmacion(self, correo_usuario):
        asunto = "Cambio de contraseña exitoso"
        mensaje = f"Hola, tu contraseña ha sido cambiada exitosamente. Si no fuiste tú, comunícate con soporte técnico inmediatamente."
        remitente = "emanuelvillalobos546@gmail.com"  # Cambia esto por tu remitente
        destinatario = correo_usuario

        # Configuración del servidor de correo
        msg = MIMEText(mensaje)
        msg['Subject'] = asunto
        msg['From'] = remitente
        msg['To'] = destinatario

        # Enviar el correo
        try:
            servidor = smtplib.SMTP('smtp.gmail.com', 587)
            servidor.starttls()
            servidor.login(remitente, "xzkstdyilfsarrdz")  # Contraseña de prueba del remitente
            servidor.sendmail(remitente, destinatario, msg.as_string())
            servidor.quit()
        except Exception as e:
            print(f"Error al enviar el correo: {e}")

# Modificación en el controlador para guardar el correo del usuario que ha iniciado sesión
class ControladorApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Aquí guardamos el correo del usuario que inició sesión
        self.correo_usuario_actual = None

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (PantallaLogin, PantallaPrincipal, PantallaEditarPerfil, PantallaRegistro, PantallaOlvideContraseña):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_pantalla(PantallaLogin)

    def mostrar_pantalla(self, contenedor):
        frame = self.frames[contenedor]
        frame.tkraise()

# Ejecución de la aplicación
if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
