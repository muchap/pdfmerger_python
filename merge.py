from tkinter import Tk, Frame, Button,LabelFrame, Label, W, E, N, S, filedialog
from tkinter.messagebox import showerror
from PyPDF2 import PdfFileMerger
import os

class Display:
	def __init__(self):
		self.root = Tk()
		self.root.columnconfigure((0,1), weight=1) # Set weight to row and
		self.root.rowconfigure((1), weight=1)  # column where the widget is

		self.root.minsize(320,160)
		self.root.title("PDF Merger v0.1")

		self.filenamesopen = []

		self.button = Button(self.root, text="Choose files", command=self.load_files, width=20, height=2)
		self.button.grid(row=0, column=0, padx=0, pady=7, sticky=N)
		self.button = Button(self.root, text="Merge", command=self.merge_files, width=20, height=2)
		self.button.grid(row=0, column=1, padx=0, pady=7, sticky=N)

		self.labelframe = LabelFrame(self.root, text="Files to merge:")
		self.labelframe.grid(columnspan=2,padx=10, pady=(0,10), sticky=W+E+N+S)
		self.left = Label(self.labelframe, text="",  justify="left", anchor=N+W) #width=41, height=5,
		self.left.grid()

		self.root.mainloop()

	def load_files(self):
		try:
			self.filenamesopen = filedialog.askopenfilenames(initialdir="/", title="Choose files to merge...",
															 filetypes=(("pdf", "*.pdf"), ("All files", "*.*")))
			filenames = [os.path.split(file)[1] for file in self.filenamesopen]
			extensions = [os.path.splitext(file)[1] for file in self.filenamesopen]
			if not all(p == ".pdf" for p in extensions):
				raise
			self.left.configure(text="\n".join(filenames))
		except:
			showerror("Open Source File", "Failed to read files!\nUnknown file format, empty/damaged file or file not found!")

	def merge_files(self):
		self.merger = PdfFileMerger()
		try:
			for pdf in self.filenamesopen:
				self.merger.append(open(pdf, 'rb'), import_bookmarks=False)
		except:
			showerror("Merger Error", "Failed to merge files\n")
			return
		self.save_files()

	def save_files(self):
		try:
			self.filenamesave = filedialog.asksaveasfilename(initialdir="/", title="Save as...",
															 filetypes=(("pdf", "*.pdf"), ("All files", "*.*")),
															 defaultextension=".pdf")
			extension = os.path.splitext(self.filenamesave)[1]
			if not ".pdf" in extension:
				raise
			with open(self.filenamesave, 'wb') as fout:
				self.merger.write(fout)
		except:
			showerror("Save Source File", "Failed to save file!\n")

if __name__ == "__main__":
	display = Display()