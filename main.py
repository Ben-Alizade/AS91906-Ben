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
        self.root.geometry("900x500")

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

    def card(parent, img, card_command, card_row, card_column):
        tk.Button(
            parent,
            image=img,
            command=card_command,
            bd=0,
            bg="#2b2b2b",
            activebackground="#2b2b2b",
            highlightthickness=0,
            cursor="hand2"
        ).grid(row=card_row, column=card_column, padx=8, pady=8)

    def show_dashboard(self):
        self.clear_screen()

        """# Create a fresh new frame container for the dashboard
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)

        # Put widgets directly inside self.current_frame
        title = tk.Label(self.current_frame, text="AI Research Radar", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        # Create buttons
        search_btn = tk.Button(self.current_frame, text="Search", command=self.show_search_library)
        fetch_btn = tk.Button(self.current_frame, text="Fetch Latest Data", command=self.show_loading_screen)
        generate_report_btn = tk.Button(self.current_frame, text="Generate Report", command="PLACEHOLDER")
        exit_btn = tk.Button(self.current_frame, text="Exit", command=self.exit)

        # Pack Buttons
        search_btn.pack()
        fetch_btn.pack()
        generate_report_btn.pack()
        exit_btn.pack()"""

        bg = "#2b2b2b"
        purple = "#a000ff"

        self.current_frame = tk.Frame(self.root, bg=bg)
        self.current_frame.pack(fill="both", expand=True)

        # top accent bar
        tk.Frame(self.current_frame, bg=purple, height=12).pack(fill="x")

        # title area
        header = tk.Frame(self.current_frame, bg=bg)
        header.pack(anchor="w", padx=40, pady=(28, 0))

        tk.Label(
            header,
            text="AI Research Radar",
            font=("Inter", 36, "bold"),
            fg="white",
            bg=bg
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Up-to-date info on the latest AI news.",
            font=("Inter", 13),
            fg="#d0d0d0",
            bg=bg
        ).pack(anchor="w", pady=(4, 0))

        # little underline
        tk.Frame(
            header,
            bg="#8c8c8c",
            width=30,
            height=2
        ).pack(anchor="w", pady=(8, 0))

        # button grid
        buttons = tk.Frame(self.current_frame, bg=bg)
        buttons.pack(pady=55)

        # load placeholder PNGs
        self.db_img = tk.PhotoImage(file="images/database.png")
        self.news_img = tk.PhotoImage(file="images/news.png")
        self.report_img = tk.PhotoImage(file="images/report.png")
        self.exit_img = tk.PhotoImage(file="images/exit.png")

        card(buttons, self.db_img, self.show_search_library, 0, 0)
        card(buttons, self.news_img, self.show_loading_screen, 0, 1)
        card(buttons, self.report_img, "placeholder", 1, 0)
        card(buttons, self.exit_img, self.exit, 1, 1)


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
