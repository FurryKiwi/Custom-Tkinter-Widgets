# Copyright © 2022 FurryKiwi <normalusage2@gmail.com>

try:
    import Tkinter as tk
    import ttk
except ImportError:  # Python 3
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox, filedialog

from abc import abstractmethod


class SelectableFrames(ttk.Frame):
    """Selectable ttk Frames that create a frame beside it when selected, and unpacks that frame when the
    selected frame changes or is selected again.

    Args: parent_frame: tk.Frame | ttk.Frame | tk.Tk,
        headers: list[str],
        background: str,
        active_background: str"""

    def __init__(self, parent_frame, headers: list, background: str, active_background: str, **kwargs):
        ttk.Frame.__init__(self, parent_frame, **kwargs)
        self.parent_frame = parent_frame
        self.headers = headers
        self.background = background
        self.active_background = active_background

        self.options_frame = None
        self.selected_label = None
        self.initial_selected = None

        self.main_frame = ttk.Frame(self, relief='ridge', borderwidth=1)
        self.main_frame.pack(side='left', fill='y', expand=True)

        self.secondary_frame = ttk.Frame(self, relief='ridge', borderwidth=1)
        self.secondary_frame.pack(side='left', fill='both', expand=True, padx=4)

        self.custom_selectable_frames()

    def custom_selectable_frames(self):
        longest_string = max(self.headers, key=len)
        for i in range(len(self.headers)):
            new_frame = ttk.Frame(self.main_frame, class_=self.headers[i], relief='ridge', borderwidth=1)
            new_frame.grid(column=0, row=i)
            new_frame.grid_propagate(True)
            new_label = tk.Label(new_frame, text=self.headers[i], width=len(longest_string), background=self.background,
                                 font=("Arial", 20, "bold"), foreground='white')
            new_label.pack()
            new_label.bind("<Button-1>", lambda event: self.change_frame(event))
            if self.initial_selected is None:
                self.initial_selected = new_label
        self.change_frame(widget=self.initial_selected)

    def change_color(self, widget):
        """Changes the background color of the label selected."""
        parent = widget.master
        class_name = parent['class']
        if widget['background'] == self.active_background:
            widget['background'] = self.background
            self.deselect_frame()
        else:
            widget['background'] = self.active_background
            self.select_frame(class_name)

    def change_frame(self, event=None, widget=None):
        """Changes the selected frame."""
        if event:
            widget = event.widget
        elif widget:
            widget = widget

        if self.selected_label is None:
            self.selected_label = widget
            self.change_color(self.selected_label)
        else:
            if self.selected_label == widget:
                self.change_color(self.selected_label)
            else:
                self.selected_label['background'] = self.background
                self.selected_label = widget
                self.change_color(self.selected_label)

    @abstractmethod
    def select_frame(self, class_name):
        """Sets the selected frame. This method is meant to be overridden by child class."""
        pass

    @abstractmethod
    def deselect_frame(self):
        """Unpacks the selected frame. This method is meant to be overridden by child class."""
        pass


# Testing Purposes ----------------
class SelectableTest(SelectableFrames):

    def __init__(self, parent_frame, headers: list, background: str, active_background: str, **kwargs):
        SelectableFrames.__init__(self, parent_frame, headers, background, active_background, **kwargs)

    def select_frame(self, class_name):
        """Sets the selected frame. This method is meant to be overridden by child class."""
        if self.options_frame is not None:
            self.deselect_frame()

        self.options_frame = OptionsFrame(self.secondary_frame, class_=class_name)
        self.options_frame.pack(expand=True, fill='both', padx=4, pady=4)

    def deselect_frame(self):
        """Unpacks the selected frame. This method is meant to be overridden by child class."""
        if self.options_frame is not None:
            self.options_frame.pack_forget()


class OptionsFrame(ttk.Frame):
    _test_values = ['This', 'is', 'some', 'test text', 'labels']

    def __init__(self, parent_frame, values=None, **kwargs):
        ttk.Frame.__init__(self, parent_frame, **kwargs)
        self.class_name = kwargs['class_']
        self.parent_frame = parent_frame
        self.title_label = ttk.Label(self, text=f"{self.class_name} Page:", font=("Arial", 20, "bold", "underline"),
                                     width=500)
        self.title_label.pack(side='top')

        self.main_frame = ttk.Frame(self, relief='ridge', borderwidth=4)
        self.main_frame.pack()
        if values:
            self.values = values
            self.test()
        # Testing Purposes ---------
        self.values = self._test_values
        self.test()

    def test(self):
        import random
        ttk.Label(self.main_frame, text=random.choice(self.values), font=("Arial", 30, 'bold')).pack(padx=4, pady=4)
        ttk.Label(self.main_frame, text=random.choice(self.values), font=("Arial", 30, 'bold')).pack(padx=4, pady=4)
        ttk.Label(self.main_frame, text=random.choice(self.values), font=("Arial", 30, 'bold')).pack(padx=4, pady=4)


if __name__ == '__main__':
    root = tk.Tk()
    # Comment these out or change them if using a theme
    # tcl_path = "Core/tcl_files/azure.tcl"
    # root.tk.call("source", tcl_path)
    # root.tk.call("set_theme", "dark")
    # -------------
    # To set the window
    w, h = 600, 600
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.title("Selectable Frame")
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    main_frame = ttk.Frame(root)
    main_frame.pack(side='top', expand=True, fill='both', anchor='nw')

    head = ["General", "Appearance", "Backup", "Restore", "Contact", "Key Bindings", "Options", "Padding"]
    test = SelectableTest(main_frame, head, "#333333", "#007efd")
    test.pack(side='left', fill='y', expand=True, anchor='nw', padx=4, pady=4)

    root.iconify()
    root.deiconify()
    root.mainloop()
