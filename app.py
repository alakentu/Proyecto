# Importamos las librerías necesarias para la aplicación
# # Librería principal de Flask
# # Extensión de Flask para manejar sesiones
# # Librería para generar PDF
# # Librería para manejar fechas
# # Librería para manejar formatos de fecha
# # Librería para manejar directorios
from flask import Flask, request, Response, render_template, flash, redirect, url_for, session
from flask_session import Session
from fpdf import FPDF
from datetime import datetime
import locale

# Creamos una instancia de Flask y le indicamos la carpeta de templates
# Configuracion de la sesión, almacenamiento de sesiones en disco y clave secreta
app = Flask(__name__, template_folder='templates')
app.config["SECRET_KEY"] = b'_5#y2L"Q5X7z\n\xec]/'
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'

app.debug = True
app.secret_key = b'_5#y2L"Q5X7z\n\xec]/'

Session(app)

# Creamos la clase para los PDF
class PDF(FPDF):
    # Cabecera del documento PDF
    def header(self):
        """Función que se ejecuta al inicio de la creación del PDF, se encarga de
        imprimir la cabecera con el logo de la universidad
        """
        self.image('static/images/logo_120.jpg', 5, 5, 28)  # Imprimimos el logo
        self.set_font('Arial', 'B', 10)  # Fuente y tamaño del título
        self.cell(0, 6, 'REPÚBLICA BOLIVARAIANA DE VENEZUELA', 0, 1, 'C')
        self.cell(0, 6, 'MINISTERIO DEL PODER POPULAR PARA LA EDUCACIÓN UNIVERSITARIA', 0, 1, 'C')
        self.cell(0, 6, 'UNIVERSIDAD NACIONAL EXPERIMENTAL DE LA GRAN CARACAS', 0, 1, 'C')
        self.cell(0, 6, '"UNEXCA"', 0, 1, 'C')
        self.ln(30)  # Salto de línea

    # Pie de página del documento PDF
    def footer(self):
        """Función que se ejecuta al final de la creación del PDF, se encarga de
        imprimir el pie de página con información de la universidad
        """
        self.set_y(-25)  # Indicamos la posición donde se va a imprimir
        self.set_font('Arial', '', 8)  # Fuente y tamaño del pie de página
        self.cell(0, 4, 'Esq, Mijares, Av, Oeste 3, Altagracia, Caracas-Venezuela 1010A, Distrito Capital. Correo: cesolicitues.unexca@gmail.com', 0, 1, 'C')
        self.cell(0, 4, 'Teléfono: 0212-850-51-81 Extensión 128. COORDINACIÓN CONTROL DE ESTUDIOS - UNEXCA', 0, 1, 'C')
        self.cell(0, 4, 'RIF G-2001128256', 0, 1, 'C')


# Generamos la constancia
def generate_certificates(names: str, lastnames: str, naciolatity: str, identity_card: str, pnf: str, turn: str, section: str, date_init: str, date_end: str, student_core: str) -> None:
    """Función que genera el PDF con la constancia de estudios

    Parámetros:
    names (str): Nombres del estudiante
    lastnames (str): Apellidos del estudiante
    naciolatity (str): Nacionalidad del estudiante
    identity_card (str): Número de cédula del estudiante
    pnf (str): Programa Nacional de Formación seleccionado
    turn (str): Turno seleccionado
    section (str): Sección seleccionada
    date_init (str): Fecha de inicio del trayecto académico
    date_end (str): Fecha de finalización del trayecto académico
    student_core (str): Núcleo al que pertenece el estudiante

    Retorna:
    None
    """
    # Creamos una instancia de la clase PDF y la guardamos en una variable.
    # Configuracion de la pagina
    pdf = PDF()
    pdf.alias_nb_pages()  # Agregamos el número de páginas al pie de página
    pdf.add_page()  # Agregamos una página al PDF
    pdf.set_left_margin(10)  # Indicamos el margen izquierdo
    pdf.set_right_margin(10)  # Indicamos el margen derecho

    # Fuente y tamaño del título
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'CONSTANCIA DE ESTUDIOS', ln=True, align='C')
    pdf.ln(15)  # Salto de línea

    # Cuerpo de la constancia
    student_name = names + " " + lastnames
    identity_card = naciolatity + "-" + identity_card
    academic_period = date_init.replace("-", "/") + " - " + date_end.replace("-", "/")
    complete_names = names.replace(" ", "_") + "_" + lastnames.replace(" ", "_")
    certificate_name = "constancia_" + complete_names.lower()

    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 10, f"Quien suscribe, Jefe(E) Ing. Yovany Díaz Coordinación Control de Estudios de la UNIVERSIDAD NACIONAL EXPERIMENTAL DE LA GRAN CARACAS, hace constar por medio de la presente que el(la) ciudadano(a) {student_name}, titular de la cédula de identidad N.º {identity_card} es estudiante activo(a) de esta universidad en el núcleo {student_core}, cursando el período académico {academic_period} del Programa Nacional de Formación PNF {pnf}, sección {section}, turno {turn.upper()}.", align='J')
    pdf.ln(10)  # Salto de línea

    # Fecha actual
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Establecemos el locale en español
    certicate_date = datetime.now().strftime("%d de %B de %Y")  # Fecha actual
    pdf.multi_cell(0, 10, f"Constancia que se expide a petición de la parte interesada en Caracas a los {certicate_date}", align='L')

    # Parrafo para la firma del documento
    pdf.ln(20)  # Salto de línea
    pdf.cell(0, 10, "Atentamente,", ln=True, align='C')
    pdf.cell(0, 10, "____________________________", ln=True, align='C')
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "JEFE(E) ING. YOVANY DÍAZ", ln=1, align='C')
    pdf.cell(0, 10, "JEFE(E) COORDINACIÓN CONTROL DE ESTUDIOS", ln=2, align='C')
    pdf.cell(0, 10, f"NÚCLEO - {student_core}", ln=3, align='C')

    pdf.output(f"constancias/{certificate_name}.pdf", "F")

@app.route('/', methods=['GET', 'POST'])  # Definimos la ruta principal de nuestra aplicación
def index():
    # Obtenemos los valores del formulario
    # Inicializamos las variables con valores vacíos
    names = ''
    lastnames = ''
    cdi = ''
    section = ''
    date_init = ''
    date_end = ''

    # Diccionario con las posibles opciones de nacionalidad
    nationalities = {
        'none' : '-- Seleccionar --',
        'V' : 'Venezolano',
        'E' : 'Extranjero'
    }

    # Diccionario con las posibles opciones de PNF
    pnfs = {
        'none' : '-- Seleccionar --',
        'admin' : 'Administración',
        'conta' : 'Contaduría',
        'infor' : 'Informática',
        'tasoc' : 'Trabajo Social',
        'turis' : 'Turismo',
        'dislo' : 'Distribución y Logística'
    }

    # Diccionario con las posibles opciones de turno
    turns = {
        'none' : '-- Seleccionar --',
        'matu' : 'Matutino',
        'vesp' : 'Vespertino',
        'noct' : 'Nocturno'
    }

    # Diccionario con las posibles opciones de núcleo
    cores = {
        'none' : '-- Seleccionar --',
        'altag' : 'ALTAGRACIA',
        'urbin' : 'LA URBINA',
        'flore' : 'LA FLORESTA',
        'caray' : 'CARAYACA/LA GUAIRA',
    }

    # Si se envía el formulario
    if request.method == 'POST':
        # Asignamos los valores recibidos
        names = request.form['names']
        lastnames = request.form['lastnames']
        cdi = request.form['cdi']
        section = request.form['section']
        date_init = request.form['date_init']
        date_end = request.form['date_end']

        selected_nat = request.form.get('nationality')  # Obtenemos la opción seleccionada de nacionalidad
        selected_pnfs = request.form.get('pnfs')  # Obtenemos la opción seleccionada de PNF
        selected_turns = request.form.get('turns')  # Obtenemos la opción seleccionada de turno
        selected_cores = request.form.get('cores')  # Obtenemos la opción seleccionada de núcleo

        # Validamos los campos
        # Si alguna de las opciones está vacía enviaremos un mensaje de error
        if not names:
            flash('Debe ingresar los nombres del/la estudiante!', 'danger')
        elif not lastnames:
            flash('Debe ingresar los apellidos del/la estudiante!', 'danger')
        elif not cdi:
            flash('Debe ingresar el número de cédula del/la estudiante!', 'danger')
        elif not section:
            flash('Debe ingresar su sección del/la estudiante!', 'danger')
        elif not date_init:
            flash('Debe establecer una fecha inicial del trayecto!', 'danger')
        elif not date_end:
            flash('Debe establecer una fecha final del trayecto!', 'danger')
        elif request.form['nationality'] == 'none':
            flash('Debe elegir la nacionalidads del/la estudiante!', 'danger')
        elif request.form['pnfs'] == 'none':
            flash('Debe elegir un PNF!', 'danger')
        elif request.form['turns'] == 'none':
            flash('Debe elegir un turno!', 'danger')
        elif request.form['cores'] == 'none':
            flash('Debe elegir un nucleo!', 'danger')
        else:  # Si todos los campos están correctamente rellenos
            # Generamos la constancia
            # Mostramos un mensaje que indica que la constancia se generó correctamente
            # Redireccionammos a la vista principal
            generate_certificates(names, lastnames, selected_nat, cdi, pnfs[selected_pnfs], turns[selected_turns], section, date_init, date_end, cores[selected_cores])
            flash('Constancia generada correctamente!', 'success')
            return redirect(url_for('index'))

    # Renderizamos la vista principal con los valores de los campos y las opciones de los diccionarios de selección.
    return render_template('index.html', names=names, lastnames=lastnames, cdi=cdi, section=section, date_init=date_init, date_end=date_end, cores=cores, nationalities=nationalities, pnfs=pnfs, turns=turns, selected='none')

# Agrega una condición al final del archivo para asegurarnos de que la aplicación web solo se ejecute,
# si se ejecuta el archivo directamente y no si se importa a otro archivo.
if __name__ == '__main__':
    app.run()