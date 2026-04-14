import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

class SAPDataManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Éditeur de Référentiel SAP")
        self.root.geometry("700x600")
        self.root.configure(bg="#f5f5f5")
        
        # Fichier de stockage local
        self.filename = "competences_sap.json"
        self.load_initial_data()
        self.setup_ui()

    def load_initial_data(self):
        # Charge le fichier s'il existe, sinon utilise la base par défaut
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = {
                "Garde d'enfants": {"Techniques": ["Préparer un biberon"], "Humaines": ["Patience"]},
                "ADVD": {"Techniques": ["Aide au transfert"], "Humaines": ["Empathie"]},
                "Employé Familial": {"Techniques": ["Entretien sols"], "Humaines": ["Autonomie"]}
            }

    def setup_ui(self):
        # Style
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12))

        # --- Top Header ---
        header = tk.Frame(self.root, bg="#2c3e50", pady=10)
        header.pack(fill=tk.X)
        tk.Label(header, text="ADMINISTRATION DES COMPÉTENCES SAP", fg="white", bg="#2c3e50", font=("Arial", 12, "bold")).pack()

        # --- Sélection Métier ---
        selection_frame = tk.Frame(self.root, pady=15, bg="#f5f5f5")
        selection_frame.pack(fill=tk.X)
        tk.Label(selection_frame, text="Métier cible :", bg="#f5f5f5").pack(side=tk.LEFT, padx=10)
        self.combo_metier = ttk.Combobox(selection_frame, values=list(self.data.keys()), state="readonly")
        self.combo_metier.pack(side=tk.LEFT, padx=5)
        self.combo_metier.bind("<<ComboboxSelected>>", self.refresh_lists)

        # --- Zone Listes ---
        list_container = tk.Frame(self.root, bg="#f5f5f5")
        list_container.pack(fill=tk.BOTH, expand=True, padx=10)

        # Colonne Techniques
        frame_tech = tk.LabelFrame(list_container, text=" Compétences Techniques ", padx=5, pady=5)
        frame_tech.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.list_tech = tk.Listbox(frame_tech, selectmode=tk.SINGLE, font=("Arial", 16))
        self.list_tech.pack(fill=tk.BOTH, expand=True)
        self.list_tech.bind('<Double-1>', lambda e: self.edit_item("Techniques"))

        # Colonne Humaines
        frame_hum = tk.LabelFrame(list_container, text=" Qualités (Savoir-être) ", padx=5, pady=5)
        frame_hum.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.list_hum = tk.Listbox(frame_hum, selectmode=tk.SINGLE, font=("Arial", 16))
        self.list_hum.pack(fill=tk.BOTH, expand=True)
        self.list_hum.bind('<Double-1>', lambda e: self.edit_item("Humaines"))

        # --- Barre d'actions (Ajouter / Supprimer) ---
        action_frame = tk.Frame(self.root, pady=10, bg="#f5f5f5")
        action_frame.pack(fill=tk.X)

        self.entry_new = tk.Entry(action_frame, font=("Arial", 16))
        self.entry_new.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        tk.Button(action_frame, text="➕ Tech", command=lambda: self.add_item("Techniques"), bg="#d4edda").pack(side=tk.LEFT, padx=2)
        tk.Button(action_frame, text="➕ Hum", command=lambda: self.add_item("Humaines"), bg="#d1ecf1").pack(side=tk.LEFT, padx=2)
        tk.Button(action_frame, text="🗑️ Supprimer", command=self.delete_item, bg="#f8d7da").pack(side=tk.LEFT, padx=10)

        # --- Footer ---
        footer = tk.Frame(self.root, pady=10, bg="#f5f5f5")
        footer.pack(fill=tk.X)
        tk.Label(footer, text="Double-cliquez sur un élément pour le modifier", font=("Arial", 8, "italic"), bg="#f5f5f5").pack()
        tk.Button(footer, text="💾 SAUVEGARDER & EXPORTER JSON", command=self.save_and_export, bg="#27ae60", fg="white", font=("Arial", 10, "bold"), pady=5).pack(pady=5)

    def refresh_lists(self, event=None):
        metier = self.combo_metier.get()
        self.list_tech.delete(0, tk.END)
        self.list_hum.delete(0, tk.END)
        if metier in self.data:
            for item in self.data[metier]["Techniques"]: self.list_tech.insert(tk.END, item)
            for item in self.data[metier]["Humaines"]: self.list_hum.insert(tk.END, item)

    def add_item(self, category):
        metier = self.combo_metier.get()
        val = self.entry_new.get().strip()
        if not metier: return messagebox.showwarning("Attention", "Sélectionnez un métier.")
        if val:
            self.data[metier][category].append(val)
            self.entry_new.delete(0, tk.END)
            self.refresh_lists()

    def edit_item(self, category):
        metier = self.combo_metier.get()
        lb = self.list_tech if category == "Techniques" else self.list_hum
        if not lb.curselection(): return
        
        idx = lb.curselection()[0]
        old_val = lb.get(idx)
        new_val = simpledialog.askstring("Modifier", f"Modifier l'élément :", initialvalue=old_val)
        
        if new_val and new_val.strip():
            self.data[metier][category][idx] = new_val.strip()
            self.refresh_lists()

    def delete_item(self):
        metier = self.combo_metier.get()
        # On regarde quelle liste a un élément sélectionné
        if self.list_tech.curselection():
            category, lb = "Techniques", self.list_tech
        elif self.list_hum.curselection():
            category, lb = "Humaines", self.list_hum
        else:
            return messagebox.showwarning("Supprimer", "Sélectionnez un élément à supprimer.")

        idx = lb.curselection()[0]
        del self.data[metier][category][idx]
        self.refresh_lists()

    def save_and_export(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Succès", f"Données exportées dans {self.filename}\nPrêt pour GitHub !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de l'export : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SAPDataManager(root)
    root.mainloop()
