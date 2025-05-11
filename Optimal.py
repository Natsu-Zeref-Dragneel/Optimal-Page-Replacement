import random
import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *

def generate_string(length: int) -> str:
    """Generates a reference string with the length provided."""
    ref_string = ""
    for i in range(length): # runs the loop until the inputtd length of the reference string is met.
        ref_string += str(random.randint(0,9)) # Generate a random number between 0 and 9, then appends it to the reference string.
    return ref_string # returns the complete reference string.

def search(ref_string: str, frames, index:int) -> int:
    """Searches for the index to be removed"""
    priority = [] # Keeps track of the priority of each frame
    cur_ref = ref_string[index:] # Substrings the reference string from the current character to the end
    for frame in frames: # runs the following until all frames have been checked
        try:
            priority.append(cur_ref.index(frame)) # appends the first instance of the frame in the reference string.
        except ValueError as err: # Catches the error if the character does not show in the reference string anymore.
            priority.append(len(ref_string)) # appends the length of the reference string for priority of the current frame.
    return priority.index(max(priority)) # returns the highest value in priority, which is the least used in the future.

def optimal(ref_string: str, length: int) -> dict:
    """Runs the Optimal Page replacement algorithm."""
    frames = [] # Keeps track of the frames for each step in the algorithm
    fr = "" # Formatted Final Frame Output for the Algorithm.

    miss = 0 # Keeps track of the miss count in the algorithm.
    hit = 0 # Keeps track of the hit count in the algorithm.
    isMiss = False # indicates if a loop cycle is either a hit or miss. default is hit.
    steps = [] # Records each step the algorithm takes.

    index = 0 # Keeps track of the current index or iteration of the loop.
    # runs the loop for each character
    for character in ref_string: # Runs the loop until all the characters in the reference string have been processed.
        # Checks if character is in frame
        if character in frames: # Checks if the character is already in the frames.
            hit += 1 # adds a hit count
        else: # if character is not in frame
            miss += 1 # adds a miss count
            isMiss = True # indicates that the cycle is a miss

            if len(frames) < length: # Check if frames is not full
                frames.append(character) # appends the character to a frame.

            elif len(frames) == length: # Check if frame is full
                index_to_remove = search(ref_string, frames, index) # Searches for the frame index to be removed.
                frames[index_to_remove] = character # replaces the frame with a new character.
        index += 1 # adds to the index or iteration count.

        # formats the current step's frames for display
        print_frame = frames.copy() # copies the frames to a temporary variable for formatting
        # Checks if the page is full and adds a dash(-) to empty frames
        if len(frames) < length:
            for i in range(length-len(frames)):
                print_frame.append('-')

        # format current string for display
        print_string = ""
        for j in print_frame:
            print_string += f" {j}"
        steps.append({"frames": print_string, "char": character, "miss": isMiss}) # add a record of the step to steps

    # Formats the final output of the algorithm.
    for f in frames:
        fr += f" {f}"

    # sends the steps and final output to be displayed
    return {"steps": steps, "miss": miss, "hit": hit, "ref": ref_string, "final": fr}

class MainWindow(QMainWindow):
    """main class for the GUI"""
    TITLE = "Optimal Page Replacement Algorithm by Vince Mico Garcia"
    WIDTH = 720
    HEIGHT = 480

    frame_length = 0
    ref_string_length = 0

    def __init__(self):
        """Creates the main window where the GUI will be displayed."""
        super().__init__()
        self.setWindowTitle(self.TITLE)
        self.resize(self.WIDTH, self.HEIGHT)
        self.setCentralWidget(self.panel())

    def panel(self):
        """Creates the panel where the GUI will be displayed."""
        self.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF;") # Sets the background color and text color of the GUI.

        self.table = QTableWidget(0, 3) # Creates a table to display the steps the algorithm took.
        self.table.setHorizontalHeaderLabels(['Page', 'Miss', 'Frames']) # Sets the headers for the table.
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #000000; color: #FFFFFF; }") # Sets the header color to black and the text color to white.
        self.table.horizontalHeader().setFont(QFont("Arial", 10, QFont.Bold)) # Sets the font of the header to Arial, size 10, and bold.
        self.table.verticalHeader().setStyleSheet("QHeaderView::section { background-color: #000000; color: #FFFFFF; }") # Sets the vertical header color to black and the text color to white.
        self.table.verticalHeader().setFont(QFont("Arial", 10, QFont.Bold)) # Sets the font of the vertical header to Arial, size 10, and bold.

        self.frame_label = QLabel('Number of Frames: 3') # Creates a label for the number of frames input.
        self.frame_textbox = QSlider() # Creates a textbox for the number of frames input.
        self.frame_textbox.setOrientation(Qt.Orientation.Horizontal)
        self.frame_textbox.setRange(3, 5) # Sets the range of the slider to only accept integers between 3 and 5.
        self.frame_textbox.setMaximumWidth(200) # Sets the maximum width of the slider to 200 pixels.
        self.frame_textbox.valueChanged.connect(lambda: self.frame_label.setText(f"Number of Frames: {self.frame_textbox.value()}")) # Sets the value of the label to the value of the slider.

        self.ref_len_label = QLabel('Length of Reference String: 20')  # Creates a label for the reference string length input.
        self.ref_len_textbox = QSlider() # Creates a textbox for the reference string length input.
        self.ref_len_textbox.setOrientation(Qt.Orientation.Horizontal) # Sets the orientation of the slider to horizontal.
        self.ref_len_textbox.setRange(20, 100) # Sets the range of the slider to only accept integers between 20 and 100.
        self.ref_len_textbox.valueChanged.connect(lambda: self.ref_len_label.setText(f"Length of Reference String: {self.ref_len_textbox.value()}")) # Sets the value of the label to the value of the slider.

        run_button = QPushButton('Run') # Creates a run button for the algorithm.
        run_button.clicked.connect(self.run) # Connects the run button with its function.

        clear_button = QPushButton('Clear') # Creates a clear button for the algorithm.
        clear_button.clicked.connect(self.clear_fields) # Connects the run button with its function.

        ref_string_label = QLabel('Reference String:') # Creates a label for the generated reference string display.
        self.ref_string_textbox = QTextEdit() # Create a textbox where the generated reference string will be displayed.
        self.ref_string_textbox.setEnabled(False) # Disables the textbox to prevent modifications.

        final_frame_label = QLabel('Final Output:') # Creates a label for the output frames of the algorithm.
        self.final_frame_textbox = QLineEdit() # Creates a textbox for the output frames of the algorithm.
        self.final_frame_textbox.setEnabled(False) # Disables the textbox to prevent modifications.

        miss_count_label = QLabel('Miss Count: ') # Creates a label for the output miss count of the algorithm.
        self.miss_count_textbox = QLineEdit() # Creates a textbox for the output miss count of the algorithm.
        self.miss_count_textbox.setEnabled(False) # Disables the textbox to prevent modifications.

        hit_count_label = QLabel('Hit Count:') # Creates a label for the output hit count of the algorithm.
        self.hit_count_textbox = QLineEdit() # Creates a textbox for the output hit count of the algorithm.
        self.hit_count_textbox.setEnabled(False) # Disables the textbox to prevent modifications.

        miss_percentage_label = QLabel('Miss Percentage') # Creates a label for the output miss percentage of the algorithm.
        self.miss_percentage_textbox = QLineEdit() # Creates a textbox for the output miss percentage of the algorithm.
        self.miss_percentage_textbox.setEnabled(False) # Disables the textbox to prevent modifications.

        results_inner = QVBoxLayout() # Creates a layout where the final output will be displayed
        # Adds the widgets to the layout
        results_inner.addWidget(ref_string_label)
        results_inner.addWidget(self.ref_string_textbox)
        results_inner.addWidget(self.span([final_frame_label, self.final_frame_textbox]))
        results_inner.addWidget(self.span([miss_count_label, self.miss_count_textbox]))
        results_inner.addWidget(self.span([hit_count_label, self.hit_count_textbox]))
        results_inner.addWidget(self.span([miss_percentage_label, self.miss_percentage_textbox]))

        results_inner_wid = QWidget() # Creates the subpanel for the final output
        results_inner_wid.setLayout(results_inner) # Sets the layout for the subpanel

        results = QHBoxLayout() # Creates a layout where the final output and steps will be displayed
        # Adds the widgets to the layout
        results.addWidget(self.table)
        results.addWidget(results_inner_wid)

        results_wid = QWidget() # Creates the subpanel for the results
        results_wid.setLayout(results) # Sets the layout for the subpanel

        layout = QVBoxLayout() # Creates a layout where the entire GUI will be displayed
        # Adds the widgets to the layout
        layout.addWidget(results_wid)
        layout.addWidget(self.frame_label)
        layout.addWidget(self.frame_textbox)
        layout.addWidget(self.ref_len_label)
        layout.addWidget(self.ref_len_textbox)
        layout.addWidget(run_button)
        layout.addWidget(clear_button)

        pane = QWidget() # Creates the main panel where the GUI will be displayed
        pane.setLayout(layout) # Sets the layout for the main panel
        return pane # returns the main panel to the main window

    def span(self, widgets:list) -> QWidget:
        """Creates a horizontal subpanel of the given widgets"""
        widget = QWidget() # Creates the widget to be returned
        layout = QHBoxLayout() # Creates the layout for the widget
        for wid in widgets: # Runs the loop for each widget given and adds it to the layout.
            layout.addWidget(wid)
        widget.setLayout(layout) # Sets the layout for the widget
        return widget # Returns the widget

    def run(self):
        """Runs the algorithm and displays the output to the GUI"""
        ref_len = self.ref_len_textbox.value() # Takes the inputted length for the reference string.
        frame_len = self.frame_textbox.value() # Takes the inputted length for the frames.
        self.clear_fields() # Clears the GUI of any previous inputs.
        self.ref_len_textbox.setValue(ref_len) # Sets the textbox back to its inputted values.
        self.frame_textbox.setValue(frame_len) # Sets the textbox back to its inputted values.
        DATA = optimal(generate_string(ref_len), frame_len) # Runs the optimal page replacement algorithm with the given parameters
        steps:list[dict] = DATA.get("steps") # Takes the steps from the output

        miss_percentage:float = DATA.get("miss")/ref_len*100 # Takes the miss count and calculates the miss percentage
        for i in range(ref_len): # Adds the steps taken to the table to display
            self.addRow(i, steps[i].get("char"), steps[i].get("miss"), steps[i].get("frames"))

        # Displays the output of the algorithm to the texboxes
        self.ref_string_textbox.setText(f"{DATA.get("ref")}")
        self.final_frame_textbox.setText(f"{DATA.get("final")}")
        self.miss_count_textbox.setText(f"{DATA.get("miss")}")
        self.miss_percentage_textbox.setText(f"{miss_percentage:.2f}%")
        self.hit_count_textbox.setText(f"{DATA.get("hit")}")

    def clear_fields(self):
        """Clears the contents of the GUI"""
        self.table.clear() # Clears the table
        while self.table.rowCount() > 0: # removes all the rows
            self.table.removeRow(0)
        self.table.setHorizontalHeaderLabels(['Page', 'Miss', 'Frames']) # Sets the header rows
        self.ref_len_textbox.setValue(20) # Clears the reference length input
        self.frame_textbox.setValue(3) # Clears the frame length input
        self.ref_string_textbox.setText("")
        self.final_frame_textbox.setText("")
        self.miss_count_textbox.setText("")
        self.miss_percentage_textbox.setText("")
        self.hit_count_textbox.setText("")

    def addRow(self, current_row: int, page: str, miss: bool, frames: list):
        """Adds a row to the table"""
        self.table.insertRow(current_row)
        self.table.setItem(current_row, 0, QTableWidgetItem(f"{page}"))
        self.table.setItem(current_row, 1, QTableWidgetItem(f"{miss}"))
        self.table.setItem(current_row, 2, QTableWidgetItem(f"{frames}"))

if __name__ == "__main__":
    # Starts the GUI
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()