import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from dbfread import DBF
import pandas as pd

class OptimizedDBFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Wyszukiwarka DBF - Optymalizowana (170k+)")
        self.root.geometry("1200x700")
        
        self.dbf_path = None
        self.df = None
        self.full_index = None
        
        self.page_size = 1000
        self.current_page = 0
        self.total_pages = 0
        self.filtered_df = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Górny panel
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(top_frame, text="Wybierz plik DBF", command=self.open_dbf).pack(side='left')
        
        ttk.Label(top_frame, text="Wyszukaj:").pack(side='left', padx=(20,5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(top_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side='left', padx=(0,5))
        search_entry.bind('<KeyRelease>', self.on_search)
        
        ttk.Button(top_frame, text="Wyczyść wyszukiwanie", command=self.clear_search).pack(side='left')
        
        # Paginacja
        self.page_label = ttk.Label(top_frame, text="Strona 0/0")
        self.page_label.pack(side='right', padx=(10,0))
        
        ttk.Button(top_frame, text="<<", command=self.prev_page, width=3).pack(side='right', padx=(0,5))
        ttk.Button(top_frame, text=">>", command=self.next_page, width=3).pack(side='right')
        
        # Treeview
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(tree_frame, columns=('A', 'B', 'C', 'D', 'E', 'F', 'G'), show='headings')
        self.tree.heading('A', text='Imię')
        self.tree.heading('B', text='Miejscowość')
        self.tree.heading('C', text='Nazwisko')
        self.tree.heading('D', text='PESEL')
        self.tree.heading('E', text='Ulica')
        self.tree.heading('F', text='Nr domu')
        self.tree.heading('G', text='Nr mieszkania')
        
        for col in self.tree['columns']:
            self.tree.column(col, width=140)
        
        v_scroll = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=v_scroll.set, xscroll=h_scroll.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        v_scroll.pack(side='right', fill='y')
        h_scroll.pack(side='bottom', fill='x')
    
    def open_dbf(self):
        self.dbf_path = filedialog.askopenfilename(filetypes=[("DBF files", "*.dbf")])
        if self.dbf_path:
            try:
                print("Ładowanie pliku...")
                table =
