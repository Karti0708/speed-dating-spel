import tkinter as tk
from tkinter import ttk, messagebox
import random

class DatingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personlighetstest Dating Simulator")
        self.root.geometry("600x500")
        
        
        self.frågor = [
            ("Föredrar du en kväll hemma eller ute på stan?", "Hemma", "Ute"),
            ("Vilket är din favoritmat?", "Pizza", "Sushi"),
            ("Vilken typ av film föredrar du?", "Action", "Romantik"),
            ("Föredrar du sommar eller vinter?", "Sommar", "Vinter"),
            ("Vilket djur passar dig bäst?", "Hund", "Katt"),
            ("Vilken musik lyssnar du mest på?", "Pop", "Rock"),
            ("Vad gör du helst på ledig dag?", "Vila", "Äventyr"),
            ("Vilken drink föredrar du?", "Öl", "Vin"),
            ("Vilken färg passar dig bäst?", "Blå", "Röd"),
            ("Vilken årstid föds du?", "Vår/Sommar", "Höst/Vinter")
        ]
        
        
        self.all_karaktärer = self.skapa_karaktärer()
        self.karaktärer = []
        self.spelarens_svar = []
        self.current_fråga = 0
        self.current_frame = None
        self.valt_kön = ""
        
        self.skapa_kön_val()

    def skapa_karaktärer(self):
        
        man_namn = ["Erik", "Lars", "Johan", "Anders", "Mikael"]
        kvinna_namn = ["Anna", "Maria", "Karin", "Emma", "Sofia"]
        
        karaktärer = []
        
        for namn in man_namn:
            karaktärer.append({
                "namn": namn,
                "kön": "Man",
                "svar": [random.choice([0,1]) for _ in self.frågor],
                "bild": self.skapa_placeholder_färg()
            })
       
        for namn in kvinna_namn:
            karaktärer.append({
                "namn": namn,
                "kön": "Kvinna",
                "svar": [random.choice([0,1]) for _ in self.frågor],
                "bild": self.skapa_placeholder_färg()
            })
        return karaktärer

    def skapa_placeholder_färg(self):
        färger = ["#FFB6C1", "#87CEEB", "#98FB98", "#DDA0DD", "#FFA07A",
                 "#20B2AA", "#FFD700", "#CD5C5C", "#7B68EE", "#FF6347"]
        return random.choice(färger)
    
    def skapa_kön_val(self):
        self.rensa_gui()
        tk.Label(self.root, text="Välj vilket kön du är intresserad av", 
                font=("Helvetica", 16, "bold")).pack(pady=30)
        
        knapp_frame = tk.Frame(self.root)
        knapp_frame.pack(pady=20)
        
        tk.Button(knapp_frame, text="Man 👨", command=lambda: self.välj_kön("Man"),
                 bg="#2196F3", fg="white", font=("Helvetica", 14), width=15).grid(row=0, column=0, padx=10)
        tk.Button(knapp_frame, text="Kvinna 👩", command=lambda: self.välj_kön("Kvinna"),
                 bg="#E91E63", fg="white", font=("Helvetica", 14), width=15).grid(row=0, column=1, padx=10)
    
    def välj_kön(self, kön):
        self.valt_kön = kön
        self.karaktärer = [k for k in self.all_karaktärer if k["kön"] == kön]
        self.starta_testet()
    
    def starta_testet(self):
        self.rensa_gui()
        self.visa_fråga()
    
    def visa_fråga(self):
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(pady=20)
        
        if self.current_fråga >= len(self.frågor):
            self.visa_resultat()
            return
        
        fråga, alt1, alt2 = self.frågor[self.current_fråga]
        
        tk.Label(self.current_frame, text=fråga, 
                font=("Helvetica", 14), wraplength=400).pack(pady=10)
        
        knapp_frame = tk.Frame(self.current_frame)
        knapp_frame.pack(pady=15)
        
        tk.Button(knapp_frame, text=alt1, command=lambda: self.spara_svar(0),
                 width=15, bg="#2196F3", fg="white", font=("Helvetica", 12)).grid(row=0, column=0, padx=10)
        tk.Button(knapp_frame, text=alt2, command=lambda: self.spara_svar(1),
                 width=15, bg="#2196F3", fg="white", font=("Helvetica", 12)).grid(row=0, column=1, padx=10)
        
        self.progress = ttk.Progressbar(self.current_frame, orient="horizontal", 
                                      length=400, mode="determinate",
                                      maximum=len(self.frågor))
        self.progress.pack(pady=10)
        self.progress["value"] = self.current_fråga + 1
        
        tk.Label(self.current_frame, text=f"Fråga {self.current_fråga + 1} av {len(self.frågor)}",
                font=("Helvetica", 10)).pack()
    
    def spara_svar(self, svar):
        self.spelarens_svar.append(svar)
        self.current_fråga += 1
        self.visa_fråga()
    
    def beräkna_match(self, karaktär_svar):
        matchande = sum(1 for p, k in zip(self.spelarens_svar, karaktär_svar) if p == k)
        return (matchande / len(self.frågor)) * 100
    
    def visa_resultat(self):
        self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(pady=20)
        
        resultat = []
        for karaktär in self.karaktärer:
            procent = self.beräkna_match(karaktär["svar"])
            resultat.append((karaktär["namn"], procent, karaktär["bild"], karaktär["kön"]))
        
        resultat.sort(key=lambda x: x[1], reverse=True)
        
        tk.Label(self.current_frame, text=f"Dina matcher ({self.valt_kön}):", 
                font=("Helvetica", 14, "bold")).pack(pady=10)
        
        canvas = tk.Canvas(self.current_frame)
        scrollbar = ttk.Scrollbar(self.current_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.create_window((0,0), window=scroll_frame, anchor="nw")
        
        for namn, procent, färg, kön in resultat:
            match_frame = tk.Frame(scroll_frame, bd=1, relief="solid", padx=10, pady=5)
            match_frame.pack(fill="x", padx=10, pady=5)
            
            tk.Label(match_frame, bg=färg, width=10, height=3).pack(side="left", padx=5)
            tk.Label(match_frame, text=f"{namn}\n{procent:.1f}% match\n{kön}", 
                    font=("Helvetica", 12)).pack(side="left", padx=10)
        
        scroll_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        tk.Button(self.current_frame, text="Gör om testet", command=self.återställ,
                 bg="#9C27B0", fg="white", font=("Helvetica", 12)).pack(pady=20)
    
    def återställ(self):
        self.spelarens_svar = []
        self.current_fråga = 0
        self.current_frame.destroy()
        self.skapa_kön_val()
    
    def rensa_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DatingApp(root)
    root.mainloop()