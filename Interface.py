import tkinter as tk  # Importa la llibreria Tkinter per a la interfície gràfica.
from tkinter import ttk, messagebox  # Importa el mòdul ttk per utilitzar widgets avançats com Treeview i messagebox per mostrar avisos.
import Conexio
from PDF import generar_informe_pdf  # Importa la funció generar_informe_pdf del fitxer pdf_generator.py

root = tk.Tk()  # Crea la finestra principal de l'aplicació.
root.title("Gestió de Vendes")

# Etiquetes i caixes de text per inserir informació de la venda.
tk.Label(root, text="Producte").grid(row=0, column=0)  # Etiqueta "Producte" a la fila 0 i columna 0.
entrada_producte = tk.Entry(root)  # Crea un camp d'entrada de text per al producte.
entrada_producte.grid(row=0, column=1)  # Ubica el camp d'entrada a la fila 0 i columna 1.

tk.Label(root, text="Quantitat").grid(row=1, column=0)  # Etiqueta "Quantitat" a la fila 1 i columna 0.
entrada_quantitat = tk.Entry(root)  # Crea un camp d'entrada per la quantitat.
entrada_quantitat.grid(row=1, column=1)  # Ubica el camp d'entrada a la fila 1 i columna 1.

tk.Label(root, text="Preu").grid(row=2, column=0)  # Etiqueta "Preu" a la fila 2 i columna 0.
entrada_preu = tk.Entry(root)  # Crea un camp d'entrada per al preu.
entrada_preu.grid(row=2, column=1)  # Ubica el camp d'entrada a la fila 2 i columna 1.

tk.Label(root, text="Data de Venda").grid(row=3, column=0)  # Etiqueta "Data de Venda" a la fila 3 i columna 0.
entrada_data = tk.Entry(root)  # Crea un camp d'entrada per la data de la venda.
entrada_data.grid(row=3, column=1)  # Ubica el camp d'entrada a la fila 3 i columna 1.

# Taula (Treeview) per mostrar les vendes.
tree = ttk.Treeview(root, columns=("producte", "quantitat", "preu", "data"), show='headings')
tree.heading("producte", text="Producte")  # Defineix el títol de la columna "Producte".
tree.heading("quantitat", text="Quantitat")  # Defineix el títol de la columna "Quantitat".
tree.heading("preu", text="Preu")  # Defineix el títol de la columna "Preu".
tree.heading("data", text="Data de Venda")  # Defineix el títol de la columna "Data de Venda".
tree.grid(row=4, column=0, columnspan=2)  # Ubica la taula a la fila 4 i fa que ocupi dues columnes.

def inserir_venda():
    connection = Conexio.connectar_bbdd()  # Es connecta a la base de dades.
    if connection:  # Si la connexió ha estat exitosa:
        cursor = connection.cursor()  # Crea un cursor per executar consultes SQL.
        query = "INSERT INTO vendes (producte, quantitat, preu, data_venda) VALUES (%s, %s, %s, %s)"  # Consulta SQL.
        dades = (entrada_producte.get(), entrada_quantitat.get(), entrada_preu.get(), entrada_data.get())  # Recullem les dades dels camps d'entrada.
        cursor.execute(query, dades)  # Executem la consulta amb les dades proporcionades.
        connection.commit()  # Guardem els canvis a la base de dades.
        cursor.close()  # Tanquem el cursor.
        connection.close()  # Tanquem la connexió.
        actualitzar_treeview()  # Actualitzem la taula per mostrar les noves dades.

def usar_dades():
    selleccio = tree.selection()
    if selleccio:
        valors = tree.item(selleccio[0], 'values')
        entrada_producte.delete(0, tk.END)
        entrada_producte.insert(0, valors[0])
        entrada_quantitat.delete(0, tk.END)
        entrada_quantitat.insert(0, valors[1])
        entrada_preu.delete(0, tk.END)
        entrada_preu.insert(0, valors[2])
        entrada_data.delete(0, tk.END)
        entrada_data.insert(0, valors[3])
    else:
        messagebox.showwarning("Atenció", "Si us plau, seleccioneu una línia per usar les dades.")


def editar_venda():
    selleccio = tree.selection()
    connection = Conexio.connectar_bbdd()
    if connection:  # Si la connexió ha estat exitosa:
        cursor = connection.cursor()  # Crea un cursor per executar consultes SQL.
        query = "UPDATE vendes SET producte = %s, quantitat = %s, preu = %s, data_venda = %s WHERE producte = %s"
        dades = (entrada_producte.get(), entrada_quantitat.get(), entrada_preu.get(),
                 entrada_data.get(), entrada_producte.get())  # Recullem les dades dels camps d'entrada.
        cursor.execute(query, dades)  # Executem la consulta amb les dades proporcionades.
        connection.commit()  # Guardem els canvis a la base de dades.
        cursor.close()  # Tanquem el cursor.
        connection.close()  # Tanquem la connexió.
        actualitzar_treeview()  # Actualitzem la taula per mostrar les noves dades.

def actualitzar_treeview():
    for fila in tree.get_children():
        tree.delete(fila)  # Elimina totes les files actuals del Treeview per actualitzar les dades.

    connection = Conexio.connectar_bbdd()  # Es connecta a la base de dades MySQL.
    if connection:  # Si la connexió té èxit:
        cursor = connection.cursor()  # Crea un cursor per executar consultes SQL.
        cursor.execute(
            "SELECT producte, quantitat, preu, data_venda FROM vendes")  # Executa una consulta per obtenir totes les vendes.
        files = cursor.fetchall()  # Reculleix totes les files retornades per la consulta.

        # Itera per cada fila obtinguda de la consulta i les insereix al Treeview.
        for fila in files:
            tree.insert("", tk.END, values=fila)  # Insereix les dades al Treeview.

        cursor.close()  # Tanca el cursor.
        connection.close()  # Tanca la connexió amb la base de dades.

def eliminar_vendes():
    connection = Conexio.connectar_bbdd()  # Es connecta a la base de dades.
    selleccio = tree.selection()
    if selleccio:
        valors = tree.item(selleccio[0], 'values')
        if connection:
            cursor = connection.cursor()
            query = "DELETE FROM vendes WHERE producte = %s"
            dades = (valors[0],)  # Usa uma tupla com um único elemento
            cursor.execute(query, dades)
            connection.commit()
            cursor.close()
            connection.close()
            actualitzar_treeview()
    else:
        messagebox.showwarning("Atenció", "Si us plau, seleccioneu una línia per usar les dades.")

# Frame per als botons.
frame_botons = tk.Frame(root)
frame_botons.grid(row=5, column=0, columnspan=2)

# Botons
boto_inserir = tk.Button(frame_botons, text="Inserir Venda", command=inserir_venda)
boto_inserir.pack(side="left", padx=10)

boto_usardades = tk.Button(frame_botons, text="Usar Dades", command=usar_dades)
boto_usardades.pack(side="left", padx=10)

boto_editar = tk.Button(frame_botons, text="Editar Venda", command=editar_venda)
boto_editar.pack(side="left", padx=10)

boto_eliminar = tk.Button(frame_botons, text="Eliminar Vendes", command=eliminar_vendes)
boto_eliminar.pack(side="left", padx=10)

boto_actualitzar = tk.Button(frame_botons, text="Actualitzar", command=actualitzar_treeview)
boto_actualitzar.pack(side="left", padx=10)

boto_pdf = tk.Button(frame_botons, text="Generar Informe PDF", command=generar_informe_pdf)
boto_pdf.pack(side="left", padx=10)


root.mainloop()
