import customtkinter as ctk
import unicodedata
from tkinter import messagebox

class Vigenere37App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURACIÓN DEL ALFABETO (37 CARACTERES) ---
        self.alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789"
        self.char_to_idx = {char: i for i, char in enumerate(self.alphabet)}
        self.idx_to_char = {i: char for i, char in enumerate(self.alphabet)}

        self.title("Vigenère 37 - Cifrador Profesional")
        self.geometry("850x650")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.setup_ui()

    def normalize_text(self, text):
        """Limpia el texto según tus reglas estrictas."""
        # Eliminar tildes
        text = "".join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )
        # Manejo especial de Ñ antes de limpiar otros caracteres
        text = text.upper().replace("Ñ", "§")
        
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
        
        msg = self.normalize_text(raw_message)
        key = self.normalize_text(raw_key)

        if not msg or not key:
            messagebox.showwarning("Atención", "El mensaje y la clave están vacíos o no contienen caracteres válidos.")
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

        self.result_output.delete("1.0", "end")
        self.result_output.insert("1.0", result)

    def create_action_buttons(self, parent, target_widget):
        """Crea la columna de botones Copiar, Pegar, Eliminar."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        
        btn_copy = ctk.CTkButton(frame, text="📄 Copiar", width=80, height=30, 
                                 command=lambda: self.action_copy(target_widget))
        btn_copy.pack(pady=2)
        
        btn_paste = ctk.CTkButton(frame, text="📋 Pegar", width=80, height=30, 
                                  command=lambda: self.action_paste(target_widget))
        btn_paste.pack(pady=2)
        
        btn_delete = ctk.CTkButton(frame, text="🗑️ Eliminar", width=80, height=30, 
                                   fg_color="#A13333", hover_color="#7B2424",
                                   command=lambda: self.action_delete(target_widget))
        btn_delete.pack(pady=2)
        
        return frame

    def setup_ui(self):
        self.label_title = ctk.CTkLabel(self, text="SISTEMA VIGENÈRE EXTENDIDO (A-Z, Ñ, 0-9)", font=("Roboto", 20, "bold"))
        self.label_title.pack(pady=15)

        # --- SECCIÓN ENTRADA ---
        self.frame_in = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_in.pack(padx=20, pady=10, fill="x")
        
        self.label_msg = ctk.CTkLabel(self.frame_in, text="MENSAJE (ENTRADA):", font=("Roboto", 12, "bold"))
        self.label_msg.grid(row=0, column=0, sticky="w")
        
        self.entry_msg = ctk.CTkTextbox(self.frame_in, height=120, width=600, border_width=2)
        self.entry_msg.grid(row=1, column=0, padx=(0, 10))
        
        self.btns_msg = self.create_action_buttons(self.frame_in, self.entry_msg)
        self.btns_msg.grid(row=1, column=1)

        # --- SECCIÓN CLAVE ---
        self.frame_key = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_key.pack(padx=20, pady=10, fill="x")
        
        self.label_key = ctk.CTkLabel(self.frame_key, text="CLAVE:", font=("Roboto", 12, "bold"))
        self.label_key.grid(row=0, column=0, sticky="w")
        
        self.entry_key = ctk.CTkEntry(self.frame_key, width=600, height=35, placeholder_text="Escribe la clave...")
        self.entry_key.grid(row=1, column=0, padx=(0, 10))
        
        self.btns_key = self.create_action_buttons(self.frame_key, self.entry_key)
        self.btns_key.grid(row=1, column=1)

        # --- BOTONES DE ACCIÓN PRINCIPAL ---
        self.btn_main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_main_frame.pack(pady=15)

        self.btn_encrypt = ctk.CTkButton(self.btn_main_frame, text="🔒 CIFRAR", font=("Roboto", 14, "bold"),
                                         width=200, height=45, fg_color="#5d4037", 
                                         command=lambda: self.process_vigenere("encrypt"))
        self.btn_encrypt.grid(row=0, column=0, padx=20)

        self.btn_decrypt = ctk.CTkButton(self.btn_main_frame, text="🔓 DESCIFRAR", font=("Roboto", 14, "bold"),
                                         width=200, height=45, fg_color="#5d4037", 
                                         command=lambda: self.process_vigenere("decrypt"))
        self.btn_decrypt.grid(row=0, column=1, padx=20)

        # --- SECCIÓN SALIDA ---
        self.frame_out = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_out.pack(padx=20, pady=10, fill="x")
        
        self.label_res = ctk.CTkLabel(self.frame_out, text="RESULTADO / SALIDA:", font=("Roboto", 12, "bold"))
        self.label_res.grid(row=0, column=0, sticky="w")
        
        self.result_output = ctk.CTkTextbox(self.frame_out, height=120, width=600, border_width=2, text_color="#00FF00")
        self.result_output.grid(row=1, column=0, padx=(0, 10))
        
        self.btns_out = self.create_action_buttons(self.frame_out, self.result_output)
        self.btns_out.grid(row=1, column=1)

if __name__ == "__main__":
    app = Vigenere37App()
    app.mainloop()