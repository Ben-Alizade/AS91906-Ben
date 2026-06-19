import tkinter as tk
from tkinter import ttk

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
        self.root.geometry("1200x600")

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

    def card(self, parent, text_line1, text_line2, img, card_command, card_row, card_column):
        # Create the Card Outer Container (The purple top-border / outline effect)
        card_frame = tk.Frame(
            parent,
            bg="#000000",
            highlightbackground="#8A00FF",
            highlightthickness=2,
            bd=0,
            width=300,
            height=120 
        )
        card_frame.grid(row=card_row, column=card_column, padx=12, pady=12, sticky="nsew")
        
        # Configure grid weight inside the card so elements stretch nicely
        card_frame.columnconfigure(0, weight=1) 
        card_frame.columnconfigure(1, weight=0)

        # 2. Text Container (Left Side)
        text_container = tk.Frame(card_frame, bg="#000000")
        text_container.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="w")

        # Line 1: e.g., "View"
        lbl1 = tk.Label(
            text_container,
            text=text_line1,
            font=("Poppins", 30, "bold"),
            fg="white",
            bg="#000000",
            anchor="w",
            justify="left"
        )
        lbl1.pack(anchor="w", fill="x")

        # Line 2: e.g., "Database"
        lbl2 = tk.Label(
            text_container,
            text=text_line2,
            font=("Poppins", 30, "bold"),
            fg="white",
            bg="#000000",
            anchor="w",
            justify="left"
        )
        lbl2.pack(anchor="w", fill="x")

        # 3. Icon Asset (Right Side)
        icon_label = tk.Label(
            card_frame,
            image=img,
            bg="#000000",
            bd=0,
            highlightthickness=0
        )
        icon_label.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="e")

        # 4. Bind Click Events to EVERYTHING inside the card so the whole card acts as a button
        interactive_elements = [card_frame, text_container, lbl1, lbl2, icon_label]
        
        for element in interactive_elements:
            element.config(cursor="hand2")
            element.bind("<Button-1>", lambda event: card_command())

    def show_dashboard(self):
        self.clear_screen()

        bg = "#2b2b2b"
        purple = "#a000ff"

        self.current_frame = tk.Frame(self.root, bg=bg) # bg=bg applies the background
        self.current_frame.pack(fill="both", expand=True)

        # top accent bar
        tk.Frame(self.current_frame, bg=purple, height=12).pack(fill="x")

        # title area
        header = tk.Frame(self.current_frame, bg=bg)
        header.pack(anchor="w", padx=40, pady=(28, 0))

        tk.Label(
            header,
            text="AI Research Radar",
            font=("Poppins", 48, "bold"),
            fg="white",
            bg=bg,
            padx=0,
            pady=0
        ).pack(anchor="w", padx=(36, 0), pady=(8, 0))

        tk.Label(
            header,
            text="Up-to-date info on the latest AI news.",
            font=("Poppins", 20),
            fg="#d0d0d0",
            bg=bg
        ).pack(anchor="w", padx=(36, 0), pady=(0, 0))

        # little underline
        tk.Frame(
            header,
            bg="#FFFFFF",
            width=50,
            height=1
        ).pack(anchor="w", padx=(40, 0), pady=(8, 0))

        # button grid
        buttons = tk.Frame(self.current_frame, bg=bg)
        buttons.pack(pady=55)

        # load placeholder PNGs
        self.db_img = tk.PhotoImage(file="images/database.png")
        self.fetch_img = tk.PhotoImage(file="images/fetch.png")
        self.report_img = tk.PhotoImage(file="images/report.png")
        self.exit_img = tk.PhotoImage(file="images/exit.png")

        # Button 1: View Database
        self.card(buttons, "View", "Database", self.db_img, self.show_search_library, 0, 0)

        # Button 2: Update News
        self.card(buttons, "Update", "News", self.fetch_img, "placeholder", 0, 1)

        # Button 3: Generate Report
        self.card(buttons, "Generate", "Report", self.report_img, "placeholder", 1, 0)

        # Button 4: Exit Program
        self.card(buttons, "Exit", "Program", self.exit_img, self.exit, 1, 1)


    def show_loading_screen(self):
        self.clear_screen()  # Clear the dashboard away

        # Create a fresh new frame container for the loading screen
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)

        # Create status text label
        self.status_label = tk.Label(self.current_frame, text="Receiving up-to-date info....", font=("Arial", 20, "bold"))
        self.status_label.pack(pady=20)

        # Start background work
        threading.Thread(target=self.run_fetch_background, daemon=True).start()

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

    def run_fetch_background(self):

        # Creates a time object to track the amount of time has passed
        start_time = time.time()
        
        arxiv_fetch_number = fetch.fetch_arxiv(self.database)
        self.status_label.config(text="Received info from arXiv!\nNow fetching from Hacker News...")
        
        hackernews_fetch_number = fetch.fetch_hackernews(self.database)
        total_added_items = arxiv_fetch_number + hackernews_fetch_number

        # Calculate the total time elapsed
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Display in minute:second format
        elapsed_time = f"{math.floor(elapsed_time // 60):.0f}:{elapsed_time % 60:.0f}"
        
        self.status_label.config(text=f"Done! Added {total_added_items} items in {elapsed_time}.")

        # Create the return button after fetching is done
        return_btn = tk.Button(self.current_frame, text="Return Home", command=self.show_dashboard)
        return_btn.pack(pady=10)



def main():
    root = tk.Tk()
    app = ResearchRadarApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
