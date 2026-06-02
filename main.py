import tkinter as tk
from tkinter import ttk

from database import DatabaseManager
from models import ResearchItem
from services import fetch
import threading

class ResearchRadarApp:

    def run_fetch_background(self, title_label):

        arxiv_items_added = fetch.fetch_arxiv(self.database)
        title_label.config(text="Received info from arxiv!\nNow fetching from hackernews...")

        hackernews_items_added = fetch.fetch_hackernews()
        total_items_added = hackernews_items_added + arxiv_items_added
        title_label.config(text=f"Added {total_items_added} new items.")

        return_btn = tk.Button(self.dashboard_frame, text="Return home", command=self.dashboard)
        return_btn.pack()

    def fetch_new_info(self):

        self.clear_page(self.dashboard_frame)
            
        fetch_loading_frame = tk.Frame(self.root)
        fetch_loading_frame.pack()
        
        title_label = tk.Label(
        fetch_loading_frame,
        text="Receiving up to date info....",
        font=("Arial", 20, "bold")
        )
        
        title_label.pack(pady=10)

        threading.Thread(target=self.run_fetch_background, args=(title_label,), daemon=True).start()

    def clear_page(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def create_sample_data(self):
        item1 = ResearchItem(
            title="Hello",
            url="url/",
            date="yesterday",
            authors="idk",
            summary="summary",
            tags={"AI", "Reinforcement learning"}
        )

        item2 = ResearchItem(
            title="Goodbye",
            url="url/33333",
            date="today",
            authors="still idk",
            summary="not a summary",
            tags={"execution", "shittywifi"}
        )

        return item1, item2

    def dashboard(self):
        
        self.dashboard_frame = tk.Frame(self.root)
        self.dashboard_frame.pack()


        title_label = tk.Label(
            self.dashboard_frame,
            text="AI research radar",
            font=("Arial", 20, "bold")
        )

        title_label.pack(pady=10)

        # create the buttons
        search_btn = tk.Button(self.dashboard_frame, text="Search", command="PLACEHOLDER")
        fetch_btn = tk.Button(self.dashboard_frame, text="Fetch Latest Data", command=self.fetch_new_info)
        saved_items_btn = tk.Button(self.dashboard_frame, text="Saved Items", command="PLACEHOLDER")
        generate_report_btn = tk.Button(self.dashboard_frame, text="Generate Report", command="PLACEHOLDER")
        exit_btn = tk.Button(self.dashboard_frame, text="Exit", command="PLACEHOLDER")


        # im PACKING down there
        search_btn.pack()
        fetch_btn.pack()
        saved_items_btn.pack()
        generate_report_btn.pack()
        exit_btn.pack()

        return self.dashboard_frame
    
    def __init__(self, root):
        self.root = root
        self.root.title("AI Research Radar")
        self.root.geometry("900x500")

        self.database = DatabaseManager()

        item1, item2 = self.create_sample_data()
        self.database.add_item(item1)
        self.database.add_item(item2)

        dashboard_frame = self.dashboard()

        # check whether items exist
        items = self.database.get_all_items()

        self.clear_page(dashboard_frame)
        self.dashboard()



def main():
    root = tk.Tk()
    app = ResearchRadarApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()