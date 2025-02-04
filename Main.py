import numpy as np
import sympy as sp
import tkinter as tk
from tkinter import ttk
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Função da superfície
def f(x, y):
    return 4 - 2*x**2 - y**2

# Cálculo Analítico da Integral Dupla
x, y = sp.symbols('x y')
integral_analitica = sp.integrate(sp.integrate(f(x, y), (y, 0, 1)), (x, 0, 1))

# Cálculo Numérico via Soma de Riemann
def volume_numerico(step=0.1):
    x_vals = np.arange(0, 1 + step, step)
    y_vals = np.arange(0, 1 + step, step)
    volume = 0
    
    for i in x_vals:
        for j in y_vals:
            volume += f(i, j) * step * step
    
    return volume, x_vals, y_vals

# Criando Interface Gráfica
class VolumeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cálculo de Volume por Integrais")
        
        self.label_analitico = tk.Label(root, text=f"Volume Analítico: {integral_analitica.evalf():.4f}")
        self.label_analitico.pack()
        
        self.label_step = tk.Label(root, text="Passo para Cálculo Numérico:")
        self.label_step.pack()
        
        self.entry_step = tk.Entry(root)
        self.entry_step.insert(0, "0.1")
        self.entry_step.pack()
        
        self.button_calcular = tk.Button(root, text="Calcular Volume Numérico", command=self.calcular)
        self.button_calcular.pack()
        
        self.label_resultado = tk.Label(root, text="")
        self.label_resultado.pack()
        
        self.button_tabela = tk.Button(root, text="Mostrar Tabela", command=self.mostrar_tabela)
        self.button_tabela.pack()
        
        self.figura = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figura.add_subplot(111, projection='3d')
        
        self.canvas = FigureCanvasTkAgg(self.figura, master=root)
        self.canvas.get_tk_widget().pack()
        
    def calcular(self):
        step = float(self.entry_step.get())
        volume, x_vals, y_vals = volume_numerico(step)
        self.label_resultado.config(text=f"Volume Numérico: {volume:.4f}")
        
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = f(X, Y)
        
        self.ax.clear()
        self.ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
        self.canvas.draw()
    
    def mostrar_tabela(self):
        step = float(self.entry_step.get())
        x_vals = np.arange(0, 1 + step, step)
        y_vals = np.arange(0, 1 + step, step)
        
        data = []
        for i in x_vals:
            for j in y_vals:
                data.append([round(i, 2), round(j, 2), round(f(i, j), 2)])
        
        df = pd.DataFrame(data, columns=["x", "y", "z"])
        tabela = tk.Toplevel()
        tabela.title("Tabela de Valores")
        
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12), background="#e6efdc", foreground="black", rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#b6d7a8", foreground="black")
        
        tree = ttk.Treeview(tabela, columns=("x", "y", "z"), show="headings", height=20)
        tree.heading("x", text="x", anchor="center")
        tree.heading("y", text="y", anchor="center")
        tree.heading("z", text="z", anchor="center")
        
        tree.column("x", anchor="center", width=100)
        tree.column("y", anchor="center", width=100)
        tree.column("z", anchor="center", width=100)
        
        for _, row in df.iterrows():
            tree.insert("", "end", values=row.tolist(), tags=('data',))
        
        tree.tag_configure('data', background="#d9ead3")
        
        tree.pack(expand=True, fill="both")
        scrollbar = ttk.Scrollbar(tabela, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

# Executando Aplicação
root = tk.Tk()
app = VolumeApp(root)
root.mainloop()
