import customtkinter as ctk
import unicodedata
from tkinter import messagebox

class Vigenere37App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURACIÓN DEL ALFABETO (37 CARACTERES) ---
        # El orden es crucial para que los índices no cambien
        self.alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789"
        self.char_to_idx = {char: i for i, char in enumerate(self.alphabet)}
        self.idx_to_char = {i: char for i, char in enumerate(self.alphabet)}

        self.title("Vigenère 37 - Cifrador Profesional")
        self.geometry("850x650")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.setup_ui()

    def normalize_text(self, text):
        """Limpia el texto según tus reglas estrictas sin romper la Ñ."""
        if not text: return ""
        
        # 1. Convertir a mayúsculas primero
        text = text.upper()
        
        # 2. PROTEGER LA Ñ: La cambiamos temporalmente por un símbolo que no esté en el abecedario
        text = text.replace("Ñ", "§")
        
        # 3. ELIMINAR TILDES (Á, É, Í, Ó, Ú)
        text = "".join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )
        
        # 4. RESTAURAR Ñ Y FILTRAR SOLO CARACTERES PERMITIDOS
        result = ""
        for char in text:
            if char == "§":
                result += "Ñ"
            elif char in self.alphabet:
                result += char
        return result

    def action_copy(self, widget):
        content = widget.get("1.0", "end-1c") if isinstance(widget, ctk.CTkTextbox) else widget.get()
        self.clipboard_clear()
        self.clipboard_append(content)
        
    def action_paste(self, widget):
        try:
            text = self.clipboard_get()
            if isinstance(widget, ctk.CTkTextbox):
                widget.insert("end", text)
            else:
                widget.delete(0, "end")
                widget.insert(0, text)
        except:
            pass

    def action_delete(self, widget):
        if isinstance(widget, ctk.CTkTextbox):
            widget.delete("1.0", "end")
        else:
            widget.delete(0, "end")

    def process_vigenere(self, mode):
        raw_message = self.entry_msg.get("1.0", "end-1c")
        raw_key = self.entry_key.get()
        
        # Normalizamos mensaje y clave
        msg = self.normalize_text(raw_message)
        key = self.normalize_text(raw_key)

        if not msg or not key:
            messagebox.showwarning("Atención", "El mensaje o la clave están vacíos tras la limpieza.")
            return

        result = ""
        key_len = len(key)
        n = 37 

        for i in range(len(msg)):
            m_idx = self.char_to_idx[msg[i]]
            k_idx = self.char_to_idx[key[i % key_len]]

            if mode == "encrypt":
                res_idx = (m_idx + k_idx) % n
            else:
                res_idx = (m_idx - k_idx + n) % n
            
            result += self.idx_to_char[res_idx]

        # IMPORTANTE: Para que el descifrado sea exacto al copiar/pegar,
        # actualizamos el cuadro de entrada con el texto ya normalizado.
        if mode == "encrypt":
            self.entry_msg.delete("1.0", "end")
            self.entry_msg.insert("1.0", msg)

        self.result_output.delete("1.0", "end")
        self.result_output.insert("1.0", result)

    def create_action_buttons(self, parent, target_widget):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        ctk.CTkButton(frame, text="📄 Copiar", width=80, height=30, command=lambda: self.action_copy(target_widget)).pack(pady=2)
        ctk.CTkButton(frame, text="📋 Pegar", width=80, height=30, command=lambda: self.action_paste(target_widget)).pack(pady=2)
        ctk.CTkButton(frame, text="🗑️ Eliminar", width=80, height=30, fg_color="#A13333", hover_color="#7B2424", command=lambda: self.action_delete(target_widget)).pack(pady=2)
        return frame

    def setup_ui(self):
        self.label_title = ctk.CTkLabel(self, text="SISTEMA VIGENÈRE EXTENDIDO (A-Z, Ñ, 0-9)", font=("Roboto", 20, "bold"))
        self.label_title.pack(pady=15)

        # Entrada
        self.frame_in = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_in.pack(padx=20, pady=10, fill="x")
        ctk.CTkLabel(self.frame_in, text="MENSAJE (ENTRADA):", font=("Roboto", 12, "bold")).grid(row=0, column=0, sticky="w")
        self.entry_msg = ctk.CTkTextbox(self.frame_in, height=120, width=600, border_width=2)
        self.entry_msg.grid(row=1, column=0, padx=(0, 10))
        self.create_action_buttons(self.frame_in, self.entry_msg).grid(row=1, column=1)

        # Clave
        self.frame_key = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_key.pack(padx=20, pady=10, fill="x")
        ctk.CTkLabel(self.frame_key, text="CLAVE:", font=("Roboto", 12, "bold")).grid(row=0, column=0, sticky="w")
        self.entry_key = ctk.CTkEntry(self.frame_key, width=600, height=35)
        self.entry_key.grid(row=1, column=0, padx=(0, 10))
        self.create_action_buttons(self.frame_key, self.entry_key).grid(row=1, column=1)

        # Botones Cifrar/Descifrar
        self.btn_main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_main_frame.pack(pady=15)
        ctk.CTkButton(self.btn_main_frame, text="🔒 CIFRAR", font=("Roboto", 14, "bold"), width=200, height=45, fg_color="#5d4037", command=lambda: self.process_vigenere("encrypt")).grid(row=0, column=0, padx=20)
        ctk.CTkButton(self.btn_main_frame, text="🔓 DESCIFRAR", font=("Roboto", 14, "bold"), width=200, height=45, fg_color="#5d4037", command=lambda: self.process_vigenere("decrypt")).grid(row=0, column=1, padx=20)

        # Salida
        self.frame_out = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_out.pack(padx=20, pady=10, fill="x")
        ctk.CTkLabel(self.frame_out, text="RESULTADO / SALIDA:", font=("Roboto", 12, "bold")).grid(row=0, column=0, sticky="w")
        self.result_output = ctk.CTkTextbox(self.frame_out, height=120, width=600, border_width=2, text_color="#00FF00")
        self.result_output.grid(row=1, column=0, padx=(0, 10))
        self.create_action_buttons(self.frame_out, self.result_output).grid(row=1, column=1)

if __name__ == "__main__":
    app = Vigenere37App()
    app.mainloop()