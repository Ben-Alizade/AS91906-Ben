import tkinter as tk
from tkinter import ttk

from database import DatabaseManager
from models import ResearchItem
from services import fetch

class ResearchRadarApp:

    def clear_page(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def create_sample_data(self):
        item1 = ResearchItem(
            title="Hello",
            url="url/",
            source="fakesource",
            summary="summary",
            tags={"AI", "Reinforcement learning"}
        )

        item2 = ResearchItem(
            title="Goodbye",
            url="url/33333",
            source="realsource",
            summary="not a summary",
            tags={"execution", "shittywifi"}
        )

        return item1, item2

    def dashboard(self):
        
        dashboard_frame = tk.Frame(self.root)
        dashboard_frame.pack()


        title_label = tk.Label(
            dashboard_frame,
            text="AI research radar",
            font=("Arial", 20, "bold")
        )

        title_label.pack(pady=10)

        # create the buttons
        search_btn = tk.Button(dashboard_frame, text="Search", command="PLACEHOLDER")
        fetch_btn = tk.Button(dashboard_frame, text="Fetch Latest Data", command="PLACEHOLDER")
        saved_items_btn = tk.Button(dashboard_frame, text="Saved Items", command="PLACEHOLDER")
        generate_report_btn = tk.Button(dashboard_frame, text="Generate Report", command="PLACEHOLDER")
        exit_btn = tk.Button(dashboard_frame, text="Exit", command="PLACEHOLDER")


        # im PACKING down there
        search_btn.pack()
        fetch_btn.pack()
        saved_items_btn.pack()
        generate_report_btn.pack()
        exit_btn.pack()

        return dashboard_frame
    
    def __init__(self, root):
        self.root = root
        self.root.title("AI Research Radar")
        self.root.geometry("900x500")

        database = DatabaseManager()

        item1, item2 = self.create_sample_data()
        database.add_item(item1)
        database.add_item(item2)

        dashboard_frame = self.dashboard()

        # check whether items exist
        items = database.get_all_items()

        for item in items:
            print(item)

        self.clear_page(dashboard_frame)
        self.dashboard()



def main():
    root = tk.Tk()
    app = ResearchRadarApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()