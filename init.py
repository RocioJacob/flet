import fpdf
# Importamos Flet
import flet as ft
# Subclase de FPDF para personalizar encabezado y pie de página
class PDF(fpdf.FPDF):
    def header(self):
        # Agregar imagen (x=10, y=8, ancho=30)
        self.image("assets/RJ.png", 10, 8, 30)
        self.set_font("Arial", "B", 12)
        # Título centrado
        self.cell(0, 10, "Datos del Formulario", border=0, ln=True, align="C")
        self.ln(10)  # Salto de línea debajo del encabezado

    def footer(self):
        # Posición a 1.5 cm del final
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, "Autor: Rocio Jacob", 0, 0, "C")

# Creamos una clase para el formulario
class FormularioApp:
    def __init__(self):
        # Campos de texto para que el usuario ingrese datos
        self.nombre = ft.TextField(label="Nombre", border_color="orange", width=300)
        self.apellido = ft.TextField(label="Apellido", border_color="orange", width=300)
        self.correo = ft.TextField(label="Correo", border_color="orange", width=300)
        self.contraseña = ft.TextField(label="Contraseña", border_color="orange", width=300, password=True, can_reveal_password=True)

        # Texto donde se mostrará el resultado
        self.resultado = ft.Text(value="", size=16)

    # Función que se ejecuta cuando se presiona el botón "Enviar"
    def enviar_datos(self, e):
        # Tomamos los valores de los campos y los mostramos en self.resultado
        self.resultado.value = (
            f"Nombre: {self.nombre.value}\n"
            f"Apellido: {self.apellido.value}\n"
            f"Correo: {self.correo.value}\n"
            f"Contraseña: {self.contraseña.value}"
        )
        # Actualizamos la página para que se vea el cambio
        self.page.update()
 # Función que se ejecuta cuando se presiona el botón "Enviar"
    def enviar_datos(self, e):
        self.resultado.value = f"Nombre: {self.nombre.value}\nApellido: {self.apellido.value}\nCorreo: {self.correo.value}\nContraseña: {self.contraseña.value}"
        self.page.update()

# Función para generar el PDF, ahora como parte de la clase principal
    def generar_pdf(self, e):
        # Se verifica si los campos están vacíos para no generar un PDF con datos nulos
        if not self.nombre.value or not self.apellido.value or not self.correo.value or not self.contraseña.value:
            self.resultado.value = "Por favor, completa todos los campos antes de generar el PDF."
            self.page.update()
            return # Detiene la ejecución si los campos están vacíos

        pdf = PDF()                             # Usamos la subclase personalizada
        pdf.add_page()                          # Agregamos una página
        pdf.set_font("Arial", size=12)          # Fuente y tamaño

        # Agregamos los datos del formulario al PDF
        pdf.cell(200, 10, txt=f"Nombre: {self.nombre.value}", ln=True)
        pdf.cell(200, 10, txt=f"Apellido: {self.apellido.value}", ln=True)
        pdf.cell(200, 10, txt=f"Correo: {self.correo.value}", ln=True)
        pdf.cell(200, 10, txt=f"Contraseña: {self.contraseña.value}", ln=True)

        # Guardamos el PDF
        pdf.output("datos_formulario.pdf")
        self.resultado.value = "PDF generado con éxito: datos_formulario.pdf"
        self.page.update()


    # Función principal que crea la interfaz
    def main(self, page: ft.Page):
        self.page = page                            # Guardamos la referencia a la página
        self.page.title = "Formulario Básico con Flet"
        self.page.bgcolor = "white"                 # Fondo blanco
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Botón que ejecuta enviar_datos cuando se hace clic
        boton_enviar = ft.ElevatedButton(text="Enviar", bgcolor="orange", color="white", on_click=self.enviar_datos)
        #boton para generar PDF
        boton_pdf = ft.ElevatedButton(text="Generar PDF", bgcolor="orange", color="white", on_click=self.generar_pdf)

        # Agregamos todos los elementos a la página en una columna
        self.page.add(
            ft.Column(
                controls=[
                    ft.Image(src="/logo.png", width=300, height=300), #agregamos una imagen de logo
                    self.nombre,
                    self.apellido,
                    self.correo,
                    self.contraseña,
                    boton_enviar,
                    boton_pdf,
                    self.resultado
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )


# Arrancamos la aplicación en el navegador
if __name__ == "__main__":
    app = FormularioApp()
    ft.app(target=app.main, view=ft.WEB_BROWSER, assets_dir="assets")