from tkinter import filedialog, Label, Button


class FileSelectionDialog:
    def __init__(self, master):
        self.master = master
        self.label = None
        self.select_button = None
        self.stat_file_paths = None

    def select_button_click(self):
        self.stat_file_paths = filedialog.askopenfilenames()
        if self.stat_file_paths == "" or \
            (not all([file_path.endswith('.csv') or file_path.endswith('.xlsx')
             for file_path in list(self.stat_file_paths)])):
            self.stat_file_paths = ""
        else:
            self.master.destroy()  # Close the grid after a file is selected

    def run(self):
        self.master.title("视频切割器")
        self.label = Label(self.master, text="选择表格文件",
                           height=5, font=("Helvetica", "13"))
        self.label.pack()
        self.select_button = Button(self.master, command=self.select_button_click, text="浏览")
        self.select_button.config(height=2, width=8)
        self.select_button.pack()

    def get_file_paths(self):
        if self.stat_file_paths is None:
            return None
        else:
            return list(self.stat_file_paths)
