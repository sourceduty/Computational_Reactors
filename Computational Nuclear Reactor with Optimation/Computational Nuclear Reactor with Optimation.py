import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Optimation model for a simplified nuclear reactor
def simulate_optimation(weights):
    coolant_flow, rod_depth, fuel_enrich, power_demand, neutron_eff = weights
    
    # Normalize weights
    w = np.array(weights) / 100

    # Reactor physics proxies
    power_output = (w[2] * (1 - w[1]) * w[4]) * 1000  # fuel * (1 - rod depth) * neutron efficiency
    temp_rise = power_output / (w[0] * 10 + 1)  # inversely related to coolant flow

    # Stability index penalizes imbalance
    balance = 1 - np.std(w)
    stability_index = max(0, balance - (temp_rise / 1000))

    return power_output, temp_rise, stability_index

# GUI Application
class NuclearOptimationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Computational Nuclear Reactor: Optimation Simulator")

        self.vars = {
            'Coolant Flow': tk.IntVar(value=50),
            'Control Rod Depth': tk.IntVar(value=50),
            'Fuel Enrichment': tk.IntVar(value=50),
            'Power Demand': tk.IntVar(value=50),
            'Neutron Moderation': tk.IntVar(value=50)
        }

        self.create_widgets()
        self.update_plot()

    def create_widgets(self):
        control_frame = ttk.LabelFrame(self.root, text="Reactor Controls")
        control_frame.grid(row=0, column=0, padx=10, pady=10)

        for i, (label, var) in enumerate(self.vars.items()):
            ttk.Label(control_frame, text=label).grid(row=i, column=0, sticky='w')
            ttk.Scale(control_frame, from_=1, to=100, orient='horizontal', variable=var,
                      command=lambda e: self.update_plot()).grid(row=i, column=1)

        self.figure, self.ax = plt.subplots(3, 1, figsize=(5, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)

    def update_plot(self):
        weights = [var.get() for var in self.vars.values()]
        power, temp, stability = simulate_optimation(weights)

        labels = ['Power Output (MW)', 'Core Temperature (°C)', 'Stability Index']
        values = [power, temp, stability * 100]

        for i in range(3):
            self.ax[i].clear()
            self.ax[i].barh([labels[i]], [values[i]])
            self.ax[i].set_xlim(0, 1000 if i < 2 else 100)
            self.ax[i].set_title(labels[i])

        self.figure.tight_layout()
        self.canvas.draw()

if __name__ == '__main__':
    root = tk.Tk()
    app = NuclearOptimationApp(root)
    root.mainloop()
