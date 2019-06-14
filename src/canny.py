import cv2 as cv
import tkinter,tkinter.filedialog,tkinter.messagebox,os
from matplotlib import pyplot as plt
from PIL import Image, ImageTk
import numpy as np

class Application(tkinter.Frame):

    def __init__(self,master=None):
        super().__init__(master)
        if master is not None:
            self.tkRoot = master

        self.img = None

        self.grid(column=0, row=0, sticky=(tkinter.N, tkinter.S, tkinter.E, tkinter.W))
        self.create_widgets()

    def create_widgets(self):
        # コントロール定義
        imgLab = tkinter.Label(self, text="画像")

        self.pathText = tkinter.StringVar()
        pathBox = tkinter.Entry(self, textvariable=self.pathText)

        selectBtn = tkinter.Button(self)
        selectBtn["text"] = "browse..."
        selectBtn["command"] = self.selectImg

        openBtn = tkinter.Button(self)
        openBtn["text"] = "Open"
        openBtn["command"] = self.openImg

        autoBtn = tkinter.Button(self)
        autoBtn["text"] = "Auto Tune"
        autoBtn["command"] = self.calcThresh

        self.minVal = tkinter.IntVar()
        self.minVal.set(0)
        self.minVal.trace('w', self.valueChanged)
        self.maxVal = tkinter.IntVar()
        self.maxVal.trace('w', self.valueChanged)
        self.maxVal.set(255)
        minSlider = tkinter.Scale(self, label="Min Threshold", orient='horizontal', from_=0, to=255, variable=self.minVal)
        maxSlider = tkinter.Scale(self, label="Max Threshold", orient='horizontal', from_=0, to=255, variable=self.maxVal)

        # コントロール配置
        selectBtn.grid(row=1, column=1, padx=5, pady=5)
        imgLab.grid(row=0,column=0)
        pathBox.grid(row=1, column=0)
        openBtn.grid(row=1, column=2)
        autoBtn.grid(row=1, column=3)
        minSlider.grid(row=2, column=0, columnspan=3)
        maxSlider.grid(row=2, column=3, columnspan=3)

    # ファイル選択ダイアログ
    def selectImg(self):
        root = tkinter.Tk()
        root.withdraw()
        fType = [("",".png")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        self.file = tkinter.filedialog.askopenfilename(filetypes = fType,initialdir = iDir)
        self.pathText.set(self.file)
        self.openImg()

    # ファイルオープン
    def openImg(self):
        self.img = cv.imread(self.pathText.get(), cv.IMREAD_GRAYSCALE)
        cImg = self.canny()
        #cv.imshow('', img)
        #cv.waitKey(0)
        #cv.destroyAllWindows()
        pilImg = Image.fromarray(cImg)
        self.tkImg = ImageTk.PhotoImage(pilImg)

        canvas = tkinter.Canvas(self, width=self.img.shape[0], height=self.img.shape[1])
        canvas.grid(row=4, rowspan=4, column=0, columnspan=6)
        canvas.create_image(0, 0, image=self.tkImg, anchor='nw')

    # CannyEdge検出
    def canny(self):
        cannyImg = cv.Canny(self.img, self.minVal.get(), self.maxVal.get())
        return cannyImg

    def calcThresh(self):
        tmp = self.img
        median = np.median(tmp)
        self.minVal.set(median * 0.66)
        self.maxVal.set(median * 1.33)

    def valueChanged(self, *args):
        if self.img is not None:
            print('call valueChanged')
            self.openImg()

root = tkinter.Tk()
root.title("canny edge")
root.geometry("800x600")
app = Application(master = root)

app.mainloop()
