# App to visualize data from a CSV file

# Libraries
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os
from webcolors import name_to_hex
from tkinter import colorchooser
from datetime import datetime

# Main Window
class CSVVisualizer:

    def __init__(self, root):
        self.root = root
        self.root.title("CSV Visualizer")
        self.root.iconbitmap("C:/Users/Alfonso Vecino/Documents/CODING/CSV_Visualizer/icons/icon.ico")

        # Data & settings initialization
        self.df = None
        self.filter_prompt_1 = ""
        self.filter_prompt_2 = ""
        self.filter_prompt_3 = ""
        self.filter_prompt_4 = ""
        self.filter_prompt_5 = ""
        self.data_1 = []
        self.data_2 = []
        self.data_3 = []
        self.data_4 = []
        self.data_5 = []
        
        # Defining the window size
        w_win = 1200
        h_win = 450

        # Centering the window when opening
        wtotal = root.winfo_screenwidth()
        htotal = root.winfo_screenheight()
        pwidth = round(wtotal/2-w_win/2)
        pheight = round(htotal/2-h_win/2)
        root.geometry(str(w_win)+"x"+str(h_win)+"+"+str(pwidth)+"+"+str(pheight))
        # Fixing the window size
        root.minsize(w_win, h_win)
        root.maxsize(w_win, h_win)

        # --- UI Layout ---
        self.setup_ui()
    
    def setup_ui(self):

        # Constraints
        self.plot_types = ["line", "bar", "scatter", "hist"]
        
        # Points of Reference for configuration bars
        self.y_px = 90
        self.x_px = 50

        # Top Labeles
        tk.Label(self.root, text="CSV Visualizer using Matplotlib and Pandas - Developed by Alfonso Vecino in August 2025").place(x=self.x_px+300,y=self.y_px-75)
        tk.Label(self.root, text="Enable").place(x=self.x_px-10, y = self.y_px - 30)
        tk.Label(self.root, text="X Axis").place(x=self.x_px+90, y = self.y_px - 30)
        tk.Label(self.root, text="Y Axis").place(x=self.x_px+260, y = self.y_px - 30)
        tk.Label(self.root, text="Chart Type").place(x=self.x_px+410, y = self.y_px - 30)
        tk.Label(self.root, text="Color").place(x=self.x_px+540, y = self.y_px - 30)
        tk.Label(self.root, text="2nd Axis").place(x=self.x_px+615, y = self.y_px - 30)
        tk.Label(self.root, text="3rd Axis").place(x=self.x_px+695, y = self.y_px - 30)
        tk.Label(self.root, text="Filters").place(x=self.x_px+785, y = self.y_px - 30)
        tk.Label(self.root, text="Filters Status").place(x=self.x_px+880, y = self.y_px - 30)
        
        # X Axis configuration Checkboxes and Labels
        tk.Label(self.root, text="X Axis configuration").place(x=40,y=310)
        self.frame = tk.Frame(self.root, highlightbackground="darkgray", highlightthickness=1, width=260, height=30).place(x=40,y=335)
        self.chbx_independent_value = tk.BooleanVar(self.root)
        self.chbx_independent = ttk.Checkbutton(self.root, variable=self.chbx_independent_value, command=self.chbx_independent_change)
        self.chbx_independent.place(x=50, y=340)
        self.chbx_independent_value.set(True)
        tk.Label(self.root, text="Independent").place(x=65,y=340)
        self.chbx_shared_value = tk.BooleanVar(self.root)
        self.chbx_shared = ttk.Checkbutton(self.root, variable=self.chbx_shared_value, command=self.chbx_shared_change)
        self.chbx_shared.place(x=150, y=340)
        tk.Label(self.root, text="Shared").place(x=170,y=340)
        self.chbx_fixed_value = tk.BooleanVar(self.root)
        self.chbx_fixed = ttk.Checkbutton(self.root, variable=self.chbx_fixed_value, command=self.chbx_fixed_change)
        self.chbx_fixed.place(x=220, y=340)
        tk.Label(self.root, text="Fix Order").place(x=240,y=340)

        # Buttons
        tk.Button(self.root, text="Load CSV", command=self.load_csv).place(x=40,y=380)
        tk.Button(self.root, text="Save Settings", command=self.save_settings).place(x=110,y=380)
        tk.Button(self.root, text="Load Settings", command=self.load_settings).place(x=200,y=380)
        tk.Button(self.root, text="Generate Chart", command=self.plot_data).place(x=295,y=380)
        tk.Button(self.root, text="Preview CSV", command=self.open_previsualizer).place(x=400,y=380)
        tk.Button(self.root, text="Reset All", command=self.reset_app).place(x=490,y=380)

        # Chart Configuration: CheckBox, Dropdowns, ColorPicker
            #1
        self.chbx1_value = tk.BooleanVar(self.root)
        self.chbx1 = ttk.Checkbutton(self.root, variable=self.chbx1_value, command=self.chbx1_change)
        self.chbx1.place(x=self.x_px, y=self.y_px)
        self.x1_var = tk.StringVar()
        self.y1_var = tk.StringVar()
        self.chr1_type = tk.StringVar(value="line")
        self.x1_drdw = ttk.Combobox(self.root, textvariable=self.x1_var)
        self.y1_drdw = ttk.Combobox(self.root, textvariable=self.y1_var)
        self.chr1_drdw = ttk.Combobox(self.root, textvariable=self.chr1_type, values=self.plot_types)
        self.x1_drdw.place(x=self.x_px + 50, y=self.y_px)
        self.y1_drdw.place(x=self.x_px + 210, y=self.y_px)
        self.chr1_drdw.place(x=self.x_px + 370, y=self.y_px)
        self.color_1_hex = 'blue'
        self.btn_color_1 = tk.Button(self.root, text="   ", command=self.select_color_1, bg=self.color_1_hex)
        self.btn_color_1.place(x = self.x_px + 550, y=self.y_px, width=20, height=20)
        self.chbx1_ax2_value = tk.BooleanVar(self.root)
        self.chbx1_ax2 = ttk.Checkbutton(self.root, variable=self.chbx1_ax2_value, command=self.chbx1_ax2_change)
        self.chbx1_ax2.place(x=self.x_px + 630, y=self.y_px)
        self.chbx1_ax3_value = tk.BooleanVar(self.root)
        self.chbx1_ax3 = ttk.Checkbutton(self.root, variable=self.chbx1_ax3_value, command=self.chbx1_ax3_change)
        self.chbx1_ax3.place(x=self.x_px + 710, y=self.y_px)
        self.btn_filter_1 = tk.Button(self.root, text="+", command=self.open_filter1, bg='gray', fg='white')
        self.btn_filter_1.place(x = self.x_px + 780, y=self.y_px, width=15, height=15)
        self.btn_filter_1_remove = tk.Button(self.root, text="-", command=self.remove_filter1, bg='red', fg='white')
        self.btn_filter_1_remove.place(x = self.x_px + 800, y=self.y_px, width=15, height=15)
        self.btn_filter_1_edit = tk.Button(self.root, text="*", command=self.edit_filter1, bg='yellow', fg='black')
        self.btn_filter_1_edit.place(x = self.x_px + 820, y=self.y_px, width=15, height=15)
        self.lbl_1_filter = tk.Label(self.root, text="None")
        self.lbl_1_filter.place(x=self.x_px + 900, y=self.y_px)
        self.x1_drdw.config(state="disabled")
        self.y1_drdw.config(state="disabled")
        self.chr1_drdw.config(state="disabled")
        self.chbx1_ax2.state(['disabled'])
        self.chbx1_ax3.state(['disabled'])
            #2
        self.dd2_px = 40
        self.chbx2_value = tk.BooleanVar(self.root)
        self.chbx2 = ttk.Checkbutton(self.root, variable=self.chbx2_value, command=self.chbx2_change)
        self.chbx2.place(x=self.x_px, y=self.y_px + self.dd2_px)
        self.x2_var = tk.StringVar()
        self.y2_var = tk.StringVar()
        self.chr2_type = tk.StringVar(value="line")
        self.x2_drdw = ttk.Combobox(self.root, textvariable=self.x2_var)
        self.y2_drdw = ttk.Combobox(self.root, textvariable=self.y2_var)
        self.chr2_drdw = ttk.Combobox(self.root, textvariable=self.chr2_type, values=self.plot_types)
        self.x2_drdw.place(x=self.x_px + 50, y=self.y_px + self.dd2_px)
        self.y2_drdw.place(x=self.x_px + 210, y=self.y_px + self.dd2_px)
        self.chr2_drdw.place(x=self.x_px + 370, y=self.y_px + self.dd2_px)
        self.color_2_hex = 'red'
        self.btn_color_2 = tk.Button(self.root, text="   ", command=self.select_color_2, bg=self.color_2_hex)
        self.btn_color_2.place(x = self.x_px + 550, y=self.y_px + self.dd2_px, width=20, height=20)
        self.chbx2_ax2_value = tk.BooleanVar(self.root)
        self.chbx2_ax2 = ttk.Checkbutton(self.root, variable=self.chbx2_ax2_value, command=self.chbx2_ax2_change)
        self.chbx2_ax2.place(x=self.x_px + 630, y=self.y_px + self.dd2_px)
        self.chbx2_ax3_value = tk.BooleanVar(self.root)
        self.chbx2_ax3 = ttk.Checkbutton(self.root, variable=self.chbx2_ax3_value, command=self.chbx2_ax3_change)
        self.chbx2_ax3.place(x=self.x_px + 710, y=self.y_px + self.dd2_px)
        self.btn_filter_2 = tk.Button(self.root, text="+", command=self.open_filter2, bg='gray', fg='white')
        self.btn_filter_2.place(x = self.x_px + 780, y=self.y_px + self.dd2_px, width=15, height=15)
        self.btn_filter_2_remove = tk.Button(self.root, text="-", command=self.remove_filter2, bg='red', fg='white')
        self.btn_filter_2_remove.place(x = self.x_px + 800, y=self.y_px + self.dd2_px, width=15, height=15)
        self.btn_filter_2_edit = tk.Button(self.root, text="*", command=self.edit_filter2, bg='yellow', fg='black')
        self.btn_filter_2_edit.place(x = self.x_px + 820, y=self.y_px + self.dd2_px, width=15, height=15)
        self.lbl_2_filter = tk.Label(self.root, text="None")
        self.lbl_2_filter.place(x=self.x_px + 900, y=self.y_px + self.dd2_px)
        self.x2_drdw.config(state="disabled")
        self.y2_drdw.config(state="disabled")
        self.chr2_drdw.config(state="disabled")
        self.chbx2_ax2.state(['disabled'])
        self.chbx2_ax3.state(['disabled'])
            #3
        self.dd3_px = 80
        self.chbx3_value = tk.BooleanVar(self.root)
        self.chbx3 = ttk.Checkbutton(self.root, variable=self.chbx3_value, command=self.chbx3_change)
        self.chbx3.place(x=self.x_px, y=self.y_px + self.dd3_px)
        self.x3_var = tk.StringVar()
        self.y3_var = tk.StringVar()
        self.chr3_type = tk.StringVar(value="line")
        self.x3_drdw = ttk.Combobox(self.root, textvariable=self.x3_var)
        self.y3_drdw = ttk.Combobox(self.root, textvariable=self.y3_var)
        self.chr3_drdw = ttk.Combobox(self.root, textvariable=self.chr3_type, values=self.plot_types)
        self.x3_drdw.place(x=self.x_px + 50, y=self.y_px + self.dd3_px)
        self.y3_drdw.place(x=self.x_px + 210, y=self.y_px + self.dd3_px)
        self.chr3_drdw.place(x=self.x_px + 370, y=self.y_px + self.dd3_px)
        self.color_3_hex = 'green'
        self.btn_color_3 = tk.Button(self.root, text="   ", command=self.select_color_3, bg=self.color_3_hex)
        self.btn_color_3.place(x = self.x_px + 550, y=self.y_px + self.dd3_px, width=20, height=20)
        self.chbx3_ax2_value = tk.BooleanVar(self.root)
        self.chbx3_ax2 = ttk.Checkbutton(self.root, variable=self.chbx3_ax2_value, command=self.chbx3_ax2_change)
        self.chbx3_ax2.place(x=self.x_px + 630, y=self.y_px + self.dd3_px)
        self.chbx3_ax3_value = tk.BooleanVar(self.root)
        self.chbx3_ax3 = ttk.Checkbutton(self.root, variable=self.chbx3_ax3_value, command=self.chbx3_ax3_change)
        self.chbx3_ax3.place(x=self.x_px + 710, y=self.y_px + self.dd3_px)
        self.btn_filter_3 = tk.Button(self.root, text="+", command=self.open_filter3, bg='gray', fg='white')
        self.btn_filter_3.place(x = self.x_px + 780, y=self.y_px + self.dd3_px, width=15, height=15)
        self.btn_filter_3_remove = tk.Button(self.root, text="-", command=self.remove_filter3, bg='red', fg='white')
        self.btn_filter_3_remove.place(x = self.x_px + 800, y=self.y_px + self.dd3_px, width=15, height=15)
        self.btn_filter_3_edit = tk.Button(self.root, text="*", command=self.edit_filter3, bg='yellow', fg='black')
        self.btn_filter_3_edit.place(x = self.x_px + 820, y=self.y_px + self.dd3_px, width=15, height=15)
        self.lbl_3_filter = tk.Label(self.root, text="None")
        self.lbl_3_filter.place(x=self.x_px + 900, y=self.y_px + self.dd3_px)
        self.x3_drdw.config(state="disabled")
        self.y3_drdw.config(state="disabled")
        self.chr3_drdw.config(state="disabled")
        self.chbx3_ax2.state(['disabled'])
        self.chbx3_ax3.state(['disabled'])
            #4
        self.dd4_px = 120
        self.chbx4_value = tk.BooleanVar(self.root)
        self.chbx4 = ttk.Checkbutton(self.root, variable=self.chbx4_value, command=self.chbx4_change)
        self.chbx4.place(x=self.x_px, y=self.y_px + self.dd4_px)
        self.x4_var = tk.StringVar()
        self.y4_var = tk.StringVar()
        self.chr4_type = tk.StringVar(value="line")
        self.x4_drdw = ttk.Combobox(self.root, textvariable=self.x4_var)
        self.y4_drdw = ttk.Combobox(self.root, textvariable=self.y4_var)
        self.chr4_drdw = ttk.Combobox(self.root, textvariable=self.chr4_type, values=self.plot_types)
        self.x4_drdw.place(x=self.x_px + 50, y=self.y_px + self.dd4_px)
        self.y4_drdw.place(x=self.x_px + 210, y=self.y_px + self.dd4_px)
        self.chr4_drdw.place(x=self.x_px + 370, y=self.y_px + self.dd4_px)
        self.color_4_hex = 'orange'
        self.btn_color_4 = tk.Button(self.root, text="   ", command=self.select_color_4, bg=self.color_4_hex)
        self.btn_color_4.place(x = self.x_px + 550, y=self.y_px + self.dd4_px, width=20, height=20)
        self.chbx4_ax2_value = tk.BooleanVar(self.root)
        self.chbx4_ax2 = ttk.Checkbutton(self.root, variable=self.chbx4_ax2_value, command=self.chbx4_ax2_change)
        self.chbx4_ax2.place(x=self.x_px + 630, y=self.y_px + self.dd4_px)
        self.chbx4_ax3_value = tk.BooleanVar(self.root)
        self.chbx4_ax3 = ttk.Checkbutton(self.root, variable=self.chbx4_ax3_value, command=self.chbx4_ax3_change)
        self.chbx4_ax3.place(x=self.x_px + 710, y=self.y_px + self.dd4_px)
        self.btn_filter_4 = tk.Button(self.root, text="+", command=self.open_filter4, bg='gray', fg='white')
        self.btn_filter_4.place(x = self.x_px + 780, y=self.y_px + self.dd4_px, width=15, height=15)
        self.btn_filter_4_remove = tk.Button(self.root, text="-", command=self.remove_filter4, bg='red', fg='white')
        self.btn_filter_4_remove.place(x = self.x_px + 800, y=self.y_px + self.dd4_px, width=15, height=15)
        self.btn_filter_4_edit = tk.Button(self.root, text="*", command=self.edit_filter4, bg='yellow', fg='black')
        self.btn_filter_4_edit.place(x = self.x_px + 820, y=self.y_px + self.dd4_px, width=15, height=15)
        self.lbl_4_filter = tk.Label(self.root, text="None")
        self.lbl_4_filter.place(x=self.x_px + 900, y=self.y_px + self.dd4_px)
        self.x4_drdw.config(state="disabled")
        self.y4_drdw.config(state="disabled")
        self.chr4_drdw.config(state="disabled")
        self.chbx4_ax2.state(['disabled'])
        self.chbx4_ax3.state(['disabled'])
            #5
        self.dd5_px = 160
        self.chbx5_value = tk.BooleanVar(self.root)
        self.chbx5 = ttk.Checkbutton(self.root, variable=self.chbx5_value, command=self.chbx5_change)
        self.chbx5.place(x=self.x_px, y=self.y_px + self.dd5_px)
        self.x5_var = tk.StringVar()
        self.y5_var = tk.StringVar()
        self.chr5_type = tk.StringVar(value="line")
        self.x5_drdw = ttk.Combobox(self.root, textvariable=self.x5_var)
        self.y5_drdw = ttk.Combobox(self.root, textvariable=self.y5_var)
        self.chr5_drdw = ttk.Combobox(self.root, textvariable=self.chr5_type, values=self.plot_types)
        self.x5_drdw.place(x=self.x_px + 50, y=self.y_px + self.dd5_px)
        self.y5_drdw.place(x=self.x_px + 210, y=self.y_px + self.dd5_px)
        self.chr5_drdw.place(x=self.x_px + 370, y=self.y_px + self.dd5_px)
        self.color_5_hex = 'black'
        self.btn_color_5 = tk.Button(self.root, text="   ", command=self.select_color_5, bg=self.color_5_hex)
        self.btn_color_5.place(x = self.x_px + 550, y=self.y_px + self.dd5_px, width=20, height=20)
        self.chbx5_ax2_value = tk.BooleanVar(self.root)
        self.chbx5_ax2 = ttk.Checkbutton(self.root, variable=self.chbx5_ax2_value, command=self.chbx5_ax2_change)
        self.chbx5_ax2.place(x=self.x_px + 630, y=self.y_px + self.dd5_px)
        self.chbx5_ax3_value = tk.BooleanVar(self.root)
        self.chbx5_ax3 = ttk.Checkbutton(self.root, variable=self.chbx5_ax3_value, command=self.chbx5_ax3_change)
        self.chbx5_ax3.place(x=self.x_px + 710, y=self.y_px + self.dd5_px)
        self.btn_filter_5 = tk.Button(self.root, text="+", command=self.open_filter5, bg='gray', fg='white')
        self.btn_filter_5.place(x = self.x_px + 780, y=self.y_px + self.dd5_px, width=15, height=15)
        self.btn_filter_5_remove = tk.Button(self.root, text="-", command=self.remove_filter5, bg='red', fg='white')
        self.btn_filter_5_remove.place(x = self.x_px + 800, y=self.y_px + self.dd5_px, width=15, height=15)
        self.btn_filter_5_edit = tk.Button(self.root, text="*", command=self.edit_filter5, bg='yellow', fg='black')
        self.btn_filter_5_edit.place(x = self.x_px + 820, y=self.y_px + self.dd5_px, width=15, height=15)
        self.lbl_5_filter = tk.Label(self.root, text="None")
        self.lbl_5_filter.place(x=self.x_px + 900, y=self.y_px + self.dd5_px)
        self.x5_drdw.config(state="disabled")
        self.y5_drdw.config(state="disabled")
        self.chr5_drdw.config(state="disabled")
        self.chbx5_ax2.state(['disabled'])
        self.chbx5_ax3.state(['disabled'])

    # Functions to configurate the X Axis options
    def chbx_independent_change(self):
        if self.chbx_independent_value.get():
            self.chbx_fixed_value.set(False)
            self.chbx_shared_value.set(False)
    def chbx_shared_change(self):
        if self.chbx_shared_value.get():
            self.chbx_fixed_value.set(False)
            self.chbx_independent_value.set(False)
    def chbx_fixed_change(self):
        if self.chbx_fixed_value.get():
            self.chbx_shared_value.set(False)
            self.chbx_independent_value.set(False)
    
    # Function to Enable/Disable each configuration bar
        #1
    def chbx1_change(self):
        if self.chbx1_value.get():
            self.x1_drdw.config(state="enabled")
            self.y1_drdw.config(state="enabled")
            self.chr1_drdw.config(state="enabled")
            self.chbx1_ax2.config(state='normal')
            self.chbx1_ax3.config(state='normal')
        else:
            self.x1_drdw.config(state="disabled")
            self.y1_drdw.config(state="disabled")
            self.chr1_drdw.config(state="disabled")
            self.chbx1_ax2.state(['disabled'])
            self.chbx1_ax3.state(['disabled'])
        #2
    def chbx2_change(self):
        if self.chbx2_value.get():
            self.x2_drdw.config(state="enabled")
            self.y2_drdw.config(state="enabled")
            self.chr2_drdw.config(state="enabled")
            self.chbx2_ax2.config(state='normal')
            self.chbx2_ax3.config(state='normal')
        else:
            self.x2_drdw.config(state="disabled")
            self.y2_drdw.config(state="disabled")
            self.chr2_drdw.config(state="disabled")
            self.chbx2_ax2.state(['disabled'])
            self.chbx2_ax3.state(['disabled'])
        #3
    def chbx3_change(self):
        if self.chbx3_value.get():
            self.x3_drdw.config(state="enabled")
            self.y3_drdw.config(state="enabled")
            self.chr3_drdw.config(state="enabled")
            self.chbx3_ax2.config(state='normal')
            self.chbx3_ax3.config(state='normal')
        else:
            self.x3_drdw.config(state="disabled")
            self.y3_drdw.config(state="disabled")
            self.chr3_drdw.config(state="disabled")
            self.chbx3_ax2.state(['disabled'])
            self.chbx3_ax3.state(['disabled'])
        #4
    def chbx4_change(self):
        if self.chbx4_value.get():
            self.x4_drdw.config(state="enabled")
            self.y4_drdw.config(state="enabled")
            self.chr4_drdw.config(state="enabled")
            self.chbx4_ax2.config(state='normal')
            self.chbx4_ax3.config(state='normal')
        else:
            self.x4_drdw.config(state="disabled")
            self.y4_drdw.config(state="disabled")
            self.chr4_drdw.config(state="disabled")
            self.chbx4_ax2.state(['disabled'])
            self.chbx4_ax3.state(['disabled'])
        #5
    def chbx5_change(self):
        if self.chbx5_value.get():
            self.x5_drdw.config(state="enabled")
            self.y5_drdw.config(state="enabled")
            self.chr5_drdw.config(state="enabled")
            self.chbx5_ax2.config(state='normal')
            self.chbx5_ax3.config(state='normal')
        else:
            self.x5_drdw.config(state="disabled")
            self.y5_drdw.config(state="disabled")
            self.chr5_drdw.config(state="disabled")
            self.chbx5_ax2.state(['disabled'])
            self.chbx5_ax3.state(['disabled'])

    # Selecting just one axis option for each configuration bar
        #1
    def chbx1_ax2_change(self):
        if self.chbx1_ax2_value.get():
            self.chbx1_ax3_value.set(False)
    def chbx1_ax3_change(self):
        if self.chbx1_ax3_value.get():
            self.chbx1_ax2_value.set(False)
        #2
    def chbx2_ax2_change(self):
        if self.chbx2_ax2_value.get():
            self.chbx2_ax3_value.set(False)
    def chbx2_ax3_change(self):
        if self.chbx2_ax3_value.get():
            self.chbx2_ax2_value.set(False)
        #3
    def chbx3_ax2_change(self):
        if self.chbx3_ax2_value.get():
            self.chbx3_ax3_value.set(False)
    def chbx3_ax3_change(self):
        if self.chbx3_ax3_value.get():
            self.chbx3_ax2_value.set(False)
        #4
    def chbx4_ax2_change(self):
        if self.chbx4_ax2_value.get():
            self.chbx4_ax3_value.set(False)
    def chbx4_ax3_change(self):
        if self.chbx4_ax3_value.get():
            self.chbx4_ax2_value.set(False)
        #5
    def chbx5_ax2_change(self):
        if self.chbx5_ax2_value.get():
            self.chbx5_ax3_value.set(False)
    def chbx5_ax3_change(self):
        if self.chbx5_ax3_value.get():
            self.chbx5_ax2_value.set(False)

    # Select color boxes
        #1
    def select_color_1(self):
        self.color_code_1 = colorchooser.askcolor(title ="Select color")
        self.color_1_hex = self.color_code_1[1]
        self.btn_color_1.config(bg=self.color_1_hex)
        #2
    def select_color_2(self):
        self.color_code_2 = colorchooser.askcolor(title ="Select color")
        self.color_2_hex = self.color_code_2[1]
        self.btn_color_2.config(bg=self.color_2_hex)
        #3
    def select_color_3(self):
        self.color_code_3 = colorchooser.askcolor(title ="Select color")
        self.color_3_hex = self.color_code_3[1]
        self.btn_color_3.config(bg=self.color_3_hex)
        #4
    def select_color_4(self):
        self.color_code_4 = colorchooser.askcolor(title ="Select color")
        self.color_4_hex = self.color_code_4[1]
        self.btn_color_4.config(bg=self.color_4_hex)
        #5
    def select_color_5(self):
        self.color_code_5 = colorchooser.askcolor(title ="Select color")
        self.color_5_hex = self.color_code_5[1]
        self.btn_color_5.config(bg=self.color_5_hex)
        
    # Load CSV Function
    def load_csv(self, **kwargs):
        # Saving the last used directory
        self.last_directory = os.getcwd()
        initialdir = kwargs.pop('initialdir', self.last_directory)
        file_path = filedialog.askopenfilename(initialdir=initialdir, **kwargs, filetypes=[("CSV Files","*.csv")])
        if file_path:
            try:
                self.df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    self.df = pd.read_csv(file_path, encoding='ISO-8859-1')
                except UnicodeDecodeError:
                    self.df = pd.read_csv(file_path, encoding='cp1252')
            
            # Populate dropdowns
            cols = list(self.df.columns)
            self.x1_drdw["values"] = cols
            self.y1_drdw["values"] = cols
            self.x2_drdw["values"] = cols
            self.y2_drdw["values"] = cols
            self.x3_drdw["values"] = cols
            self.y3_drdw["values"] = cols
            self.x4_drdw["values"] = cols
            self.y4_drdw["values"] = cols
            self.x5_drdw["values"] = cols
            self.y5_drdw["values"] = cols
            messagebox.showinfo("CSV Loaded", f"Loaded {len(self.df)} rows and {len(cols)} columns.")
            return self.df
              
    # Plot Function
    def plot_data(self):
        
        # If there is no CSV selected, the process is aborted
        if self.df is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return
        
        # If there is no X axis configurated, it ends the execution
        if self.chbx_independent_value.get() == False:
            if self.chbx_fixed_value.get() == False:
                if self.chbx_shared_value.get() ==False:
                    messagebox.showwarning("No X Axis configurated", "Please select an X Axis option before generating the chart.")
                    return

        # Creating the data frame filtered (if there is any filter)
        self.df_filtered_1 = self.df
        self.df_filtered_2 = self.df
        self.df_filtered_3 = self.df
        self.df_filtered_4 = self.df
        self.df_filtered_5 = self.df

        # Adding "row order" column to preserve the original csv order
        self.df_filtered_1["_row_order"] = range(len(self.df_filtered_1))
        self.df_filtered_2["_row_order"] = range(len(self.df_filtered_2))
        self.df_filtered_3["_row_order"] = range(len(self.df_filtered_3))
        self.df_filtered_4["_row_order"] = range(len(self.df_filtered_4))
        self.df_filtered_5["_row_order"] = range(len(self.df_filtered_5))

        if len(self.data_1) > 0:
            self.mask_1 = eval(self.filter_prompt_1)
            self.df_filtered_1 = self.df[self.mask_1]
        if len(self.data_2) > 0:
            self.mask_2 = eval(self.filter_prompt_2)
            self.df_filtered_2 = self.df[self.mask_2]
        if len(self.data_3) > 0:
            self.mask_3 = eval(self.filter_prompt_3)
            self.df_filtered_3 = self.df[self.mask_3]
        if len(self.data_4) > 0:
            self.mask_4 = eval(self.filter_prompt_4)
            self.df_filtered_4 = self.df[self.mask_4]
        if len(self.data_5) > 0:
            self.mask_5 = eval(self.filter_prompt_5)
            self.df_filtered_5 = self.df[self.mask_5]

        # Reading the information from each configuration bar
        self.x1_col = self.x1_var.get()
        self.y1_col = self.y1_var.get()
        chart1 = self.chr1_type.get()
        self.x2_col = self.x2_var.get()
        self.y2_col = self.y2_var.get()
        chart2 = self.chr2_type.get()
        self.x3_col = self.x3_var.get()
        self.y3_col = self.y3_var.get()
        chart3 = self.chr3_type.get()
        self.x4_col = self.x4_var.get()
        self.y4_col = self.y4_var.get()
        chart4 = self.chr4_type.get()
        self.x5_col = self.x5_var.get()
        self.y5_col = self.y5_var.get()
        chart5 = self.chr5_type.get()

        # Axis definition
        self.fig, self.ax = plt.subplots()
        self.numax2 = 0
        self.numax3 = 0

        # Detecting how many bars have 2 axis selected
        if self.chbx1_ax2_value.get():
            self.numax2 += 1
        if self.chbx2_ax2_value.get():
            self.numax2 += 1
        if self.chbx3_ax2_value.get():
            self.numax2 += 1
        if self.chbx4_ax2_value.get():
            self.numax2 += 1
        if self.chbx5_ax2_value.get():
            self.numax2 += 1
        # Detecting how many bars have 3 axis selected
        if self.chbx1_ax3_value.get():
            self.numax3 += 1
        if self.chbx2_ax3_value.get():
            self.numax3 += 1
        if self.chbx3_ax3_value.get():
            self.numax3 += 1
        if self.chbx4_ax3_value.get():
            self.numax3 += 1
        if self.chbx5_ax3_value.get():
            self.numax3 += 1
        # The auxiliar axis are created only if the user selected one or more bars
        if self.numax2 > 0:
            self.ax2 = self.ax.twinx()
        if self.numax3 > 0:
            self.ax3 = self.ax.twinx()

        # Plot configuration for Bar 1
        if self.chbx1_value.get():

            if chart1 != "hist" and (not self.x1_col or not self.y1_col):
                messagebox.showwarning("Missing Columns in Bar 1", "Select X and Y for this chart type.")
                return
            try:
                if chart1 == "line":        # Plot Line ---------------------------------------------------------------
                    if self.chbx1_ax2_value.get():      # 2nd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_1.plot(x=self.x1_col, y=self.y1_col, color=self.color_1_hex, kind="line", ax=self.ax2)    # Independent
                        if self.chbx_shared_value.get():
                            self.ax2.plot(self.df_filtered_1[self.x1_col], self.df_filtered_1[self.y1_col], color=self.color_1_hex)    # Shared
                        if self.chbx_fixed_value.get():
                            self.ax2.plot(self.df_filtered_1["_row_order"], self.df_filtered_1[self.y1_col], color=self.color_1_hex)   # Fixed
                        self.color1_2nd_y_axis()
                    elif self.chbx1_ax3_value.get():    # 3rd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_1.plot(x=self.x1_col, y=self.y1_col, color=self.color_1_hex, kind="line", ax=self.ax3)    # Independent
                        if self.chbx_shared_value.get():
                            self.ax3.plot(self.df_filtered_1[self.x1_col], self.df_filtered_1[self.y1_col], color=self.color_1_hex)    # Shared
                        if self.chbx_fixed_value.get():
                            self.ax3.plot(self.df_filtered_1["_row_order"], self.df_filtered_1[self.y1_col], color=self.color_1_hex)   # Fixed
                        self.color1_3rd_y_axis()
                    else:                               # Main Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_1.plot(x=self.x1_col, y=self.y1_col, color=self.color_1_hex, kind="line", ax=self.ax)     # Independent
                        if self.chbx_shared_value.get():
                            self.ax.plot(self.df_filtered_1[self.x1_col], self.df_filtered_1[self.y1_col], color=self.color_1_hex)     # Shared
                        if self.chbx_fixed_value.get():
                            self.ax.plot(self.df_filtered_1["_row_order"], self.df_filtered_1[self.y1_col], color=self.color_1_hex)    # Fixed
                        self.color1_main_y_axis()
                    self.color1_main_x_axis()
                elif chart1 == "bar":       # Plot Bar ----------------------------------------------------------------
                    if self.chbx1_ax2_value.get():      # 2nd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_1.plot(x=self.x1_col, y=self.y1_col, color=self.color_1_hex, kind="bar", ax=self.ax2)     # Independent
                        if self.chbx_shared_value.get():
                            self.ax2.bar(self.df_filtered_1[self.x1_col], self.df_filtered_1[self.y1_col], color=self.color_1_hex)     # Shared
                        if self.chbx_fixed_value.get():
                            self.ax2.bar(self.df_filtered_1["_row_order"], self.df_filtered_1[self.y1_col], color=self.color_1_hex)    # Fixed
                        self.color1_2nd_y_axis()
                    elif self.chbx1_ax3_value.get():    # 3rd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_1.plot(x=self.x1_col, y=self.y1_col, color=self.color_1_hex, kind="bar", ax=self.ax3)     # Independent
                        if self.chbx_shared_value.get():
                            self.ax3.bar(self.df_filtered_1[self.x1_col], self.df_filtered_1[self.y1_col], color=self.color_1_hex)     # Shared
                        if self.chbx_fixed_value.get():
                            self.ax3.bar(self.df_filtered_1["_row_order"], self.df_filtered_1[self.y1_col], color=self.color_1_hex)    # Fixed
                        self.color1_3rd_y_axis()
                    else:                               # Main Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_1.plot(x=self.x1_col, y=self.y1_col, color=self.color_1_hex, kind="bar", ax=self.ax)      # Independent
                        if self.chbx_shared_value.get():
                            self.ax.bar(self.df_filtered_1[self.x1_col], self.df_filtered_1[self.y1_col], color=self.color_1_hex)      # Shared
                        if self.chbx_fixed_value.get():
                            self.ax.bar(self.df_filtered_1["_row_order"], self.df_filtered_1[self.y1_col], color=self.color_1_hex)     # Fixed
                        self.color1_main_y_axis()
                    self.color1_main_x_axis()
                elif chart1 == "scatter":   # Plot Scatter ------------------------------------------------------------
                    if self.chbx1_ax2_value.get():      # 2nd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_1.plot.scatter(x=self.x1_col, y=self.y1_col, color=self.color_1_hex, ax=self.ax2)         # Independent
                        if self.chbx_shared_value.get():
                            self.ax2.scatter(self.df_filtered_1[self.x1_col], self.df_filtered_1[self.y1_col], color=self.color_1_hex) # Shared
                        if self.chbx_fixed_value.get():
                            self.ax2.scatter(self.df_filtered_1["_row_order"], self.df_filtered_1[self.y1_col], color=self.color_1_hex)# Fixed
                        self.color1_2nd_y_axis()
                    elif self.chbx1_ax3_value.get():    # 3rd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_1.plot.scatter(x=self.x1_col, y=self.y1_col, color=self.color_1_hex, ax=self.ax3)         # Independent
                        if self.chbx_shared_value.get():
                            self.ax3.scatter(self.df_filtered_1[self.x1_col], self.df_filtered_1[self.y1_col], color=self.color_1_hex) # Shared
                        if self.chbx_fixed_value.get():
                            self.ax3.scatter(self.df_filtered_1["_row_order"], self.df_filtered_1[self.y1_col], color=self.color_1_hex)# Fixed
                        self.color1_3rd_y_axis()
                    else:                               # Main Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_1.plot.scatter(x=self.x1_col, y=self.y1_col, color=self.color_1_hex, ax=self.ax)          # Independent
                        if self.chbx_shared_value.get():
                            self.ax.scatter(self.df_filtered_1[self.x1_col], self.df_filtered_1[self.y1_col], color=self.color_1_hex)  # Shared
                        if self.chbx_fixed_value.get():
                            self.ax.scatter(self.df_filtered_1["_row_order"], self.df_filtered_1[self.y1_col], color=self.color_1_hex) # Fixed
                        self.color1_main_y_axis()
                    self.color1_main_x_axis()
                elif chart1 == "hist":      # Plot Histogram ----------------------------------------------------------
                    if self.chbx1_ax2_value.get():      # 2nd Axis
                        self.df_filtered_1[self.x1_col].plot(kind="hist", color=self.color_1_hex, ax=self.ax2)                      
                        self.color1_2nd_y_axis()
                    elif self.chbx1_ax3_value.get():    # 3rd Axis
                        self.df_filtered_1[self.x1_col].plot(kind="hist", color=self.color_1_hex, ax=self.ax3)
                        self.color1_3rd_y_axis()
                    else:                               # Main Axis
                        self.df_filtered_1[self.x1_col].plot(kind="hist", color=self.color_1_hex, ax=self.ax)
                        self.color1_main_y_axis()
                    self.color1_main_x_axis()
            except Exception as e:
                messagebox.showerror("Plot Error", str(e))
                return
        
        # Plot configuration for Bar 2
        if self.chbx2_value.get():

            if chart2 != "hist" and (not self.x2_col or not self.y2_col):
                messagebox.showwarning("Missing Columns in Bar 2", "Select X and Y for this chart type.")
                return
            try:
                if chart2 == "line":        # Plot Line ---------------------------------------------------------------
                    if self.chbx2_ax2_value.get():      # 2nd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_2.plot(x=self.x2_col, y=self.y2_col, color=self.color_2_hex, kind="line", ax=self.ax2)    # Independent
                        if self.chbx_shared_value.get():
                            self.ax2.plot(self.df_filtered_2[self.x2_col], self.df_filtered_2[self.y2_col], color=self.color_2_hex)    # Shared
                        if self.chbx_fixed_value.get():
                            self.ax2.plot(self.df_filtered_2["_row_order"], self.df_filtered_2[self.y2_col], color=self.color_2_hex)   # Fixed
                        self.color2_2nd_y_axis()
                    elif self.chbx2_ax3_value.get():    # 3rd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_2.plot(x=self.x2_col, y=self.y2_col, color=self.color_2_hex, kind="line", ax=self.ax3)    # Independent
                        if self.chbx_shared_value.get():
                            self.ax3.plot(self.df_filtered_2[self.x2_col], self.df_filtered_2[self.y2_col], color=self.color_2_hex)    # Shared
                        if self.chbx_fixed_value.get():
                            self.ax3.plot(self.df_filtered_2["_row_order"], self.df_filtered_2[self.y2_col], color=self.color_2_hex)   # Fixed
                        self.color2_3rd_y_axis()
                    else:                               # Main Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_2.plot(x=self.x2_col, y=self.y2_col, color=self.color_2_hex, kind="line", ax=self.ax)     # Independent
                        if self.chbx_shared_value.get():
                            self.ax.plot(self.df_filtered_2[self.x2_col], self.df_filtered_2[self.y2_col], color=self.color_2_hex)     # Shared
                        if self.chbx_fixed_value.get():
                            self.ax.plot(self.df_filtered_2["_row_order"], self.df_filtered_2[self.y2_col], color=self.color_2_hex)    # Fixed
                        self.color2_main_y_axis()
                    self.color2_main_x_axis()
                elif chart2 == "bar":       # Plot Bar ----------------------------------------------------------------
                    if self.chbx2_ax2_value.get():      # 2nd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_2.plot(x=self.x2_col, y=self.y2_col, color=self.color_2_hex, kind="bar", ax=self.ax2)     # Independent
                        if self.chbx_shared_value.get():
                            self.ax2.bar(self.df_filtered_2[self.x2_col], self.df_filtered_2[self.y2_col], color=self.color_2_hex)     # Shared
                        if self.chbx_fixed_value.get():
                            self.ax2.bar(self.df_filtered_2["_row_order"], self.df_filtered_2[self.y2_col], color=self.color_2_hex)    # Fixed
                        self.color2_2nd_y_axis()
                    elif self.chbx2_ax3_value.get():    # 3rd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_2.plot(x=self.x2_col, y=self.y2_col, color=self.color_2_hex, kind="bar", ax=self.ax3)     # Independent
                        if self.chbx_shared_value.get():
                            self.ax3.bar(self.df_filtered_2[self.x2_col], self.df_filtered_2[self.y2_col], color=self.color_2_hex)     # Shared
                        if self.chbx_fixed_value.get():
                            self.ax3.bar(self.df_filtered_2["_row_order"], self.df_filtered_2[self.y2_col], color=self.color_2_hex)    # Fixed
                        self.color2_3rd_y_axis()
                    else:                               # Main Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_2.plot(x=self.x2_col, y=self.y2_col, color=self.color_2_hex, kind="bar", ax=self.ax)      # Independent
                        if self.chbx_shared_value.get():
                            self.ax.bar(self.df_filtered_2[self.x2_col], self.df_filtered_2[self.y2_col], color=self.color_2_hex)      # Shared
                        if self.chbx_fixed_value.get():
                            self.ax.bar(self.df_filtered_2["_row_order"], self.df_filtered_2[self.y2_col], color=self.color_2_hex)     # Fixed
                        self.color2_main_y_axis()
                    self.color2_main_x_axis()
                elif chart2 == "scatter":   # Plot Scatter ------------------------------------------------------------
                    if self.chbx2_ax2_value.get():      # 2nd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_2.plot.scatter(x=self.x2_col, y=self.y2_col, color=self.color_2_hex, ax=self.ax2)         # Independent
                        if self.chbx_shared_value.get():
                            self.ax2.scatter(self.df_filtered_2[self.x2_col], self.df_filtered_2[self.y2_col], color=self.color_2_hex) # Shared
                        if self.chbx_fixed_value.get():
                            self.ax2.scatter(self.df_filtered_2["_row_order"], self.df_filtered_2[self.y2_col], color=self.color_2_hex)# Fixed
                        self.color2_2nd_y_axis()
                    elif self.chbx2_ax3_value.get():    # 3rd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_2.plot.scatter(x=self.x2_col, y=self.y2_col, color=self.color_2_hex, ax=self.ax3)         # Independent
                        if self.chbx_shared_value.get():
                            self.ax3.scatter(self.df_filtered_2[self.x2_col], self.df_filtered_2[self.y2_col], color=self.color_2_hex) # Shared
                        if self.chbx_fixed_value.get():
                            self.ax3.scatter(self.df_filtered_2["_row_order"], self.df_filtered_2[self.y2_col], color=self.color_2_hex)# Fixed
                        self.color2_3rd_y_axis()
                    else:                               # Main Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_2.plot.scatter(x=self.x2_col, y=self.y2_col, color=self.color_2_hex, ax=self.ax)          # Independent
                        if self.chbx_shared_value.get():
                            self.ax.scatter(self.df_filtered_2[self.x2_col], self.df_filtered_2[self.y2_col], color=self.color_2_hex)  # Shared
                        if self.chbx_fixed_value.get():
                            self.ax.scatter(self.df_filtered_2["_row_order"], self.df_filtered_2[self.y2_col], color=self.color_2_hex) # Fixed
                        self.color2_main_y_axis()
                    self.color2_main_x_axis()
                elif chart2 == "hist":      # Plot Histogram ----------------------------------------------------------
                    if self.chbx2_ax2_value.get():      # 2nd Axis
                        self.df_filtered_2[self.x2_col].plot(kind="hist", color=self.color_2_hex, ax=self.ax2)
                        self.color2_2nd_y_axis()
                    elif self.chbx2_ax3_value.get():    # 3rd Axis
                        self.df_filtered_2[self.x2_col].plot(kind="hist", color=self.color_2_hex, ax=self.ax3)
                        self.color2_3rd_y_axis()
                    else:                               # Main Axis
                        self.df_filtered_2[self.x2_col].plot(kind="hist", color=self.color_2_hex, ax=self.ax)
                        self.color2_main_y_axis()
                    self.color2_main_x_axis()
            except Exception as e:
                messagebox.showerror("Plot Error", str(e))
                return
            
        # Plot configuration for Bar 3
        if self.chbx3_value.get():

            if chart3 != "hist" and (not self.x3_col or not self.y3_col):
                messagebox.showwarning("Missing Columns in Bar 3", "Select X and Y for this chart type.")
                return
            try:
                if chart3 == "line":        # Plot Line ---------------------------------------------------------------
                    if self.chbx3_ax2_value.get():      # 2nd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_3.plot(x=self.x3_col, y=self.y3_col, color=self.color_3_hex, kind="line", ax=self.ax2)    # Independent
                        if self.chbx_shared_value.get():
                            self.ax2.plot(self.df_filtered_3[self.x3_col], self.df_filtered_3[self.y3_col], color=self.color_3_hex)    # Shared
                        if self.chbx_fixed_value.get():
                            self.ax2.plot(self.df_filtered_3["_row_order"], self.df_filtered_3[self.y3_col], color=self.color_3_hex)   # Fixed
                        self.color3_2nd_y_axis()
                    elif self.chbx3_ax3_value.get():    # 3rd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_3.plot(x=self.x3_col, y=self.y3_col, color=self.color_3_hex, kind="line", ax=self.ax3)    # Independent
                        if self.chbx_shared_value.get():
                            self.ax3.plot(self.df_filtered_3[self.x3_col], self.df_filtered_3[self.y3_col], color=self.color_3_hex)    # Shared
                        if self.chbx_fixed_value.get():
                            self.ax3.plot(self.df_filtered_3["_row_order"], self.df_filtered_3[self.y3_col], color=self.color_3_hex)   # Fixed
                        self.color3_3rd_y_axis()
                    else:                               # Main Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_3.plot(x=self.x3_col, y=self.y3_col, color=self.color_3_hex, kind="line", ax=self.ax)     # Independent
                        if self.chbx_shared_value.get():
                            self.ax.plot(self.df_filtered_3[self.x3_col], self.df_filtered_3[self.y3_col], color=self.color_3_hex)     # Shared
                        if self.chbx_fixed_value.get():
                            self.ax.plot(self.df_filtered_3["_row_order"], self.df_filtered_3[self.y3_col], color=self.color_3_hex)    # Fixed
                        self.color3_main_y_axis()
                    self.color3_main_x_axis()
                elif chart3 == "bar":       # Plot Bar ----------------------------------------------------------------
                    if self.chbx3_ax2_value.get():      # 2nd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_3.plot(x=self.x3_col, y=self.y3_col, color=self.color_3_hex, kind="bar", ax=self.ax2)     # Independent
                        if self.chbx_shared_value.get():
                            self.ax2.bar(self.df_filtered_3[self.x3_col], self.df_filtered_3[self.y3_col], color=self.color_3_hex)     # Shared
                        if self.chbx_fixed_value.get():
                            self.ax2.bar(self.df_filtered_3["_row_order"], self.df_filtered_3[self.y3_col], color=self.color_3_hex)    # Fixed
                        self.color3_2nd_y_axis()
                    elif self.chbx3_ax3_value.get():    # 3rd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_3.plot(x=self.x3_col, y=self.y3_col, color=self.color_3_hex, kind="bar", ax=self.ax3)     # Independent
                        if self.chbx_shared_value.get():
                            self.ax3.bar(self.df_filtered_3[self.x3_col], self.df_filtered_3[self.y3_col], color=self.color_3_hex)     # Shared
                        if self.chbx_fixed_value.get():
                            self.ax3.bar(self.df_filtered_3["_row_order"], self.df_filtered_3[self.y3_col], color=self.color_3_hex)    # Fixed
                        self.color3_3rd_y_axis()
                    else:                               # Main Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_3.plot(x=self.x3_col, y=self.y3_col, color=self.color_3_hex, kind="bar", ax=self.ax)      # Independent
                        if self.chbx_shared_value.get():
                            self.ax.bar(self.df_filtered_3[self.x3_col], self.df_filtered_3[self.y3_col], color=self.color_3_hex)      # Shared
                        if self.chbx_fixed_value.get():
                            self.ax.bar(self.df_filtered_3["_row_order"], self.df_filtered_3[self.y3_col], color=self.color_3_hex)     # Fixed
                        self.color3_main_y_axis()
                    self.color3_main_x_axis()
                elif chart3 == "scatter":   # Plot Scatter ------------------------------------------------------------
                    if self.chbx3_ax2_value.get():      # 2nd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_3.plot.scatter(x=self.x3_col, y=self.y3_col, color=self.color_3_hex, ax=self.ax2)         # Independent
                        if self.chbx_shared_value.get():
                            self.ax2.scatter(self.df_filtered_3[self.x3_col], self.df_filtered_3[self.y3_col], color=self.color_3_hex) # Shared
                        if self.chbx_fixed_value.get():
                            self.ax2.scatter(self.df_filtered_3["_row_order"], self.df_filtered_3[self.y3_col], color=self.color_3_hex)# Fixed
                        self.color3_2nd_y_axis()
                    elif self.chbx3_ax3_value.get():    # 3rd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_3.plot.scatter(x=self.x3_col, y=self.y3_col, color=self.color_3_hex, ax=self.ax3)         # Independent
                        if self.chbx_shared_value.get():
                            self.ax3.scatter(self.df_filtered_3[self.x3_col], self.df_filtered_3[self.y3_col], color=self.color_3_hex) # Shared
                        if self.chbx_fixed_value.get():
                            self.ax3.scatter(self.df_filtered_3["_row_order"], self.df_filtered_3[self.y3_col], color=self.color_3_hex)# Fixed
                        self.color3_3rd_y_axis()
                    else:                               # Main Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_3.plot.scatter(x=self.x3_col, y=self.y3_col, color=self.color_3_hex, ax=self.ax)          # Independent
                        if self.chbx_shared_value.get():
                            self.ax.scatter(self.df_filtered_3[self.x3_col], self.df_filtered_3[self.y3_col], color=self.color_3_hex)  # Shared
                        if self.chbx_fixed_value.get():
                            self.ax.scatter(self.df_filtered_3["_row_order"], self.df_filtered_3[self.y3_col], color=self.color_3_hex) # Fixed
                        self.color3_main_y_axis()
                    self.color3_main_x_axis()
                elif chart3 == "hist":      # Plot Histogram ----------------------------------------------------------
                    if self.chbx3_ax2_value.get():      # 2nd Axis
                        self.df_filtered_3[self.x3_col].plot(kind="hist", color=self.color_3_hex, ax=self.ax2)
                        self.color3_2nd_y_axis()
                    elif self.chbx3_ax3_value.get():    # 3rd Axis
                        self.df_filtered_3[self.x3_col].plot(kind="hist", color=self.color_3_hex, ax=self.ax3)
                        self.color3_3rd_y_axis()
                    else:                               # Main Axis
                        self.df_filtered_3[self.x3_col].plot(kind="hist", color=self.color_3_hex, ax=self.ax)
                        self.color3_main_y_axis()
                    self.color3_main_x_axis()
            except Exception as e:
                messagebox.showerror("Plot Error", str(e))
                return
            
        # Plot configuration for Bar 4
        if self.chbx4_value.get():

            if chart4 != "hist" and (not self.x4_col or not self.y4_col):
                messagebox.showwarning("Missing Columns in Bar 4", "Select X and Y for this chart type.")
                return
            try:
                if chart4 == "line":        # Plot Line ---------------------------------------------------------------
                    if self.chbx4_ax2_value.get():      # 2nd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_4.plot(x=self.x4_col, y=self.y4_col, color=self.color_4_hex, kind="line", ax=self.ax2)    # Independent
                        if self.chbx_shared_value.get():
                            self.ax2.plot(self.df_filtered_4[self.x4_col], self.df_filtered_4[self.y4_col], color=self.color_4_hex)    # Shared
                        if self.chbx_fixed_value.get():
                            self.ax2.plot(self.df_filtered_4["_row_order"], self.df_filtered_4[self.y4_col], color=self.color_4_hex)   # Fixed
                        self.color4_2nd_y_axis()
                    elif self.chbx4_ax3_value.get():    # 3rd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_4.plot(x=self.x4_col, y=self.y4_col, color=self.color_4_hex, kind="line", ax=self.ax3)    # Independent
                        if self.chbx_shared_value.get():
                            self.ax3.plot(self.df_filtered_4[self.x4_col], self.df_filtered_4[self.y4_col], color=self.color_4_hex)    # Shared
                        if self.chbx_fixed_value.get():
                            self.ax3.plot(self.df_filtered_4["_row_order"], self.df_filtered_4[self.y4_col], color=self.color_4_hex)   # Fixed
                        self.color4_3rd_y_axis()
                    else:                               # Main Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_4.plot(x=self.x4_col, y=self.y4_col, color=self.color_4_hex, kind="line", ax=self.ax)     # Independent
                        if self.chbx_shared_value.get():
                            self.ax.plot(self.df_filtered_4[self.x4_col], self.df_filtered_4[self.y4_col], color=self.color_4_hex)     # Shared
                        if self.chbx_fixed_value.get():
                            self.ax.plot(self.df_filtered_4["_row_order"], self.df_filtered_4[self.y4_col], color=self.color_4_hex)    # Fixed
                        self.color4_main_y_axis()
                    self.color4_main_x_axis()
                elif chart4 == "bar":       # Plot Bar ----------------------------------------------------------------
                    if self.chbx4_ax2_value.get():      # 2nd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_4.plot(x=self.x4_col, y=self.y4_col, color=self.color_4_hex, kind="bar", ax=self.ax2)     # Independent
                        if self.chbx_shared_value.get():
                            self.ax2.bar(self.df_filtered_4[self.x4_col], self.df_filtered_4[self.y4_col], color=self.color_4_hex)     # Shared
                        if self.chbx_fixed_value.get():
                            self.ax2.bar(self.df_filtered_4["_row_order"], self.df_filtered_4[self.y4_col], color=self.color_4_hex)    # Fixed
                        self.color4_2nd_y_axis()
                    elif self.chbx4_ax3_value.get():    # 3rd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_4.plot(x=self.x4_col, y=self.y4_col, color=self.color_4_hex, kind="bar", ax=self.ax3)     # Independent
                        if self.chbx_shared_value.get():
                            self.ax3.bar(self.df_filtered_4[self.x4_col], self.df_filtered_4[self.y4_col], color=self.color_4_hex)     # Shared
                        if self.chbx_fixed_value.get():
                            self.ax3.bar(self.df_filtered_4["_row_order"], self.df_filtered_4[self.y4_col], color=self.color_4_hex)    # Fixed
                        self.color4_3rd_y_axis()
                    else:                               # Main Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_4.plot(x=self.x4_col, y=self.y4_col, color=self.color_4_hex, kind="bar", ax=self.ax)      # Independent
                        if self.chbx_shared_value.get():
                            self.ax.bar(self.df_filtered_4[self.x4_col], self.df_filtered_4[self.y4_col], color=self.color_4_hex)      # Shared
                        if self.chbx_fixed_value.get():
                            self.ax.bar(self.df_filtered_4["_row_order"], self.df_filtered_4[self.y4_col], color=self.color_4_hex)     # Fixed
                        self.color4_main_y_axis()
                    self.color4_main_x_axis()
                elif chart4 == "scatter":   # Plot Scatter ------------------------------------------------------------
                    if self.chbx4_ax2_value.get():      # 2nd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_4.plot.scatter(x=self.x4_col, y=self.y4_col, color=self.color_4_hex, ax=self.ax2)         # Independent
                        if self.chbx_shared_value.get():
                            self.ax2.scatter(self.df_filtered_4[self.x4_col], self.df_filtered_4[self.y4_col], color=self.color_4_hex) # Shared
                        if self.chbx_fixed_value.get():
                            self.ax2.scatter(self.df_filtered_4["_row_order"], self.df_filtered_4[self.y4_col], color=self.color_4_hex)# Fixed
                        self.color4_2nd_y_axis()
                    elif self.chbx4_ax3_value.get():    # 3rd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_4.plot.scatter(x=self.x4_col, y=self.y4_col, color=self.color_4_hex, ax=self.ax3)         # Independent
                        if self.chbx_shared_value.get():
                            self.ax3.scatter(self.df_filtered_4[self.x4_col], self.df_filtered_4[self.y4_col], color=self.color_4_hex) # Shared
                        if self.chbx_fixed_value.get():
                            self.ax3.scatter(self.df_filtered_4["_row_order"], self.df_filtered_4[self.y4_col], color=self.color_4_hex)# Fixed
                        self.color4_3rd_y_axis()
                    else:                               # Main Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_4.plot.scatter(x=self.x4_col, y=self.y4_col, color=self.color_4_hex, ax=self.ax)          # Independent
                        if self.chbx_shared_value.get():
                            self.ax.scatter(self.df_filtered_4[self.x4_col], self.df_filtered_4[self.y4_col], color=self.color_4_hex)  # Shared
                        if self.chbx_fixed_value.get():
                            self.ax.scatter(self.df_filtered_4["_row_order"], self.df_filtered_4[self.y4_col], color=self.color_4_hex) # Fixed
                        self.color4_main_y_axis()
                    self.color4_main_x_axis()
                elif chart4 == "hist":      # Plot Histogram ----------------------------------------------------------
                    if self.chbx4_ax2_value.get():      # 2nd Axis
                        self.df_filtered_4[self.x4_col].plot(kind="hist", color=self.color_4_hex, ax=self.ax2)
                        self.color4_2nd_y_axis()
                    elif self.chbx4_ax3_value.get():    # 3rd Axis
                        self.df_filtered_4[self.x4_col].plot(kind="hist", color=self.color_4_hex, ax=self.ax3)
                        self.color4_3rd_y_axis()
                    else:                               # Main Axis
                        self.df_filtered_4[self.x4_col].plot(kind="hist", color=self.color_4_hex, ax=self.ax)
                        self.color4_main_y_axis()
                    self.color4_main_x_axis()
            except Exception as e:
                messagebox.showerror("Plot Error", str(e))
                return
            
        # Plot configuration for Bar 5
        if self.chbx5_value.get():

            if chart5 != "hist" and (not self.x5_col or not self.y5_col):
                messagebox.showwarning("Missing Columns in Bar 5", "Select X and Y for this chart type.")
                return
            try:
                if chart5 == "line":        # Plot Line ---------------------------------------------------------------
                    if self.chbx5_ax2_value.get():      # 2nd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_5.plot(x=self.x5_col, y=self.y5_col, color=self.color_5_hex, kind="line", ax=self.ax2)    # Independent
                        if self.chbx_shared_value.get():
                            self.ax2.plot(self.df_filtered_5[self.x5_col], self.df_filtered_5[self.y5_col], color=self.color_5_hex)    # Shared
                        if self.chbx_fixed_value.get():
                            self.ax2.plot(self.df_filtered_5["_row_order"], self.df_filtered_5[self.y5_col], color=self.color_5_hex)   # Fixed
                        self.color5_2nd_y_axis()
                    elif self.chbx5_ax3_value.get():    # 3rd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_5.plot(x=self.x5_col, y=self.y5_col, color=self.color_5_hex, kind="line", ax=self.ax3)    # Independent
                        if self.chbx_shared_value.get():
                            self.ax3.plot(self.df_filtered_5[self.x5_col], self.df_filtered_5[self.y5_col], color=self.color_5_hex)    # Shared
                        if self.chbx_fixed_value.get():
                            self.ax3.plot(self.df_filtered_5["_row_order"], self.df_filtered_5[self.y5_col], color=self.color_5_hex)   # Fixed
                        self.color5_3rd_y_axis()
                    else:                               # Main Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_5.plot(x=self.x5_col, y=self.y5_col, color=self.color_5_hex, kind="line", ax=self.ax)     # Independent
                        if self.chbx_shared_value.get():
                            self.ax.plot(self.df_filtered_5[self.x5_col], self.df_filtered_5[self.y5_col], color=self.color_5_hex)     # Shared
                        if self.chbx_fixed_value.get():
                            self.ax.plot(self.df_filtered_5["_row_order"], self.df_filtered_5[self.y5_col], color=self.color_5_hex)    # Fixed
                        self.color5_main_y_axis()
                    self.color5_main_x_axis()
                elif chart5 == "bar":       # Plot Bar ----------------------------------------------------------------
                    if self.chbx5_ax2_value.get():      # 2nd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_5.plot(x=self.x5_col, y=self.y5_col, color=self.color_5_hex, kind="bar", ax=self.ax2)     # Independent
                        if self.chbx_shared_value.get():
                            self.ax2.bar(self.df_filtered_5[self.x5_col], self.df_filtered_5[self.y5_col], color=self.color_5_hex)     # Shared
                        if self.chbx_fixed_value.get():
                            self.ax2.bar(self.df_filtered_5["_row_order"], self.df_filtered_5[self.y5_col], color=self.color_5_hex)    # Fixed
                        self.color5_2nd_y_axis()
                    elif self.chbx5_ax3_value.get():    # 3rd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_5.plot(x=self.x5_col, y=self.y5_col, color=self.color_5_hex, kind="bar", ax=self.ax3)     # Independent
                        if self.chbx_shared_value.get():
                            self.ax3.bar(self.df_filtered_5[self.x5_col], self.df_filtered_5[self.y5_col], color=self.color_5_hex)     # Shared
                        if self.chbx_fixed_value.get():
                            self.ax3.bar(self.df_filtered_5["_row_order"], self.df_filtered_5[self.y5_col], color=self.color_5_hex)    # Fixed
                        self.color5_3rd_y_axis()
                    else:                               # Main Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_5.plot(x=self.x5_col, y=self.y5_col, color=self.color_5_hex, kind="bar", ax=self.ax)      # Independent
                        if self.chbx_shared_value.get():
                            self.ax.bar(self.df_filtered_5[self.x5_col], self.df_filtered_5[self.y5_col], color=self.color_5_hex)      # Shared
                        if self.chbx_fixed_value.get():
                            self.ax.bar(self.df_filtered_5["_row_order"], self.df_filtered_5[self.y5_col], color=self.color_5_hex)     # Fixed
                        self.color5_main_y_axis()
                    self.color5_main_x_axis()
                elif chart5 == "scatter":   # Plot Scatter ------------------------------------------------------------
                    if self.chbx5_ax2_value.get():      # 2nd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_5.plot.scatter(x=self.x5_col, y=self.y5_col, color=self.color_5_hex, ax=self.ax2)         # Independent
                        if self.chbx_shared_value.get():
                            self.ax2.scatter(self.df_filtered_5[self.x5_col], self.df_filtered_5[self.y5_col], color=self.color_5_hex) # Shared
                        if self.chbx_fixed_value.get():
                            self.ax2.scatter(self.df_filtered_5["_row_order"], self.df_filtered_5[self.y5_col], color=self.color_5_hex)# Fixed
                        self.color5_2nd_y_axis()
                    elif self.chbx5_ax3_value.get():    # 3rd Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_5.plot.scatter(x=self.x5_col, y=self.y5_col, color=self.color_5_hex, ax=self.ax3)         # Independent
                        if self.chbx_shared_value.get():
                            self.ax3.scatter(self.df_filtered_5[self.x5_col], self.df_filtered_5[self.y5_col], color=self.color_5_hex) # Shared
                        if self.chbx_fixed_value.get():
                            self.ax3.scatter(self.df_filtered_5["_row_order"], self.df_filtered_5[self.y5_col], color=self.color_5_hex)# Fixed
                        self.color5_3rd_y_axis()
                    else:                               # Main Axis
                        if self.chbx_independent_value.get():
                            self.df_filtered_5.plot.scatter(x=self.x5_col, y=self.y5_col, color=self.color_5_hex, ax=self.ax)          # Independent
                        if self.chbx_shared_value.get():
                            self.ax.scatter(self.df_filtered_5[self.x5_col], self.df_filtered_5[self.y5_col], color=self.color_5_hex)  # Shared
                        if self.chbx_fixed_value.get():
                            self.ax.scatter(self.df_filtered_5["_row_order"], self.df_filtered_5[self.y5_col], color=self.color_5_hex) # Fixed
                        self.color5_main_y_axis()
                    self.color5_main_x_axis()
                elif chart5 == "hist":      # Plot Histogram ----------------------------------------------------------
                    if self.chbx5_ax2_value.get():      # 2nd Axis
                        self.df_filtered_5[self.x5_col].plot(kind="hist", color=self.color_5_hex, ax=self.ax2)
                        self.color5_2nd_y_axis()
                    elif self.chbx5_ax3_value.get():    # 3rd Axis
                        self.df_filtered_5[self.x5_col].plot(kind="hist", color=self.color_5_hex, ax=self.ax3)
                        self.color5_3rd_y_axis()
                    else:                               # Main Axis
                        self.df_filtered_5[self.x5_col].plot(kind="hist", color=self.color_5_hex, ax=self.ax)
                        self.color5_main_y_axis()
                    self.color5_main_x_axis()
            except Exception as e:
                messagebox.showerror("Plot Error", str(e))
                return
            

        # Show chart in Tkinter
        plt.show()

    # Functions to assign color to different axis (if exsts) for configuration bar 1
    def color1_main_y_axis(self):
        self.ax.tick_params(axis='y', colors=self.color_1_hex)
        self.ax.set_ylabel(self.y1_col, color=self.color_1_hex)
    def color1_2nd_y_axis(self):
        self.ax2.tick_params(axis='y', colors=self.color_1_hex)
        self.ax2.set_ylabel(self.y1_col, color=self.color_1_hex)
    def color1_3rd_y_axis(self):
        self.ax3.spines['right'].set_position(('outward', 60))
        self.ax3.tick_params(axis='y', colors=self.color_1_hex)
        self.ax3.set_ylabel(self.y1_col, color=self.color_1_hex)
    def color1_main_x_axis(self): 
        self.ax.set_xlabel(self.x1_col)  
        self.ax.tick_params(axis='x', colors='black')
    
    # Functions to assign color to different axis (if exsts) for configuration bar 2
    def color2_main_y_axis(self):
        self.ax.tick_params(axis='y', colors=self.color_2_hex)
        self.ax.set_ylabel(self.y2_col, color=self.color_2_hex)
    def color2_2nd_y_axis(self):
        self.ax2.tick_params(axis='y', colors=self.color_2_hex)
        self.ax2.set_ylabel(self.y2_col, color=self.color_2_hex)
    def color2_3rd_y_axis(self):
        self.ax3.spines['right'].set_position(('outward', 60))
        self.ax3.tick_params(axis='y', colors=self.color_2_hex)
        self.ax3.set_ylabel(self.y2_col, color=self.color_2_hex)
    def color2_main_x_axis(self): 
        self.ax.set_xlabel(self.x2_col)  
        self.ax.tick_params(axis='x', colors='black')

    # Functions to assign color to different axis (if exsts) for configuration bar 3
    def color3_main_y_axis(self):
        self.ax.tick_params(axis='y', colors=self.color_3_hex)
        self.ax.set_ylabel(self.y3_col, color=self.color_3_hex)
    def color3_2nd_y_axis(self):
        self.ax2.tick_params(axis='y', colors=self.color_3_hex)
        self.ax2.set_ylabel(self.y3_col, color=self.color_3_hex)
    def color3_3rd_y_axis(self):
        self.ax3.spines['right'].set_position(('outward', 60))
        self.ax3.tick_params(axis='y', colors=self.color_3_hex)
        self.ax3.set_ylabel(self.y3_col, color=self.color_3_hex)
    def color3_main_x_axis(self): 
        self.ax.set_xlabel(self.x3_col)  
        self.ax.tick_params(axis='x', colors='black')

    # Functions to assign color to different axis (if exsts) for configuration bar 4
    def color4_main_y_axis(self):
        self.ax.tick_params(axis='y', colors=self.color_4_hex)
        self.ax.set_ylabel(self.y4_col, color=self.color_4_hex)
    def color4_2nd_y_axis(self):
        self.ax2.tick_params(axis='y', colors=self.color_4_hex)
        self.ax2.set_ylabel(self.y4_col, color=self.color_4_hex)
    def color4_3rd_y_axis(self):
        self.ax3.spines['right'].set_position(('outward', 60))
        self.ax3.tick_params(axis='y', colors=self.color_4_hex)
        self.ax3.set_ylabel(self.y4_col, color=self.color_4_hex)
    def color4_main_x_axis(self): 
        self.ax.set_xlabel(self.x4_col)  
        self.ax.tick_params(axis='x', colors='black')
    
    # Functions to assign color to different axis (if exsts) for configuration bar 5
    def color5_main_y_axis(self):
        self.ax.tick_params(axis='y', colors=self.color_5_hex)
        self.ax.set_ylabel(self.y5_col, color=self.color_5_hex)
    def color5_2nd_y_axis(self):
        self.ax2.tick_params(axis='y', colors=self.color_5_hex)
        self.ax2.set_ylabel(self.y5_col, color=self.color_5_hex)
    def color5_3rd_y_axis(self):
        self.ax3.spines['right'].set_position(('outward', 60))
        self.ax3.tick_params(axis='y', colors=self.color_5_hex)
        self.ax3.set_ylabel(self.y5_col, color=self.color_5_hex)
    def color5_main_x_axis(self): 
        self.ax.set_xlabel(self.x5_col)  
        self.ax.tick_params(axis='x', colors='black')

    # Open Previsualizer Funcion
    def open_previsualizer(self):

        # If there is no CSV selected, the process is aborted
        if self.df is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return
        # Opening the window and sending the DataFrame to be used there
        CSVPreVisualizer(self.root, self.df)

    # Functions for filter 1 *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    # Open Filter Window Funcion for Bar 1
    def open_filter1(self):
        # If there is no CSV selected, the process is aborted
        if self.df is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return
        # Opening the window and sending the DataFrame to be used there
        Filter1(self, self.df, self.data_1)
    
    # Editing the filter for Bar 1
    def edit_filter1(self):

        # If there is no CSV selected, the process is aborted
        if self.df is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return
        
        # If there is no data stored, the process is aborted
        if not self.data_1:
            messagebox.showwarning("No Filter to edit", "Please add a filter first.")
            return
        else:
            Filter1(self, self.df, self.data_1)

    # Removing the filter for bar 1
    def remove_filter1(self):
        # If there is no data stored, the process is aborted
        if not self.data_1:
            messagebox.showwarning("No Filter to remove", "Please add a filter first.")
            return
        else:
            # Confirmation before deleting the filter
            self.answer = messagebox.askyesno(title="You are deleting a filter!",parent=self.root, message="Are you sure you want to delete this filter?")
            if self.answer:
                self.clear_filter1()
            else:
                return
            
    # Clearing the filter 1
    def clear_filter1(self):
        self.data_1.clear()
        self.filter_prompt_1 = ""
        self.lbl_1_filter.config(text="None")

    # Saving the info obtained in the filter window
    def write_filter_1(self):        
        self.lbl_1_filter.config(text=self.data_1)
    # END Functions for filter 1 *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

    # Functions for filter 2 *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    # Open Filter Window Funcion for Bar 2
    def open_filter2(self):
        # If there is no CSV selected, the process is aborted
        if self.df is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return
        # Opening the window and sending the DataFrame to be used there
        Filter2(self, self.df, self.data_2)
    
    # Editing the filter for Bar 2
    def edit_filter2(self):

        # If there is no CSV selected, the process is aborted
        if self.df is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return
        
        # If there is no data stored, the process is aborted
        if not self.data_2:
            messagebox.showwarning("No Filter to edit", "Please add a filter first.")
            return
        else:
            Filter2(self, self.df, self.data_2)

    # Removing the filter for bar 2
    def remove_filter2(self):
        # If there is no data stored, the process is aborted
        if not self.data_2:
            messagebox.showwarning("No Filter to remove", "Please add a filter first.")
            return
        else:
            # Confirmation before deleting the filter
            self.answer = messagebox.askyesno(title="You are deleting a filter!",parent=self.root, message="Are you sure you want to delete this filter?")
            if self.answer:
                self.clear_filter2()
            else:
                return
            
    # Clearing the filter 2
    def clear_filter2(self):
        self.data_2.clear()
        self.filter_prompt_2 = ""
        self.lbl_2_filter.config(text="None")

    # Saving the info obtained in the filter window
    def write_filter_2(self):        
        self.lbl_2_filter.config(text=self.data_2)
    # END Functions for filter 2 *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

    # Functions for filter 3 *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    # Open Filter Window Funcion for Bar 3
    def open_filter3(self):
        # If there is no CSV selected, the process is aborted
        if self.df is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return
        # Opening the window and sending the DataFrame to be used there
        Filter3(self, self.df, self.data_3)
    
    # Editing the filter for Bar 3
    def edit_filter3(self):

        # If there is no CSV selected, the process is aborted
        if self.df is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return
        
        # If there is no data stored, the process is aborted
        if not self.data_3:
            messagebox.showwarning("No Filter to edit", "Please add a filter first.")
            return
        else:
            Filter3(self, self.df, self.data_3)

    # Removing the filter for bar 3
    def remove_filter3(self):
        # If there is no data stored, the process is aborted
        if not self.data_3:
            messagebox.showwarning("No Filter to remove", "Please add a filter first.")
            return
        else:
            # Confirmation before deleting the filter
            self.answer = messagebox.askyesno(title="You are deleting a filter!",parent=self.root, message="Are you sure you want to delete this filter?")
            if self.answer:
                self.clear_filter3()
            else:
                return
            
    # Clearing the filter 3
    def clear_filter3(self):
        self.data_3.clear()
        self.filter_prompt_3 = ""
        self.lbl_3_filter.config(text="None")

    # Saving the info obtained in the filter window
    def write_filter_3(self):        
        self.lbl_3_filter.config(text=self.data_3)
    # END Functions for filter 3 *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

    # Functions for filter 4 *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    # Open Filter Window Funcion for Bar 4
    def open_filter4(self):
        # If there is no CSV selected, the process is aborted
        if self.df is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return
        # Opening the window and sending the DataFrame to be used there
        Filter4(self, self.df, self.data_4)
    
    # Editing the filter for Bar 4
    def edit_filter4(self):

        # If there is no CSV selected, the process is aborted
        if self.df is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return
        
        # If there is no data stored, the process is aborted
        if not self.data_4:
            messagebox.showwarning("No Filter to edit", "Please add a filter first.")
            return
        else:
            Filter4(self, self.df, self.data_4)

    # Removing the filter for Bar 4
    def remove_filter4(self):
        # If there is no data stored, the process is aborted
        if not self.data_4:
            messagebox.showwarning("No Filter to remove", "Please add a filter first.")
            return
        else:
            # Confirmation before deleting the filter
            self.answer = messagebox.askyesno(title="You are deleting a filter!",parent=self.root, message="Are you sure you want to delete this filter?")
            if self.answer:
                self.clear_filter4()
            else:
                return
            
    # Clearing the filter 4
    def clear_filter4(self):
        self.data_4.clear()
        self.filter_prompt_4 = ""
        self.lbl_4_filter.config(text="None")

    # Saving the info obtained in the filter window
    def write_filter_4(self):        
        self.lbl_4_filter.config(text=self.data_4)
    # END Functions for filter 4 *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

    # Functions for filter 5 *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    # Open Filter Window Funcion for Bar 5
    def open_filter5(self):
        # If there is no CSV selected, the process is aborted
        if self.df is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return
        # Opening the window and sending the DataFrame to be used there
        Filter5(self, self.df, self.data_5)
    
    # Editing the filter for Bar 5
    def edit_filter5(self):

        # If there is no CSV selected, the process is aborted
        if self.df is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return
        
        # If there is no data stored, the process is aborted
        if not self.data_5:
            messagebox.showwarning("No Filter to edit", "Please add a filter first.")
            return
        else:
            Filter5(self, self.df, self.data_5)

    # Removing the filter for Bar 5
    def remove_filter5(self):
        # If there is no data stored, the process is aborted
        if not self.data_5:
            messagebox.showwarning("No Filter to remove", "Please add a filter first.")
            return
        else:
            # Confirmation before deleting the filter
            self.answer = messagebox.askyesno(title="You are deleting a filter!",parent=self.root, message="Are you sure you want to delete this filter?")
            if self.answer:
                self.clear_filter5()
            else:
                return
            
    # Clearing the filter 5
    def clear_filter5(self):
        self.data_5.clear()
        self.filter_prompt_5 = ""
        self.lbl_5_filter.config(text="None")

    # Saving the info obtained in the filter window
    def write_filter_5(self):        
        self.lbl_5_filter.config(text=self.data_5)
    # END Functions for filter 5 *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

    # Saving templates as json files
    def save_settings(self):
        if not self.df is None:
            # Collecting the data
            settings = {
                    # X Axis configuration
                "chbx_independent_option": self.chbx_independent_value.get(),
                "chbx_shared_option": self.chbx_shared_value.get(),
                "chbx_fixed_option": self.chbx_fixed_value.get(),
                    # 1
                "1_chbx_status": self.chbx1_value.get(),
                "1_x_axis": self.x1_var.get(),
                "1_y_axis": self.y1_var.get(),
                "1_chart_type": self.chr1_type.get(),
                "1_color_hex": self.color_1_hex,
                "1_2nd_axis_status": self.chbx1_ax2_value.get(),
                "1_3rd_axis_status": self.chbx1_ax3_value.get(),
                "1_data": self.data_1,
                "1_filter_prompt": self.filter_prompt_1,
                    # 2
                "2_chbx_status": self.chbx2_value.get(),
                "2_x_axis": self.x2_var.get(),
                "2_y_axis": self.y2_var.get(),
                "2_chart_type": self.chr2_type.get(),
                "2_color_hex": self.color_2_hex,
                "2_2nd_axis_status": self.chbx2_ax2_value.get(),
                "2_3rd_axis_status": self.chbx2_ax3_value.get(),
                "2_data": self.data_2,
                "2_filter_prompt": self.filter_prompt_2,
                    # 3
                "3_chbx_status": self.chbx3_value.get(),
                "3_x_axis": self.x3_var.get(),
                "3_y_axis": self.y3_var.get(),
                "3_chart_type": self.chr3_type.get(),
                "3_color_hex": self.color_3_hex,
                "3_2nd_axis_status": self.chbx3_ax2_value.get(),
                "3_3rd_axis_status": self.chbx3_ax3_value.get(),
                "3_data": self.data_3,
                "3_filter_prompt": self.filter_prompt_3,
                    # 4
                "4_chbx_status": self.chbx4_value.get(),
                "4_x_axis": self.x4_var.get(),
                "4_y_axis": self.y4_var.get(),
                "4_chart_type": self.chr4_type.get(),
                "4_color_hex": self.color_4_hex,
                "4_2nd_axis_status": self.chbx4_ax2_value.get(),
                "4_3rd_axis_status": self.chbx4_ax3_value.get(),
                "4_data": self.data_4,
                "4_filter_prompt": self.filter_prompt_4,
                    # 5
                "5_chbx_status": self.chbx5_value.get(),
                "5_x_axis": self.x5_var.get(),
                "5_y_axis": self.y5_var.get(),
                "5_chart_type": self.chr5_type.get(),
                "5_color_hex": self.color_5_hex,
                "5_2nd_axis_status": self.chbx5_ax2_value.get(),
                "5_3rd_axis_status": self.chbx5_ax3_value.get(),
                "5_data": self.data_5,
                "5_filter_prompt": self.filter_prompt_5
            }

            # Let user choose where to save the JSON file
            self.json_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], title="Save Settings File")

            if self.json_path:
                try:
                    with open(self.json_path, "w") as f:
                        json.dump(settings, f, indent=4)
                    messagebox.showinfo("Saved", f"Settings saved to {self.json_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not save settings:\n{e}")
        else:
            messagebox.showwarning("No Data", "Load a CSV before saving settings.")
    
    def load_settings(self):
        # Choosing the file
        self.json_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], title="Open Settings File")

        if self.json_path:  # Only proceed if the user picked a file
            try:
                with open(self.json_path, "r") as f:
                    settings = json.load(f)
                # Apply the settings saved
                    # X Axis configuration
                self.chbx_independent_value.set(settings.get("chbx_independent_option", "")),
                self.chbx_shared_value.set(settings.get("chbx_shared_option", "")),
                self.chbx_fixed_value.set(settings.get("chbx_fixed_option", "")),
                    # bar 1
                self.chbx1_value.set(settings.get("1_chbx_status", ""))
                self.chbx1_change()
                self.x1_var.set(settings.get("1_x_axis", ""))
                self.y1_var.set(settings.get("1_y_axis", ""))
                self.chr1_type.set(settings.get("1_chart_type", ""))
                self.color_1_hex = settings.get("1_color_hex", "")
                self.btn_color_1.config(bg=self.color_1_hex)
                self.chbx1_ax2_value.set(settings.get("1_2nd_axis_status", ""))
                self.chbx1_ax3_value.set(settings.get("1_3rd_axis_status", ""))
                if len(settings.get("1_data", "")) > 0:
                    self.data_1 = settings.get("1_data", "")
                    self.lbl_1_filter.config(text=self.data_1)
                    self.filter_prompt_1 = settings.get("1_filter_prompt", "")
                    # Bar 2
                self.chbx2_value.set(settings.get("2_chbx_status", ""))
                self.chbx2_change()
                self.x2_var.set(settings.get("2_x_axis", ""))
                self.y2_var.set(settings.get("2_y_axis", ""))
                self.chr2_type.set(settings.get("2_chart_type", ""))
                self.color_2_hex = settings.get("2_color_hex", "")
                self.btn_color_2.config(bg=self.color_2_hex)
                self.chbx2_ax2_value.set(settings.get("2_2nd_axis_status", ""))
                self.chbx2_ax3_value.set(settings.get("2_3rd_axis_status", ""))
                if len(settings.get("2_data", "")) > 0:
                    self.data_2 = settings.get("2_data", "")
                    self.lbl_2_filter.config(text=self.data_2)
                    self.filter_prompt_2 = settings.get("2_filter_prompt", "")
                    # Bar 3
                self.chbx3_value.set(settings.get("3_chbx_status", ""))
                self.chbx3_change()
                self.x3_var.set(settings.get("3_x_axis", ""))
                self.y3_var.set(settings.get("3_y_axis", ""))
                self.chr3_type.set(settings.get("3_chart_type", ""))
                self.color_3_hex = settings.get("3_color_hex", "")
                self.btn_color_3.config(bg=self.color_3_hex)
                self.chbx3_ax2_value.set(settings.get("3_2nd_axis_status", ""))
                self.chbx3_ax3_value.set(settings.get("3_3rd_axis_status", ""))
                if len(settings.get("3_data", "")) > 0:
                    self.data_3 = settings.get("3_data", "")
                    self.lbl_3_filter.config(text=self.data_3)
                    self.filter_prompt_3 = settings.get("3_filter_prompt", "")
                    # Bar 4
                self.chbx4_value.set(settings.get("4_chbx_status", ""))
                self.chbx4_change()
                self.x4_var.set(settings.get("4_x_axis", ""))
                self.y4_var.set(settings.get("4_y_axis", ""))
                self.chr4_type.set(settings.get("4_chart_type", ""))
                self.color_4_hex = settings.get("4_color_hex", "")
                self.btn_color_4.config(bg=self.color_4_hex)
                self.chbx4_ax2_value.set(settings.get("4_2nd_axis_status", ""))
                self.chbx4_ax3_value.set(settings.get("4_3rd_axis_status", ""))
                if len(settings.get("4_data", "")) > 0:
                    self.data_4 = settings.get("4_data", "")
                    self.lbl_4_filter.config(text=self.data_4)
                    self.filter_prompt_4 = settings.get("4_filter_prompt", "")
                    # Bar 5
                self.chbx5_value.set(settings.get("5_chbx_status", ""))
                self.chbx5_change()
                self.x5_var.set(settings.get("5_x_axis", ""))
                self.y5_var.set(settings.get("5_y_axis", ""))
                self.chr5_type.set(settings.get("5_chart_type", ""))
                self.color_5_hex = settings.get("5_color_hex", "")
                self.btn_color_5.config(bg=self.color_5_hex)
                self.chbx5_ax2_value.set(settings.get("5_2nd_axis_status", ""))
                self.chbx5_ax3_value.set(settings.get("5_3rd_axis_status", ""))
                if len(settings.get("5_data", "")) > 0:
                    self.data_5 = settings.get("5_data", "")
                    self.lbl_5_filter.config(text=self.data_5)
                    self.filter_prompt_5 = settings.get("5_filter_prompt", "")

                # Notify the user that the load was correct
                messagebox.showinfo("Loaded", f"Settings loaded from {self.json_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load settings:\n{e}")

    # Clear all settings
    def reset_app(self):
        
        self.x1_var.set("")
        self.x2_var.set("")
        self.x3_var.set("")
        self.x4_var.set("")
        self.x5_var.set("")
        self.y1_var.set("")
        self.y2_var.set("")
        self.y3_var.set("")
        self.y4_var.set("")
        self.y5_var.set("")
        self.chr1_type.set("")
        self.chr2_type.set("")
        self.chr3_type.set("")
        self.chr4_type.set("")
        self.chr5_type.set("")
        self.btn_color_1.config(bg='blue')
        self.btn_color_2.config(bg='red')
        self.btn_color_3.config(bg='green')
        self.btn_color_4.config(bg='orange')
        self.btn_color_5.config(bg='black')
        self.data_1.clear()
        self.data_2.clear()
        self.data_3.clear()
        self.data_4.clear()
        self.data_5.clear()
        self.filter_prompt_1 = ""
        self.filter_prompt_2 = ""
        self.filter_prompt_3 = ""
        self.filter_prompt_4 = ""
        self.filter_prompt_5 = ""
        self.lbl_1_filter.config(text="None")
        self.lbl_2_filter.config(text="None")
        self.lbl_3_filter.config(text="None")
        self.lbl_4_filter.config(text="None")
        self.lbl_5_filter.config(text="None")
        self.setup_ui()

# Class to the CSV previsualizer window
class CSVPreVisualizer:
    
    # Initialization Function
    def __init__(self, parent, df, title="CSV Previsualizer"):

        # Window Characteristics
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.w_win = 800
        self.h_win = 600
        self.wtotal = root.winfo_screenwidth()
        self.htotal = root.winfo_screenheight()
        self.pwidth = round(self.wtotal/2-self.w_win/2)
        self.pheight = round(self.htotal/2-self.h_win/2)
        self.window.geometry(str(self.w_win)+"x"+str(self.h_win)+"+"+str(self.pwidth)+"+"+str(self.pheight))

        # Creating the DataFrame (this came from the previous class)
        self.df = df

        # Launching the UI
        self.setup_ui()
    
        
    # User Interface Function
    def setup_ui(self):

        # Frame for organization
        frame = ttk.Frame(self.window, padding="20")
        frame.pack(fill="both", expand=True)

        # Container frame for Treeview + scrollbars
        container = ttk.Frame(frame)
        container.pack(fill="both", expand=True)

        # Treeview widget
        self.tree = ttk.Treeview(container, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbars
        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        # Configure grid weights so tree expands properly
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Clear previous table
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(self.df.columns)

        # Set headings
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="w")

        # Insert first 30 rows (to avoid UI freezing on large CSVs)
        for _, row in self.df.head(30).iterrows():
            self.tree.insert("", "end", values=list(row))

# Class to the CSV filter for BAR 1 window
class Filter1:
    
    # Initialization Function
    def __init__(self, parent, df, data_1, title="Filter Configuration for Bar # 1"):
        
        self.parent = parent

        # Window Characteristics
        self.window = tk.Toplevel(parent.root)
        self.window.title(title)
        self.w_win = 700
        self.h_win = 310
        self.wtotal = root.winfo_screenwidth()
        self.htotal = root.winfo_screenheight()
        self.pwidth = round(self.wtotal/2-self.w_win/2)
        self.pheight = round(self.htotal/2-self.h_win/2)
        self.window.geometry(str(self.w_win)+"x"+str(self.h_win)+"+"+str(self.pwidth)+"+"+str(self.pheight))

        
        # Creating the DataFrame (this came from the previous class)
        self.df = df

        #Creating the data
        self.data_1 = data_1

        # Launching the UI
        self.setup_ui()
        self.check_data()
    
        
    # User Interface Function
    def setup_ui(self):

        # Points of reference
        self.x = 40
        self.y = 80

        # Top Labels
        tk.Label(self.window, text="You can create up to 5 filters for each bar.").place(x=self.x-6, y = self.y - 60)
        tk.Label(self.window, text="Item").place(x=self.x-6, y = self.y - 30)
        tk.Label(self.window, text="Column").place(x=self.x+85, y = self.y - 30)
        tk.Label(self.window, text="Status").place(x=self.x+205, y = self.y - 30)
        tk.Label(self.window, text="Condition").place(x=self.x+330     , y = self.y - 30)
        tk.Label(self.window, text="Value").place(x=self.x+490, y = self.y - 30)
        tk.Label(self.window, text="Reset").place(x=self.x+590, y = self.y - 30)

        # Buttons
        tk.Button(self.window, text="Save Filter", command=self.save_filter).place(x=self.x+555,y=self.y+180)

        # Extracting the columns from the original dataframe into a list
        cols = list(self.df.columns)

        # 5 dropdowns are created and filled with the CSV's columns + labels with data types. Order: Subfilter Name, Column, Status, Condition, Value
        self.space = 35
            #1
        self.lbl_1_name = tk.Label(self.window, text="1.")
        self.lbl_1_name.place(x=self.x, y=self.y)
        self.var_1 = tk.StringVar()
        self.drdw_1 = ttk.Combobox(self.window, textvariable=self.var_1)
        self.drdw_1.place(x=self.x+35, y=self.y)
        self.drdw_1["values"] = cols
        self.var_1_cond = tk.StringVar()
        self.drdw_1_cond = ttk.Combobox(self.window, textvariable=self.var_1_cond)
        self.drdw_1_cond.place(x=self.x+285, y=self.y)
        self.lbl_1 = tk.Label(self.window, text="Select column.")
        self.lbl_1.place(x=self.x+185, y=self.y)
        self.entry_1_value = tk.StringVar()
        self.entry_1 = ttk.Entry(self.window, textvariable=self.entry_1_value)
        self.entry_1.place(x=self.x+445, y=self.y)
        self.btn_reset_1 = tk.Button(self.window, text="!", command=self.reset_filter1, bg='red', fg='white')
        self.btn_reset_1.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #2
        self.lbl_2_name = tk.Label(self.window, text="2.")
        self.lbl_2_name.place(x=self.x, y=self.y)
        self.var_2 = tk.StringVar()
        self.drdw_2 = ttk.Combobox(self.window, textvariable=self.var_2)
        self.drdw_2.place(x=self.x+35, y=self.y)
        self.drdw_2["values"] = cols
        self.var_2_cond = tk.StringVar()
        self.drdw_2_cond = ttk.Combobox(self.window, textvariable=self.var_2_cond)
        self.drdw_2_cond.place(x=self.x+285, y=self.y)
        self.lbl_2 = tk.Label(self.window, text="Select column.")
        self.lbl_2.place(x=self.x+185, y=self.y)
        self.entry_2_value = tk.StringVar()
        self.entry_2 = ttk.Entry(self.window, textvariable=self.entry_2_value)
        self.entry_2.place(x=self.x+445, y=self.y)
        self.btn_reset_2 = tk.Button(self.window, text="!", command=self.reset_filter2, bg='red', fg='white')
        self.btn_reset_2.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #3
        self.lbl_3_name = tk.Label(self.window, text="3.")
        self.lbl_3_name.place(x=self.x, y=self.y)
        self.var_3 = tk.StringVar()
        self.drdw_3 = ttk.Combobox(self.window, textvariable=self.var_3)
        self.drdw_3.place(x=self.x+35, y=self.y)
        self.drdw_3["values"] = cols
        self.var_3_cond = tk.StringVar()
        self.drdw_3_cond = ttk.Combobox(self.window, textvariable=self.var_3_cond)
        self.drdw_3_cond.place(x=self.x+285, y=self.y)
        self.lbl_3 = tk.Label(self.window, text="Select column.")
        self.lbl_3.place(x=self.x+185, y=self.y)
        self.entry_3_value = tk.StringVar()
        self.entry_3 = ttk.Entry(self.window, textvariable=self.entry_3_value)
        self.entry_3.place(x=self.x+445, y=self.y)
        self.btn_reset_3 = tk.Button(self.window, text="!", command=self.reset_filter3, bg='red', fg='white')
        self.btn_reset_3.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #4
        self.lbl_4_name = tk.Label(self.window, text="4.")
        self.lbl_4_name.place(x=self.x, y=self.y)
        self.var_4 = tk.StringVar()
        self.drdw_4 = ttk.Combobox(self.window, textvariable=self.var_4)
        self.drdw_4.place(x=self.x+35, y=self.y)
        self.drdw_4["values"] = cols
        self.var_4_cond = tk.StringVar()
        self.drdw_4_cond = ttk.Combobox(self.window, textvariable=self.var_4_cond)
        self.drdw_4_cond.place(x=self.x+285, y=self.y)
        self.lbl_4 = tk.Label(self.window, text="Select column.")
        self.lbl_4.place(x=self.x+185, y=self.y)
        self.entry_4_value = tk.StringVar()
        self.entry_4 = ttk.Entry(self.window, textvariable=self.entry_4_value)
        self.entry_4.place(x=self.x+445, y=self.y)
        self.btn_reset_4 = tk.Button(self.window, text="!", command=self.reset_filter4, bg='red', fg='white')
        self.btn_reset_4.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #5
        self.lbl_5_name = tk.Label(self.window, text="5.")
        self.lbl_5_name.place(x=self.x, y=self.y)
        self.var_5 = tk.StringVar()
        self.drdw_5 = ttk.Combobox(self.window, textvariable=self.var_5)
        self.drdw_5.place(x=self.x+35, y=self.y)
        self.drdw_5["values"] = cols
        self.var_5_cond = tk.StringVar()
        self.drdw_5_cond = ttk.Combobox(self.window, textvariable=self.var_5_cond)
        self.drdw_5_cond.place(x=self.x+285, y=self.y)
        self.lbl_5 = tk.Label(self.window, text="Select column.")
        self.lbl_5.place(x=self.x+185, y=self.y)
        self.entry_5_value = tk.StringVar()
        self.entry_5 = ttk.Entry(self.window, textvariable=self.entry_5_value)
        self.entry_5.place(x=self.x+445, y=self.y)
        self.btn_reset_5 = tk.Button(self.window, text="!", command=self.reset_filter5, bg='red', fg='white')
        self.btn_reset_5.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space

        # Action when value of dropdown changes
        self.drdw_1.bind("<<ComboboxSelected>>", self.drdw_1_change)
        self.drdw_2.bind("<<ComboboxSelected>>", self.drdw_2_change)
        self.drdw_3.bind("<<ComboboxSelected>>", self.drdw_3_change)
        self.drdw_4.bind("<<ComboboxSelected>>", self.drdw_4_change)
        self.drdw_5.bind("<<ComboboxSelected>>", self.drdw_5_change)

    # Function to identify the data type for subfilter 1 and displaying filtering options
    def drdw_1_change(self, event):
        current_value = self.var_1.get()
        current_type = self.df[current_value].dtype
        self.drdw_1_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_1_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_1_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_1_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_1_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_1_cond["values"] = ["=="]
        
        self.lbl_1.config(text=current_type)
    
    # Function to identify the data type for subfilter 2 and displaying filtering options
    def drdw_2_change(self, event):
        current_value = self.var_2.get()
        current_type = self.df[current_value].dtype
        self.drdw_2_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_2_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_2_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_2_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_2_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_2_cond["values"] = ["=="]

        self.lbl_2.config(text=current_type)
    
    # Function to identify the data type for subfilter 3 and displaying filtering options
    def drdw_3_change(self, event):
        current_value = self.var_3.get()
        current_type = self.df[current_value].dtype
        self.drdw_3_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_3_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_3_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_3_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_3_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_3_cond["values"] = ["=="]

        self.lbl_3.config(text=current_type)

    # Function to identify the data type for subfilter 4 and displaying filtering options
    def drdw_4_change(self, event):
        current_value = self.var_4.get()
        current_type = self.df[current_value].dtype
        self.drdw_4_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_4_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_4_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_4_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_4_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_4_cond["values"] = ["=="]

        self.lbl_4.config(text=current_type)
    
    # Function to identify the data type for subfilter 5 and displaying filtering options
    def drdw_5_change(self, event):
        current_value = self.var_5.get()
        current_type = self.df[current_value].dtype
        self.drdw_5_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_5_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_5_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_5_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_5_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_5_cond["values"] = ["=="]

        self.lbl_5.config(text=current_type)

    # Reset Subfilter 1 values
    def reset_filter1(self):
        self.drdw_1.set("")
        self.drdw_1_cond.set("")
        self.entry_1_value.set("")
        self.lbl_1.config(text="Select column.")
    
    # Reset Subfilter 2 values
    def reset_filter2(self):
        self.drdw_2.set("")
        self.drdw_2_cond.set("")
        self.entry_2_value.set("")
        self.lbl_2.config(text="Select column.")
    
    # Reset Subfilter 3 values
    def reset_filter3(self):
        self.drdw_3.set("")
        self.drdw_3_cond.set("")
        self.entry_3_value.set("")
        self.lbl_3.config(text="Select column.")

    # Reset Subfilter 4 values
    def reset_filter4(self):
        self.drdw_4.set("")
        self.drdw_4_cond.set("")
        self.entry_4_value.set("")
        self.lbl_4.config(text="Select column.")
    
    # Reset Subfilter 5 values
    def reset_filter5(self):
        self.drdw_5.set("")
        self.drdw_5_cond.set("")
        self.entry_5_value.set("")
        self.lbl_5.config(text="Select column.")

    # Saving the filter configuration    
    def save_filter(self):

        self.num_filters = 0
        self.filter_prompt_1 = ""
        self.data_1 = []

        # Checking the data type and validating it for subfilter 1 ------------------------------------
        self.value_1 = self.entry_1.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_1 != "":
            if self.var_1_cond.get() != "":
                if self.lbl_1.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 1.")
                    return                
                elif self.lbl_1.cget('text') == "Integer":
                    if self.value_1.isdigit():
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_1.append(self.var_1.get())
                            self.data_1.append(self.lbl_1.cget('text'))
                            self.data_1.append(self.var_1_cond.get())
                            self.data_1.append(self.value_1)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_1.append(self.var_1.get())
                            self.data_1.append(self.lbl_1.cget('text'))
                            self.data_1.append(self.var_1_cond.get())
                            self.data_1.append(self.value_1)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 1.")
                        return
                elif self.lbl_1.cget('text') == "Decimals":
                    try:                        
                        float(self.value_1)                        
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_1.append(self.var_1.get())
                            self.data_1.append(self.lbl_1.cget('text'))
                            self.data_1.append(self.var_1_cond.get())
                            self.data_1.append(self.value_1)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_1.append(self.var_1.get())
                            self.data_1.append(self.lbl_1.cget('text'))
                            self.data_1.append(self.var_1_cond.get())
                            self.data_1.append(self.value_1)                  
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 1.")
                        return               
                elif self.lbl_1.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_1, "%Y-%m-%d")
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_1.append(self.var_1.get())
                            self.data_1.append(self.lbl_1.cget('text'))
                            self.data_1.append(self.var_1_cond.get())
                            self.data_1.append(self.value_1)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_1.append(self.var_1.get())
                            self.data_1.append(self.lbl_1.cget('text'))
                            self.data_1.append(self.var_1_cond.get())
                            self.data_1.append(self.value_1)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 1.")
                        return
                elif self.lbl_1.cget('text') == "True/False":
                    if self.value_1 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_1.append(self.var_1.get())
                            self.data_1.append(self.lbl_1.cget('text'))
                            self.data_1.append(self.var_1_cond.get())
                            self.data_1.append(self.value_1)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_1.append(self.var_1.get())
                            self.data_1.append(self.lbl_1.cget('text'))
                            self.data_1.append(self.var_1_cond.get())
                            self.data_1.append(self.value_1)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 1.")
                        return
                elif self.lbl_1.cget('text') == "Text":
                    if self.filter_prompt_1 == "":
                        self.filter_prompt_1 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                        self.data_1.append(self.var_1.get())
                        self.data_1.append(self.lbl_1.cget('text'))
                        self.data_1.append(self.var_1_cond.get())
                        self.data_1.append(self.value_1)
                    else:
                        self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                        self.data_1.append(self.var_1.get())
                        self.data_1.append(self.lbl_1.cget('text'))
                        self.data_1.append(self.var_1_cond.get())
                        self.data_1.append(self.value_1)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 1.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_1 == "" and self.lbl_1.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 1.")
            return

        # Checking the data type and validating it for subfilter 2 ------------------------------------
        self.value_2 = self.entry_2.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_2 != "":
            if self.var_2_cond.get() != "":
                if self.lbl_2.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 2.")
                    return                
                elif self.lbl_2.cget('text') == "Integer":
                    if self.value_2.isdigit():
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_1.append(self.var_2.get())
                            self.data_1.append(self.lbl_2.cget('text'))
                            self.data_1.append(self.var_2_cond.get())
                            self.data_1.append(self.value_2)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_1.append(self.var_2.get())
                            self.data_1.append(self.lbl_2.cget('text'))
                            self.data_1.append(self.var_2_cond.get())
                            self.data_1.append(self.value_2)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 2.")
                        return
                elif self.lbl_2.cget('text') == "Decimals":
                    try:                        
                        float(self.value_2)                        
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_1.append(self.var_2.get())
                            self.data_1.append(self.lbl_2.cget('text'))
                            self.data_1.append(self.var_2_cond.get())
                            self.data_1.append(self.value_2)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_1.append(self.var_2.get())
                            self.data_1.append(self.lbl_2.cget('text'))
                            self.data_1.append(self.var_2_cond.get())
                            self.data_1.append(self.value_2)                 
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 2.")
                        return               
                elif self.lbl_2.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_2, "%Y-%m-%d")
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_1.append(self.var_2.get())
                            self.data_1.append(self.lbl_2.cget('text'))
                            self.data_1.append(self.var_2_cond.get())
                            self.data_1.append(self.value_2)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_1.append(self.var_2.get())
                            self.data_1.append(self.lbl_2.cget('text'))
                            self.data_1.append(self.var_2_cond.get())
                            self.data_1.append(self.value_2)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 2.")
                        return
                elif self.lbl_2.cget('text') == "True/False":
                    if self.value_2 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_1.append(self.var_2.get())
                            self.data_1.append(self.lbl_2.cget('text'))
                            self.data_1.append(self.var_2_cond.get())
                            self.data_1.append(self.value_2)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_1.append(self.var_2.get())
                            self.data_1.append(self.lbl_2.cget('text'))
                            self.data_1.append(self.var_2_cond.get())
                            self.data_1.append(self.value_2)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 2.")
                        return
                elif self.lbl_2.cget('text') == "Text":
                    if self.filter_prompt_1 == "":
                        self.filter_prompt_1 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                        self.data_1.append(self.var_2.get())
                        self.data_1.append(self.lbl_2.cget('text'))
                        self.data_1.append(self.var_2_cond.get())
                        self.data_1.append(self.value_2)
                    else:
                        self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                        self.data_1.append(self.var_2.get())
                        self.data_1.append(self.lbl_2.cget('text'))
                        self.data_1.append(self.var_2_cond.get())
                        self.data_1.append(self.value_2)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 2.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_2 == "" and self.lbl_2.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 2.")
            return
        
        # Checking the data type and validating it for subfilter 3 ------------------------------------
        self.value_3 = self.entry_3.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_3 != "":
            if self.var_3_cond.get() != "":
                if self.lbl_3.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 3.")
                    return                
                elif self.lbl_3.cget('text') == "Integer":
                    if self.value_3.isdigit():
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_1.append(self.var_3.get())
                            self.data_1.append(self.lbl_3.cget('text'))
                            self.data_1.append(self.var_3_cond.get())
                            self.data_1.append(self.value_3)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_1.append(self.var_3.get())
                            self.data_1.append(self.lbl_3.cget('text'))
                            self.data_1.append(self.var_3_cond.get())
                            self.data_1.append(self.value_3)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 3.")
                        return
                elif self.lbl_3.cget('text') == "Decimals":
                    try:                        
                        float(self.value_3)                        
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_1.append(self.var_3.get())
                            self.data_1.append(self.lbl_3.cget('text'))
                            self.data_1.append(self.var_3_cond.get())
                            self.data_1.append(self.value_3)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_1.append(self.var_3.get())
                            self.data_1.append(self.lbl_3.cget('text'))
                            self.data_1.append(self.var_3_cond.get())
                            self.data_1.append(self.value_3)                   
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 3.")
                        return               
                elif self.lbl_3.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_3, "%Y-%m-%d")
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                            self.data_1.append(self.var_3.get())
                            self.data_1.append(self.lbl_3.cget('text'))
                            self.data_1.append(self.var_3_cond.get())
                            self.data_1.append(self.value_3)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''                  
                            self.data_1.append(self.var_3.get())
                            self.data_1.append(self.lbl_3.cget('text'))
                            self.data_1.append(self.var_3_cond.get())
                            self.data_1.append(self.value_3)
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 3.")
                        return
                elif self.lbl_3.cget('text') == "True/False":
                    if self.value_3 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                            self.data_1.append(self.var_3.get())
                            self.data_1.append(self.lbl_3.cget('text'))
                            self.data_1.append(self.var_3_cond.get())
                            self.data_1.append(self.value_3)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                            self.data_1.append(self.var_3.get())
                            self.data_1.append(self.lbl_3.cget('text'))
                            self.data_1.append(self.var_3_cond.get())
                            self.data_1.append(self.value_3)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 3.")
                        return
                elif self.lbl_3.cget('text') == "Text":
                    if self.filter_prompt_1 == "":
                        self.filter_prompt_1 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                        self.data_1.append(self.var_3.get())
                        self.data_1.append(self.lbl_3.cget('text'))
                        self.data_1.append(self.var_3_cond.get())
                        self.data_1.append(self.value_3)
                    else:
                        self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                        self.data_1.append(self.var_3.get())
                        self.data_1.append(self.lbl_3.cget('text'))
                        self.data_1.append(self.var_3_cond.get())
                        self.data_1.append(self.value_3)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 3.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_3 == "" and self.lbl_3.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 3.")
            return

        # Checking the data type and validating it for subfilter 4 ------------------------------------
        self.value_4 = self.entry_4.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_4 != "":
            if self.var_4_cond.get() != "":
                if self.lbl_4.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 4.")
                    return                
                elif self.lbl_4.cget('text') == "Integer":
                    if self.value_4.isdigit():
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_1.append(self.var_4.get())
                            self.data_1.append(self.lbl_4.cget('text'))
                            self.data_1.append(self.var_4_cond.get())
                            self.data_1.append(self.value_4)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_1.append(self.var_4.get())
                            self.data_1.append(self.lbl_4.cget('text'))
                            self.data_1.append(self.var_4_cond.get())
                            self.data_1.append(self.value_4)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 4.")
                        return
                elif self.lbl_4.cget('text') == "Decimals":
                    try:                        
                        float(self.value_4)                        
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_1.append(self.var_4.get())
                            self.data_1.append(self.lbl_4.cget('text'))
                            self.data_1.append(self.var_4_cond.get())
                            self.data_1.append(self.value_4)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_1.append(self.var_4.get())
                            self.data_1.append(self.lbl_4.cget('text'))
                            self.data_1.append(self.var_4_cond.get())
                            self.data_1.append(self.value_4)                  
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 4.")
                        return               
                elif self.lbl_4.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_4, "%Y-%m-%d")
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_1.append(self.var_4.get())
                            self.data_1.append(self.lbl_4.cget('text'))
                            self.data_1.append(self.var_4_cond.get())
                            self.data_1.append(self.value_4)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_1.append(self.var_4.get())
                            self.data_1.append(self.lbl_4.cget('text'))
                            self.data_1.append(self.var_4_cond.get())
                            self.data_1.append(self.value_4)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 4.")
                        return
                elif self.lbl_4.cget('text') == "True/False":
                    if self.value_4 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_1.append(self.var_4.get())
                            self.data_1.append(self.lbl_4.cget('text'))
                            self.data_1.append(self.var_4_cond.get())
                            self.data_1.append(self.value_4)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_1.append(self.var_4.get())
                            self.data_1.append(self.lbl_4.cget('text'))
                            self.data_1.append(self.var_4_cond.get())
                            self.data_1.append(self.value_4)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 4.")
                        return
                elif self.lbl_4.cget('text') == "Text":
                    if self.filter_prompt_1 == "":
                        self.filter_prompt_1 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                        self.data_1.append(self.var_4.get())
                        self.data_1.append(self.lbl_4.cget('text'))
                        self.data_1.append(self.var_4_cond.get())
                        self.data_1.append(self.value_4)
                    else:
                        self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                        self.data_1.append(self.var_4.get())
                        self.data_1.append(self.lbl_4.cget('text'))
                        self.data_1.append(self.var_4_cond.get())
                        self.data_1.append(self.value_4)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 4.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_4 == "" and self.lbl_4.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 4.")
            return
        
        # Checking the data type and validating it for subfilter 5 ------------------------------------
        self.value_5 = self.entry_5.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_5 != "":
            if self.var_5_cond.get() != "":
                if self.lbl_5.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 5.")
                    return                
                elif self.lbl_5.cget('text') == "Integer":
                    if self.value_5.isdigit():
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_1.append(self.var_5.get())
                            self.data_1.append(self.lbl_5.cget('text'))
                            self.data_1.append(self.var_5_cond.get())
                            self.data_1.append(self.value_5)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_1.append(self.var_5.get())
                            self.data_1.append(self.lbl_5.cget('text'))
                            self.data_1.append(self.var_5_cond.get())
                            self.data_1.append(self.value_5)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 5.")
                        return
                elif self.lbl_5.cget('text') == "Decimals":
                    try:                        
                        float(self.value_5)                        
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_1.append(self.var_5.get())
                            self.data_1.append(self.lbl_5.cget('text'))
                            self.data_1.append(self.var_5_cond.get())
                            self.data_1.append(self.value_5)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_1.append(self.var_5.get())
                            self.data_1.append(self.lbl_5.cget('text'))
                            self.data_1.append(self.var_5_cond.get())
                            self.data_1.append(self.value_5)                   
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 5.")
                        return               
                elif self.lbl_5.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_5, "%Y-%m-%d")
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_1.append(self.var_5.get())
                            self.data_1.append(self.lbl_5.cget('text'))
                            self.data_1.append(self.var_5_cond.get())
                            self.data_1.append(self.value_5)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_1.append(self.var_5.get())
                            self.data_1.append(self.lbl_5.cget('text'))
                            self.data_1.append(self.var_5_cond.get())
                            self.data_1.append(self.value_5)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 5.")
                        return
                elif self.lbl_5.cget('text') == "True/False":
                    if self.value_5 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_1 == "":
                            self.filter_prompt_1 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_1.append(self.var_5.get())
                            self.data_1.append(self.lbl_5.cget('text'))
                            self.data_1.append(self.var_5_cond.get())
                            self.data_1.append(self.value_5)
                        else:
                            self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_1.append(self.var_5.get())
                            self.data_1.append(self.lbl_5.cget('text'))
                            self.data_1.append(self.var_5_cond.get())
                            self.data_1.append(self.value_5)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 5.")
                        return
                elif self.lbl_5.cget('text') == "Text":
                    if self.filter_prompt_1 == "":
                        self.filter_prompt_1 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                        self.data_1.append(self.var_5.get())
                        self.data_1.append(self.lbl_5.cget('text'))
                        self.data_1.append(self.var_5_cond.get())
                        self.data_1.append(self.value_5)
                    else:
                        self.filter_prompt_1 = self.filter_prompt_1 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                        self.data_1.append(self.var_5.get())
                        self.data_1.append(self.lbl_5.cget('text'))
                        self.data_1.append(self.var_5_cond.get())
                        self.data_1.append(self.value_5)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 5.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_5 == "" and self.lbl_5.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 5.")
            return

        # If the user is saving something empty, the app will notify
        if not self.data_1:
            self.answer1 = messagebox.askyesno(title="Nothing to save",parent=self.window, message="You are not saving any filter, would you like to close the window?")
            if self.answer1:
                self.window.destroy()
                return
            else:
                return

        # Saving the information and closing the window
        self.answer = messagebox.askyesno(title="Saving this filter",parent=self.window, message="Are you sure you want to save this filter?\n" + self.filter_prompt_1)
        if self.answer:
            self.parent.filter_prompt_1 = self.filter_prompt_1  # Saving the prompt into the Main Window Class
            self.parent.data_1 = self.data_1                    # Saving the Data into a list in the Main Window Class
            self.parent.write_filter_1()
            self.window.destroy()
            return
        else:
            return

    # If there was data sent from Main Class (Edit the filter), then the data is loaded:
    def check_data(self):
        if not self.data_1:
            return
        else:
            if len(self.data_1) == 4:
                self.drdw_1.set(self.data_1[0])
                self.lbl_1.config(text=self.data_1[1])
                self.drdw_1_cond.set(self.data_1[2])
                self.entry_1_value.set(self.data_1[3])
            elif len(self.data_1) == 8:
                self.drdw_1.set(self.data_1[0])
                self.lbl_1.config(text=self.data_1[1])
                self.drdw_1_cond.set(self.data_1[2])
                self.entry_1_value.set(self.data_1[3])
                self.drdw_2.set(self.data_1[4])
                self.lbl_2.config(text=self.data_1[5])
                self.drdw_2_cond.set(self.data_1[6])
                self.entry_2_value.set(self.data_1[7])
            elif len(self.data_1) == 12:
                self.drdw_1.set(self.data_1[0])
                self.lbl_1.config(text=self.data_1[1])
                self.drdw_1_cond.set(self.data_1[2])
                self.entry_1_value.set(self.data_1[3])
                self.drdw_2.set(self.data_1[4])
                self.lbl_2.config(text=self.data_1[5])
                self.drdw_2_cond.set(self.data_1[6])
                self.entry_2_value.set(self.data_1[7])
                self.drdw_3.set(self.data_1[8])
                self.lbl_3.config(text=self.data_1[9])
                self.drdw_3_cond.set(self.data_1[10])
                self.entry_3_value.set(self.data_1[11])
            elif len(self.data_1) == 16:
                self.drdw_1.set(self.data_1[0])
                self.lbl_1.config(text=self.data_1[1])
                self.drdw_1_cond.set(self.data_1[2])
                self.entry_1_value.set(self.data_1[3])
                self.drdw_2.set(self.data_1[4])
                self.lbl_2.config(text=self.data_1[5])
                self.drdw_2_cond.set(self.data_1[6])
                self.entry_2_value.set(self.data_1[7])
                self.drdw_3.set(self.data_1[8])
                self.lbl_3.config(text=self.data_1[9])
                self.drdw_3_cond.set(self.data_1[10])
                self.entry_3_value.set(self.data_1[11])
                self.drdw_4.set(self.data_1[12])
                self.lbl_4.config(text=self.data_1[13])
                self.drdw_4_cond.set(self.data_1[14])
                self.entry_4_value.set(self.data_1[15])
            elif len(self.data_1) == 20:
                self.drdw_1.set(self.data_1[0])
                self.lbl_1.config(text=self.data_1[1])
                self.drdw_1_cond.set(self.data_1[2])
                self.entry_1_value.set(self.data_1[3])
                self.drdw_2.set(self.data_1[4])
                self.lbl_2.config(text=self.data_1[5])
                self.drdw_2_cond.set(self.data_1[6])
                self.entry_2_value.set(self.data_1[7])
                self.drdw_3.set(self.data_1[8])
                self.lbl_3.config(text=self.data_1[9])
                self.drdw_3_cond.set(self.data_1[10])
                self.entry_3_value.set(self.data_1[11])
                self.drdw_4.set(self.data_1[12])
                self.lbl_4.config(text=self.data_1[13])
                self.drdw_4_cond.set(self.data_1[14])
                self.entry_4_value.set(self.data_1[15])
                self.drdw_5.set(self.data_1[16])
                self.lbl_5.config(text=self.data_1[17])
                self.drdw_5_cond.set(self.data_1[18])
                self.entry_5_value.set(self.data_1[19])

# Class to the CSV filter for BAR 2 window
class Filter2:
    
    # Initialization Function
    def __init__(self, parent, df, data_2, title="Filter Configuration for Bar # 2"):
        
        self.parent = parent

        # Window Characteristics
        self.window = tk.Toplevel(parent.root)
        self.window.title(title)
        self.w_win = 700
        self.h_win = 310
        self.wtotal = root.winfo_screenwidth()
        self.htotal = root.winfo_screenheight()
        self.pwidth = round(self.wtotal/2-self.w_win/2)
        self.pheight = round(self.htotal/2-self.h_win/2)
        self.window.geometry(str(self.w_win)+"x"+str(self.h_win)+"+"+str(self.pwidth)+"+"+str(self.pheight))

        
        # Creating the DataFrame (this came from the previous class)
        self.df = df

        #Creating the data
        self.data_2 = data_2

        # Launching the UI
        self.setup_ui()
        self.check_data()
    
        
    # User Interface Function
    def setup_ui(self):

        # Points of reference
        self.x = 40
        self.y = 80

        # Top Labels
        tk.Label(self.window, text="You can create up to 5 filters for each bar.").place(x=self.x-6, y = self.y - 60)
        tk.Label(self.window, text="Item").place(x=self.x-6, y = self.y - 30)
        tk.Label(self.window, text="Column").place(x=self.x+85, y = self.y - 30)
        tk.Label(self.window, text="Status").place(x=self.x+205, y = self.y - 30)
        tk.Label(self.window, text="Condition").place(x=self.x+330     , y = self.y - 30)
        tk.Label(self.window, text="Value").place(x=self.x+490, y = self.y - 30)
        tk.Label(self.window, text="Reset").place(x=self.x+590, y = self.y - 30)

        # Buttons
        tk.Button(self.window, text="Save Filter", command=self.save_filter).place(x=self.x+555,y=self.y+180)

        # Extracting the columns from the original dataframe into a list
        cols = list(self.df.columns)

        # 5 dropdowns are created and filled with the CSV's columns + labels with data types. Order: Subfilter Name, Column, Status, Condition, Value
        self.space = 35
            #1
        self.lbl_1_name = tk.Label(self.window, text="1.")
        self.lbl_1_name.place(x=self.x, y=self.y)
        self.var_1 = tk.StringVar()
        self.drdw_1 = ttk.Combobox(self.window, textvariable=self.var_1)
        self.drdw_1.place(x=self.x+35, y=self.y)
        self.drdw_1["values"] = cols
        self.var_1_cond = tk.StringVar()
        self.drdw_1_cond = ttk.Combobox(self.window, textvariable=self.var_1_cond)
        self.drdw_1_cond.place(x=self.x+285, y=self.y)
        self.lbl_1 = tk.Label(self.window, text="Select column.")
        self.lbl_1.place(x=self.x+185, y=self.y)
        self.entry_1_value = tk.StringVar()
        self.entry_1 = ttk.Entry(self.window, textvariable=self.entry_1_value)
        self.entry_1.place(x=self.x+445, y=self.y)
        self.btn_reset_1 = tk.Button(self.window, text="!", command=self.reset_filter1, bg='red', fg='white')
        self.btn_reset_1.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #2
        self.lbl_2_name = tk.Label(self.window, text="2.")
        self.lbl_2_name.place(x=self.x, y=self.y)
        self.var_2 = tk.StringVar()
        self.drdw_2 = ttk.Combobox(self.window, textvariable=self.var_2)
        self.drdw_2.place(x=self.x+35, y=self.y)
        self.drdw_2["values"] = cols
        self.var_2_cond = tk.StringVar()
        self.drdw_2_cond = ttk.Combobox(self.window, textvariable=self.var_2_cond)
        self.drdw_2_cond.place(x=self.x+285, y=self.y)
        self.lbl_2 = tk.Label(self.window, text="Select column.")
        self.lbl_2.place(x=self.x+185, y=self.y)
        self.entry_2_value = tk.StringVar()
        self.entry_2 = ttk.Entry(self.window, textvariable=self.entry_2_value)
        self.entry_2.place(x=self.x+445, y=self.y)
        self.btn_reset_2 = tk.Button(self.window, text="!", command=self.reset_filter2, bg='red', fg='white')
        self.btn_reset_2.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #3
        self.lbl_3_name = tk.Label(self.window, text="3.")
        self.lbl_3_name.place(x=self.x, y=self.y)
        self.var_3 = tk.StringVar()
        self.drdw_3 = ttk.Combobox(self.window, textvariable=self.var_3)
        self.drdw_3.place(x=self.x+35, y=self.y)
        self.drdw_3["values"] = cols
        self.var_3_cond = tk.StringVar()
        self.drdw_3_cond = ttk.Combobox(self.window, textvariable=self.var_3_cond)
        self.drdw_3_cond.place(x=self.x+285, y=self.y)
        self.lbl_3 = tk.Label(self.window, text="Select column.")
        self.lbl_3.place(x=self.x+185, y=self.y)
        self.entry_3_value = tk.StringVar()
        self.entry_3 = ttk.Entry(self.window, textvariable=self.entry_3_value)
        self.entry_3.place(x=self.x+445, y=self.y)
        self.btn_reset_3 = tk.Button(self.window, text="!", command=self.reset_filter3, bg='red', fg='white')
        self.btn_reset_3.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #4
        self.lbl_4_name = tk.Label(self.window, text="4.")
        self.lbl_4_name.place(x=self.x, y=self.y)
        self.var_4 = tk.StringVar()
        self.drdw_4 = ttk.Combobox(self.window, textvariable=self.var_4)
        self.drdw_4.place(x=self.x+35, y=self.y)
        self.drdw_4["values"] = cols
        self.var_4_cond = tk.StringVar()
        self.drdw_4_cond = ttk.Combobox(self.window, textvariable=self.var_4_cond)
        self.drdw_4_cond.place(x=self.x+285, y=self.y)
        self.lbl_4 = tk.Label(self.window, text="Select column.")
        self.lbl_4.place(x=self.x+185, y=self.y)
        self.entry_4_value = tk.StringVar()
        self.entry_4 = ttk.Entry(self.window, textvariable=self.entry_4_value)
        self.entry_4.place(x=self.x+445, y=self.y)
        self.btn_reset_4 = tk.Button(self.window, text="!", command=self.reset_filter4, bg='red', fg='white')
        self.btn_reset_4.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #5
        self.lbl_5_name = tk.Label(self.window, text="5.")
        self.lbl_5_name.place(x=self.x, y=self.y)
        self.var_5 = tk.StringVar()
        self.drdw_5 = ttk.Combobox(self.window, textvariable=self.var_5)
        self.drdw_5.place(x=self.x+35, y=self.y)
        self.drdw_5["values"] = cols
        self.var_5_cond = tk.StringVar()
        self.drdw_5_cond = ttk.Combobox(self.window, textvariable=self.var_5_cond)
        self.drdw_5_cond.place(x=self.x+285, y=self.y)
        self.lbl_5 = tk.Label(self.window, text="Select column.")
        self.lbl_5.place(x=self.x+185, y=self.y)
        self.entry_5_value = tk.StringVar()
        self.entry_5 = ttk.Entry(self.window, textvariable=self.entry_5_value)
        self.entry_5.place(x=self.x+445, y=self.y)
        self.btn_reset_5 = tk.Button(self.window, text="!", command=self.reset_filter5, bg='red', fg='white')
        self.btn_reset_5.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space

        # Action when value of dropdown changes
        self.drdw_1.bind("<<ComboboxSelected>>", self.drdw_1_change)
        self.drdw_2.bind("<<ComboboxSelected>>", self.drdw_2_change)
        self.drdw_3.bind("<<ComboboxSelected>>", self.drdw_3_change)
        self.drdw_4.bind("<<ComboboxSelected>>", self.drdw_4_change)
        self.drdw_5.bind("<<ComboboxSelected>>", self.drdw_5_change)

    # Function to identify the data type for subfilter 1 and displaying filtering options
    def drdw_1_change(self, event):
        current_value = self.var_1.get()
        current_type = self.df[current_value].dtype
        self.drdw_1_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_1_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_1_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_1_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_1_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_1_cond["values"] = ["=="]
        
        self.lbl_1.config(text=current_type)
    
    # Function to identify the data type for subfilter 2 and displaying filtering options
    def drdw_2_change(self, event):
        current_value = self.var_2.get()
        current_type = self.df[current_value].dtype
        self.drdw_2_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_2_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_2_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_2_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_2_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_2_cond["values"] = ["=="]

        self.lbl_2.config(text=current_type)
    
    # Function to identify the data type for subfilter 3 and displaying filtering options
    def drdw_3_change(self, event):
        current_value = self.var_3.get()
        current_type = self.df[current_value].dtype
        self.drdw_3_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_3_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_3_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_3_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_3_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_3_cond["values"] = ["=="]

        self.lbl_3.config(text=current_type)

    # Function to identify the data type for subfilter 4 and displaying filtering options
    def drdw_4_change(self, event):
        current_value = self.var_4.get()
        current_type = self.df[current_value].dtype
        self.drdw_4_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_4_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_4_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_4_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_4_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_4_cond["values"] = ["=="]

        self.lbl_4.config(text=current_type)
    
    # Function to identify the data type for subfilter 5 and displaying filtering options
    def drdw_5_change(self, event):
        current_value = self.var_5.get()
        current_type = self.df[current_value].dtype
        self.drdw_5_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_5_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_5_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_5_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_5_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_5_cond["values"] = ["=="]

        self.lbl_5.config(text=current_type)

    # Reset Subfilter 1 values
    def reset_filter1(self):
        self.drdw_1.set("")
        self.drdw_1_cond.set("")
        self.entry_1_value.set("")
        self.lbl_1.config(text="Select column.")
    
    # Reset Subfilter 2 values
    def reset_filter2(self):
        self.drdw_2.set("")
        self.drdw_2_cond.set("")
        self.entry_2_value.set("")
        self.lbl_2.config(text="Select column.")
    
    # Reset Subfilter 3 values
    def reset_filter3(self):
        self.drdw_3.set("")
        self.drdw_3_cond.set("")
        self.entry_3_value.set("")
        self.lbl_3.config(text="Select column.")

    # Reset Subfilter 4 values
    def reset_filter4(self):
        self.drdw_4.set("")
        self.drdw_4_cond.set("")
        self.entry_4_value.set("")
        self.lbl_4.config(text="Select column.")
    
    # Reset Subfilter 5 values
    def reset_filter5(self):
        self.drdw_5.set("")
        self.drdw_5_cond.set("")
        self.entry_5_value.set("")
        self.lbl_5.config(text="Select column.")

    # Saving the filter configuration    
    def save_filter(self):

        self.num_filters = 0
        self.filter_prompt_2 = ""
        self.data_2 = []

        # Checking the data type and validating it for subfilter 1 ------------------------------------
        self.value_1 = self.entry_1.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_1 != "":
            if self.var_1_cond.get() != "":
                if self.lbl_1.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 1.")
                    return                
                elif self.lbl_1.cget('text') == "Integer":
                    if self.value_1.isdigit():
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_2.append(self.var_1.get())
                            self.data_2.append(self.lbl_1.cget('text'))
                            self.data_2.append(self.var_1_cond.get())
                            self.data_2.append(self.value_1)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_2.append(self.var_1.get())
                            self.data_2.append(self.lbl_1.cget('text'))
                            self.data_2.append(self.var_1_cond.get())
                            self.data_2.append(self.value_1)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 1.")
                        return
                elif self.lbl_1.cget('text') == "Decimals":
                    try:                        
                        float(self.value_1)                        
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_2.append(self.var_1.get())
                            self.data_2.append(self.lbl_1.cget('text'))
                            self.data_2.append(self.var_1_cond.get())
                            self.data_2.append(self.value_1)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_2.append(self.var_1.get())
                            self.data_2.append(self.lbl_1.cget('text'))
                            self.data_2.append(self.var_1_cond.get())
                            self.data_2.append(self.value_1)                  
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 1.")
                        return               
                elif self.lbl_1.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_1, "%Y-%m-%d")
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_2.append(self.var_1.get())
                            self.data_2.append(self.lbl_1.cget('text'))
                            self.data_2.append(self.var_1_cond.get())
                            self.data_2.append(self.value_1)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_2.append(self.var_1.get())
                            self.data_2.append(self.lbl_1.cget('text'))
                            self.data_2.append(self.var_1_cond.get())
                            self.data_2.append(self.value_1)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 1.")
                        return
                elif self.lbl_1.cget('text') == "True/False":
                    if self.value_1 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_2.append(self.var_1.get())
                            self.data_2.append(self.lbl_1.cget('text'))
                            self.data_2.append(self.var_1_cond.get())
                            self.data_2.append(self.value_1)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_2.append(self.var_1.get())
                            self.data_2.append(self.lbl_1.cget('text'))
                            self.data_2.append(self.var_1_cond.get())
                            self.data_2.append(self.value_1)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 1.")
                        return
                elif self.lbl_1.cget('text') == "Text":
                    if self.filter_prompt_2 == "":
                        self.filter_prompt_2 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                        self.data_2.append(self.var_1.get())
                        self.data_2.append(self.lbl_1.cget('text'))
                        self.data_2.append(self.var_1_cond.get())
                        self.data_2.append(self.value_1)
                    else:
                        self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                        self.data_2.append(self.var_1.get())
                        self.data_2.append(self.lbl_1.cget('text'))
                        self.data_2.append(self.var_1_cond.get())
                        self.data_2.append(self.value_1)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 1.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_1 == "" and self.lbl_1.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 1.")
            return

        # Checking the data type and validating it for subfilter 2 ------------------------------------
        self.value_2 = self.entry_2.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_2 != "":
            if self.var_2_cond.get() != "":
                if self.lbl_2.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 2.")
                    return                
                elif self.lbl_2.cget('text') == "Integer":
                    if self.value_2.isdigit():
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_2.append(self.var_2.get())
                            self.data_2.append(self.lbl_2.cget('text'))
                            self.data_2.append(self.var_2_cond.get())
                            self.data_2.append(self.value_2)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_2.append(self.var_2.get())
                            self.data_2.append(self.lbl_2.cget('text'))
                            self.data_2.append(self.var_2_cond.get())
                            self.data_2.append(self.value_2)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 2.")
                        return
                elif self.lbl_2.cget('text') == "Decimals":
                    try:                        
                        float(self.value_2)                        
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_2.append(self.var_2.get())
                            self.data_2.append(self.lbl_2.cget('text'))
                            self.data_2.append(self.var_2_cond.get())
                            self.data_2.append(self.value_2)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_2.append(self.var_2.get())
                            self.data_2.append(self.lbl_2.cget('text'))
                            self.data_2.append(self.var_2_cond.get())
                            self.data_2.append(self.value_2)                 
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 2.")
                        return               
                elif self.lbl_2.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_2, "%Y-%m-%d")
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_2.append(self.var_2.get())
                            self.data_2.append(self.lbl_2.cget('text'))
                            self.data_2.append(self.var_2_cond.get())
                            self.data_2.append(self.value_2)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_2.append(self.var_2.get())
                            self.data_2.append(self.lbl_2.cget('text'))
                            self.data_2.append(self.var_2_cond.get())
                            self.data_2.append(self.value_2)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 2.")
                        return
                elif self.lbl_2.cget('text') == "True/False":
                    if self.value_2 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_2.append(self.var_2.get())
                            self.data_2.append(self.lbl_2.cget('text'))
                            self.data_2.append(self.var_2_cond.get())
                            self.data_2.append(self.value_2)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_2.append(self.var_2.get())
                            self.data_2.append(self.lbl_2.cget('text'))
                            self.data_2.append(self.var_2_cond.get())
                            self.data_2.append(self.value_2)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 2.")
                        return
                elif self.lbl_2.cget('text') == "Text":
                    if self.filter_prompt_2 == "":
                        self.filter_prompt_2 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                        self.data_2.append(self.var_2.get())
                        self.data_2.append(self.lbl_2.cget('text'))
                        self.data_2.append(self.var_2_cond.get())
                        self.data_2.append(self.value_2)
                    else:
                        self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                        self.data_2.append(self.var_2.get())
                        self.data_2.append(self.lbl_2.cget('text'))
                        self.data_2.append(self.var_2_cond.get())
                        self.data_2.append(self.value_2)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 2.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_2 == "" and self.lbl_2.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 2.")
            return
        
        # Checking the data type and validating it for subfilter 3 ------------------------------------
        self.value_3 = self.entry_3.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_3 != "":
            if self.var_3_cond.get() != "":
                if self.lbl_3.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 3.")
                    return                
                elif self.lbl_3.cget('text') == "Integer":
                    if self.value_3.isdigit():
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_2.append(self.var_3.get())
                            self.data_2.append(self.lbl_3.cget('text'))
                            self.data_2.append(self.var_3_cond.get())
                            self.data_2.append(self.value_3)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_2.append(self.var_3.get())
                            self.data_2.append(self.lbl_3.cget('text'))
                            self.data_2.append(self.var_3_cond.get())
                            self.data_2.append(self.value_3)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 3.")
                        return
                elif self.lbl_3.cget('text') == "Decimals":
                    try:                        
                        float(self.value_3)                        
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_2.append(self.var_3.get())
                            self.data_2.append(self.lbl_3.cget('text'))
                            self.data_2.append(self.var_3_cond.get())
                            self.data_2.append(self.value_3)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_2.append(self.var_3.get())
                            self.data_2.append(self.lbl_3.cget('text'))
                            self.data_2.append(self.var_3_cond.get())
                            self.data_2.append(self.value_3)                   
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 3.")
                        return               
                elif self.lbl_3.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_3, "%Y-%m-%d")
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                            self.data_2.append(self.var_3.get())
                            self.data_2.append(self.lbl_3.cget('text'))
                            self.data_2.append(self.var_3_cond.get())
                            self.data_2.append(self.value_3)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''                  
                            self.data_2.append(self.var_3.get())
                            self.data_2.append(self.lbl_3.cget('text'))
                            self.data_2.append(self.var_3_cond.get())
                            self.data_2.append(self.value_3)
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 3.")
                        return
                elif self.lbl_3.cget('text') == "True/False":
                    if self.value_3 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                            self.data_2.append(self.var_3.get())
                            self.data_2.append(self.lbl_3.cget('text'))
                            self.data_2.append(self.var_3_cond.get())
                            self.data_2.append(self.value_3)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                            self.data_2.append(self.var_3.get())
                            self.data_2.append(self.lbl_3.cget('text'))
                            self.data_2.append(self.var_3_cond.get())
                            self.data_2.append(self.value_3)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 3.")
                        return
                elif self.lbl_3.cget('text') == "Text":
                    if self.filter_prompt_2 == "":
                        self.filter_prompt_2 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                        self.data_2.append(self.var_3.get())
                        self.data_2.append(self.lbl_3.cget('text'))
                        self.data_2.append(self.var_3_cond.get())
                        self.data_2.append(self.value_3)
                    else:
                        self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                        self.data_2.append(self.var_3.get())
                        self.data_2.append(self.lbl_3.cget('text'))
                        self.data_2.append(self.var_3_cond.get())
                        self.data_2.append(self.value_3)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 3.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_3 == "" and self.lbl_3.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 3.")
            return

        # Checking the data type and validating it for subfilter 4 ------------------------------------
        self.value_4 = self.entry_4.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_4 != "":
            if self.var_4_cond.get() != "":
                if self.lbl_4.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 4.")
                    return                
                elif self.lbl_4.cget('text') == "Integer":
                    if self.value_4.isdigit():
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_2.append(self.var_4.get())
                            self.data_2.append(self.lbl_4.cget('text'))
                            self.data_2.append(self.var_4_cond.get())
                            self.data_2.append(self.value_4)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_2.append(self.var_4.get())
                            self.data_2.append(self.lbl_4.cget('text'))
                            self.data_2.append(self.var_4_cond.get())
                            self.data_2.append(self.value_4)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 4.")
                        return
                elif self.lbl_4.cget('text') == "Decimals":
                    try:                        
                        float(self.value_4)                        
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_2.append(self.var_4.get())
                            self.data_2.append(self.lbl_4.cget('text'))
                            self.data_2.append(self.var_4_cond.get())
                            self.data_2.append(self.value_4)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_2.append(self.var_4.get())
                            self.data_2.append(self.lbl_4.cget('text'))
                            self.data_2.append(self.var_4_cond.get())
                            self.data_2.append(self.value_4)                  
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 4.")
                        return               
                elif self.lbl_4.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_4, "%Y-%m-%d")
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_2.append(self.var_4.get())
                            self.data_2.append(self.lbl_4.cget('text'))
                            self.data_2.append(self.var_4_cond.get())
                            self.data_2.append(self.value_4)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_2.append(self.var_4.get())
                            self.data_2.append(self.lbl_4.cget('text'))
                            self.data_2.append(self.var_4_cond.get())
                            self.data_2.append(self.value_4)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 4.")
                        return
                elif self.lbl_4.cget('text') == "True/False":
                    if self.value_4 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_2.append(self.var_4.get())
                            self.data_2.append(self.lbl_4.cget('text'))
                            self.data_2.append(self.var_4_cond.get())
                            self.data_2.append(self.value_4)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_2.append(self.var_4.get())
                            self.data_2.append(self.lbl_4.cget('text'))
                            self.data_2.append(self.var_4_cond.get())
                            self.data_2.append(self.value_4)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 4.")
                        return
                elif self.lbl_4.cget('text') == "Text":
                    if self.filter_prompt_2 == "":
                        self.filter_prompt_2 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                        self.data_2.append(self.var_4.get())
                        self.data_2.append(self.lbl_4.cget('text'))
                        self.data_2.append(self.var_4_cond.get())
                        self.data_2.append(self.value_4)
                    else:
                        self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                        self.data_2.append(self.var_4.get())
                        self.data_2.append(self.lbl_4.cget('text'))
                        self.data_2.append(self.var_4_cond.get())
                        self.data_2.append(self.value_4)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 4.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_4 == "" and self.lbl_4.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 4.")
            return
        
        # Checking the data type and validating it for subfilter 5 ------------------------------------
        self.value_5 = self.entry_5.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_5 != "":
            if self.var_5_cond.get() != "":
                if self.lbl_5.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 5.")
                    return                
                elif self.lbl_5.cget('text') == "Integer":
                    if self.value_5.isdigit():
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_2.append(self.var_5.get())
                            self.data_2.append(self.lbl_5.cget('text'))
                            self.data_2.append(self.var_5_cond.get())
                            self.data_2.append(self.value_5)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_2.append(self.var_5.get())
                            self.data_2.append(self.lbl_5.cget('text'))
                            self.data_2.append(self.var_5_cond.get())
                            self.data_2.append(self.value_5)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 5.")
                        return
                elif self.lbl_5.cget('text') == "Decimals":
                    try:                        
                        float(self.value_5)                        
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_2.append(self.var_5.get())
                            self.data_2.append(self.lbl_5.cget('text'))
                            self.data_2.append(self.var_5_cond.get())
                            self.data_2.append(self.value_5)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_2.append(self.var_5.get())
                            self.data_2.append(self.lbl_5.cget('text'))
                            self.data_2.append(self.var_5_cond.get())
                            self.data_2.append(self.value_5)                   
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 5.")
                        return               
                elif self.lbl_5.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_5, "%Y-%m-%d")
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_2.append(self.var_5.get())
                            self.data_2.append(self.lbl_5.cget('text'))
                            self.data_2.append(self.var_5_cond.get())
                            self.data_2.append(self.value_5)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_2.append(self.var_5.get())
                            self.data_2.append(self.lbl_5.cget('text'))
                            self.data_2.append(self.var_5_cond.get())
                            self.data_2.append(self.value_5)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 5.")
                        return
                elif self.lbl_5.cget('text') == "True/False":
                    if self.value_5 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_2 == "":
                            self.filter_prompt_2 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_2.append(self.var_5.get())
                            self.data_2.append(self.lbl_5.cget('text'))
                            self.data_2.append(self.var_5_cond.get())
                            self.data_2.append(self.value_5)
                        else:
                            self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_2.append(self.var_5.get())
                            self.data_2.append(self.lbl_5.cget('text'))
                            self.data_2.append(self.var_5_cond.get())
                            self.data_2.append(self.value_5)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 5.")
                        return
                elif self.lbl_5.cget('text') == "Text":
                    if self.filter_prompt_2 == "":
                        self.filter_prompt_2 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                        self.data_2.append(self.var_5.get())
                        self.data_2.append(self.lbl_5.cget('text'))
                        self.data_2.append(self.var_5_cond.get())
                        self.data_2.append(self.value_5)
                    else:
                        self.filter_prompt_2 = self.filter_prompt_2 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                        self.data_2.append(self.var_5.get())
                        self.data_2.append(self.lbl_5.cget('text'))
                        self.data_2.append(self.var_5_cond.get())
                        self.data_2.append(self.value_5)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 5.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_5 == "" and self.lbl_5.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 5.")
            return

        # If the user is saving something empty, the app will notify
        if not self.data_2:
            self.answer1 = messagebox.askyesno(title="Nothing to save",parent=self.window, message="You are not saving any filter, would you like to close the window?")
            if self.answer1:
                self.window.destroy()
                return
            else:
                return

        # Saving the information and closing the window
        self.answer = messagebox.askyesno(title="Saving this filter",parent=self.window, message="Are you sure you want to save this filter?\n" + self.filter_prompt_2)
        if self.answer:
            self.parent.filter_prompt_2 = self.filter_prompt_2  # Saving the prompt into the Main Window Class
            self.parent.data_2 = self.data_2                    # Saving the Data into a list in the Main Window Class
            self.parent.write_filter_2()
            self.window.destroy()
            return
        else:
            return

    # If there was data sent from Main Class (Edit the filter), then the data is loaded:
    def check_data(self):
        if not self.data_2:
            return
        else:
            if len(self.data_2) == 4:
                self.drdw_1.set(self.data_2[0])
                self.lbl_1.config(text=self.data_2[1])
                self.drdw_1_cond.set(self.data_2[2])
                self.entry_1_value.set(self.data_2[3])
            elif len(self.data_2) == 8:
                self.drdw_1.set(self.data_2[0])
                self.lbl_1.config(text=self.data_2[1])
                self.drdw_1_cond.set(self.data_2[2])
                self.entry_1_value.set(self.data_2[3])
                self.drdw_2.set(self.data_2[4])
                self.lbl_2.config(text=self.data_2[5])
                self.drdw_2_cond.set(self.data_2[6])
                self.entry_2_value.set(self.data_2[7])
            elif len(self.data_2) == 12:
                self.drdw_1.set(self.data_2[0])
                self.lbl_1.config(text=self.data_2[1])
                self.drdw_1_cond.set(self.data_2[2])
                self.entry_1_value.set(self.data_2[3])
                self.drdw_2.set(self.data_2[4])
                self.lbl_2.config(text=self.data_2[5])
                self.drdw_2_cond.set(self.data_2[6])
                self.entry_2_value.set(self.data_2[7])
                self.drdw_3.set(self.data_2[8])
                self.lbl_3.config(text=self.data_2[9])
                self.drdw_3_cond.set(self.data_2[10])
                self.entry_3_value.set(self.data_2[11])
            elif len(self.data_2) == 16:
                self.drdw_1.set(self.data_2[0])
                self.lbl_1.config(text=self.data_2[1])
                self.drdw_1_cond.set(self.data_2[2])
                self.entry_1_value.set(self.data_2[3])
                self.drdw_2.set(self.data_2[4])
                self.lbl_2.config(text=self.data_2[5])
                self.drdw_2_cond.set(self.data_2[6])
                self.entry_2_value.set(self.data_2[7])
                self.drdw_3.set(self.data_2[8])
                self.lbl_3.config(text=self.data_2[9])
                self.drdw_3_cond.set(self.data_2[10])
                self.entry_3_value.set(self.data_2[11])
                self.drdw_4.set(self.data_2[12])
                self.lbl_4.config(text=self.data_2[13])
                self.drdw_4_cond.set(self.data_2[14])
                self.entry_4_value.set(self.data_2[15])
            elif len(self.data_2) == 20:
                self.drdw_1.set(self.data_2[0])
                self.lbl_1.config(text=self.data_2[1])
                self.drdw_1_cond.set(self.data_2[2])
                self.entry_1_value.set(self.data_2[3])
                self.drdw_2.set(self.data_2[4])
                self.lbl_2.config(text=self.data_2[5])
                self.drdw_2_cond.set(self.data_2[6])
                self.entry_2_value.set(self.data_2[7])
                self.drdw_3.set(self.data_2[8])
                self.lbl_3.config(text=self.data_2[9])
                self.drdw_3_cond.set(self.data_2[10])
                self.entry_3_value.set(self.data_2[11])
                self.drdw_4.set(self.data_2[12])
                self.lbl_4.config(text=self.data_2[13])
                self.drdw_4_cond.set(self.data_2[14])
                self.entry_4_value.set(self.data_2[15])
                self.drdw_5.set(self.data_2[16])
                self.lbl_5.config(text=self.data_2[17])
                self.drdw_5_cond.set(self.data_2[18])
                self.entry_5_value.set(self.data_2[19])

# Class to the CSV filter for BAR 3 window
class Filter3:
    
    # Initialization Function
    def __init__(self, parent, df, data_3, title="Filter Configuration for Bar # 3"):
        
        self.parent = parent

        # Window Characteristics
        self.window = tk.Toplevel(parent.root)
        self.window.title(title)
        self.w_win = 700
        self.h_win = 310
        self.wtotal = root.winfo_screenwidth()
        self.htotal = root.winfo_screenheight()
        self.pwidth = round(self.wtotal/2-self.w_win/2)
        self.pheight = round(self.htotal/2-self.h_win/2)
        self.window.geometry(str(self.w_win)+"x"+str(self.h_win)+"+"+str(self.pwidth)+"+"+str(self.pheight))

        
        # Creating the DataFrame (this came from the previous class)
        self.df = df

        #Creating the data
        self.data_3 = data_3

        # Launching the UI
        self.setup_ui()
        self.check_data()
    
        
    # User Interface Function
    def setup_ui(self):

        # Points of reference
        self.x = 40
        self.y = 80

        # Top Labels
        tk.Label(self.window, text="You can create up to 5 filters for each bar.").place(x=self.x-6, y = self.y - 60)
        tk.Label(self.window, text="Item").place(x=self.x-6, y = self.y - 30)
        tk.Label(self.window, text="Column").place(x=self.x+85, y = self.y - 30)
        tk.Label(self.window, text="Status").place(x=self.x+205, y = self.y - 30)
        tk.Label(self.window, text="Condition").place(x=self.x+330     , y = self.y - 30)
        tk.Label(self.window, text="Value").place(x=self.x+490, y = self.y - 30)
        tk.Label(self.window, text="Reset").place(x=self.x+590, y = self.y - 30)

        # Buttons
        tk.Button(self.window, text="Save Filter", command=self.save_filter).place(x=self.x+555,y=self.y+180)

        # Extracting the columns from the original dataframe into a list
        cols = list(self.df.columns)

        # 5 dropdowns are created and filled with the CSV's columns + labels with data types. Order: Subfilter Name, Column, Status, Condition, Value
        self.space = 35
            #1
        self.lbl_1_name = tk.Label(self.window, text="1.")
        self.lbl_1_name.place(x=self.x, y=self.y)
        self.var_1 = tk.StringVar()
        self.drdw_1 = ttk.Combobox(self.window, textvariable=self.var_1)
        self.drdw_1.place(x=self.x+35, y=self.y)
        self.drdw_1["values"] = cols
        self.var_1_cond = tk.StringVar()
        self.drdw_1_cond = ttk.Combobox(self.window, textvariable=self.var_1_cond)
        self.drdw_1_cond.place(x=self.x+285, y=self.y)
        self.lbl_1 = tk.Label(self.window, text="Select column.")
        self.lbl_1.place(x=self.x+185, y=self.y)
        self.entry_1_value = tk.StringVar()
        self.entry_1 = ttk.Entry(self.window, textvariable=self.entry_1_value)
        self.entry_1.place(x=self.x+445, y=self.y)
        self.btn_reset_1 = tk.Button(self.window, text="!", command=self.reset_filter1, bg='red', fg='white')
        self.btn_reset_1.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #2
        self.lbl_2_name = tk.Label(self.window, text="2.")
        self.lbl_2_name.place(x=self.x, y=self.y)
        self.var_2 = tk.StringVar()
        self.drdw_2 = ttk.Combobox(self.window, textvariable=self.var_2)
        self.drdw_2.place(x=self.x+35, y=self.y)
        self.drdw_2["values"] = cols
        self.var_2_cond = tk.StringVar()
        self.drdw_2_cond = ttk.Combobox(self.window, textvariable=self.var_2_cond)
        self.drdw_2_cond.place(x=self.x+285, y=self.y)
        self.lbl_2 = tk.Label(self.window, text="Select column.")
        self.lbl_2.place(x=self.x+185, y=self.y)
        self.entry_2_value = tk.StringVar()
        self.entry_2 = ttk.Entry(self.window, textvariable=self.entry_2_value)
        self.entry_2.place(x=self.x+445, y=self.y)
        self.btn_reset_2 = tk.Button(self.window, text="!", command=self.reset_filter2, bg='red', fg='white')
        self.btn_reset_2.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #3
        self.lbl_3_name = tk.Label(self.window, text="3.")
        self.lbl_3_name.place(x=self.x, y=self.y)
        self.var_3 = tk.StringVar()
        self.drdw_3 = ttk.Combobox(self.window, textvariable=self.var_3)
        self.drdw_3.place(x=self.x+35, y=self.y)
        self.drdw_3["values"] = cols
        self.var_3_cond = tk.StringVar()
        self.drdw_3_cond = ttk.Combobox(self.window, textvariable=self.var_3_cond)
        self.drdw_3_cond.place(x=self.x+285, y=self.y)
        self.lbl_3 = tk.Label(self.window, text="Select column.")
        self.lbl_3.place(x=self.x+185, y=self.y)
        self.entry_3_value = tk.StringVar()
        self.entry_3 = ttk.Entry(self.window, textvariable=self.entry_3_value)
        self.entry_3.place(x=self.x+445, y=self.y)
        self.btn_reset_3 = tk.Button(self.window, text="!", command=self.reset_filter3, bg='red', fg='white')
        self.btn_reset_3.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #4
        self.lbl_4_name = tk.Label(self.window, text="4.")
        self.lbl_4_name.place(x=self.x, y=self.y)
        self.var_4 = tk.StringVar()
        self.drdw_4 = ttk.Combobox(self.window, textvariable=self.var_4)
        self.drdw_4.place(x=self.x+35, y=self.y)
        self.drdw_4["values"] = cols
        self.var_4_cond = tk.StringVar()
        self.drdw_4_cond = ttk.Combobox(self.window, textvariable=self.var_4_cond)
        self.drdw_4_cond.place(x=self.x+285, y=self.y)
        self.lbl_4 = tk.Label(self.window, text="Select column.")
        self.lbl_4.place(x=self.x+185, y=self.y)
        self.entry_4_value = tk.StringVar()
        self.entry_4 = ttk.Entry(self.window, textvariable=self.entry_4_value)
        self.entry_4.place(x=self.x+445, y=self.y)
        self.btn_reset_4 = tk.Button(self.window, text="!", command=self.reset_filter4, bg='red', fg='white')
        self.btn_reset_4.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #5
        self.lbl_5_name = tk.Label(self.window, text="5.")
        self.lbl_5_name.place(x=self.x, y=self.y)
        self.var_5 = tk.StringVar()
        self.drdw_5 = ttk.Combobox(self.window, textvariable=self.var_5)
        self.drdw_5.place(x=self.x+35, y=self.y)
        self.drdw_5["values"] = cols
        self.var_5_cond = tk.StringVar()
        self.drdw_5_cond = ttk.Combobox(self.window, textvariable=self.var_5_cond)
        self.drdw_5_cond.place(x=self.x+285, y=self.y)
        self.lbl_5 = tk.Label(self.window, text="Select column.")
        self.lbl_5.place(x=self.x+185, y=self.y)
        self.entry_5_value = tk.StringVar()
        self.entry_5 = ttk.Entry(self.window, textvariable=self.entry_5_value)
        self.entry_5.place(x=self.x+445, y=self.y)
        self.btn_reset_5 = tk.Button(self.window, text="!", command=self.reset_filter5, bg='red', fg='white')
        self.btn_reset_5.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space

        # Action when value of dropdown changes
        self.drdw_1.bind("<<ComboboxSelected>>", self.drdw_1_change)
        self.drdw_2.bind("<<ComboboxSelected>>", self.drdw_2_change)
        self.drdw_3.bind("<<ComboboxSelected>>", self.drdw_3_change)
        self.drdw_4.bind("<<ComboboxSelected>>", self.drdw_4_change)
        self.drdw_5.bind("<<ComboboxSelected>>", self.drdw_5_change)

    # Function to identify the data type for subfilter 1 and displaying filtering options
    def drdw_1_change(self, event):
        current_value = self.var_1.get()
        current_type = self.df[current_value].dtype
        self.drdw_1_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_1_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_1_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_1_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_1_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_1_cond["values"] = ["=="]
        
        self.lbl_1.config(text=current_type)
    
    # Function to identify the data type for subfilter 2 and displaying filtering options
    def drdw_2_change(self, event):
        current_value = self.var_2.get()
        current_type = self.df[current_value].dtype
        self.drdw_2_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_2_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_2_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_2_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_2_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_2_cond["values"] = ["=="]

        self.lbl_2.config(text=current_type)
    
    # Function to identify the data type for subfilter 3 and displaying filtering options
    def drdw_3_change(self, event):
        current_value = self.var_3.get()
        current_type = self.df[current_value].dtype
        self.drdw_3_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_3_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_3_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_3_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_3_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_3_cond["values"] = ["=="]

        self.lbl_3.config(text=current_type)

    # Function to identify the data type for subfilter 4 and displaying filtering options
    def drdw_4_change(self, event):
        current_value = self.var_4.get()
        current_type = self.df[current_value].dtype
        self.drdw_4_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_4_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_4_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_4_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_4_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_4_cond["values"] = ["=="]

        self.lbl_4.config(text=current_type)
    
    # Function to identify the data type for subfilter 5 and displaying filtering options
    def drdw_5_change(self, event):
        current_value = self.var_5.get()
        current_type = self.df[current_value].dtype
        self.drdw_5_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_5_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_5_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_5_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_5_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_5_cond["values"] = ["=="]

        self.lbl_5.config(text=current_type)

    # Reset Subfilter 1 values
    def reset_filter1(self):
        self.drdw_1.set("")
        self.drdw_1_cond.set("")
        self.entry_1_value.set("")
        self.lbl_1.config(text="Select column.")
    
    # Reset Subfilter 2 values
    def reset_filter2(self):
        self.drdw_2.set("")
        self.drdw_2_cond.set("")
        self.entry_2_value.set("")
        self.lbl_2.config(text="Select column.")
    
    # Reset Subfilter 3 values
    def reset_filter3(self):
        self.drdw_3.set("")
        self.drdw_3_cond.set("")
        self.entry_3_value.set("")
        self.lbl_3.config(text="Select column.")

    # Reset Subfilter 4 values
    def reset_filter4(self):
        self.drdw_4.set("")
        self.drdw_4_cond.set("")
        self.entry_4_value.set("")
        self.lbl_4.config(text="Select column.")
    
    # Reset Subfilter 5 values
    def reset_filter5(self):
        self.drdw_5.set("")
        self.drdw_5_cond.set("")
        self.entry_5_value.set("")
        self.lbl_5.config(text="Select column.")

    # Saving the filter configuration    
    def save_filter(self):

        self.num_filters = 0
        self.filter_prompt_3 = ""
        self.data_3 = []

        # Checking the data type and validating it for subfilter 1 ------------------------------------
        self.value_1 = self.entry_1.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_1 != "":
            if self.var_1_cond.get() != "":
                if self.lbl_1.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 1.")
                    return                
                elif self.lbl_1.cget('text') == "Integer":
                    if self.value_1.isdigit():
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_3.append(self.var_1.get())
                            self.data_3.append(self.lbl_1.cget('text'))
                            self.data_3.append(self.var_1_cond.get())
                            self.data_3.append(self.value_1)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_3.append(self.var_1.get())
                            self.data_3.append(self.lbl_1.cget('text'))
                            self.data_3.append(self.var_1_cond.get())
                            self.data_3.append(self.value_1)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 1.")
                        return
                elif self.lbl_1.cget('text') == "Decimals":
                    try:                        
                        float(self.value_1)                        
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_3.append(self.var_1.get())
                            self.data_3.append(self.lbl_1.cget('text'))
                            self.data_3.append(self.var_1_cond.get())
                            self.data_3.append(self.value_1)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_3.append(self.var_1.get())
                            self.data_3.append(self.lbl_1.cget('text'))
                            self.data_3.append(self.var_1_cond.get())
                            self.data_3.append(self.value_1)                  
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 1.")
                        return               
                elif self.lbl_1.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_1, "%Y-%m-%d")
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_3.append(self.var_1.get())
                            self.data_3.append(self.lbl_1.cget('text'))
                            self.data_3.append(self.var_1_cond.get())
                            self.data_3.append(self.value_1)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_3.append(self.var_1.get())
                            self.data_3.append(self.lbl_1.cget('text'))
                            self.data_3.append(self.var_1_cond.get())
                            self.data_3.append(self.value_1)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 1.")
                        return
                elif self.lbl_1.cget('text') == "True/False":
                    if self.value_1 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_3.append(self.var_1.get())
                            self.data_3.append(self.lbl_1.cget('text'))
                            self.data_3.append(self.var_1_cond.get())
                            self.data_3.append(self.value_1)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_3.append(self.var_1.get())
                            self.data_3.append(self.lbl_1.cget('text'))
                            self.data_3.append(self.var_1_cond.get())
                            self.data_3.append(self.value_1)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 1.")
                        return
                elif self.lbl_1.cget('text') == "Text":
                    if self.filter_prompt_3 == "":
                        self.filter_prompt_3 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                        self.data_3.append(self.var_1.get())
                        self.data_3.append(self.lbl_1.cget('text'))
                        self.data_3.append(self.var_1_cond.get())
                        self.data_3.append(self.value_1)
                    else:
                        self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                        self.data_3.append(self.var_1.get())
                        self.data_3.append(self.lbl_1.cget('text'))
                        self.data_3.append(self.var_1_cond.get())
                        self.data_3.append(self.value_1)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 1.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_1 == "" and self.lbl_1.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 1.")
            return

        # Checking the data type and validating it for subfilter 2 ------------------------------------
        self.value_2 = self.entry_2.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_2 != "":
            if self.var_2_cond.get() != "":
                if self.lbl_2.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 2.")
                    return                
                elif self.lbl_2.cget('text') == "Integer":
                    if self.value_2.isdigit():
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_3.append(self.var_2.get())
                            self.data_3.append(self.lbl_2.cget('text'))
                            self.data_3.append(self.var_2_cond.get())
                            self.data_3.append(self.value_2)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_3.append(self.var_2.get())
                            self.data_3.append(self.lbl_2.cget('text'))
                            self.data_3.append(self.var_2_cond.get())
                            self.data_3.append(self.value_2)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 2.")
                        return
                elif self.lbl_2.cget('text') == "Decimals":
                    try:                        
                        float(self.value_2)                        
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_3.append(self.var_2.get())
                            self.data_3.append(self.lbl_2.cget('text'))
                            self.data_3.append(self.var_2_cond.get())
                            self.data_3.append(self.value_2)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_3.append(self.var_2.get())
                            self.data_3.append(self.lbl_2.cget('text'))
                            self.data_3.append(self.var_2_cond.get())
                            self.data_3.append(self.value_2)                 
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 2.")
                        return               
                elif self.lbl_2.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_2, "%Y-%m-%d")
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_3.append(self.var_2.get())
                            self.data_3.append(self.lbl_2.cget('text'))
                            self.data_3.append(self.var_2_cond.get())
                            self.data_3.append(self.value_2)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_3.append(self.var_2.get())
                            self.data_3.append(self.lbl_2.cget('text'))
                            self.data_3.append(self.var_2_cond.get())
                            self.data_3.append(self.value_2)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 2.")
                        return
                elif self.lbl_2.cget('text') == "True/False":
                    if self.value_2 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_3.append(self.var_2.get())
                            self.data_3.append(self.lbl_2.cget('text'))
                            self.data_3.append(self.var_2_cond.get())
                            self.data_3.append(self.value_2)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_3.append(self.var_2.get())
                            self.data_3.append(self.lbl_2.cget('text'))
                            self.data_3.append(self.var_2_cond.get())
                            self.data_3.append(self.value_2)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 2.")
                        return
                elif self.lbl_2.cget('text') == "Text":
                    if self.filter_prompt_3 == "":
                        self.filter_prompt_3 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                        self.data_3.append(self.var_2.get())
                        self.data_3.append(self.lbl_2.cget('text'))
                        self.data_3.append(self.var_2_cond.get())
                        self.data_3.append(self.value_2)
                    else:
                        self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                        self.data_3.append(self.var_2.get())
                        self.data_3.append(self.lbl_2.cget('text'))
                        self.data_3.append(self.var_2_cond.get())
                        self.data_3.append(self.value_2)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 2.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_2 == "" and self.lbl_2.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 2.")
            return
        
        # Checking the data type and validating it for subfilter 3 ------------------------------------
        self.value_3 = self.entry_3.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_3 != "":
            if self.var_3_cond.get() != "":
                if self.lbl_3.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 3.")
                    return                
                elif self.lbl_3.cget('text') == "Integer":
                    if self.value_3.isdigit():
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_3.append(self.var_3.get())
                            self.data_3.append(self.lbl_3.cget('text'))
                            self.data_3.append(self.var_3_cond.get())
                            self.data_3.append(self.value_3)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_3.append(self.var_3.get())
                            self.data_3.append(self.lbl_3.cget('text'))
                            self.data_3.append(self.var_3_cond.get())
                            self.data_3.append(self.value_3)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 3.")
                        return
                elif self.lbl_3.cget('text') == "Decimals":
                    try:                        
                        float(self.value_3)                        
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_3.append(self.var_3.get())
                            self.data_3.append(self.lbl_3.cget('text'))
                            self.data_3.append(self.var_3_cond.get())
                            self.data_3.append(self.value_3)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_3.append(self.var_3.get())
                            self.data_3.append(self.lbl_3.cget('text'))
                            self.data_3.append(self.var_3_cond.get())
                            self.data_3.append(self.value_3)                   
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 3.")
                        return               
                elif self.lbl_3.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_3, "%Y-%m-%d")
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                            self.data_3.append(self.var_3.get())
                            self.data_3.append(self.lbl_3.cget('text'))
                            self.data_3.append(self.var_3_cond.get())
                            self.data_3.append(self.value_3)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''                  
                            self.data_3.append(self.var_3.get())
                            self.data_3.append(self.lbl_3.cget('text'))
                            self.data_3.append(self.var_3_cond.get())
                            self.data_3.append(self.value_3)
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 3.")
                        return
                elif self.lbl_3.cget('text') == "True/False":
                    if self.value_3 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                            self.data_3.append(self.var_3.get())
                            self.data_3.append(self.lbl_3.cget('text'))
                            self.data_3.append(self.var_3_cond.get())
                            self.data_3.append(self.value_3)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                            self.data_3.append(self.var_3.get())
                            self.data_3.append(self.lbl_3.cget('text'))
                            self.data_3.append(self.var_3_cond.get())
                            self.data_3.append(self.value_3)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 3.")
                        return
                elif self.lbl_3.cget('text') == "Text":
                    if self.filter_prompt_3 == "":
                        self.filter_prompt_3 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                        self.data_3.append(self.var_3.get())
                        self.data_3.append(self.lbl_3.cget('text'))
                        self.data_3.append(self.var_3_cond.get())
                        self.data_3.append(self.value_3)
                    else:
                        self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                        self.data_3.append(self.var_3.get())
                        self.data_3.append(self.lbl_3.cget('text'))
                        self.data_3.append(self.var_3_cond.get())
                        self.data_3.append(self.value_3)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 3.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_3 == "" and self.lbl_3.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 3.")
            return

        # Checking the data type and validating it for subfilter 4 ------------------------------------
        self.value_4 = self.entry_4.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_4 != "":
            if self.var_4_cond.get() != "":
                if self.lbl_4.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 4.")
                    return                
                elif self.lbl_4.cget('text') == "Integer":
                    if self.value_4.isdigit():
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_3.append(self.var_4.get())
                            self.data_3.append(self.lbl_4.cget('text'))
                            self.data_3.append(self.var_4_cond.get())
                            self.data_3.append(self.value_4)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_3.append(self.var_4.get())
                            self.data_3.append(self.lbl_4.cget('text'))
                            self.data_3.append(self.var_4_cond.get())
                            self.data_3.append(self.value_4)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 4.")
                        return
                elif self.lbl_4.cget('text') == "Decimals":
                    try:                        
                        float(self.value_4)                        
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_3.append(self.var_4.get())
                            self.data_3.append(self.lbl_4.cget('text'))
                            self.data_3.append(self.var_4_cond.get())
                            self.data_3.append(self.value_4)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_3.append(self.var_4.get())
                            self.data_3.append(self.lbl_4.cget('text'))
                            self.data_3.append(self.var_4_cond.get())
                            self.data_3.append(self.value_4)                  
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 4.")
                        return               
                elif self.lbl_4.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_4, "%Y-%m-%d")
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_3.append(self.var_4.get())
                            self.data_3.append(self.lbl_4.cget('text'))
                            self.data_3.append(self.var_4_cond.get())
                            self.data_3.append(self.value_4)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_3.append(self.var_4.get())
                            self.data_3.append(self.lbl_4.cget('text'))
                            self.data_3.append(self.var_4_cond.get())
                            self.data_3.append(self.value_4)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 4.")
                        return
                elif self.lbl_4.cget('text') == "True/False":
                    if self.value_4 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_3.append(self.var_4.get())
                            self.data_3.append(self.lbl_4.cget('text'))
                            self.data_3.append(self.var_4_cond.get())
                            self.data_3.append(self.value_4)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_3.append(self.var_4.get())
                            self.data_3.append(self.lbl_4.cget('text'))
                            self.data_3.append(self.var_4_cond.get())
                            self.data_3.append(self.value_4)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 4.")
                        return
                elif self.lbl_4.cget('text') == "Text":
                    if self.filter_prompt_3 == "":
                        self.filter_prompt_3 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                        self.data_3.append(self.var_4.get())
                        self.data_3.append(self.lbl_4.cget('text'))
                        self.data_3.append(self.var_4_cond.get())
                        self.data_3.append(self.value_4)
                    else:
                        self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                        self.data_3.append(self.var_4.get())
                        self.data_3.append(self.lbl_4.cget('text'))
                        self.data_3.append(self.var_4_cond.get())
                        self.data_3.append(self.value_4)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 4.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_4 == "" and self.lbl_4.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 4.")
            return
        
        # Checking the data type and validating it for subfilter 5 ------------------------------------
        self.value_5 = self.entry_5.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_5 != "":
            if self.var_5_cond.get() != "":
                if self.lbl_5.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 5.")
                    return                
                elif self.lbl_5.cget('text') == "Integer":
                    if self.value_5.isdigit():
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_3.append(self.var_5.get())
                            self.data_3.append(self.lbl_5.cget('text'))
                            self.data_3.append(self.var_5_cond.get())
                            self.data_3.append(self.value_5)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_3.append(self.var_5.get())
                            self.data_3.append(self.lbl_5.cget('text'))
                            self.data_3.append(self.var_5_cond.get())
                            self.data_3.append(self.value_5)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 5.")
                        return
                elif self.lbl_5.cget('text') == "Decimals":
                    try:                        
                        float(self.value_5)                        
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_3.append(self.var_5.get())
                            self.data_3.append(self.lbl_5.cget('text'))
                            self.data_3.append(self.var_5_cond.get())
                            self.data_3.append(self.value_5)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_3.append(self.var_5.get())
                            self.data_3.append(self.lbl_5.cget('text'))
                            self.data_3.append(self.var_5_cond.get())
                            self.data_3.append(self.value_5)                   
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 5.")
                        return               
                elif self.lbl_5.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_5, "%Y-%m-%d")
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_3.append(self.var_5.get())
                            self.data_3.append(self.lbl_5.cget('text'))
                            self.data_3.append(self.var_5_cond.get())
                            self.data_3.append(self.value_5)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_3.append(self.var_5.get())
                            self.data_3.append(self.lbl_5.cget('text'))
                            self.data_3.append(self.var_5_cond.get())
                            self.data_3.append(self.value_5)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 5.")
                        return
                elif self.lbl_5.cget('text') == "True/False":
                    if self.value_5 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_3 == "":
                            self.filter_prompt_3 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_3.append(self.var_5.get())
                            self.data_3.append(self.lbl_5.cget('text'))
                            self.data_3.append(self.var_5_cond.get())
                            self.data_3.append(self.value_5)
                        else:
                            self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_3.append(self.var_5.get())
                            self.data_3.append(self.lbl_5.cget('text'))
                            self.data_3.append(self.var_5_cond.get())
                            self.data_3.append(self.value_5)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 5.")
                        return
                elif self.lbl_5.cget('text') == "Text":
                    if self.filter_prompt_3 == "":
                        self.filter_prompt_3 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                        self.data_3.append(self.var_5.get())
                        self.data_3.append(self.lbl_5.cget('text'))
                        self.data_3.append(self.var_5_cond.get())
                        self.data_3.append(self.value_5)
                    else:
                        self.filter_prompt_3 = self.filter_prompt_3 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                        self.data_3.append(self.var_5.get())
                        self.data_3.append(self.lbl_5.cget('text'))
                        self.data_3.append(self.var_5_cond.get())
                        self.data_3.append(self.value_5)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 5.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_5 == "" and self.lbl_5.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 5.")
            return

        # If the user is saving something empty, the app will notify
        if not self.data_3:
            self.answer1 = messagebox.askyesno(title="Nothing to save",parent=self.window, message="You are not saving any filter, would you like to close the window?")
            if self.answer1:
                self.window.destroy()
                return
            else:
                return

        # Saving the information and closing the window
        self.answer = messagebox.askyesno(title="Saving this filter",parent=self.window, message="Are you sure you want to save this filter?\n" + self.filter_prompt_3)
        if self.answer:
            self.parent.filter_prompt_3 = self.filter_prompt_3  # Saving the prompt into the Main Window Class
            self.parent.data_3 = self.data_3                    # Saving the Data into a list in the Main Window Class
            self.parent.write_filter_3()
            self.window.destroy()
            return
        else:
            return

    # If there was data sent from Main Class (Edit the filter), then the data is loaded:
    def check_data(self):
        if not self.data_3:
            return
        else:
            if len(self.data_3) == 4:
                self.drdw_1.set(self.data_3[0])
                self.lbl_1.config(text=self.data_3[1])
                self.drdw_1_cond.set(self.data_3[2])
                self.entry_1_value.set(self.data_3[3])
            elif len(self.data_3) == 8:
                self.drdw_1.set(self.data_3[0])
                self.lbl_1.config(text=self.data_3[1])
                self.drdw_1_cond.set(self.data_3[2])
                self.entry_1_value.set(self.data_3[3])
                self.drdw_2.set(self.data_3[4])
                self.lbl_2.config(text=self.data_3[5])
                self.drdw_2_cond.set(self.data_3[6])
                self.entry_2_value.set(self.data_3[7])
            elif len(self.data_3) == 12:
                self.drdw_1.set(self.data_3[0])
                self.lbl_1.config(text=self.data_3[1])
                self.drdw_1_cond.set(self.data_3[2])
                self.entry_1_value.set(self.data_3[3])
                self.drdw_2.set(self.data_3[4])
                self.lbl_2.config(text=self.data_3[5])
                self.drdw_2_cond.set(self.data_3[6])
                self.entry_2_value.set(self.data_3[7])
                self.drdw_3.set(self.data_3[8])
                self.lbl_3.config(text=self.data_3[9])
                self.drdw_3_cond.set(self.data_3[10])
                self.entry_3_value.set(self.data_3[11])
            elif len(self.data_3) == 16:
                self.drdw_1.set(self.data_3[0])
                self.lbl_1.config(text=self.data_3[1])
                self.drdw_1_cond.set(self.data_3[2])
                self.entry_1_value.set(self.data_3[3])
                self.drdw_2.set(self.data_3[4])
                self.lbl_2.config(text=self.data_3[5])
                self.drdw_2_cond.set(self.data_3[6])
                self.entry_2_value.set(self.data_3[7])
                self.drdw_3.set(self.data_3[8])
                self.lbl_3.config(text=self.data_3[9])
                self.drdw_3_cond.set(self.data_3[10])
                self.entry_3_value.set(self.data_3[11])
                self.drdw_4.set(self.data_3[12])
                self.lbl_4.config(text=self.data_3[13])
                self.drdw_4_cond.set(self.data_3[14])
                self.entry_4_value.set(self.data_3[15])
            elif len(self.data_3) == 20:
                self.drdw_1.set(self.data_3[0])
                self.lbl_1.config(text=self.data_3[1])
                self.drdw_1_cond.set(self.data_3[2])
                self.entry_1_value.set(self.data_3[3])
                self.drdw_2.set(self.data_3[4])
                self.lbl_2.config(text=self.data_3[5])
                self.drdw_2_cond.set(self.data_3[6])
                self.entry_2_value.set(self.data_3[7])
                self.drdw_3.set(self.data_3[8])
                self.lbl_3.config(text=self.data_3[9])
                self.drdw_3_cond.set(self.data_3[10])
                self.entry_3_value.set(self.data_3[11])
                self.drdw_4.set(self.data_3[12])
                self.lbl_4.config(text=self.data_3[13])
                self.drdw_4_cond.set(self.data_3[14])
                self.entry_4_value.set(self.data_3[15])
                self.drdw_5.set(self.data_3[16])
                self.lbl_5.config(text=self.data_3[17])
                self.drdw_5_cond.set(self.data_3[18])
                self.entry_5_value.set(self.data_3[19])

# Class to the CSV filter for BAR 4 window
class Filter4:
    
    # Initialization Function
    def __init__(self, parent, df, data_4, title="Filter Configuration for Bar # 4"):
        
        self.parent = parent

        # Window Characteristics
        self.window = tk.Toplevel(parent.root)
        self.window.title(title)
        self.w_win = 700
        self.h_win = 310
        self.wtotal = root.winfo_screenwidth()
        self.htotal = root.winfo_screenheight()
        self.pwidth = round(self.wtotal/2-self.w_win/2)
        self.pheight = round(self.htotal/2-self.h_win/2)
        self.window.geometry(str(self.w_win)+"x"+str(self.h_win)+"+"+str(self.pwidth)+"+"+str(self.pheight))

        # Creating the DataFrame (this came from the Main class)
        self.df = df

        #Creating the data
        self.data_4 = data_4

        # Launching the UI
        self.setup_ui()
        self.check_data()
    
        
    # User Interface Function
    def setup_ui(self):

        # Points of reference
        self.x = 40
        self.y = 80

        # Top Labels
        tk.Label(self.window, text="You can create up to 5 filters for each bar.").place(x=self.x-6, y = self.y - 60)
        tk.Label(self.window, text="Item").place(x=self.x-6, y = self.y - 30)
        tk.Label(self.window, text="Column").place(x=self.x+85, y = self.y - 30)
        tk.Label(self.window, text="Status").place(x=self.x+205, y = self.y - 30)
        tk.Label(self.window, text="Condition").place(x=self.x+330     , y = self.y - 30)
        tk.Label(self.window, text="Value").place(x=self.x+490, y = self.y - 30)
        tk.Label(self.window, text="Reset").place(x=self.x+590, y = self.y - 30)

        # Buttons
        tk.Button(self.window, text="Save Filter", command=self.save_filter).place(x=self.x+555,y=self.y+180)

        # Extracting the columns from the original dataframe into a list
        cols = list(self.df.columns)

        # 5 dropdowns are created and filled with the CSV's columns + labels with data types. Order: Subfilter Name, Column, Status, Condition, Value
        self.space = 35
            #1
        self.lbl_1_name = tk.Label(self.window, text="1.")
        self.lbl_1_name.place(x=self.x, y=self.y)
        self.var_1 = tk.StringVar()
        self.drdw_1 = ttk.Combobox(self.window, textvariable=self.var_1)
        self.drdw_1.place(x=self.x+35, y=self.y)
        self.drdw_1["values"] = cols
        self.var_1_cond = tk.StringVar()
        self.drdw_1_cond = ttk.Combobox(self.window, textvariable=self.var_1_cond)
        self.drdw_1_cond.place(x=self.x+285, y=self.y)
        self.lbl_1 = tk.Label(self.window, text="Select column.")
        self.lbl_1.place(x=self.x+185, y=self.y)
        self.entry_1_value = tk.StringVar()
        self.entry_1 = ttk.Entry(self.window, textvariable=self.entry_1_value)
        self.entry_1.place(x=self.x+445, y=self.y)
        self.btn_reset_1 = tk.Button(self.window, text="!", command=self.reset_filter1, bg='red', fg='white')
        self.btn_reset_1.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #2
        self.lbl_2_name = tk.Label(self.window, text="2.")
        self.lbl_2_name.place(x=self.x, y=self.y)
        self.var_2 = tk.StringVar()
        self.drdw_2 = ttk.Combobox(self.window, textvariable=self.var_2)
        self.drdw_2.place(x=self.x+35, y=self.y)
        self.drdw_2["values"] = cols
        self.var_2_cond = tk.StringVar()
        self.drdw_2_cond = ttk.Combobox(self.window, textvariable=self.var_2_cond)
        self.drdw_2_cond.place(x=self.x+285, y=self.y)
        self.lbl_2 = tk.Label(self.window, text="Select column.")
        self.lbl_2.place(x=self.x+185, y=self.y)
        self.entry_2_value = tk.StringVar()
        self.entry_2 = ttk.Entry(self.window, textvariable=self.entry_2_value)
        self.entry_2.place(x=self.x+445, y=self.y)
        self.btn_reset_2 = tk.Button(self.window, text="!", command=self.reset_filter2, bg='red', fg='white')
        self.btn_reset_2.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #3
        self.lbl_3_name = tk.Label(self.window, text="3.")
        self.lbl_3_name.place(x=self.x, y=self.y)
        self.var_3 = tk.StringVar()
        self.drdw_3 = ttk.Combobox(self.window, textvariable=self.var_3)
        self.drdw_3.place(x=self.x+35, y=self.y)
        self.drdw_3["values"] = cols
        self.var_3_cond = tk.StringVar()
        self.drdw_3_cond = ttk.Combobox(self.window, textvariable=self.var_3_cond)
        self.drdw_3_cond.place(x=self.x+285, y=self.y)
        self.lbl_3 = tk.Label(self.window, text="Select column.")
        self.lbl_3.place(x=self.x+185, y=self.y)
        self.entry_3_value = tk.StringVar()
        self.entry_3 = ttk.Entry(self.window, textvariable=self.entry_3_value)
        self.entry_3.place(x=self.x+445, y=self.y)
        self.btn_reset_3 = tk.Button(self.window, text="!", command=self.reset_filter3, bg='red', fg='white')
        self.btn_reset_3.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #4
        self.lbl_4_name = tk.Label(self.window, text="4.")
        self.lbl_4_name.place(x=self.x, y=self.y)
        self.var_4 = tk.StringVar()
        self.drdw_4 = ttk.Combobox(self.window, textvariable=self.var_4)
        self.drdw_4.place(x=self.x+35, y=self.y)
        self.drdw_4["values"] = cols
        self.var_4_cond = tk.StringVar()
        self.drdw_4_cond = ttk.Combobox(self.window, textvariable=self.var_4_cond)
        self.drdw_4_cond.place(x=self.x+285, y=self.y)
        self.lbl_4 = tk.Label(self.window, text="Select column.")
        self.lbl_4.place(x=self.x+185, y=self.y)
        self.entry_4_value = tk.StringVar()
        self.entry_4 = ttk.Entry(self.window, textvariable=self.entry_4_value)
        self.entry_4.place(x=self.x+445, y=self.y)
        self.btn_reset_4 = tk.Button(self.window, text="!", command=self.reset_filter4, bg='red', fg='white')
        self.btn_reset_4.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #5
        self.lbl_5_name = tk.Label(self.window, text="5.")
        self.lbl_5_name.place(x=self.x, y=self.y)
        self.var_5 = tk.StringVar()
        self.drdw_5 = ttk.Combobox(self.window, textvariable=self.var_5)
        self.drdw_5.place(x=self.x+35, y=self.y)
        self.drdw_5["values"] = cols
        self.var_5_cond = tk.StringVar()
        self.drdw_5_cond = ttk.Combobox(self.window, textvariable=self.var_5_cond)
        self.drdw_5_cond.place(x=self.x+285, y=self.y)
        self.lbl_5 = tk.Label(self.window, text="Select column.")
        self.lbl_5.place(x=self.x+185, y=self.y)
        self.entry_5_value = tk.StringVar()
        self.entry_5 = ttk.Entry(self.window, textvariable=self.entry_5_value)
        self.entry_5.place(x=self.x+445, y=self.y)
        self.btn_reset_5 = tk.Button(self.window, text="!", command=self.reset_filter5, bg='red', fg='white')
        self.btn_reset_5.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space

        # Action when value of dropdown changes
        self.drdw_1.bind("<<ComboboxSelected>>", self.drdw_1_change)
        self.drdw_2.bind("<<ComboboxSelected>>", self.drdw_2_change)
        self.drdw_3.bind("<<ComboboxSelected>>", self.drdw_3_change)
        self.drdw_4.bind("<<ComboboxSelected>>", self.drdw_4_change)
        self.drdw_5.bind("<<ComboboxSelected>>", self.drdw_5_change)

    # Function to identify the data type for subfilter 1 and displaying filtering options
    def drdw_1_change(self, event):
        current_value = self.var_1.get()
        current_type = self.df[current_value].dtype
        self.drdw_1_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_1_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_1_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_1_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_1_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_1_cond["values"] = ["=="]
        
        self.lbl_1.config(text=current_type)
    
    # Function to identify the data type for subfilter 2 and displaying filtering options
    def drdw_2_change(self, event):
        current_value = self.var_2.get()
        current_type = self.df[current_value].dtype
        self.drdw_2_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_2_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_2_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_2_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_2_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_2_cond["values"] = ["=="]

        self.lbl_2.config(text=current_type)
    
    # Function to identify the data type for subfilter 3 and displaying filtering options
    def drdw_3_change(self, event):
        current_value = self.var_3.get()
        current_type = self.df[current_value].dtype
        self.drdw_3_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_3_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_3_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_3_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_3_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_3_cond["values"] = ["=="]

        self.lbl_3.config(text=current_type)

    # Function to identify the data type for subfilter 4 and displaying filtering options
    def drdw_4_change(self, event):
        current_value = self.var_4.get()
        current_type = self.df[current_value].dtype
        self.drdw_4_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_4_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_4_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_4_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_4_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_4_cond["values"] = ["=="]

        self.lbl_4.config(text=current_type)
    
    # Function to identify the data type for subfilter 5 and displaying filtering options
    def drdw_5_change(self, event):
        current_value = self.var_5.get()
        current_type = self.df[current_value].dtype
        self.drdw_5_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_5_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_5_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_5_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_5_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_5_cond["values"] = ["=="]

        self.lbl_5.config(text=current_type)

    # Reset Subfilter 1 values
    def reset_filter1(self):
        self.drdw_1.set("")
        self.drdw_1_cond.set("")
        self.entry_1_value.set("")
        self.lbl_1.config(text="Select column.")
    
    # Reset Subfilter 2 values
    def reset_filter2(self):
        self.drdw_2.set("")
        self.drdw_2_cond.set("")
        self.entry_2_value.set("")
        self.lbl_2.config(text="Select column.")
    
    # Reset Subfilter 3 values
    def reset_filter3(self):
        self.drdw_3.set("")
        self.drdw_3_cond.set("")
        self.entry_3_value.set("")
        self.lbl_3.config(text="Select column.")

    # Reset Subfilter 4 values
    def reset_filter4(self):
        self.drdw_4.set("")
        self.drdw_4_cond.set("")
        self.entry_4_value.set("")
        self.lbl_4.config(text="Select column.")
    
    # Reset Subfilter 5 values
    def reset_filter5(self):
        self.drdw_5.set("")
        self.drdw_5_cond.set("")
        self.entry_5_value.set("")
        self.lbl_5.config(text="Select column.")

    # Saving the filter configuration    
    def save_filter(self):

        self.num_filters = 0
        self.filter_prompt_4 = ""
        self.data_4 = []

        # Checking the data type and validating it for subfilter 1 ------------------------------------
        self.value_1 = self.entry_1.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_1 != "":
            if self.var_1_cond.get() != "":
                if self.lbl_1.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 1.")
                    return                
                elif self.lbl_1.cget('text') == "Integer":
                    if self.value_1.isdigit():
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_4.append(self.var_1.get())
                            self.data_4.append(self.lbl_1.cget('text'))
                            self.data_4.append(self.var_1_cond.get())
                            self.data_4.append(self.value_1)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_4.append(self.var_1.get())
                            self.data_4.append(self.lbl_1.cget('text'))
                            self.data_4.append(self.var_1_cond.get())
                            self.data_4.append(self.value_1)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 1.")
                        return
                elif self.lbl_1.cget('text') == "Decimals":
                    try:                        
                        float(self.value_1)                        
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_4.append(self.var_1.get())
                            self.data_4.append(self.lbl_1.cget('text'))
                            self.data_4.append(self.var_1_cond.get())
                            self.data_4.append(self.value_1)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_4.append(self.var_1.get())
                            self.data_4.append(self.lbl_1.cget('text'))
                            self.data_4.append(self.var_1_cond.get())
                            self.data_4.append(self.value_1)                  
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 1.")
                        return               
                elif self.lbl_1.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_1, "%Y-%m-%d")
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_4.append(self.var_1.get())
                            self.data_4.append(self.lbl_1.cget('text'))
                            self.data_4.append(self.var_1_cond.get())
                            self.data_4.append(self.value_1)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_4.append(self.var_1.get())
                            self.data_4.append(self.lbl_1.cget('text'))
                            self.data_4.append(self.var_1_cond.get())
                            self.data_4.append(self.value_1)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 1.")
                        return
                elif self.lbl_1.cget('text') == "True/False":
                    if self.value_1 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_4.append(self.var_1.get())
                            self.data_4.append(self.lbl_1.cget('text'))
                            self.data_4.append(self.var_1_cond.get())
                            self.data_4.append(self.value_1)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_4.append(self.var_1.get())
                            self.data_4.append(self.lbl_1.cget('text'))
                            self.data_4.append(self.var_1_cond.get())
                            self.data_4.append(self.value_1)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 1.")
                        return
                elif self.lbl_1.cget('text') == "Text":
                    if self.filter_prompt_4 == "":
                        self.filter_prompt_4 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                        self.data_4.append(self.var_1.get())
                        self.data_4.append(self.lbl_1.cget('text'))
                        self.data_4.append(self.var_1_cond.get())
                        self.data_4.append(self.value_1)
                    else:
                        self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                        self.data_4.append(self.var_1.get())
                        self.data_4.append(self.lbl_1.cget('text'))
                        self.data_4.append(self.var_1_cond.get())
                        self.data_4.append(self.value_1)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 1.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_1 == "" and self.lbl_1.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 1.")
            return

        # Checking the data type and validating it for subfilter 2 ------------------------------------
        self.value_2 = self.entry_2.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_2 != "":
            if self.var_2_cond.get() != "":
                if self.lbl_2.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 2.")
                    return                
                elif self.lbl_2.cget('text') == "Integer":
                    if self.value_2.isdigit():
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_4.append(self.var_2.get())
                            self.data_4.append(self.lbl_2.cget('text'))
                            self.data_4.append(self.var_2_cond.get())
                            self.data_4.append(self.value_2)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_4.append(self.var_2.get())
                            self.data_4.append(self.lbl_2.cget('text'))
                            self.data_4.append(self.var_2_cond.get())
                            self.data_4.append(self.value_2)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 2.")
                        return
                elif self.lbl_2.cget('text') == "Decimals":
                    try:                        
                        float(self.value_2)                        
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_4.append(self.var_2.get())
                            self.data_4.append(self.lbl_2.cget('text'))
                            self.data_4.append(self.var_2_cond.get())
                            self.data_4.append(self.value_2)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_4.append(self.var_2.get())
                            self.data_4.append(self.lbl_2.cget('text'))
                            self.data_4.append(self.var_2_cond.get())
                            self.data_4.append(self.value_2)                 
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 2.")
                        return               
                elif self.lbl_2.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_2, "%Y-%m-%d")
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_4.append(self.var_2.get())
                            self.data_4.append(self.lbl_2.cget('text'))
                            self.data_4.append(self.var_2_cond.get())
                            self.data_4.append(self.value_2)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_4.append(self.var_2.get())
                            self.data_4.append(self.lbl_2.cget('text'))
                            self.data_4.append(self.var_2_cond.get())
                            self.data_4.append(self.value_2)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 2.")
                        return
                elif self.lbl_2.cget('text') == "True/False":
                    if self.value_2 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_4.append(self.var_2.get())
                            self.data_4.append(self.lbl_2.cget('text'))
                            self.data_4.append(self.var_2_cond.get())
                            self.data_4.append(self.value_2)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_4.append(self.var_2.get())
                            self.data_4.append(self.lbl_2.cget('text'))
                            self.data_4.append(self.var_2_cond.get())
                            self.data_4.append(self.value_2)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 2.")
                        return
                elif self.lbl_2.cget('text') == "Text":
                    if self.filter_prompt_4 == "":
                        self.filter_prompt_4 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                        self.data_4.append(self.var_2.get())
                        self.data_4.append(self.lbl_2.cget('text'))
                        self.data_4.append(self.var_2_cond.get())
                        self.data_4.append(self.value_2)
                    else:
                        self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                        self.data_4.append(self.var_2.get())
                        self.data_4.append(self.lbl_2.cget('text'))
                        self.data_4.append(self.var_2_cond.get())
                        self.data_4.append(self.value_2)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 2.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_2 == "" and self.lbl_2.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 2.")
            return
        
        # Checking the data type and validating it for subfilter 3 ------------------------------------
        self.value_3 = self.entry_3.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_3 != "":
            if self.var_3_cond.get() != "":
                if self.lbl_3.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 3.")
                    return                
                elif self.lbl_3.cget('text') == "Integer":
                    if self.value_3.isdigit():
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_4.append(self.var_3.get())
                            self.data_4.append(self.lbl_3.cget('text'))
                            self.data_4.append(self.var_3_cond.get())
                            self.data_4.append(self.value_3)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_4.append(self.var_3.get())
                            self.data_4.append(self.lbl_3.cget('text'))
                            self.data_4.append(self.var_3_cond.get())
                            self.data_4.append(self.value_3)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 3.")
                        return
                elif self.lbl_3.cget('text') == "Decimals":
                    try:                        
                        float(self.value_3)                        
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_4.append(self.var_3.get())
                            self.data_4.append(self.lbl_3.cget('text'))
                            self.data_4.append(self.var_3_cond.get())
                            self.data_4.append(self.value_3)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_4.append(self.var_3.get())
                            self.data_4.append(self.lbl_3.cget('text'))
                            self.data_4.append(self.var_3_cond.get())
                            self.data_4.append(self.value_3)                   
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 3.")
                        return               
                elif self.lbl_3.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_3, "%Y-%m-%d")
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                            self.data_4.append(self.var_3.get())
                            self.data_4.append(self.lbl_3.cget('text'))
                            self.data_4.append(self.var_3_cond.get())
                            self.data_4.append(self.value_3)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''                  
                            self.data_4.append(self.var_3.get())
                            self.data_4.append(self.lbl_3.cget('text'))
                            self.data_4.append(self.var_3_cond.get())
                            self.data_4.append(self.value_3)
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 3.")
                        return
                elif self.lbl_3.cget('text') == "True/False":
                    if self.value_3 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                            self.data_4.append(self.var_3.get())
                            self.data_4.append(self.lbl_3.cget('text'))
                            self.data_4.append(self.var_3_cond.get())
                            self.data_4.append(self.value_3)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                            self.data_4.append(self.var_3.get())
                            self.data_4.append(self.lbl_3.cget('text'))
                            self.data_4.append(self.var_3_cond.get())
                            self.data_4.append(self.value_3)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 3.")
                        return
                elif self.lbl_3.cget('text') == "Text":
                    if self.filter_prompt_4 == "":
                        self.filter_prompt_4 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                        self.data_4.append(self.var_3.get())
                        self.data_4.append(self.lbl_3.cget('text'))
                        self.data_4.append(self.var_3_cond.get())
                        self.data_4.append(self.value_3)
                    else:
                        self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                        self.data_4.append(self.var_3.get())
                        self.data_4.append(self.lbl_3.cget('text'))
                        self.data_4.append(self.var_3_cond.get())
                        self.data_4.append(self.value_3)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 3.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_3 == "" and self.lbl_3.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 3.")
            return

        # Checking the data type and validating it for subfilter 4 ------------------------------------
        self.value_4 = self.entry_4.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_4 != "":
            if self.var_4_cond.get() != "":
                if self.lbl_4.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 4.")
                    return                
                elif self.lbl_4.cget('text') == "Integer":
                    if self.value_4.isdigit():
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_4.append(self.var_4.get())
                            self.data_4.append(self.lbl_4.cget('text'))
                            self.data_4.append(self.var_4_cond.get())
                            self.data_4.append(self.value_4)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_4.append(self.var_4.get())
                            self.data_4.append(self.lbl_4.cget('text'))
                            self.data_4.append(self.var_4_cond.get())
                            self.data_4.append(self.value_4)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 4.")
                        return
                elif self.lbl_4.cget('text') == "Decimals":
                    try:                        
                        float(self.value_4)                        
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_4.append(self.var_4.get())
                            self.data_4.append(self.lbl_4.cget('text'))
                            self.data_4.append(self.var_4_cond.get())
                            self.data_4.append(self.value_4)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_4.append(self.var_4.get())
                            self.data_4.append(self.lbl_4.cget('text'))
                            self.data_4.append(self.var_4_cond.get())
                            self.data_4.append(self.value_4)                  
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 4.")
                        return               
                elif self.lbl_4.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_4, "%Y-%m-%d")
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_4.append(self.var_4.get())
                            self.data_4.append(self.lbl_4.cget('text'))
                            self.data_4.append(self.var_4_cond.get())
                            self.data_4.append(self.value_4)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_4.append(self.var_4.get())
                            self.data_4.append(self.lbl_4.cget('text'))
                            self.data_4.append(self.var_4_cond.get())
                            self.data_4.append(self.value_4)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 4.")
                        return
                elif self.lbl_4.cget('text') == "True/False":
                    if self.value_4 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_4.append(self.var_4.get())
                            self.data_4.append(self.lbl_4.cget('text'))
                            self.data_4.append(self.var_4_cond.get())
                            self.data_4.append(self.value_4)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_4.append(self.var_4.get())
                            self.data_4.append(self.lbl_4.cget('text'))
                            self.data_4.append(self.var_4_cond.get())
                            self.data_4.append(self.value_4)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 4.")
                        return
                elif self.lbl_4.cget('text') == "Text":
                    if self.filter_prompt_4 == "":
                        self.filter_prompt_4 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                        self.data_4.append(self.var_4.get())
                        self.data_4.append(self.lbl_4.cget('text'))
                        self.data_4.append(self.var_4_cond.get())
                        self.data_4.append(self.value_4)
                    else:
                        self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                        self.data_4.append(self.var_4.get())
                        self.data_4.append(self.lbl_4.cget('text'))
                        self.data_4.append(self.var_4_cond.get())
                        self.data_4.append(self.value_4)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 4.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_4 == "" and self.lbl_4.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 4.")
            return
        
        # Checking the data type and validating it for subfilter 5 ------------------------------------
        self.value_5 = self.entry_5.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_5 != "":
            if self.var_5_cond.get() != "":
                if self.lbl_5.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 5.")
                    return                
                elif self.lbl_5.cget('text') == "Integer":
                    if self.value_5.isdigit():
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_4.append(self.var_5.get())
                            self.data_4.append(self.lbl_5.cget('text'))
                            self.data_4.append(self.var_5_cond.get())
                            self.data_4.append(self.value_5)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_4.append(self.var_5.get())
                            self.data_4.append(self.lbl_5.cget('text'))
                            self.data_4.append(self.var_5_cond.get())
                            self.data_4.append(self.value_5)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 5.")
                        return
                elif self.lbl_5.cget('text') == "Decimals":
                    try:                        
                        float(self.value_5)                        
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_4.append(self.var_5.get())
                            self.data_4.append(self.lbl_5.cget('text'))
                            self.data_4.append(self.var_5_cond.get())
                            self.data_4.append(self.value_5)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_4.append(self.var_5.get())
                            self.data_4.append(self.lbl_5.cget('text'))
                            self.data_4.append(self.var_5_cond.get())
                            self.data_4.append(self.value_5)                   
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 5.")
                        return               
                elif self.lbl_5.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_5, "%Y-%m-%d")
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_4.append(self.var_5.get())
                            self.data_4.append(self.lbl_5.cget('text'))
                            self.data_4.append(self.var_5_cond.get())
                            self.data_4.append(self.value_5)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_4.append(self.var_5.get())
                            self.data_4.append(self.lbl_5.cget('text'))
                            self.data_4.append(self.var_5_cond.get())
                            self.data_4.append(self.value_5)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 5.")
                        return
                elif self.lbl_5.cget('text') == "True/False":
                    if self.value_5 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_4 == "":
                            self.filter_prompt_4 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_4.append(self.var_5.get())
                            self.data_4.append(self.lbl_5.cget('text'))
                            self.data_4.append(self.var_5_cond.get())
                            self.data_4.append(self.value_5)
                        else:
                            self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_4.append(self.var_5.get())
                            self.data_4.append(self.lbl_5.cget('text'))
                            self.data_4.append(self.var_5_cond.get())
                            self.data_4.append(self.value_5)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 5.")
                        return
                elif self.lbl_5.cget('text') == "Text":
                    if self.filter_prompt_4 == "":
                        self.filter_prompt_4 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                        self.data_4.append(self.var_5.get())
                        self.data_4.append(self.lbl_5.cget('text'))
                        self.data_4.append(self.var_5_cond.get())
                        self.data_4.append(self.value_5)
                    else:
                        self.filter_prompt_4 = self.filter_prompt_4 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                        self.data_4.append(self.var_5.get())
                        self.data_4.append(self.lbl_5.cget('text'))
                        self.data_4.append(self.var_5_cond.get())
                        self.data_4.append(self.value_5)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 5.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_5 == "" and self.lbl_5.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 5.")
            return

        # If the user is saving something empty, the app will notify
        if not self.data_4:
            self.answer1 = messagebox.askyesno(title="Nothing to save",parent=self.window, message="You are not saving any filter, would you like to close the window?")
            if self.answer1:
                self.window.destroy()
                return
            else:
                return

        # Saving the information and closing the window
        self.answer = messagebox.askyesno(title="Saving this filter",parent=self.window, message="Are you sure you want to save this filter?\n" + self.filter_prompt_4)
        if self.answer:
            self.parent.filter_prompt_4 = self.filter_prompt_4  # Saving the prompt into the Main Window Class
            self.parent.data_4 = self.data_4                    # Saving the Data into a list in the Main Window Class
            self.parent.write_filter_4()
            self.window.destroy()
            return
        else:
            return

    # If there was data sent from Main Class (Edit the filter), then the data is loaded:
    def check_data(self):
        if not self.data_4:
            return
        else:
            if len(self.data_4) == 4:
                self.drdw_1.set(self.data_4[0])
                self.lbl_1.config(text=self.data_4[1])
                self.drdw_1_cond.set(self.data_4[2])
                self.entry_1_value.set(self.data_4[3])
            elif len(self.data_4) == 8:
                self.drdw_1.set(self.data_4[0])
                self.lbl_1.config(text=self.data_4[1])
                self.drdw_1_cond.set(self.data_4[2])
                self.entry_1_value.set(self.data_4[3])
                self.drdw_2.set(self.data_4[4])
                self.lbl_2.config(text=self.data_4[5])
                self.drdw_2_cond.set(self.data_4[6])
                self.entry_2_value.set(self.data_4[7])
            elif len(self.data_4) == 12:
                self.drdw_1.set(self.data_4[0])
                self.lbl_1.config(text=self.data_4[1])
                self.drdw_1_cond.set(self.data_4[2])
                self.entry_1_value.set(self.data_4[3])
                self.drdw_2.set(self.data_4[4])
                self.lbl_2.config(text=self.data_4[5])
                self.drdw_2_cond.set(self.data_4[6])
                self.entry_2_value.set(self.data_4[7])
                self.drdw_3.set(self.data_4[8])
                self.lbl_3.config(text=self.data_4[9])
                self.drdw_3_cond.set(self.data_4[10])
                self.entry_3_value.set(self.data_4[11])
            elif len(self.data_4) == 16:
                self.drdw_1.set(self.data_4[0])
                self.lbl_1.config(text=self.data_4[1])
                self.drdw_1_cond.set(self.data_4[2])
                self.entry_1_value.set(self.data_4[3])
                self.drdw_2.set(self.data_4[4])
                self.lbl_2.config(text=self.data_4[5])
                self.drdw_2_cond.set(self.data_4[6])
                self.entry_2_value.set(self.data_4[7])
                self.drdw_3.set(self.data_4[8])
                self.lbl_3.config(text=self.data_4[9])
                self.drdw_3_cond.set(self.data_4[10])
                self.entry_3_value.set(self.data_4[11])
                self.drdw_4.set(self.data_4[12])
                self.lbl_4.config(text=self.data_4[13])
                self.drdw_4_cond.set(self.data_4[14])
                self.entry_4_value.set(self.data_4[15])
            elif len(self.data_4) == 20:
                self.drdw_1.set(self.data_4[0])
                self.lbl_1.config(text=self.data_4[1])
                self.drdw_1_cond.set(self.data_4[2])
                self.entry_1_value.set(self.data_4[3])
                self.drdw_2.set(self.data_4[4])
                self.lbl_2.config(text=self.data_4[5])
                self.drdw_2_cond.set(self.data_4[6])
                self.entry_2_value.set(self.data_4[7])
                self.drdw_3.set(self.data_4[8])
                self.lbl_3.config(text=self.data_4[9])
                self.drdw_3_cond.set(self.data_4[10])
                self.entry_3_value.set(self.data_4[11])
                self.drdw_4.set(self.data_4[12])
                self.lbl_4.config(text=self.data_4[13])
                self.drdw_4_cond.set(self.data_4[14])
                self.entry_4_value.set(self.data_4[15])
                self.drdw_5.set(self.data_4[16])
                self.lbl_5.config(text=self.data_4[17])
                self.drdw_5_cond.set(self.data_4[18])
                self.entry_5_value.set(self.data_4[19])

# Class to the CSV filter for BAR 5 window
class Filter5:
    
    # Initialization Function
    def __init__(self, parent, df, data_5, title="Filter Configuration for Bar # 5"):
        
        self.parent = parent

        # Window Characteristics
        self.window = tk.Toplevel(parent.root)
        self.window.title(title)
        self.w_win = 700
        self.h_win = 310
        self.wtotal = root.winfo_screenwidth()
        self.htotal = root.winfo_screenheight()
        self.pwidth = round(self.wtotal/2-self.w_win/2)
        self.pheight = round(self.htotal/2-self.h_win/2)
        self.window.geometry(str(self.w_win)+"x"+str(self.h_win)+"+"+str(self.pwidth)+"+"+str(self.pheight))

        # Creating the DataFrame (this came from the Main class)
        self.df = df

        #Creating the data
        self.data_5 = data_5

        # Launching the UI
        self.setup_ui()
        self.check_data()
    
        
    # User Interface Function
    def setup_ui(self):

        # Points of reference
        self.x = 40
        self.y = 80

        # Top Labels
        tk.Label(self.window, text="You can create up to 5 filters for each bar.").place(x=self.x-6, y = self.y - 60)
        tk.Label(self.window, text="Item").place(x=self.x-6, y = self.y - 30)
        tk.Label(self.window, text="Column").place(x=self.x+85, y = self.y - 30)
        tk.Label(self.window, text="Status").place(x=self.x+205, y = self.y - 30)
        tk.Label(self.window, text="Condition").place(x=self.x+330     , y = self.y - 30)
        tk.Label(self.window, text="Value").place(x=self.x+490, y = self.y - 30)
        tk.Label(self.window, text="Reset").place(x=self.x+590, y = self.y - 30)

        # Buttons
        tk.Button(self.window, text="Save Filter", command=self.save_filter).place(x=self.x+555,y=self.y+180)

        # Extracting the columns from the original dataframe into a list
        cols = list(self.df.columns)

        # 5 dropdowns are created and filled with the CSV's columns + labels with data types. Order: Subfilter Name, Column, Status, Condition, Value
        self.space = 35
            #1
        self.lbl_1_name = tk.Label(self.window, text="1.")
        self.lbl_1_name.place(x=self.x, y=self.y)
        self.var_1 = tk.StringVar()
        self.drdw_1 = ttk.Combobox(self.window, textvariable=self.var_1)
        self.drdw_1.place(x=self.x+35, y=self.y)
        self.drdw_1["values"] = cols
        self.var_1_cond = tk.StringVar()
        self.drdw_1_cond = ttk.Combobox(self.window, textvariable=self.var_1_cond)
        self.drdw_1_cond.place(x=self.x+285, y=self.y)
        self.lbl_1 = tk.Label(self.window, text="Select column.")
        self.lbl_1.place(x=self.x+185, y=self.y)
        self.entry_1_value = tk.StringVar()
        self.entry_1 = ttk.Entry(self.window, textvariable=self.entry_1_value)
        self.entry_1.place(x=self.x+445, y=self.y)
        self.btn_reset_1 = tk.Button(self.window, text="!", command=self.reset_filter1, bg='red', fg='white')
        self.btn_reset_1.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #2
        self.lbl_2_name = tk.Label(self.window, text="2.")
        self.lbl_2_name.place(x=self.x, y=self.y)
        self.var_2 = tk.StringVar()
        self.drdw_2 = ttk.Combobox(self.window, textvariable=self.var_2)
        self.drdw_2.place(x=self.x+35, y=self.y)
        self.drdw_2["values"] = cols
        self.var_2_cond = tk.StringVar()
        self.drdw_2_cond = ttk.Combobox(self.window, textvariable=self.var_2_cond)
        self.drdw_2_cond.place(x=self.x+285, y=self.y)
        self.lbl_2 = tk.Label(self.window, text="Select column.")
        self.lbl_2.place(x=self.x+185, y=self.y)
        self.entry_2_value = tk.StringVar()
        self.entry_2 = ttk.Entry(self.window, textvariable=self.entry_2_value)
        self.entry_2.place(x=self.x+445, y=self.y)
        self.btn_reset_2 = tk.Button(self.window, text="!", command=self.reset_filter2, bg='red', fg='white')
        self.btn_reset_2.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #3
        self.lbl_3_name = tk.Label(self.window, text="3.")
        self.lbl_3_name.place(x=self.x, y=self.y)
        self.var_3 = tk.StringVar()
        self.drdw_3 = ttk.Combobox(self.window, textvariable=self.var_3)
        self.drdw_3.place(x=self.x+35, y=self.y)
        self.drdw_3["values"] = cols
        self.var_3_cond = tk.StringVar()
        self.drdw_3_cond = ttk.Combobox(self.window, textvariable=self.var_3_cond)
        self.drdw_3_cond.place(x=self.x+285, y=self.y)
        self.lbl_3 = tk.Label(self.window, text="Select column.")
        self.lbl_3.place(x=self.x+185, y=self.y)
        self.entry_3_value = tk.StringVar()
        self.entry_3 = ttk.Entry(self.window, textvariable=self.entry_3_value)
        self.entry_3.place(x=self.x+445, y=self.y)
        self.btn_reset_3 = tk.Button(self.window, text="!", command=self.reset_filter3, bg='red', fg='white')
        self.btn_reset_3.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #4
        self.lbl_4_name = tk.Label(self.window, text="4.")
        self.lbl_4_name.place(x=self.x, y=self.y)
        self.var_4 = tk.StringVar()
        self.drdw_4 = ttk.Combobox(self.window, textvariable=self.var_4)
        self.drdw_4.place(x=self.x+35, y=self.y)
        self.drdw_4["values"] = cols
        self.var_4_cond = tk.StringVar()
        self.drdw_4_cond = ttk.Combobox(self.window, textvariable=self.var_4_cond)
        self.drdw_4_cond.place(x=self.x+285, y=self.y)
        self.lbl_4 = tk.Label(self.window, text="Select column.")
        self.lbl_4.place(x=self.x+185, y=self.y)
        self.entry_4_value = tk.StringVar()
        self.entry_4 = ttk.Entry(self.window, textvariable=self.entry_4_value)
        self.entry_4.place(x=self.x+445, y=self.y)
        self.btn_reset_4 = tk.Button(self.window, text="!", command=self.reset_filter4, bg='red', fg='white')
        self.btn_reset_4.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space
            #5
        self.lbl_5_name = tk.Label(self.window, text="5.")
        self.lbl_5_name.place(x=self.x, y=self.y)
        self.var_5 = tk.StringVar()
        self.drdw_5 = ttk.Combobox(self.window, textvariable=self.var_5)
        self.drdw_5.place(x=self.x+35, y=self.y)
        self.drdw_5["values"] = cols
        self.var_5_cond = tk.StringVar()
        self.drdw_5_cond = ttk.Combobox(self.window, textvariable=self.var_5_cond)
        self.drdw_5_cond.place(x=self.x+285, y=self.y)
        self.lbl_5 = tk.Label(self.window, text="Select column.")
        self.lbl_5.place(x=self.x+185, y=self.y)
        self.entry_5_value = tk.StringVar()
        self.entry_5 = ttk.Entry(self.window, textvariable=self.entry_5_value)
        self.entry_5.place(x=self.x+445, y=self.y)
        self.btn_reset_5 = tk.Button(self.window, text="!", command=self.reset_filter5, bg='red', fg='white')
        self.btn_reset_5.place(x=self.x+600, y=self.y, width=15, height=15)
        self.y += self.space

        # Action when value of dropdown changes
        self.drdw_1.bind("<<ComboboxSelected>>", self.drdw_1_change)
        self.drdw_2.bind("<<ComboboxSelected>>", self.drdw_2_change)
        self.drdw_3.bind("<<ComboboxSelected>>", self.drdw_3_change)
        self.drdw_4.bind("<<ComboboxSelected>>", self.drdw_4_change)
        self.drdw_5.bind("<<ComboboxSelected>>", self.drdw_5_change)

    # Function to identify the data type for subfilter 1 and displaying filtering options
    def drdw_1_change(self, event):
        current_value = self.var_1.get()
        current_type = self.df[current_value].dtype
        self.drdw_1_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_1_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_1_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_1_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_1_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_1_cond["values"] = ["=="]
        
        self.lbl_1.config(text=current_type)
    
    # Function to identify the data type for subfilter 2 and displaying filtering options
    def drdw_2_change(self, event):
        current_value = self.var_2.get()
        current_type = self.df[current_value].dtype
        self.drdw_2_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_2_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_2_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_2_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_2_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_2_cond["values"] = ["=="]

        self.lbl_2.config(text=current_type)
    
    # Function to identify the data type for subfilter 3 and displaying filtering options
    def drdw_3_change(self, event):
        current_value = self.var_3.get()
        current_type = self.df[current_value].dtype
        self.drdw_3_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_3_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_3_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_3_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_3_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_3_cond["values"] = ["=="]

        self.lbl_3.config(text=current_type)

    # Function to identify the data type for subfilter 4 and displaying filtering options
    def drdw_4_change(self, event):
        current_value = self.var_4.get()
        current_type = self.df[current_value].dtype
        self.drdw_4_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_4_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_4_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_4_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_4_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_4_cond["values"] = ["=="]

        self.lbl_4.config(text=current_type)
    
    # Function to identify the data type for subfilter 5 and displaying filtering options
    def drdw_5_change(self, event):
        current_value = self.var_5.get()
        current_type = self.df[current_value].dtype
        self.drdw_5_cond.set("")

        if current_type=="int64":
            current_type="Integer"
            self.drdw_5_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="object":
            current_type="Text"
            self.drdw_5_cond["values"] = ["=="]
        elif current_type=="float64":
            current_type="Decimals"
            self.drdw_5_cond["values"] = [">", "<", ">=", "<=", "==", "!="]
        elif current_type=="bool":
            current_type="True/False"
            self.drdw_5_cond["values"] = [True, False]
        elif current_type=="datetime64[ns]":
            current_type="Dates/Times"
            self.drdw_5_cond["values"] = ["=="]

        self.lbl_5.config(text=current_type)

    # Reset Subfilter 1 values
    def reset_filter1(self):
        self.drdw_1.set("")
        self.drdw_1_cond.set("")
        self.entry_1_value.set("")
        self.lbl_1.config(text="Select column.")
    
    # Reset Subfilter 2 values
    def reset_filter2(self):
        self.drdw_2.set("")
        self.drdw_2_cond.set("")
        self.entry_2_value.set("")
        self.lbl_2.config(text="Select column.")
    
    # Reset Subfilter 3 values
    def reset_filter3(self):
        self.drdw_3.set("")
        self.drdw_3_cond.set("")
        self.entry_3_value.set("")
        self.lbl_3.config(text="Select column.")

    # Reset Subfilter 4 values
    def reset_filter4(self):
        self.drdw_4.set("")
        self.drdw_4_cond.set("")
        self.entry_4_value.set("")
        self.lbl_4.config(text="Select column.")
    
    # Reset Subfilter 5 values
    def reset_filter5(self):
        self.drdw_5.set("")
        self.drdw_5_cond.set("")
        self.entry_5_value.set("")
        self.lbl_5.config(text="Select column.")

    # Saving the filter configuration    
    def save_filter(self):

        self.num_filters = 0
        self.filter_prompt_5 = ""
        self.data_5 = []

        # Checking the data type and validating it for subfilter 1 ------------------------------------
        self.value_1 = self.entry_1.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_1 != "":
            if self.var_1_cond.get() != "":
                if self.lbl_1.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 1.")
                    return                
                elif self.lbl_1.cget('text') == "Integer":
                    if self.value_1.isdigit():
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_5.append(self.var_1.get())
                            self.data_5.append(self.lbl_1.cget('text'))
                            self.data_5.append(self.var_1_cond.get())
                            self.data_5.append(self.value_1)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_5.append(self.var_1.get())
                            self.data_5.append(self.lbl_1.cget('text'))
                            self.data_5.append(self.var_1_cond.get())
                            self.data_5.append(self.value_1)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 1.")
                        return
                elif self.lbl_1.cget('text') == "Decimals":
                    try:                        
                        float(self.value_1)                        
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_5.append(self.var_1.get())
                            self.data_5.append(self.lbl_1.cget('text'))
                            self.data_5.append(self.var_1_cond.get())
                            self.data_5.append(self.value_1)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + " " + self.value_1 + ")"
                            self.data_5.append(self.var_1.get())
                            self.data_5.append(self.lbl_1.cget('text'))
                            self.data_5.append(self.var_1_cond.get())
                            self.data_5.append(self.value_1)                  
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 1.")
                        return               
                elif self.lbl_1.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_1, "%Y-%m-%d")
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_5.append(self.var_1.get())
                            self.data_5.append(self.lbl_1.cget('text'))
                            self.data_5.append(self.var_1_cond.get())
                            self.data_5.append(self.value_1)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_5.append(self.var_1.get())
                            self.data_5.append(self.lbl_1.cget('text'))
                            self.data_5.append(self.var_1_cond.get())
                            self.data_5.append(self.value_1)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 1.")
                        return
                elif self.lbl_1.cget('text') == "True/False":
                    if self.value_1 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_5.append(self.var_1.get())
                            self.data_5.append(self.lbl_1.cget('text'))
                            self.data_5.append(self.var_1_cond.get())
                            self.data_5.append(self.value_1)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                            self.data_5.append(self.var_1.get())
                            self.data_5.append(self.lbl_1.cget('text'))
                            self.data_5.append(self.var_1_cond.get())
                            self.data_5.append(self.value_1)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 1.")
                        return
                elif self.lbl_1.cget('text') == "Text":
                    if self.filter_prompt_5 == "":
                        self.filter_prompt_5 = '''(self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                        self.data_5.append(self.var_1.get())
                        self.data_5.append(self.lbl_1.cget('text'))
                        self.data_5.append(self.var_1_cond.get())
                        self.data_5.append(self.value_1)
                    else:
                        self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_1.get() + '''"] ''' + self.var_1_cond.get() + ''' "''' + self.value_1 + '''")'''
                        self.data_5.append(self.var_1.get())
                        self.data_5.append(self.lbl_1.cget('text'))
                        self.data_5.append(self.var_1_cond.get())
                        self.data_5.append(self.value_1)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 1.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_1 == "" and self.lbl_1.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 1.")
            return

        # Checking the data type and validating it for subfilter 2 ------------------------------------
        self.value_2 = self.entry_2.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_2 != "":
            if self.var_2_cond.get() != "":
                if self.lbl_2.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 2.")
                    return                
                elif self.lbl_2.cget('text') == "Integer":
                    if self.value_2.isdigit():
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_5.append(self.var_2.get())
                            self.data_5.append(self.lbl_2.cget('text'))
                            self.data_5.append(self.var_2_cond.get())
                            self.data_5.append(self.value_2)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_5.append(self.var_2.get())
                            self.data_5.append(self.lbl_2.cget('text'))
                            self.data_5.append(self.var_2_cond.get())
                            self.data_5.append(self.value_2)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 2.")
                        return
                elif self.lbl_2.cget('text') == "Decimals":
                    try:                        
                        float(self.value_2)                        
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_5.append(self.var_2.get())
                            self.data_5.append(self.lbl_2.cget('text'))
                            self.data_5.append(self.var_2_cond.get())
                            self.data_5.append(self.value_2)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + " " + self.value_2 + ")"
                            self.data_5.append(self.var_2.get())
                            self.data_5.append(self.lbl_2.cget('text'))
                            self.data_5.append(self.var_2_cond.get())
                            self.data_5.append(self.value_2)                 
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 2.")
                        return               
                elif self.lbl_2.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_2, "%Y-%m-%d")
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_5.append(self.var_2.get())
                            self.data_5.append(self.lbl_2.cget('text'))
                            self.data_5.append(self.var_2_cond.get())
                            self.data_5.append(self.value_2)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_5.append(self.var_2.get())
                            self.data_5.append(self.lbl_2.cget('text'))
                            self.data_5.append(self.var_2_cond.get())
                            self.data_5.append(self.value_2)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 2.")
                        return
                elif self.lbl_2.cget('text') == "True/False":
                    if self.value_2 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_5.append(self.var_2.get())
                            self.data_5.append(self.lbl_2.cget('text'))
                            self.data_5.append(self.var_2_cond.get())
                            self.data_5.append(self.value_2)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                            self.data_5.append(self.var_2.get())
                            self.data_5.append(self.lbl_2.cget('text'))
                            self.data_5.append(self.var_2_cond.get())
                            self.data_5.append(self.value_2)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 2.")
                        return
                elif self.lbl_2.cget('text') == "Text":
                    if self.filter_prompt_5 == "":
                        self.filter_prompt_5 = '''(self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                        self.data_5.append(self.var_2.get())
                        self.data_5.append(self.lbl_2.cget('text'))
                        self.data_5.append(self.var_2_cond.get())
                        self.data_5.append(self.value_2)
                    else:
                        self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_2.get() + '''"] ''' + self.var_2_cond.get() + ''' "''' + self.value_2 + '''")'''
                        self.data_5.append(self.var_2.get())
                        self.data_5.append(self.lbl_2.cget('text'))
                        self.data_5.append(self.var_2_cond.get())
                        self.data_5.append(self.value_2)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 2.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_2 == "" and self.lbl_2.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 2.")
            return
        
        # Checking the data type and validating it for subfilter 3 ------------------------------------
        self.value_3 = self.entry_3.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_3 != "":
            if self.var_3_cond.get() != "":
                if self.lbl_3.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 3.")
                    return                
                elif self.lbl_3.cget('text') == "Integer":
                    if self.value_3.isdigit():
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_5.append(self.var_3.get())
                            self.data_5.append(self.lbl_3.cget('text'))
                            self.data_5.append(self.var_3_cond.get())
                            self.data_5.append(self.value_3)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_5.append(self.var_3.get())
                            self.data_5.append(self.lbl_3.cget('text'))
                            self.data_5.append(self.var_3_cond.get())
                            self.data_5.append(self.value_3)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 3.")
                        return
                elif self.lbl_3.cget('text') == "Decimals":
                    try:                        
                        float(self.value_3)                        
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_5.append(self.var_3.get())
                            self.data_5.append(self.lbl_3.cget('text'))
                            self.data_5.append(self.var_3_cond.get())
                            self.data_5.append(self.value_3)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + " " + self.value_3 + ")"
                            self.data_5.append(self.var_3.get())
                            self.data_5.append(self.lbl_3.cget('text'))
                            self.data_5.append(self.var_3_cond.get())
                            self.data_5.append(self.value_3)                   
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 3.")
                        return               
                elif self.lbl_3.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_3, "%Y-%m-%d")
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                            self.data_5.append(self.var_3.get())
                            self.data_5.append(self.lbl_3.cget('text'))
                            self.data_5.append(self.var_3_cond.get())
                            self.data_5.append(self.value_3)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''                  
                            self.data_5.append(self.var_3.get())
                            self.data_5.append(self.lbl_3.cget('text'))
                            self.data_5.append(self.var_3_cond.get())
                            self.data_5.append(self.value_3)
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 3.")
                        return
                elif self.lbl_3.cget('text') == "True/False":
                    if self.value_3 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                            self.data_5.append(self.var_3.get())
                            self.data_5.append(self.lbl_3.cget('text'))
                            self.data_5.append(self.var_3_cond.get())
                            self.data_5.append(self.value_3)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                            self.data_5.append(self.var_3.get())
                            self.data_5.append(self.lbl_3.cget('text'))
                            self.data_5.append(self.var_3_cond.get())
                            self.data_5.append(self.value_3)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 3.")
                        return
                elif self.lbl_3.cget('text') == "Text":
                    if self.filter_prompt_5 == "":
                        self.filter_prompt_5 = '''(self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                        self.data_5.append(self.var_3.get())
                        self.data_5.append(self.lbl_3.cget('text'))
                        self.data_5.append(self.var_3_cond.get())
                        self.data_5.append(self.value_3)
                    else:
                        self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_3.get() + '''"] ''' + self.var_3_cond.get() + ''' "''' + self.value_3 + '''")'''
                        self.data_5.append(self.var_3.get())
                        self.data_5.append(self.lbl_3.cget('text'))
                        self.data_5.append(self.var_3_cond.get())
                        self.data_5.append(self.value_3)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 3.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_3 == "" and self.lbl_3.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 3.")
            return

        # Checking the data type and validating it for subfilter 4 ------------------------------------
        self.value_4 = self.entry_4.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_4 != "":
            if self.var_4_cond.get() != "":
                if self.lbl_4.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 4.")
                    return                
                elif self.lbl_4.cget('text') == "Integer":
                    if self.value_4.isdigit():
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_5.append(self.var_4.get())
                            self.data_5.append(self.lbl_4.cget('text'))
                            self.data_5.append(self.var_4_cond.get())
                            self.data_5.append(self.value_4)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_5.append(self.var_4.get())
                            self.data_5.append(self.lbl_4.cget('text'))
                            self.data_5.append(self.var_4_cond.get())
                            self.data_5.append(self.value_4)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 4.")
                        return
                elif self.lbl_4.cget('text') == "Decimals":
                    try:                        
                        float(self.value_4)                        
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_5.append(self.var_4.get())
                            self.data_5.append(self.lbl_4.cget('text'))
                            self.data_5.append(self.var_4_cond.get())
                            self.data_5.append(self.value_4)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + " " + self.value_4 + ")"
                            self.data_5.append(self.var_4.get())
                            self.data_5.append(self.lbl_4.cget('text'))
                            self.data_5.append(self.var_4_cond.get())
                            self.data_5.append(self.value_4)                  
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 4.")
                        return               
                elif self.lbl_4.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_4, "%Y-%m-%d")
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_5.append(self.var_4.get())
                            self.data_5.append(self.lbl_4.cget('text'))
                            self.data_5.append(self.var_4_cond.get())
                            self.data_5.append(self.value_4)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_5.append(self.var_4.get())
                            self.data_5.append(self.lbl_4.cget('text'))
                            self.data_5.append(self.var_4_cond.get())
                            self.data_5.append(self.value_4)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 4.")
                        return
                elif self.lbl_4.cget('text') == "True/False":
                    if self.value_4 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_5.append(self.var_4.get())
                            self.data_5.append(self.lbl_4.cget('text'))
                            self.data_5.append(self.var_4_cond.get())
                            self.data_5.append(self.value_4)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                            self.data_5.append(self.var_4.get())
                            self.data_5.append(self.lbl_4.cget('text'))
                            self.data_5.append(self.var_4_cond.get())
                            self.data_5.append(self.value_4)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 4.")
                        return
                elif self.lbl_4.cget('text') == "Text":
                    if self.filter_prompt_5 == "":
                        self.filter_prompt_5 = '''(self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                        self.data_5.append(self.var_4.get())
                        self.data_5.append(self.lbl_4.cget('text'))
                        self.data_5.append(self.var_4_cond.get())
                        self.data_5.append(self.value_4)
                    else:
                        self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_4.get() + '''"] ''' + self.var_4_cond.get() + ''' "''' + self.value_4 + '''")'''
                        self.data_5.append(self.var_4.get())
                        self.data_5.append(self.lbl_4.cget('text'))
                        self.data_5.append(self.var_4_cond.get())
                        self.data_5.append(self.value_4)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 4.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_4 == "" and self.lbl_4.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 4.")
            return
        
        # Checking the data type and validating it for subfilter 5 ------------------------------------
        self.value_5 = self.entry_5.get()

        # If there is value on the entry box, then it is evaluated
        if self.value_5 != "":
            if self.var_5_cond.get() != "":
                if self.lbl_5.cget('text')=="Select column.":
                    messagebox.showerror(title="Error", parent=self.window, message="You have not selected a column to filter in subfilter 5.")
                    return                
                elif self.lbl_5.cget('text') == "Integer":
                    if self.value_5.isdigit():
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_5.append(self.var_5.get())
                            self.data_5.append(self.lbl_5.cget('text'))
                            self.data_5.append(self.var_5_cond.get())
                            self.data_5.append(self.value_5)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_5.append(self.var_5.get())
                            self.data_5.append(self.lbl_5.cget('text'))
                            self.data_5.append(self.var_5_cond.get())
                            self.data_5.append(self.value_5)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not an integer in subfilter 5.")
                        return
                elif self.lbl_5.cget('text') == "Decimals":
                    try:                        
                        float(self.value_5)                        
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_5.append(self.var_5.get())
                            self.data_5.append(self.lbl_5.cget('text'))
                            self.data_5.append(self.var_5_cond.get())
                            self.data_5.append(self.value_5)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + " " + self.value_5 + ")"
                            self.data_5.append(self.var_5.get())
                            self.data_5.append(self.lbl_5.cget('text'))
                            self.data_5.append(self.var_5_cond.get())
                            self.data_5.append(self.value_5)                   
                    except ValueError:   
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a decimal in subfilter 5.")
                        return               
                elif self.lbl_5.cget('text') == "Dates/Times":
                    try:
                        datetime.strptime(self.value_5, "%Y-%m-%d")
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_5.append(self.var_5.get())
                            self.data_5.append(self.lbl_5.cget('text'))
                            self.data_5.append(self.var_5_cond.get())
                            self.data_5.append(self.value_5)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_5.append(self.var_5.get())
                            self.data_5.append(self.lbl_5.cget('text'))
                            self.data_5.append(self.var_5_cond.get())
                            self.data_5.append(self.value_5)                  
                    except ValueError:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a date in subfilter 5.")
                        return
                elif self.lbl_5.cget('text') == "True/False":
                    if self.value_5 in ["true", "yes", "1", "false", "no", "0"]:
                        if self.filter_prompt_5 == "":
                            self.filter_prompt_5 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_5.append(self.var_5.get())
                            self.data_5.append(self.lbl_5.cget('text'))
                            self.data_5.append(self.var_5_cond.get())
                            self.data_5.append(self.value_5)
                        else:
                            self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                            self.data_5.append(self.var_5.get())
                            self.data_5.append(self.lbl_5.cget('text'))
                            self.data_5.append(self.var_5_cond.get())
                            self.data_5.append(self.value_5)
                    else:
                        messagebox.showerror(title="Error", parent=self.window, message="The value you entered is not a boolean in subfilter 5.")
                        return
                elif self.lbl_5.cget('text') == "Text":
                    if self.filter_prompt_5 == "":
                        self.filter_prompt_5 = '''(self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                        self.data_5.append(self.var_5.get())
                        self.data_5.append(self.lbl_5.cget('text'))
                        self.data_5.append(self.var_5_cond.get())
                        self.data_5.append(self.value_5)
                    else:
                        self.filter_prompt_5 = self.filter_prompt_5 + ''' & (self.df["''' + self.var_5.get() + '''"] ''' + self.var_5_cond.get() + ''' "''' + self.value_5 + '''")'''
                        self.data_5.append(self.var_5.get())
                        self.data_5.append(self.lbl_5.cget('text'))
                        self.data_5.append(self.var_5_cond.get())
                        self.data_5.append(self.value_5)
            else: 
                messagebox.showerror(title="Error", parent=self.window, message="You have not selected any condition in subfilter 5.")
                return

        # If there is no value entered, but a filter is selected, it will tell user and stop execution
        if self.value_5 == "" and self.lbl_5.cget('text') != "Select column.":
            messagebox.showerror(title="Error", parent=self.window, message="You have not entered any value or condition in subfilter 5.")
            return

        # If the user is saving something empty, the app will notify
        if not self.data_5:
            self.answer1 = messagebox.askyesno(title="Nothing to save",parent=self.window, message="You are not saving any filter, would you like to close the window?")
            if self.answer1:
                self.window.destroy()
                return
            else:
                return

        # Saving the information and closing the window
        self.answer = messagebox.askyesno(title="Saving this filter",parent=self.window, message="Are you sure you want to save this filter?\n" + self.filter_prompt_5)
        if self.answer:
            self.parent.filter_prompt_5 = self.filter_prompt_5  # Saving the prompt into the Main Window Class
            self.parent.data_5 = self.data_5                    # Saving the Data into a list in the Main Window Class
            self.parent.write_filter_5()
            self.window.destroy()
            return
        else:
            return

    # If there was data sent from Main Class (Edit the filter), then the data is loaded:
    def check_data(self):
        if not self.data_5:
            return
        else:
            if len(self.data_5) == 4:
                self.drdw_1.set(self.data_5[0])
                self.lbl_1.config(text=self.data_5[1])
                self.drdw_1_cond.set(self.data_5[2])
                self.entry_1_value.set(self.data_5[3])
            elif len(self.data_5) == 8:
                self.drdw_1.set(self.data_5[0])
                self.lbl_1.config(text=self.data_5[1])
                self.drdw_1_cond.set(self.data_5[2])
                self.entry_1_value.set(self.data_5[3])
                self.drdw_2.set(self.data_5[4])
                self.lbl_2.config(text=self.data_5[5])
                self.drdw_2_cond.set(self.data_5[6])
                self.entry_2_value.set(self.data_5[7])
            elif len(self.data_5) == 12:
                self.drdw_1.set(self.data_5[0])
                self.lbl_1.config(text=self.data_5[1])
                self.drdw_1_cond.set(self.data_5[2])
                self.entry_1_value.set(self.data_5[3])
                self.drdw_2.set(self.data_5[4])
                self.lbl_2.config(text=self.data_5[5])
                self.drdw_2_cond.set(self.data_5[6])
                self.entry_2_value.set(self.data_5[7])
                self.drdw_3.set(self.data_5[8])
                self.lbl_3.config(text=self.data_5[9])
                self.drdw_3_cond.set(self.data_5[10])
                self.entry_3_value.set(self.data_5[11])
            elif len(self.data_5) == 16:
                self.drdw_1.set(self.data_5[0])
                self.lbl_1.config(text=self.data_5[1])
                self.drdw_1_cond.set(self.data_5[2])
                self.entry_1_value.set(self.data_5[3])
                self.drdw_2.set(self.data_5[4])
                self.lbl_2.config(text=self.data_5[5])
                self.drdw_2_cond.set(self.data_5[6])
                self.entry_2_value.set(self.data_5[7])
                self.drdw_3.set(self.data_5[8])
                self.lbl_3.config(text=self.data_5[9])
                self.drdw_3_cond.set(self.data_5[10])
                self.entry_3_value.set(self.data_5[11])
                self.drdw_4.set(self.data_5[12])
                self.lbl_4.config(text=self.data_5[13])
                self.drdw_4_cond.set(self.data_5[14])
                self.entry_4_value.set(self.data_5[15])
            elif len(self.data_5) == 20:
                self.drdw_1.set(self.data_5[0])
                self.lbl_1.config(text=self.data_5[1])
                self.drdw_1_cond.set(self.data_5[2])
                self.entry_1_value.set(self.data_5[3])
                self.drdw_2.set(self.data_5[4])
                self.lbl_2.config(text=self.data_5[5])
                self.drdw_2_cond.set(self.data_5[6])
                self.entry_2_value.set(self.data_5[7])
                self.drdw_3.set(self.data_5[8])
                self.lbl_3.config(text=self.data_5[9])
                self.drdw_3_cond.set(self.data_5[10])
                self.entry_3_value.set(self.data_5[11])
                self.drdw_4.set(self.data_5[12])
                self.lbl_4.config(text=self.data_5[13])
                self.drdw_4_cond.set(self.data_5[14])
                self.entry_4_value.set(self.data_5[15])
                self.drdw_5.set(self.data_5[16])
                self.lbl_5.config(text=self.data_5[17])
                self.drdw_5_cond.set(self.data_5[18])
                self.entry_5_value.set(self.data_5[19])


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVVisualizer(root)
    root.mainloop()
