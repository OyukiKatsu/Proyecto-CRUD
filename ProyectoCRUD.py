import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Alumno:
    def __init__(self, nombre, apellido1, apellido2, edad, direccion, telefono, clase):
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.edad = edad
        self.direccion = direccion
        self.telefono = telefono
        self.clase = clase

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Alumnos")
        self.root.geometry("1000x600")
        self.root.configure(bg="white")
        
        self.clases = []

        self.frame_menu = tk.Frame(self.root, bg="lightgray", height=50)
        self.frame_menu.pack(fill=tk.X)

        self.boton_crear = tk.Button(self.frame_menu, text="Crear", command=self.mostrar_crear)
        self.boton_crear.pack(side=tk.LEFT, padx=5, pady=5)
        self.boton_lista = tk.Button(self.frame_menu, text="Lista", command=self.mostrar_lista)
        self.boton_lista.pack(side=tk.LEFT, padx=5, pady=5)
        self.boton_alumno = tk.Button(self.frame_menu, text="Alumno", command=self.mostrar_alumno)
        self.boton_alumno.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.boton_borrar_bd = tk.Button(self.frame_menu, text="Borrar base de datos", command=self.borrar_base_datos)
        self.boton_borrar_bd.pack(side=tk.LEFT, padx=5, pady=5)

        self.frame_logs = tk.Frame(self.root, bg="white", width=600)
        self.frame_logs.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
        self.texto_logs = tk.Text(self.frame_logs, state='disabled', bg="white", fg="black")
        self.texto_logs.pack(fill=tk.BOTH, expand=True)

        self.frame_principal = tk.Frame(self.root, bg="white", width=400)
        self.frame_principal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.crear_base_datos()
        self.cargar_clases()

    def crear_base_datos(self):
        conexion = sqlite3.connect("alumnos.db")
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alumnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido1 TEXT NOT NULL,
                apellido2 TEXT NOT NULL,
                edad INTEGER NOT NULL,
                direccion TEXT NOT NULL,
                telefono TEXT NOT NULL,
                clase TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE
            )
        ''')
        conexion.commit()
        conexion.close()

    def cargar_clases(self):
        conexion = sqlite3.connect("alumnos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM clases")
        self.clases = [fila[0] for fila in cursor.fetchall()]
        conexion.close()


        # Función para mostrar un mensajes en la parte derecha de la applicación
    def log(self, mensaje):
        self.texto_logs.config(state='normal')
        self.texto_logs.delete(1.0, tk.END)
        self.texto_logs.insert(tk.END, mensaje + "\n")
        self.texto_logs.config(state='disabled')

       #Funciones llamadas por pulsadores
       #    |
       #    |
       #    V   
    def mostrar_crear(self):
        self.limpiar_frame_principal()

        tk.Label(self.frame_principal, text="Nombre:", anchor="w", justify="left").grid(row=0, column=0, sticky="w")
        self.nombre_entry = tk.Entry(self.frame_principal)
        self.nombre_entry.grid(row=0, column=1, sticky="w")

        tk.Label(self.frame_principal, text="Primer apellido:", anchor="w", justify="left").grid(row=1, column=0, sticky="w")
        self.apellido1_entry = tk.Entry(self.frame_principal)
        self.apellido1_entry.grid(row=1, column=1, sticky="w")

        tk.Label(self.frame_principal, text="Segundo apellido:", anchor="w", justify="left").grid(row=2, column=0, sticky="w")
        self.apellido2_entry = tk.Entry(self.frame_principal)
        self.apellido2_entry.grid(row=2, column=1, sticky="w")

        tk.Label(self.frame_principal, text="Edad:", anchor="w", justify="left").grid(row=3, column=0, sticky="w")
        self.edad_entry = tk.Entry(self.frame_principal)
        self.edad_entry.grid(row=3, column=1, sticky="w")

        tk.Label(self.frame_principal, text="Dirección:", anchor="w", justify="left").grid(row=4, column=0, sticky="w")
        self.direccion_entry = tk.Entry(self.frame_principal)
        self.direccion_entry.grid(row=4, column=1, sticky="w")

        tk.Label(self.frame_principal, text="Teléfono:", anchor="w", justify="left").grid(row=5, column=0, sticky="w")
        self.telefono_entry = tk.Entry(self.frame_principal)
        self.telefono_entry.grid(row=5, column=1, sticky="w")

        tk.Label(self.frame_principal, text="Clase:", anchor="w", justify="left").grid(row=6, column=0, sticky="w")
        self.clase_combobox = ttk.Combobox(self.frame_principal, values=self.clases)
        self.clase_combobox.grid(row=6, column=1, sticky="w")

        tk.Button(self.frame_principal, text="Guardar", command=self.guardar_alumno).grid(row=7, columnspan=2, pady=5)

    def mostrar_lista(self):
        self.texto_logs.config(state='normal')
        self.texto_logs.delete(1.0, tk.END) 
        
        conexion = sqlite3.connect("alumnos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM alumnos ORDER BY clase")
        alumnos = cursor.fetchall()
        
        if alumnos:
            for alumno in alumnos:
                info = f"Nombre: {alumno[1]} \n     Apellido: {alumno[2]} {alumno[3]}\n     Edad: {alumno[4]}\n     Dirección: {alumno[5]}\n     Teléfono: {alumno[6]}\n     Clase: {alumno[7]}\n"
                self.texto_logs.insert(tk.END, info)
        else:
            self.texto_logs.insert(tk.END, "No hay alumnos registrados.\n")
        
        self.texto_logs.config(state='disabled')
        conexion.close()

    def mostrar_alumno(self):
        self.limpiar_frame_principal()

        
        conexion = sqlite3.connect("alumnos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM alumnos")
        alumnos = cursor.fetchall()
        conexion.close()
#######################################################################################################
        nombres = [f"{a[1]} {a[2]} {a[3]} - Clase: {a[7]} - id: {a[0]}" for a in alumnos]
        self.alumno_combobox = ttk.Combobox(self.frame_principal, values=nombres)
        self.alumno_combobox.grid(row=0, column=0, columnspan=2, pady=5)
        self.alumno_combobox.bind("<<ComboboxSelected>>", self.cargar_alumno)

        
        self.mostrar_campos_editar()

    def mostrar_campos_editar(self):
        tk.Label(self.frame_principal, text="Nombre:", anchor="w", justify="left").grid(row=1, column=0, sticky="w")
        self.nombre_entry = tk.Entry(self.frame_principal)
        self.nombre_entry.grid(row=1, column=1, sticky="w")

        tk.Label(self.frame_principal, text="Primer apellido:", anchor="w", justify="left").grid(row=2, column=0, sticky="w")
        self.apellido1_entry = tk.Entry(self.frame_principal)
        self.apellido1_entry.grid(row=2, column=1, sticky="w")

        tk.Label(self.frame_principal, text="Segundo apellido:", anchor="w", justify="left").grid(row=3, column=0, sticky="w")
        self.apellido2_entry = tk.Entry(self.frame_principal)
        self.apellido2_entry.grid(row=3, column=1, sticky="w")

        tk.Label(self.frame_principal, text="Edad:", anchor="w", justify="left").grid(row=4, column=0, sticky="w")
        self.edad_entry = tk.Entry(self.frame_principal)
        self.edad_entry.grid(row=4, column=1, sticky="w")

        tk.Label(self.frame_principal, text="Dirección:", anchor="w", justify="left").grid(row=5, column=0, sticky="w")
        self.direccion_entry = tk.Entry(self.frame_principal)
        self.direccion_entry.grid(row=5, column=1, sticky="w")

        tk.Label(self.frame_principal, text="Teléfono:", anchor="w", justify="left").grid(row=6, column=0, sticky="w")
        self.telefono_entry = tk.Entry(self.frame_principal)
        self.telefono_entry.grid(row=6, column=1, sticky="w")

        tk.Label(self.frame_principal, text="Clase:", anchor="w", justify="left").grid(row=7, column=0, sticky="w")
        self.clase_combobox = ttk.Combobox(self.frame_principal, values=self.clases)
        self.clase_combobox.grid(row=7, column=1, sticky="w")

        tk.Button(self.frame_principal, text="Actualizar", command=self.actualizar_alumno).grid(row=8, column=0, pady=5)
        tk.Button(self.frame_principal, text="Eliminar", command=self.eliminar_alumno).grid(row=8, column=1, pady=5)

    def cargar_alumno(self, event):

        texto_alumno = self.alumno_combobox.get()
        

        alumno_id = texto_alumno.split(" - id: ")[-1]
        
        conexion = sqlite3.connect("alumnos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM alumnos WHERE id=?", (alumno_id,))
        alumno = cursor.fetchone()
        conexion.close()

        if alumno:
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, alumno[1])
            self.apellido1_entry.delete(0, tk.END)
            self.apellido1_entry.insert(0, alumno[2])
            self.apellido2_entry.delete(0, tk.END)
            self.apellido2_entry.insert(0, alumno[3])
            self.edad_entry.delete(0, tk.END)
            self.edad_entry.insert(0, alumno[4])
            self.direccion_entry.delete(0, tk.END)
            self.direccion_entry.insert(0, alumno[5])
            self.telefono_entry.delete(0, tk.END)
            self.telefono_entry.insert(0, alumno[6])
            self.clase_combobox.set(alumno[7])

    def guardar_alumno(self):
        nombre = self.nombre_entry.get()
        apellido1 = self.apellido1_entry.get()
        apellido2 = self.apellido2_entry.get()
        edad = self.edad_entry.get()
        direccion = self.direccion_entry.get()
        telefono = self.telefono_entry.get()
        clase = self.clase_combobox.get()

    
        if clase not in self.clases:
            conexion = sqlite3.connect("alumnos.db")
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO clases (nombre) VALUES (?)", (clase,))
            conexion.commit()
            conexion.close()
            self.clases.append(clase) 

        conexion = sqlite3.connect("alumnos.db")
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO alumnos (nombre, apellido1, apellido2, edad, direccion, telefono, clase) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (nombre, apellido1, apellido2, edad, direccion, telefono, clase))
        conexion.commit()
        conexion.close()

        self.log(f"Alumno {nombre} {apellido1} añadido correctamente.")

    def actualizar_alumno(self):

        texto_alumno = self.alumno_combobox.get()
        

        alumno_id = texto_alumno.split(" - id: ")[-1] 

        conexion = sqlite3.connect("alumnos.db")
        cursor = conexion.cursor()
        
        nombre = self.nombre_entry.get()
        apellido1 = self.apellido1_entry.get()
        apellido2 = self.apellido2_entry.get()
        edad = self.edad_entry.get()
        direccion = self.direccion_entry.get()
        telefono = self.telefono_entry.get()
        clase = self.clase_combobox.get()

        cursor.execute("UPDATE alumnos SET nombre=?, apellido1=?, apellido2=?, edad=?, direccion=?, telefono=?, clase=? WHERE id=?",
                    (nombre, apellido1, apellido2, edad, direccion, telefono, clase, alumno_id))
        conexion.commit()
        conexion.close()

        self.log(f"Alumno {nombre} actualizado correctamente.")

    def eliminar_alumno(self):

        texto_alumno = self.alumno_combobox.get()
        

        alumno_id = texto_alumno.split(" - id: ")[-1] 

        conexion = sqlite3.connect("alumnos.db")
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM alumnos WHERE id=?", (alumno_id,))
        conexion.commit()
        conexion.close()

        self.log(f"El alumno ha sido eliminado con éxito.")
        self.mostrar_lista()

    def borrar_base_datos(self):
        conexion = sqlite3.connect("alumnos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM alumnos")
        numero_alumnos = cursor.fetchone()[0]
        conexion.close()

        if numero_alumnos > 0:
            
            respuesta = messagebox.askyesno("Confirmar eliminación", f"Se borrarán {numero_alumnos} alumnos. ¿Estás seguro que deseas eliminar?")
            if respuesta:
                conexion = sqlite3.connect("alumnos.db")
                cursor = conexion.cursor()
                cursor.execute("DROP TABLE IF EXISTS alumnos")
                cursor.execute("DROP TABLE IF EXISTS clases")
                conexion.commit()
                conexion.close()
                self.log("La base de datos ha sido eliminada exitosamente.")
                self.crear_base_datos()  
        else:
            messagebox.showinfo("Información", "No hay alumnos registrados en la base de datos.")

    def limpiar_frame_principal(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
