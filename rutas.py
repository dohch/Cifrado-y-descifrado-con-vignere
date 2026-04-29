import math
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

# --- CONFIGURACIÓN DE ESTÉTICA ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class CifradorPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cifrador por Rutas Multi-Algoritmo (Mejorado)")
        self.geometry("900x780")
        self.configure(fg_color="#8FBC8F") 

        # Título
        self.lbl_titulo = ctk.CTkLabel(self, text="SISTEMA DE CIFRADO POR TRASPOSICIÓN", 
                                       font=("Courier New", 22, "bold"), text_color="#1B3022")
        self.lbl_titulo.pack(pady=15)

        # --- SECCIÓN ENTRADA ---
        self.frame_entrada_main = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_entrada_main.pack(padx=30, fill="x")
        
        tk.Label(self.frame_entrada_main, text="MENSAJE (ENTRADA):", bg="#8FBC8F", fg="black", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w")
        
        self.txt_entrada = ctk.CTkTextbox(self.frame_entrada_main, height=120, width=650, corner_radius=15, border_width=2, 
                                          fg_color="#1A1A1A", text_color="#00FF00", font=("Consolas", 14))
        self.txt_entrada.grid(row=1, column=0, pady=5)

        # Botones laterales entrada
        self.frame_util_ent = ctk.CTkFrame(self.frame_entrada_main, fg_color="transparent")
        self.frame_util_ent.grid(row=1, column=1, padx=10)
        
        self.btn_copy_ent = self.crear_boton_util(self.frame_util_ent, "📄 Copiar", lambda: self.copiar(self.txt_entrada))
        self.btn_paste_ent = self.crear_boton_util(self.frame_util_ent, "📋 Pegar", lambda: self.pegar(self.txt_entrada))
        self.btn_del_ent = self.crear_boton_util(self.frame_util_ent, "🗑️ Eliminar", lambda: self.eliminar(self.txt_entrada), hover="#E57373")

        # --- SECCIÓN CONFIGURACIÓN ---
        self.frame_config = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_config.pack(padx=30, fill="x", pady=15)

        self.lbl_clave = ctk.CTkLabel(self.frame_config, text="CLAVE (COLS):", text_color="black", font=("Arial", 11, "bold"))
        self.lbl_clave.grid(row=0, column=0, padx=10, sticky="w")
        self.entry_clave = ctk.CTkEntry(self.frame_config, width=80, corner_radius=10, fg_color="white", text_color="black")
        self.entry_clave.insert(0, "4")
        self.entry_clave.grid(row=1, column=0, padx=10, pady=5)

        self.lbl_ruta = ctk.CTkLabel(self.frame_config, text="RUTA DE LECTURA:", text_color="black", font=("Arial", 11, "bold"))
        self.lbl_ruta.grid(row=0, column=1, padx=20, sticky="w")
        self.combo_ruta = ctk.CTkComboBox(self.frame_config, width=350, corner_radius=10,
                                          values=["1. Columnas (Abajo)", "2. Columnas (Arriba)", "3. Filas (Izq-Der)", 
                                                  "4. Filas (Der-Izq)", "5. Zigzag / Serpentina", "6. Espiral (Horario)", 
                                                  "7. Espiral (Anti-horario)", "8. Diagonal"])
        self.combo_ruta.set("5. Zigzag / Serpentina")
        self.combo_ruta.grid(row=1, column=1, padx=20, pady=5)

        # --- BOTONES DE MADERA (ACCIONES PRINCIPALES) ---
        self.frame_btns = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_btns.pack(pady=10)

        self.btn_cifrar = ctk.CTkButton(self.frame_btns, text="🔒 Cifrar", corner_radius=15, fg_color="#5D4037", hover_color="#3E2723", 
                                        font=("Arial", 16, "bold"), height=50, width=180, command=self.ejecutar_cifrado)
        self.btn_cifrar.pack(side="left", padx=15)

        self.btn_descifrar = ctk.CTkButton(self.frame_btns, text="🔓 Descifrar", corner_radius=15, fg_color="#5D4037", hover_color="#3E2723", 
                                           font=("Arial", 16, "bold"), height=50, width=180, command=self.ejecutar_descifrado)
        self.btn_descifrar.pack(side="left", padx=15)

        # --- SECCIÓN SALIDA ---
        self.frame_salida_main = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_salida_main.pack(padx=30, fill="x", pady=10)

        tk.Label(self.frame_salida_main, text="RESULTADO / SALIDA:", bg="#8FBC8F", fg="black", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w")
        
        self.txt_salida = ctk.CTkTextbox(self.frame_salida_main, height=150, width=650, corner_radius=15, border_width=2,
                                         fg_color="#0A1F0A", text_color="#00FF00", font=("Consolas", 16))
        self.txt_salida.grid(row=1, column=0, pady=5)

        # Botones laterales salida
        self.frame_util_sal = ctk.CTkFrame(self.frame_salida_main, fg_color="transparent")
        self.frame_util_sal.grid(row=1, column=1, padx=10)
        
        self.btn_copy_sal = self.crear_boton_util(self.frame_util_sal, "📄 Copiar", lambda: self.copiar(self.txt_salida))
        self.btn_paste_sal = self.crear_boton_util(self.frame_util_sal, "📋 Pegar", lambda: self.pegar(self.txt_salida))
        self.btn_del_sal = self.crear_boton_util(self.frame_util_sal, "🗑️ Eliminar", lambda: self.eliminar(self.txt_salida), hover="#E57373")

    # --- FUNCIONES DE INTERFAZ ---
    def crear_boton_util(self, parent, texto, comando, hover="#909090"):
        btn = ctk.CTkButton(parent, text=texto, width=100, height=32, fg_color="#B0B0B0", 
                            text_color="black", hover_color=hover, command=comando)
        btn.pack(pady=3)
        return btn

    def copiar(self, widget):
        contenido = widget.get("1.0", "end-1c")
        if contenido.strip():
            self.clipboard_clear()
            self.clipboard_append(contenido)
            messagebox.showinfo("Copiado", "Texto en el portapapeles.")

    def pegar(self, widget):
        try:
            texto = self.clipboard_get()
            widget.insert(tk.INSERT, texto)
        except:
            messagebox.showwarning("Aviso", "El portapapeles está vacío.")

    def eliminar(self, widget):
        widget.delete("1.0", "end")

    # --- MOTOR LÓGICO ---
    def aplicar_reglas(self, texto):
        texto = texto.upper()
        reemplazos = {'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ü': 'U'}
        for t, s in reemplazos.items(): texto = texto.replace(t, s)
        valido = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789"
        return "".join([c for c in texto if c in valido])

    def obtener_coordenadas(self, filas, columnas, ruta):
        coords = []
        if "1. Columnas (Abajo)" in ruta:
            for c in range(columnas):
                for f in range(filas): coords.append((f, c))
        elif "2. Columnas (Arriba)" in ruta:
            for c in range(columnas):
                for f in range(filas-1, -1, -1): coords.append((f, c))
        elif "3. Filas (Izq-Der)" in ruta:
            for f in range(filas):
                for c in range(columnas): coords.append((f, c))
        elif "4. Filas (Der-Izq)" in ruta:
            for f in range(filas):
                for c in range(columnas-1, -1, -1): coords.append((f, c))
        elif "5. Zigzag / Serpentina" in ruta:
            for f in range(filas):
                r = range(columnas) if f % 2 == 0 else range(columnas-1, -1, -1)
                for c in r: coords.append((f, c))
        elif "6. Espiral (Horario)" in ruta:
            t, b, l, r = 0, filas-1, 0, columnas-1
            while t <= b and l <= r:
                for i in range(l, r+1): coords.append((t, i))
                t += 1
                for i in range(t, b+1): coords.append((i, r))
                r -= 1
                if t <= b:
                    for i in range(r, l-1, -1): coords.append((b, i))
                    b -= 1
                if l <= r:
                    for i in range(b, t-1, -1): coords.append((i, l))
                    l += 1
        elif "7. Espiral (Anti-horario)" in ruta:
            t, b, l, r = 0, filas-1, 0, columnas-1
            while t <= b and l <= r:
                for i in range(t, b+1): coords.append((i, l))
                l += 1
                for i in range(l, r+1): coords.append((b, i))
                b -= 1
                if l <= r:
                    for i in range(b, t-1, -1): coords.append((i, r))
                    r -= 1
                if t <= b:
                    for i in range(r, l-1, -1): coords.append((t, i))
                    t += 1
        elif "8. Diagonal" in ruta:
            for s in range(filas + columnas - 1):
                for c in range(max(0, s - filas + 1), min(s + 1, columnas)):
                    f = s - c
                    if f < filas: coords.append((f, c))
        return coords

    def ejecutar_cifrado(self):
        try:
            clave_val = self.entry_clave.get().strip()
            if not clave_val.isdigit(): raise ValueError
            clave = int(clave_val)
            msj = self.aplicar_reglas(self.txt_entrada.get("1.0", "end-1c"))
            if not msj: return
            filas = math.ceil(len(msj) / clave)
            msj += "X" * (filas * clave - len(msj))
            matriz = [list(msj[i:i+clave]) for i in range(0, len(msj), clave)]
            orden = self.obtener_coordenadas(filas, clave, self.combo_ruta.get())
            res = "".join([matriz[f][c] for f, c in orden])
            self.txt_salida.delete("1.0", "end")
            self.txt_salida.insert("1.0", res)
        except:
            messagebox.showerror("Error", "Revisa la clave (debe ser número entero).")

    def ejecutar_descifrado(self):
        try:
            clave_val = self.entry_clave.get().strip()
            if not clave_val.isdigit(): raise ValueError
            clave = int(clave_val)
            cifrado = self.txt_entrada.get("1.0", "end-1c").replace(" ", "").replace("\n", "")
            if not cifrado: return
            filas = len(cifrado) // clave
            matriz = [['' for _ in range(clave)] for _ in range(filas)]
            orden = self.obtener_coordenadas(filas, clave, self.combo_ruta.get())
            for i, (f, c) in enumerate(orden): matriz[f][c] = cifrado[i]
            res = "".join(["".join(fila) for fila in matriz])
            self.txt_salida.delete("1.0", "end")
            self.txt_salida.insert("1.0", res)
        except:
            messagebox.showerror("Error", "Error al descifrar. Revisa los datos de entrada.")

if __name__ == "__main__":
    app = CifradorPro()
    app.mainloop()