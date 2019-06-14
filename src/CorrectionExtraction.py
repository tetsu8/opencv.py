import cv2 as cv
import tkinter,tkinter.filedialog,tkinter.messagebox,os
from matplotlib import pyplot as plt
from PIL import Image

class Application(tkinter.Frame):

    def __init__(self,master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tkinter.Button(self)
        self.hi_there["text"] = "選択"
        self.hi_there["command"] = self.selectImg
        self.hi_there.pack(side="left")

    def selectImg(self):
        root = tkinter.Tk()
        root.withdraw()
        fType = [("",".png")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        self.file = tkinter.filedialog.askopenfilename(filetypes = fType,initialdir = iDir)


    def adThreshold(self):
        img = cv.imread("bv02.png",0)
        #gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        #cv.imshow('org',img)
        #cv.waitKey(0)

        ellepse_kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(20,20))
        rect_kernel = cv.getStructuringElement(cv.MORPH_RECT,(25,25))

        #fg = cv.morphologyEx(img, cv.MORPH_OPEN, rect_kernel)
        fg = cv.morphologyEx(img, cv.MORPH_OPEN, rect_kernel)

        #cv.imshow('fg', fg)
        #cv.waitKey(0)

        bg = cv.absdiff(img, fg)
        #cv.imshow('bg', bg)
        #cv.waitKey(0)


        #ret = cv.adaptiveThreshold(bg,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,551,5)
        ret = cv.adaptiveThreshold(bg,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,651,5)
        #cv.imwrite('AdaptiveThreshold_sample_2.png', ret)

        #cv.imshow('ret',ret)
        #cv.waitKey(0)
        plt.subplot(121),plt.imshow(img,cmap = 'gray')
        plt.title('org'), plt.xticks([]), plt.yticks([])
        #plt.subplot(142),plt.imshow(fg,cmap = 'gray')
        #plt.title('fg'), plt.xticks([]), plt.yticks([])
        #plt.subplot(143),plt.imshow(bg,cmap = 'gray')
        #plt.title('bg'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(ret,cmap = 'gray')
        plt.title('AdaptiveThreshold'), plt.xticks([]), plt.yticks([])

        plt.show()



root = tkinter.Tk()
root.title("adThreshold test")
root.geometry("500x500")
app = Application(master = root)

app.mainloop()

