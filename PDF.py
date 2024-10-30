from fpdf import FPDF
import Conexio

class PDF(FPDF):

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Pàgina {self.page_no()}', 0, 0, 'C')

def generar_informe_pdf():
    connection = Conexio.connectar_bbdd()  # Es connecta a la base de dades.
    if connection:  # Si la connexió té èxit:
        cursor = connection.cursor()  # Crea un cursor per executar consultes SQL.
        cursor.execute("SELECT producte, quantitat, preu, data_venda FROM vendes")
        files = cursor.fetchall()  # Reculleix totes les files retornades per la consulta.
        cursor.close()  # Tanca el cursor.
        connection.close()  # Tanca la connexió amb la base de dades.

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Informe de Vendes", ln=True, align='C')
        pdf.ln(10)

        # Afegim la capçalera de la taula
        pdf.set_font("Arial", 'B', size=10)
        pdf.cell(50, 10, txt="Producte", border=1)
        pdf.cell(30, 10, txt="Quantitat", border=1)
        pdf.cell(40, 10, txt="Preu", border=1)
        pdf.cell(50, 10, txt="Data de Venda", border=1)
        pdf.ln()

        # Afegim les files de la taula
        pdf.set_font("Arial", size=10)
        for fila in files:
            pdf.cell(50, 10, txt=str(fila[0]), border=1)
            pdf.cell(30, 10, txt=str(fila[1]), border=1)
            pdf.cell(40, 10, txt=str(fila[2]), border=1)
            pdf.cell(50, 10, txt=str(fila[3]), border=1)
            pdf.ln()

        # Guardem el fitxer PDF
        pdf.output("informe_vendes.pdf")