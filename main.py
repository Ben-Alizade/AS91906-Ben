import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from database import DatabaseManager
from models import ResearchItem
from services import fetch

import threading
import time
import math

class ResearchRadarApp:

    # Initial Functions --------------------------------

    def __init__(self, root):
        self.root = root
        self.root.title("AI Research Radar")
        self.root.geometry("1200x650")

        # Initialise the databasemanager class enabling operations
        self.database = DatabaseManager()

        # Track the active screen frame
        self.current_frame = None
        
        # Start at the dashboard
        self.show_dashboard()

    def clear_screen(self):
        """Destroys the current screen if it exists."""
        if self.current_frame is not None:
            self.current_frame.destroy()

    # Pages -----------------------------------------------------------------------

    def card(self, parent, image_obj, command, row, col):
        
        # 1. Create the button widget
        # 'compound="top"' places the image directly above the text
        btn = tk.Button(
            parent,
            image=image_obj,
            command=command if command != "placeholder" else None,
            compound="top",
            font=("Poppins", 14, "bold"),
            fg="white",
            bg="#3a3a3a",         # Slightly lighter gray card background
            activebackground="#505050", # Highlight color when clicked
            activeforeground="white",
            bd=0,                 # Flat design (no border)
            relief="flat",
            padx=20,
            pady=20,
            cursor="hand2"        # Changes cursor to a hand on hover
        )
        
        # 2. Place it into the grid
        # 'padx' and 'pady' create spacing *between* the buttons
        btn.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Optional: Configure the grid inside the buttons frame to make sizes uniform
        parent.grid_columnconfigure(col, weight=1)
        parent.grid_rowconfigure(row, weight=1)


    def show_dashboard(self):
        self.clear_screen()

        bg = "#2b2b2b"
        purple = "#a000ff"

        self.current_frame = tk.Frame(self.root, bg=bg) # bg=bg applies the background
        self.current_frame.pack(fill="both", expand=True)

        # top accent bar
        tk.Frame(self.current_frame, bg=purple, height=20).pack(fill="x")

        # title area
        header = tk.Frame(self.current_frame, bg=bg)
        header.pack(anchor="w", padx=40, pady=(28, 0))

        tk.Label(
            header,
            text="AI Research Radar",
            font=("Poppins", 48, "bold"),
            fg="white",
            bg=bg,
        ).pack(anchor="w", padx=(36, 0), pady=(8, 0))

        tk.Label(
            header,
            text="Up-to-date info on the latest AI news.",
            font=("Poppins", 20),
            fg="#d0d0d0",
            bg=bg
        ).pack(anchor="w", padx=(36, 0), pady=(0, 8))

        # little underline
        tk.Frame(
            self.current_frame,
            bg="#FFFFFF",
            width=50,
            height=1
        ).pack(anchor="w", padx=(76, 0), pady=(0, 0))


        # button grid
        buttons = tk.Frame(self.current_frame, bg=bg)
        buttons.pack(anchor="w", padx=(60, 0), pady=(40, 0))

        # load placeholder PNGs
        icon_size = (440, 140)

        # load, resize, and convert PNGs using Pillow
        img1 = Image.open("images/view_database.png").resize(icon_size, Image.Resampling.LANCZOS)
        self.db_img = ImageTk.PhotoImage(img1)

        img2 = Image.open("images/update_news.png").resize(icon_size, Image.Resampling.LANCZOS)
        self.fetch_img = ImageTk.PhotoImage(img2)

        img3 = Image.open("images/generate_report.png").resize(icon_size, Image.Resampling.LANCZOS)
        self.report_img = ImageTk.PhotoImage(img3)

        img4 = Image.open("images/exit_program.png").resize(icon_size, Image.Resampling.LANCZOS)
        self.exit_img = ImageTk.PhotoImage(img4)

        # Button 1: View Database
        self.card(buttons, self.db_img, self.show_search_library, 0, 0)

        # Button 2: Update News
        self.card(buttons, self.fetch_img, self.show_loading_screen, 0, 1)

        # Button 3: Generate Report
        self.card(buttons,  self.report_img, "placeholder", 1, 0)

        # Button 4: Exit Program
        self.card(buttons, self.exit_img, self.exit, 1, 1)



    def show_loading_screen(self):
        self.clear_screen()

        bg = "#2b2b2b"
        purple = "#a000ff"

        self.current_frame = tk.Frame(self.root, bg=bg) # bg=bg applies the background
        self.current_frame.pack(fill="both", expand=True)

        # top accent bar
        tk.Frame(self.current_frame, bg=purple, height=20).pack(fill="x")

        # Create main label
        tk.Label(
            self.current_frame,
            text="Retrieving Data...",
            font=("Poppins", 48, "bold"),
            fg="white",
            justify="center",
            bg=bg,
        ).pack(anchor="center", padx=(36, 0), pady=(80, 0))

        # Currently fetching from...
        self.fetch_label = tk.Label(
            self.current_frame,
            text="Currently fetching from ArXiv...",
            font=("Poppins", 20),
            fg="#d0d0d0",
            justify="center",
            bg=bg
        )
        self.fetch_label.pack(anchor="center", padx=(36, 0), pady=(0, 8))

        # little underline
        tk.Frame(
            self.current_frame,
            bg="#FFFFFF",
            width=50,
            height=1
        ).pack(anchor="center", padx=(76, 0), pady=(0, 40))

        # Create a frame for the metrics
        metrics_frame = tk.Frame(self.current_frame, bg=bg)
        metrics_frame.pack(anchor="center", pady=(0, 0))


        # Left column: items added
        items_block = tk.Frame(metrics_frame, bg=bg)
        items_block.grid(row=0, column=0, padx=50)

        tk.Label(
            items_block, 
            text="Items Added:", 
            font=("Poppins", 16), 
            fg="#d0d0d0", 
            bg=bg
        ).pack(anchor="w")

        # Store a reference (self.items_label) so I can update the text later
        self.items_label = tk.Label(
            items_block, 
            text="0/2k", 
            font=("Poppins", 48, "bold"), 
            fg=purple, 
            bg=bg
        )
        self.items_label.pack(anchor="w")

        # Right column: time elapsed
        time_block = tk.Frame(metrics_frame, bg=bg)
        time_block.grid(row=0, column=1, padx=50)

        tk.Label(
            time_block, 
            text="Time Elapsed:", 
            font=("Poppins", 16), 
            fg="#d0d0d0", 
            bg=bg
        ).pack(anchor="e")

        # Store a reference (self.time_label) to easily update the clock live
        self.time_label = tk.Label(
            time_block, 
            text="0:21", 
            font=("Poppins", 48, "bold"), 
            fg=purple, 
            bg=bg
        )
        self.time_label.pack(anchor="e")

        # Start background work
        self.start_scraping_job()

    def show_search_library(self):
        self.clear_screen()

        tree = ttk.Treeview(self.root, columns=("title", "url", "tags", "trending", "read", "saved"), show="headings")
        tree.pack()

        research_items = self.database.get_all_items()

        for row in research_items:
            tree.insert("", tk.END, values=row)

        self.show_selected_item("selected_item")


    def show_selected_item(self, selected_item):
        self.clear_screen
        print(selected_item)

    def exit(self):
        self.root.quit()


    # Page Operations -----------------------------------------------------------------------

    def start_scraping_job(self):

        # Set initial tracking variables
        self.start_time = time.time()
        self.is_scraping = True
        self.item_count = 0

        # Run a thread to automatically update the 
        scraper_thread = threading.Thread(target=self.network_scraper_task, daemon=True)
        scraper_thread.start()

        # 2. Start the main thread GUI label updater loop
        self.update_gui_loop()

    def network_scraper_task(self):

        fetch.fetch_arxiv(self.database, self)
        self.fetch_label.config(text="Currently fetching from HackerNews...")
        fetch.fetch_hackernews(self.database, self)
        self.is_scraping = False

    def update_gui_loop(self):

        # Update items
        self.items_label.config(text=f"{self.item_count}/2k")

        # Ypdate the clock
        elapsed = int(time.time() - self.start_time)
        self.time_label.config(text=f"{elapsed // 60}:{elapsed % 60:02d}")

        # Check if thread is still running
        if self.is_scraping:
            # Call this same function again in 100 milliseconds
            self.root.after(100, self.update_gui_loop)
        else:
            # Scraping finished! Safely create the button on the main thread
            self.items_label.config(font=("Poppins Black", 48, "bold"))
            return_btn = tk.Button(self.current_frame, text="Return Home", command=self.show_dashboard)
            return_btn.pack(pady=10)

    

def main():
    root = tk.Tk()
    app = ResearchRadarApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
