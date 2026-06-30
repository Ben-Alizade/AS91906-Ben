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

    def create_frame(self):

        bg = "#2b2b2b"
        purple = "#a000ff"

        self.current_frame = tk.Frame(self.root, bg=bg) # bg=bg applies the background
        self.current_frame.pack(fill="both", expand=True)

        # top accent bar
        tk.Frame(self.current_frame, bg=purple, height=20).pack(fill="x")

        return bg, purple

    def card(self, parent, image_obj, command, row, col):
        
        # Create the button widget
        button = tk.Button(
            parent,
            image=image_obj,
            command=command if command != "placeholder" else None,
            compound="top",
            font=("Poppins", 14, "bold"),
            fg="white",
            bg="#3a3a3a",
            activebackground="#505050", # Highlight color when clicked
            activeforeground="white",
            bd=0,
            relief="flat",
            padx=20,
            pady=20,
            cursor="hand2"        # Changes cursor to a hand on hover
        )
        
        # Place it into the grid
        button.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Optional: Configure the grid inside the buttons frame to make sizes uniform
        parent.grid_columnconfigure(col, weight=1)
        parent.grid_rowconfigure(row, weight=1)


    def show_dashboard(self):
        self.clear_screen()

        bg, purple = self.create_frame()

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
        self.icon_size = (440, 140)

        # load, resize, and convert PNGs using Pillow
        img1 = Image.open("images/view_database.png").resize(self.icon_size, Image.Resampling.LANCZOS)
        self.db_img = ImageTk.PhotoImage(img1)

        img2 = Image.open("images/update_news.png").resize(self.icon_size, Image.Resampling.LANCZOS)
        self.fetch_img = ImageTk.PhotoImage(img2)

        img3 = Image.open("images/generate_report.png").resize(self.icon_size, Image.Resampling.LANCZOS)
        self.report_img = ImageTk.PhotoImage(img3)

        img4 = Image.open("images/exit_program.png").resize(self.icon_size, Image.Resampling.LANCZOS)
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
        bg, purple = self.create_frame()

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
            text="0/2000", 
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
        bg, purple = self.create_frame()

        # Controls area ----------------------------------------------------
        controls = tk.Frame(self.current_frame, bg=bg)
        controls.pack(fill="x", padx=40, pady=(20, 10))

        # Title Search
        tk.Label(controls, text="Search:", font=("Poppins", 11), fg="white", bg=bg).pack(side="left")
        search_var = tk.StringVar()
        search_entry = tk.Entry(controls, textvariable=search_var, bg="#3a3a3a", fg="white", bd=0, width=20)
        search_entry.pack(side="left", padx=10)

        # Filters for Saved & Read
        saved_var = tk.StringVar(value="both")
        read_var = tk.StringVar(value="both")
        
        ttk.Combobox(controls, textvariable=saved_var, values=["both", "yes", "no"], width=8).pack(side="right", padx=5)
        tk.Label(controls, text="Saved:", fg="white", bg=bg).pack(side="right")
        
        ttk.Combobox(controls, textvariable=read_var, values=["both", "yes", "no"], width=8).pack(side="right", padx=5)
        tk.Label(controls, text="Read:", fg="white", bg=bg).pack(side="right")

        # Table area -------------------------------------------------------
        table_frame = tk.Frame(self.current_frame, bg=bg)
        table_frame.pack(fill="both", expand=True, padx=40, pady=(10, 40))

        # Configure dark colors and #A100FF header for the Treeview style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="black", fieldbackground="black", foreground="white", rowheight=25)
        style.configure("Treeview.Heading", background="#A100FF", foreground="white", font=("Poppins", 11, "bold"))

        # Setup scrollbar
        scrollbar = tk.Scrollbar(table_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Setup the 6 columns
        columns = ("title", "url", "date", "tags", "read", "saved")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        tree.pack(side="left", fill="both", expand=True)

        # Set headings
        for col in columns:
            tree.heading(col, text=col.replace("_", " ").title())
            tree.column(col, anchor="center" if col in ("read", "saved") else "w")

        # Live population engine -------------------------------------------
        research_items = self.database.get_all_items()

        def update_view(*args):
            tree.delete(*tree.get_children())
            query = search_var.get().lower()
            
            for item in research_items:
                # Run quick string and state logic filters
                if query and query not in item[1].lower(): continue
                if saved_var.get() == "yes" and not item.saved: continue
                if saved_var.get() == "no" and item.saved: continue
                if read_var.get() == "yes" and not item.read: continue
                if read_var.get() == "no" and item.read: continue

                # Insert data rows (using text marks for boolean lookups)
                tree.insert("", tk.END, values=(
                    item[1],
                    item[2],
                    item[3],
                    ", ".join(item[6]),
                    "▣ Yes" if item[8] else "□ No",
                    "▣ Yes" if item[9] else "□ No"
                ))

        # Core operational triggers -----------------------------------------
        search_var.trace_add("write", update_view)
        saved_var.trace_add("write", update_view)
        read_var.trace_add("write", update_view)

        # Draw default library matrix list
        update_view()

        
    def show_completion_screen(self, items, time_elapsed):
        self.clear_screen()
        bg, purple = self.create_frame()

        self.item_count = 0

        # Create main label
        tk.Label(
            self.current_frame,
            text=f"Done! Added {items} items in {time_elapsed}.",
            font=("Poppins", 48, "bold"),
            fg="white",
            justify="center",
            bg=bg,
        ).pack(anchor="center", padx=(36, 0), pady=(80, 0))

        
        self.fetch_label = tk.Label(
            self.current_frame,
            text="Head to the search library to view these items.",
            font=("Poppins", 20),
            fg="#d0d0d0",
            justify="center",
            bg=bg
        )
        self.fetch_label.pack(anchor="center", padx=(36, 0), pady=(0, 8))


        # Scraping finished! Safely create the button on the main thread
        img = Image.open("images/exit_program.png").resize(self.icon_size, Image.Resampling.LANCZOS)
        self.return_img = ImageTk.PhotoImage(img)

        # Create the button widget
        return_button = tk.Button(
            self.current_frame,
            image=self.return_img,
            command=self.show_dashboard,
            compound="top",
            font=("Poppins", 14, "bold"),
            fg="white",
            bg="#3a3a3a",
            activebackground="#505050",
            activeforeground="white",
            bd=0,
            relief="flat",
            padx=20,
            pady=20,
            cursor="hand2"
        ).pack(anchor="center", pady=(10, 0))



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
        self.items_label.config(text=f"{self.item_count}/2000")

        # Ypdate the clock
        elapsed = int(time.time() - self.start_time)
        time_label_display = f"{elapsed // 60}:{elapsed % 60:02d}"
        self.time_label.config(text=time_label_display)

        # Check if thread is still running
        if self.is_scraping:
            # Call this same function again in 100 milliseconds
            self.root.after(100, self.update_gui_loop)
        else:
            self.show_completion_screen(self.item_count, time_label_display)
    

def main():
    root = tk.Tk()
    app = ResearchRadarApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
