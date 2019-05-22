import sys
sys.path.append("../..")
import tkinter as tk
import tkinter.filedialog
from MyCrypto.aes.block_cipher import AES_block

class UI:
    
    def __init__(self):
        self.filename = None
        self.mode = None
        ''' UI '''
        self.root = tk.Tk()
        self.mainFrame = tk.Frame(self.root)
        ''' TOP '''
        self.topFrame = tk.Frame(self.mainFrame)
        ''' LEFT TOP '''
        self.leftTopFrame = tk.LabelFrame(self.topFrame, text='Method')
        self.method = tk.StringVar()
        self.method.set('encrypt')
        self.encryptRadio = tk.Radiobutton(self.leftTopFrame, text='Encrypt', variable=self.method, value='encrypt', indicatoron=0)
        self.encryptRadio.grid(row=0, column=0)
        self.decryptRadio = tk.Radiobutton(self.leftTopFrame, text='Decrypt', variable=self.method, value='decrypt', indicatoron=0)
        self.decryptRadio.grid(row=0, column=1)
        self.leftTopFrame.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
        ''' LEFT TOP END '''
        ''' LEFT DOWN '''
        self.leftDownFrame = tk.LabelFrame(self.topFrame, text='Mode')
        modes = ('ECB', 'CBC', 'CFB')
        self.modeList = tk.Listbox(self.leftDownFrame, height=len(modes), width=15, selectmode=tk.SINGLE, listvariable=tk.StringVar(value=modes))
        self.modeList.grid(row=0, column=0)
        self.leftDownFrame.grid(row=1, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
        ''' LEFT DOWN END '''
        ''' RIGHT TOP '''
        self.rightTopFrame = tk.LabelFrame(self.topFrame, text='Parameters')
        tk.Label(self.rightTopFrame, text='Key').grid(row=0, column=0, sticky=tk.E)
        self.keyEntry = tk.Entry(self.rightTopFrame)
        self.keyEntry.grid(row=0, column=1)
        tk.Label(self.rightTopFrame, text='IV').grid(row=1, column=0, sticky=tk.E)
        self.ivEntry = tk.Entry(self.rightTopFrame)
        self.ivEntry.grid(row=1, column=1)
        self.rightTopFrame.grid(row=0, column=1, sticky=tk.E+tk.W+tk.N+tk.S)
        ''' RIGHT TOP END '''
        ''' RIGHT DOWN '''
        self.rightDownFrame = tk.LabelFrame(self.topFrame, text='Input File')
        tk.Button(self.rightDownFrame, text='Choose File', command=self.chooseFile).grid(row=0, sticky=tk.W)
        self.fileLabel = tk.Label(self.rightDownFrame, text='No file')
        self.fileLabel.grid(row=1, sticky=tk.W)
        self.rightDownFrame.grid(row=1, column=1, sticky=tk.E+tk.W+tk.N+tk.S)
        ''' RIGHT DOWN END '''
        self.topFrame.grid(row=0, sticky=tk.E+tk.W)
        ''' TOP END '''
        tk.Button(self.mainFrame, text='Run', command=self.run).grid(row=1)
        self.statusLabel = tk.Label(self.mainFrame, text='Ready')
        self.statusLabel.grid(row=2, sticky=tk.W)
        ''' DOWN END '''
        self.mainFrame.grid()
        self.root.title('My cipher')
    
    def chooseFile(self):
        filename = tkinter.filedialog.askopenfilename()
        if filename != '':
            self.fileLabel.config(text=filename)
            self.filename = filename
    
    def run(self):
        key = self.keyEntry.get()
        if key == '':
            self.statusLabel.config(text='No key!')
            return
        else:
            key = int(key, 16)
        iv = self.ivEntry.get()
        if iv == '':
            self.statusLabel.config(text='No initial vector!')
            return
        else:
            iv = int(iv, 16)
        if not self.modeList.curselection():
            self.statusLabel.config(text='Please choose a mode!')
            return
        else:
            self.mode = self.modeList.get(self.modeList.curselection()).lower()
        if not self.filename:
            self.statusLabel.config(text='Please choose a file!')
            return
        method = self.method.get()
        self.statusLabel.config(text='Running...')
        aes_block = AES_block(key, mode=self.mode, iv=iv)
        aes_block.from_file(self.filename, method=method)
        self.statusLabel.config(text='Completed!')
    
    def mainloop(self):
        self.root.mainloop()

if __name__ == '__main__':
    UI().mainloop()
