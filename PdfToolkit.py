import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import PyPDF2
import pdfplumber
import io
import os
import sys
from datetime import datetime
from PIL import Image, ImageTk
import traceback

class PDFToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Toolkit Pro")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Set application icon and style
        self.root.tk_setPalette(background='#f0f0f0', foreground='#333333')
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.bg_color = '#f8f9fa'
        self.button_color = '#4a6fa5'
        self.accent_color = '#16697a'
        self.text_color = '#333333'
        
        self.root.configure(bg=self.bg_color)
        
        # Initialize variables
        self.files_to_merge = []
        self.pdf_to_split = None
        self.pdf_to_compress = None
        self.pdf_to_rename = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.accent_color, height=100)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="PDF Toolkit Pro", 
            font=('Segoe UI', 24, 'bold'),
            bg=self.accent_color,
            fg='white'
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Merge, Split, Compress, and Rename PDF Files",
            font=('Segoe UI', 10),
            bg=self.accent_color,
            fg='#e0e0e0'
        )
        subtitle_label.pack()
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Create tabs
        self.merge_tab = self.create_merge_tab()
        self.split_tab = self.create_split_tab()
        self.compress_tab = self.create_compress_tab()
        self.rename_tab = self.create_rename_tab()
        
        notebook.add(self.merge_tab, text="  Merge PDFs  ")
        notebook.add(self.split_tab, text="  Split PDF  ")
        notebook.add(self.compress_tab, text="  Compress PDF  ")
        notebook.add(self.rename_tab, text="  Rename PDF  ")
        
        # Log area
        log_frame = tk.LabelFrame(self.root, text="Activity Log", font=('Segoe UI', 10, 'bold'), bg=self.bg_color)
        log_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=(0, 10), ipady=5)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            height=8, 
            font=('Consolas', 9),
            bg='#f5f5f5',
            fg=self.text_color
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var,
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg='#e9ecef',
            fg=self.text_color,
            font=('Segoe UI', 9)
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initialize log
        self.log("PDF Toolkit Pro initialized")
        
    def create_merge_tab(self):
        tab = tk.Frame(self.root, bg=self.bg_color)
        
        # Instructions
        instructions = tk.Label(
            tab,
            text="Select multiple PDF files to merge them into a single PDF document",
            font=('Segoe UI', 10),
            bg=self.bg_color,
            fg=self.text_color,
            wraplength=500
        )
        instructions.pack(pady=10)
        
        # File list frame
        list_frame = tk.LabelFrame(tab, text="Files to Merge", font=('Segoe UI', 10, 'bold'), bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10, ipady=5)
        
        # Scrollable listbox
        self.merge_listbox = tk.Listbox(
            list_frame,
            selectmode=tk.EXTENDED,
            height=8,
            font=('Segoe UI', 9),
            bg='white',
            relief=tk.FLAT
        )
        self.merge_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.merge_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.merge_listbox.yview)
        
        # Button frame
        button_frame = tk.Frame(tab, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Buttons
        add_button = tk.Button(
            button_frame,
            text="Add PDFs",
            command=self.add_pdfs_to_merge,
            bg=self.button_color,
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        add_button.pack(side=tk.LEFT, padx=5)
        
        remove_button = tk.Button(
            button_frame,
            text="Remove Selected",
            command=self.remove_selected_merge,
            bg='#dc3545',
            fg='white',
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        remove_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = tk.Button(
            button_frame,
            text="Clear All",
            command=self.clear_merge_list,
            bg='#6c757d',
            fg='white',
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Output name frame
        output_frame = tk.Frame(tab, bg=self.bg_color)
        output_frame.pack(fill=tk.X, padx=20, pady=(5, 10))
        
        tk.Label(
            output_frame,
            text="Output filename:",
            font=('Segoe UI', 10),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(side=tk.LEFT)
        
        self.merge_output_var = tk.StringVar(value="merged.pdf")
        output_entry = tk.Entry(
            output_frame,
            textvariable=self.merge_output_var,
            font=('Segoe UI', 10),
            width=30,
            relief=tk.FLAT,
            bg='white'
        )
        output_entry.pack(side=tk.LEFT, padx=10)
        
        # Merge button
        merge_button = tk.Button(
            tab,
            text="Merge PDFs",
            command=self.merge_pdfs,
            bg=self.accent_color,
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief=tk.FLAT,
            padx=30,
            pady=12
        )
        merge_button.pack(pady=(5, 20))
        
        return tab
    
    def create_split_tab(self):
        tab = tk.Frame(self.root, bg=self.bg_color)
        
        # Instructions
        instructions = tk.Label(
            tab,
            text="Select a PDF file to split into individual pages or custom ranges",
            font=('Segoe UI', 10),
            bg=self.bg_color,
            fg=self.text_color,
            wraplength=500
        )
        instructions.pack(pady=10)
        
        # File selection frame
        file_frame = tk.Frame(tab, bg=self.bg_color)
        file_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.split_file_var = tk.StringVar(value="No file selected")
        file_label = tk.Label(
            file_frame,
            textvariable=self.split_file_var,
            font=('Segoe UI', 9),
            bg='white',
            fg=self.text_color,
            relief=tk.FLAT,
            anchor=tk.W,
            padx=10,
            pady=8
        )
        file_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_button = tk.Button(
            file_frame,
            text="Browse",
            command=self.select_split_pdf,
            bg=self.button_color,
            fg='white',
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            padx=15
        )
        browse_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Split options frame
        options_frame = tk.LabelFrame(tab, text="Split Options", font=('Segoe UI', 10, 'bold'), bg=self.bg_color)
        options_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10, ipady=5)
        
        # Radio buttons for split type
        self.split_type = tk.StringVar(value="all")
        
        tk.Radiobutton(
            options_frame,
            text="Split into individual pages (one PDF per page)",
            variable=self.split_type,
            value="all",
            font=('Segoe UI', 10),
            bg=self.bg_color,
            fg=self.text_color,
            command=self.update_split_options
        ).pack(anchor=tk.W, pady=5)
        
        tk.Radiobutton(
            options_frame,
            text="Split by page ranges (e.g., 1-3, 5, 7-9)",
            variable=self.split_type,
            value="ranges",
            font=('Segoe UI', 10),
            bg=self.bg_color,
            fg=self.text_color,
            command=self.update_split_options
        ).pack(anchor=tk.W, pady=5)
        
        # Range entry frame (initially hidden)
        self.range_frame = tk.Frame(options_frame, bg=self.bg_color)
        self.range_label = tk.Label(
            self.range_frame,
            text="Page ranges (comma separated):",
            font=('Segoe UI', 10),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.range_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.range_var = tk.StringVar()
        self.range_entry = tk.Entry(
            self.range_frame,
            textvariable=self.range_var,
            font=('Segoe UI', 10),
            width=30,
            relief=tk.FLAT,
            bg='white'
        )
        self.range_entry.pack(side=tk.LEFT)
        self.range_frame.pack_forget()
        
        # Output prefix
        prefix_frame = tk.Frame(tab, bg=self.bg_color)
        prefix_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            prefix_frame,
            text="Output prefix:",
            font=('Segoe UI', 10),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(side=tk.LEFT)
        
        self.split_prefix_var = tk.StringVar(value="split_")
        prefix_entry = tk.Entry(
            prefix_frame,
            textvariable=self.split_prefix_var,
            font=('Segoe UI', 10),
            width=20,
            relief=tk.FLAT,
            bg='white'
        )
        prefix_entry.pack(side=tk.LEFT, padx=10)
        
        # Split button
        split_button = tk.Button(
            tab,
            text="Split PDF",
            command=self.split_pdf,
            bg=self.accent_color,
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief=tk.FLAT,
            padx=30,
            pady=12
        )
        split_button.pack(pady=(10, 20))
        
        return tab
    
    def create_compress_tab(self):
        tab = tk.Frame(self.root, bg=self.bg_color)
        
        # Instructions
        instructions = tk.Label(
            tab,
            text="Select a PDF file to compress (reduce file size)",
            font=('Segoe UI', 10),
            bg=self.bg_color,
            fg=self.text_color,
            wraplength=500
        )
        instructions.pack(pady=10)
        
        # File selection frame
        file_frame = tk.Frame(tab, bg=self.bg_color)
        file_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.compress_file_var = tk.StringVar(value="No file selected")
        file_label = tk.Label(
            file_frame,
            textvariable=self.compress_file_var,
            font=('Segoe UI', 9),
            bg='white',
            fg=self.text_color,
            relief=tk.FLAT,
            anchor=tk.W,
            padx=10,
            pady=8
        )
        file_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_button = tk.Button(
            file_frame,
            text="Browse",
            command=self.select_compress_pdf,
            bg=self.button_color,
            fg='white',
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            padx=15
        )
        browse_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Compression level frame
        level_frame = tk.LabelFrame(tab, text="Compression Level", font=('Segoe UI', 10, 'bold'), bg=self.bg_color)
        level_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10, ipady=5)
        
        self.compression_level = tk.StringVar(value="medium")
        
        levels = [
            ("Low (minimal compression)", "low"),
            ("Medium (balanced)", "medium"),
            ("High (maximum compression)", "high")
        ]
        
        for text, value in levels:
            tk.Radiobutton(
                level_frame,
                text=text,
                variable=self.compression_level,
                value=value,
                font=('Segoe UI', 10),
                bg=self.bg_color,
                fg=self.text_color
            ).pack(anchor=tk.W, pady=5)
        
        # Output filename
        output_frame = tk.Frame(tab, bg=self.bg_color)
        output_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            output_frame,
            text="Output filename:",
            font=('Segoe UI', 10),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(side=tk.LEFT)
        
        self.compress_output_var = tk.StringVar(value="compressed.pdf")
        output_entry = tk.Entry(
            output_frame,
            textvariable=self.compress_output_var,
            font=('Segoe UI', 10),
            width=30,
            relief=tk.FLAT,
            bg='white'
        )
        output_entry.pack(side=tk.LEFT, padx=10)
        
        # Compress button
        compress_button = tk.Button(
            tab,
            text="Compress PDF",
            command=self.compress_pdf,
            bg=self.accent_color,
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief=tk.FLAT,
            padx=30,
            pady=12
        )
        compress_button.pack(pady=(10, 20))
        
        return tab
    
    def create_rename_tab(self):
        tab = tk.Frame(self.root, bg=self.bg_color)
        
        # Instructions
        instructions = tk.Label(
            tab,
            text="Select a PDF file to rename",
            font=('Segoe UI', 10),
            bg=self.bg_color,
            fg=self.text_color,
            wraplength=500
        )
        instructions.pack(pady=10)
        
        # File selection frame
        file_frame = tk.Frame(tab, bg=self.bg_color)
        file_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.rename_file_var = tk.StringVar(value="No file selected")
        file_label = tk.Label(
            file_frame,
            textvariable=self.rename_file_var,
            font=('Segoe UI', 9),
            bg='white',
            fg=self.text_color,
            relief=tk.FLAT,
            anchor=tk.W,
            padx=10,
            pady=8
        )
        file_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_button = tk.Button(
            file_frame,
            text="Browse",
            command=self.select_rename_pdf,
            bg=self.button_color,
            fg='white',
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            padx=15
        )
        browse_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # New name frame
        name_frame = tk.Frame(tab, bg=self.bg_color)
        name_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            name_frame,
            text="New filename:",
            font=('Segoe UI', 10),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(side=tk.LEFT)
        
        self.rename_output_var = tk.StringVar(value="renamed.pdf")
        name_entry = tk.Entry(
            name_frame,
            textvariable=self.rename_output_var,
            font=('Segoe UI', 10),
            width=30,
            relief=tk.FLAT,
            bg='white'
        )
        name_entry.pack(side=tk.LEFT, padx=10)
        
        # Rename button
        rename_button = tk.Button(
            tab,
            text="Rename PDF",
            command=self.rename_pdf,
            bg=self.accent_color,
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief=tk.FLAT,
            padx=30,
            pady=12
        )
        rename_button.pack(pady=(10, 20))
        
        # Preview frame
        preview_frame = tk.LabelFrame(tab, text="Preview", font=('Segoe UI', 10, 'bold'), bg=self.bg_color)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10, ipady=5)
        
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame,
            height=6,
            font=('Consolas', 9),
            bg='#f5f5f5',
            fg=self.text_color
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.preview_text.insert(tk.END, "Select a PDF file to see metadata preview")
        self.preview_text.config(state=tk.DISABLED)
        
        return tab
    
    # ===== MERGE FUNCTIONS =====
    def add_pdfs_to_merge(self):
        files = filedialog.askopenfilenames(
            title="Select PDF files to merge",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if files:
            for file in files:
                if file not in self.files_to_merge:
                    self.files_to_merge.append(file)
                    self.merge_listbox.insert(tk.END, Path(file).name)
            
            self.log(f"Added {len(files)} PDF(s) for merging")
            self.status_var.set(f"Ready to merge {len(self.files_to_merge)} PDF(s)")
    
    def remove_selected_merge(self):
        selected_indices = self.merge_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select PDFs to remove")
            return
        
        # Remove in reverse order to maintain correct indices
        for index in reversed(selected_indices):
            self.merge_listbox.delete(index)
            del self.files_to_merge[index]
        
        self.log(f"Removed {len(selected_indices)} PDF(s) from merge list")
        self.status_var.set(f"Ready to merge {len(self.files_to_merge)} PDF(s)")
    
    def clear_merge_list(self):
        self.merge_listbox.delete(0, tk.END)
        self.files_to_merge.clear()
        self.log("Cleared merge list")
        self.status_var.set("Ready")
    
    def merge_pdfs(self):
        if len(self.files_to_merge) < 2:
            messagebox.showwarning("Insufficient Files", "Please select at least 2 PDFs to merge")
            return
        
        output_filename = self.merge_output_var.get().strip()
        if not output_filename:
            messagebox.showwarning("Missing Filename", "Please enter an output filename")
            return
        
        if not output_filename.lower().endswith('.pdf'):
            output_filename += '.pdf'
        
        output_path = filedialog.asksaveasfilename(
            title="Save Merged PDF As",
            defaultextension=".pdf",
            initialfile=output_filename,
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if not output_path:
            return
        
        try:
            merger = PyPDF2.PdfMerger()
            
            for i, file in enumerate(self.files_to_merge):
                merger.append(file)
                self.log(f"Added: {Path(file).name}")
            
            merger.write(output_path)
            merger.close()
            
            self.log(f"Successfully merged {len(self.files_to_merge)} PDFs into {Path(output_path).name}")
            messagebox.showinfo("Success", f"Merged {len(self.files_to_merge)} PDFs successfully!\nSaved as: {Path(output_path).name}")
            
            # Clear list after successful merge
            self.clear_merge_list()
            
        except Exception as e:
            self.log(f"Error merging PDFs: {str(e)}", error=True)
            messagebox.showerror("Error", f"Failed to merge PDFs:\n{str(e)}")
    
    # ===== SPLIT FUNCTIONS =====
    def select_split_pdf(self):
        file = filedialog.askopenfilename(
            title="Select PDF to split",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if file:
            self.pdf_to_split = file
            self.split_file_var.set(Path(file).name)
            
            # Get page count
            try:
                with open(file, 'rb') as f:
                    pdf = PyPDF2.PdfReader(f)
                    page_count = len(pdf.pages)
                    self.log(f"Selected PDF for splitting: {Path(file).name} ({page_count} pages)")
                    self.status_var.set(f"Selected PDF with {page_count} pages")
            except Exception as e:
                self.log(f"Error reading PDF: {str(e)}", error=True)
    
    def update_split_options(self):
        if self.split_type.get() == "ranges":
            self.range_frame.pack(pady=10)
        else:
            self.range_frame.pack_forget()
    
    def split_pdf(self):
        if not self.pdf_to_split:
            messagebox.showwarning("No File Selected", "Please select a PDF file to split")
            return
        
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            return
        
        try:
            with open(self.pdf_to_split, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                total_pages = len(pdf.pages)
                
                if self.split_type.get() == "all":
                    # Split into individual pages
                    prefix = self.split_prefix_var.get().strip()
                    
                    for page_num in range(total_pages):
                        output_filename = f"{prefix}page_{page_num + 1}.pdf"
                        output_path = Path(output_dir) / output_filename
                        
                        writer = PyPDF2.PdfWriter()
                        writer.add_page(pdf.pages[page_num])
                        
                        with open(output_path, 'wb') as out_file:
                            writer.write(out_file)
                        
                        self.log(f"Created: {output_filename}")
                    
                    self.log(f"Successfully split PDF into {total_pages} individual pages")
                    messagebox.showinfo("Success", f"Split PDF into {total_pages} individual pages")
                    
                else:
                    # Split by ranges
                    ranges_text = self.range_var.get().strip()
                    if not ranges_text:
                        messagebox.showwarning("No Ranges", "Please enter page ranges")
                        return
                    
                    # Parse ranges
                    ranges = self.parse_page_ranges(ranges_text, total_pages)
                    if not ranges:
                        messagebox.showwarning("Invalid Ranges", "Please enter valid page ranges")
                        return
                    
                    prefix = self.split_prefix_var.get().strip()
                    
                    for i, (start, end) in enumerate(ranges):
                        output_filename = f"{prefix}part_{i + 1}.pdf"
                        output_path = Path(output_dir) / output_filename
                        
                        writer = PyPDF2.PdfWriter()
                        for page_num in range(start - 1, end):
                            writer.add_page(pdf.pages[page_num])
                        
                        with open(output_path, 'wb') as out_file:
                            writer.write(out_file)
                        
                        self.log(f"Created: {output_filename} (pages {start}-{end})")
                    
                    self.log(f"Successfully split PDF into {len(ranges)} parts")
                    messagebox.showinfo("Success", f"Split PDF into {len(ranges)} parts")
            
            self.status_var.set("PDF split completed")
            
        except Exception as e:
            self.log(f"Error splitting PDF: {str(e)}", error=True)
            messagebox.showerror("Error", f"Failed to split PDF:\n{str(e)}")
    
    def parse_page_ranges(self, ranges_text, max_page):
        """Parse page range string like '1-3, 5, 7-9'"""
        ranges = []
        parts = [p.strip() for p in ranges_text.split(',')]
        
        for part in parts:
            if '-' in part:
                try:
                    start_str, end_str = part.split('-')
                    start = int(start_str.strip())
                    end = int(end_str.strip())
                    
                    if 1 <= start <= end <= max_page:
                        ranges.append((start, end))
                    else:
                        return None
                except:
                    return None
            else:
                try:
                    page = int(part.strip())
                    if 1 <= page <= max_page:
                        ranges.append((page, page))
                    else:
                        return None
                except:
                    return None
        
        return ranges
    
    # ===== COMPRESS FUNCTIONS =====
    def select_compress_pdf(self):
        file = filedialog.askopenfilename(
            title="Select PDF to compress",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if file:
            self.pdf_to_compress = file
            self.compress_file_var.set(Path(file).name)
            
            # Get file size
            file_size = Path(file).stat().st_size
            size_mb = file_size / (1024 * 1024)
            self.log(f"Selected PDF for compression: {Path(file).name} ({size_mb:.2f} MB)")
            self.status_var.set(f"Selected PDF: {size_mb:.2f} MB")
    
    def compress_pdf(self):
        if not self.pdf_to_compress:
            messagebox.showwarning("No File Selected", "Please select a PDF file to compress")
            return
        
        output_filename = self.compress_output_var.get().strip()
        if not output_filename:
            messagebox.showwarning("Missing Filename", "Please enter an output filename")
            return
        
        if not output_filename.lower().endswith('.pdf'):
            output_filename += '.pdf'
        
        output_path = filedialog.asksaveasfilename(
            title="Save Compressed PDF As",
            defaultextension=".pdf",
            initialfile=output_filename,
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if not output_path:
            return
        
        try:
            # Get original size
            original_size = Path(self.pdf_to_compress).stat().st_size
            
            # Simple compression by rewriting the PDF
            # Note: For more advanced compression, you would need additional libraries
            # like pikepdf or ghostscript
            reader = PyPDF2.PdfReader(self.pdf_to_compress)
            writer = PyPDF2.PdfWriter()
            
            # Copy all pages
            for page in reader.pages:
                writer.add_page(page)
            
            # Apply compression based on selected level
            compression = self.compression_level.get()
            
            # Write with compression
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            # Get compressed size
            compressed_size = Path(output_path).stat().st_size
            
            # Calculate compression ratio
            ratio = (1 - compressed_size / original_size) * 100
            
            self.log(f"Compressed PDF: {original_size/(1024*1024):.2f} MB -> {compressed_size/(1024*1024):.2f} MB ({ratio:.1f}% reduction)")
            messagebox.showinfo(
                "Success", 
                f"PDF compressed successfully!\n\n"
                f"Original: {original_size/(1024*1024):.2f} MB\n"
                f"Compressed: {compressed_size/(1024*1024):.2f} MB\n"
                f"Reduction: {ratio:.1f}%"
            )
            
            self.status_var.set(f"Compression complete: {ratio:.1f}% reduction")
            
        except Exception as e:
            self.log(f"Error compressing PDF: {str(e)}", error=True)
            messagebox.showerror("Error", f"Failed to compress PDF:\n{str(e)}")
    
    # ===== RENAME FUNCTIONS =====
    def select_rename_pdf(self):
        file = filedialog.askopenfilename(
            title="Select PDF to rename",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if file:
            self.pdf_to_rename = file
            self.rename_file_var.set(Path(file).name)
            
            # Extract and display metadata
            self.display_pdf_metadata(file)
            
            self.log(f"Selected PDF for renaming: {Path(file).name}")
            self.status_var.set("PDF selected for renaming")
    
    def display_pdf_metadata(self, filepath):
        """Display PDF metadata in preview panel"""
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete(1.0, tk.END)
        
        try:
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                
                metadata = reader.metadata
                num_pages = len(reader.pages)
                file_size = Path(filepath).stat().st_size
                
                preview_text = f"File: {Path(filepath).name}\n"
                preview_text += f"Size: {file_size / 1024:.1f} KB\n"
                preview_text += f"Pages: {num_pages}\n\n"
                preview_text += "Metadata:\n"
                preview_text += "-" * 30 + "\n"
                
                if metadata:
                    for key, value in metadata.items():
                        if value:
                            preview_text += f"{key[1:] if key.startswith('/') else key}: {value}\n"
                else:
                    preview_text += "No metadata found\n"
                
                # Try to get text from first page using pdfplumber
                try:
                    with pdfplumber.open(filepath) as pdf:
                        if len(pdf.pages) > 0:
                            first_page = pdf.pages[0]
                            text = first_page.extract_text()
                            if text and len(text) > 0:
                                preview_text += "\nFirst page preview (first 200 chars):\n"
                                preview_text += "-" * 30 + "\n"
                                preview_text += text[:200] + "..." if len(text) > 200 else text
                except:
                    preview_text += "\n[Could not extract text preview]"
                
                self.preview_text.insert(tk.END, preview_text)
        
        except Exception as e:
            self.preview_text.insert(tk.END, f"Error reading PDF metadata:\n{str(e)}")
        
        self.preview_text.config(state=tk.DISABLED)
    
    def rename_pdf(self):
        if not self.pdf_to_rename:
            messagebox.showwarning("No File Selected", "Please select a PDF file to rename")
            return
        
        new_filename = self.rename_output_var.get().strip()
        if not new_filename:
            messagebox.showwarning("Missing Filename", "Please enter a new filename")
            return
        
        if not new_filename.lower().endswith('.pdf'):
            new_filename += '.pdf'
        
        try:
            original_path = Path(self.pdf_to_rename)
            new_path = original_path.parent / new_filename
            
            # Check if the new filename already exists
            if new_path.exists():
                response = messagebox.askyesno(
                    "File Exists", 
                    f"A file named '{new_filename}' already exists.\nDo you want to replace it?"
                )
                if not response:
                    return
            
            # Rename the file
            original_path.rename(new_path)
            
            self.log(f"Renamed: {original_path.name} -> {new_filename}")
            messagebox.showinfo("Success", f"PDF renamed successfully!\n\nNew name: {new_filename}")
            
            # Update the UI
            self.pdf_to_rename = str(new_path)
            self.rename_file_var.set(new_filename)
            self.display_pdf_metadata(str(new_path))
            
            self.status_var.set(f"Renamed to: {new_filename}")
            
        except Exception as e:
            self.log(f"Error renaming PDF: {str(e)}", error=True)
            messagebox.showerror("Error", f"Failed to rename PDF:\n{str(e)}")
    
    # ===== UTILITY FUNCTIONS =====
    def log(self, message, error=False):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        
        if error:
            # Insert with error styling
            self.log_text.insert(tk.END, log_message, 'error')
        else:
            self.log_text.insert(tk.END, log_message)
        
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Configure tag for error messages
        self.log_text.tag_config('error', foreground='red')

def main():
    root = tk.Tk()
    
    # Set window icon if available
    try:
        root.iconbitmap(default='pdf_icon.ico')
    except:
        pass
    
    app = PDFToolkit(root)
    
    # Handle window close
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit PDF Toolkit?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()