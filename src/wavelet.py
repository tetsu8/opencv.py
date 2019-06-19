import numpy as np
import cv2
import copy
import math
import waveletfilter

class ComplexWavelet:
    @staticmethod
    def analysis(img: np.ndarray , n: int, length: int):
        print('Call ComplexWavelet.analysis(img = {}, n = {}, length = {})'.format(img.shape,n,length))
        nx, ny = img.shape

        outRe = copy.copy(img)
        outIm = copy.copy(img)

        re = 0
        im = 1

        subre = np.zeros((2, nx * ny))
        sub1 = np.zeros((2, nx * ny))
        sub2 = np.zeros((2, nx * ny))

        # copy
        subre = copy.copy(outRe)

        print('#1 split')
        sub1 = ComplexWavelet.split(subre, re, re, length)
        sub2 = ComplexWavelet.split(subre, im, im, length)

        # subtract sub2 from sub1
        cv2.subtract(sub1, sub2, sub1)

        outRe = copy.copy(sub1)

        print('#2 split')
        sub1 = ComplexWavelet.split(subre, re, im, length)
        sub2 = ComplexWavelet.split(subre, im, re, length)

        cv2.add(sub1, sub2, sub1)

        outRe = copy.copy(sub1)

        nx /= 2
        ny /= 2

        print('#3 split')
        for i in range(1,n):
            subre = copy.copy(outRe)
            subim = copy.copy(outIm)

            sub1 = ComplexWavelet.split(subre, re, re, length)
            sub2 = ComplexWavelet.split(subre, im, im, length)
            sub3 = ComplexWavelet.split(subim, re, re, length)
            sub4 = ComplexWavelet.split(subim, im, im, length)

            cv2.subtract(sub1, sub2, sub1)
            cv2.subtract(sub1, sub3, sub1)
            cv2.subtract(sub1, sub4, sub1)

            outRe = copy.copy(sub1)

            sub1 = ComplexWavelet.split(subre, re, im, length)
            sub2 = ComplexWavelet.split(subre, im, re, length)
            sub3 = ComplexWavelet.split(subre, re, im, length)
            sub4 = ComplexWavelet.split(subre, im, re, length)

            cv2.add(sub1, sub2, sub1)
            cv2.add(sub1, sub3, sub1)
            cv2.subtract(sub1, sub4, sub1)

            outIm = copy.copy(sub1)

            nx /= 2
            ny /= 2

        outComplex = [outRe, outIm]
        return outComplex

    @staticmethod
    def synthesis(inRe: np.ndarray, inIm: np.ndarray, n: int, length: int):
        div = math.pow(2.0, float(n-1))
        nxcoarse = inRe.shape[0] / div
        nycoarse = inRe.shape[1] / div

        outRe = copy.copy(inRe)
        outIm = copy.copy(inIm)

        re, im = 0, 1

        for i in range(n):
            subre = copy.copy(outRe)
            subim = copy.copy(outIm)

            sub1 = ComplexWavelet.merge(subre, re, re, length)
            sub2 = ComplexWavelet.merge(subre, im, im, length)
            sub3 = ComplexWavelet.merge(subim, re, re, length)
            sub4 = ComplexWavelet.merge(subim, im, im, length)

            cv2.subtract(sub1, sub2, sub1)
            cv2.add(sub1, sub3, sub1)
            cv2.add(sub1, sub4, sub1)

            outRe = copy.copy(sub1)

            sub1 = ComplexWavelet.merge(subre, re, im, length)
            sub2 = ComplexWavelet.merge(subre, im, re, length)
            sub3 = ComplexWavelet.merge(subim, re, im, length)
            sub4 = ComplexWavelet.merge(subim, im, re, length)

            cv2.subtract(sub3, sub1, sub3)
            cv2.subtract(sub3, sub2, sub3)
            cv2.subtract(sub3, sub4, sub3)

            outIm = copy.copy(sub3)

            nx *= 2
            ny *= 2

        return [outRe, outIm]


    @staticmethod
    def split(img: np.ndarray, type1: int, type2: int, length: int) -> np.ndarray:
        print('Call ComplexWavelet.split(img = {}, type1 = {}, type2 = {}, length = {})'.format(img,type1,type2,length))
        nx, ny = img.shape
        #print('split() img shape nx={}, ny={}'.format(nx,ny))
        out = np.zeros((nx, ny))
        #print('split out initialize = {}'.format(out))

        wf = waveletfilter.Filter(length)

        print('start process split1D() row')
        if nx >= 1:
        #if False:
            rowi = [0.0] * nx
            rowo = [0.0] * nx
            for y in range(ny):
                rowi = img[y,:]
                if type1 == 0:
                    rowo = ComplexWavelet.split1D(rowi, wf.h, wf.g)
                elif type1 == 1:
                    rowo = ComplexWavelet.split1D(rowi, wf.hi, wf.gi)
                #print('Call split1D y={}, rowo={}'.format(y, rowo))
                out = np.insert(out, y, rowo, axis=0)
                out = np.delete(out, y+1, axis=0)
                #print('row info out shape={}, row len={}, count={}'.format(out.shape, len(rowo), y))
                #out = ComplexWavelet.replaceArray(out, rowo, y, 0)
        else:
            out = copy.copy(img)
        print('end process split1D() row')

        print('start process split1D() col')
        if ny > 1:
            coli = [0.0] * ny
            colo = [0.0] * ny
            for x in range(nx):
                coli = img[:,x]
                if type2 == 0:
                    colo = ComplexWavelet.split1D(coli, wf.h, wf.g)
                elif type2 == 1:
                    colo = ComplexWavelet.split1D(coli, wf.hi, wf.gi)
                #print('Call split1D x={}, colo={}'.format(x,colo))
                #print('col info out shape={}, colo len={}, count={}'.format(out.shape, len(colo), x))
                out = np.insert(out, x, colo, axis=1)
                out = np.delete(out, x, axis = 1)
                #out = ComplexWavelet.replaceArray(out, colo, x, 1)
        print('end process split1D() col')

        return out

    @staticmethod
    def split1D(valin: list, h: list, g: list):
        n = len(valin)
        valout = [0.0] * n
        n2 = int(n / 2)
        nh = len(h)
        ng = len(g)

        voutL = [0.0] * n
        voutH = [0.0] * n

        for i in range(n):
            pix = 0.0
            for k in range(nh):
                j1 = i + k - (nh / 2)
                if j1 < 0:
                    while j1 < n:
                        j1 += n
                    j1 %= n
                elif j1 >= n:
                    j1 %= n

                #print('valin = {}, len = {}, index = {}'.format(valin, len(valin), j1))
                #print('h[] = {}, index_k = {}'.format(h,k))
                pix = pix + h[k] * valin[int(j1)]

            voutL[i] = pix

        for i in range(n):
            pix = 0.0
            for k in range(ng):
                j1 = i + k - (ng / 2)
                if j1 < 0:
                    while j1 < n:
                        j1 += n
                    j1 %= n
                elif j1 >= n:
                    j1 %= n

                pix = pix + g[k] * valin[int(j1)]

            voutH[i] = pix

        for k in range(n2):
            valout[k] = voutL[2*k]
        for k in range(n2, n):
            valout[k] = voutH[2*k-n]

        return valout

    @staticmethod
    def merge(img: np.ndarray, type1: int, type2: int, length: int) -> np.ndarray:
        nx, ny = img.shape
        out = np.zeros((nx, ny))
        wf = waveletfilter.Filter(length)

        if nx >= 1:
            for y in range(ny):
                rowin = img[y,:]
                rowout = np.zeros((1,nx))

                if type1 == 0:
                    rowout = ComplexWavelet.merge1D(rowi, wf.h, wf.g)
                elif type1 == 1:
                    rowout = ComplexWavelet.merge1D(rowi, wf.hi, wf.gi)

                out = np.insert(out, y, rowout, axis=0)
                out = np.delete(out, y+1, axis=0)
        else:
            out = copy.copy(img)

        if ny > 1:
            colout = np.zeros((1,ny))
            for x in range(nx):
                colin = img[:,x]

                if type2 == 0:
                    colo = ComplexWavelet.merge1D(coli, wf.h, wf.g)
                elif type2 == 1:
                    colo = ComplexWavelet.merge1D(coli, wf.hi, wf.gi)

                out = np.insert(out, x, colout, axis=1)
                out = np.delete(out, x+1, axis=1)

        return out

    @staticmethod
    def merge1D(valin: list, h: list, g: list) -> list:
        n = len(valin)
        valout = [0.0] * n
        n2 = int(n / 2)
        nh = len(h)
        ng = len(g)

        vinL = [0.0] * n
        vinH = [0.0] * n

        for k in range(n2):
            vinL[2*k] = valin[k]
            vinH[2*k] = valin[k + n2]

        for i in range(n):
            pix = 0.0
            for k in range(nh):
                j1 = i - k + (nh / 2)
                if j1 < 0:
                    while j1 < n:
                        j1 += n
                    j1 %= n
                elif j1 >= n:
                    j1 %= n

                pix = pix + h[k] * vinL[int(j1)]

            vout[i] = pix

        for i in range(n):
            pix = 0.0
            for k in range(ng):
                j1 = i - k + (ng / 2)
                if j1 < 0:
                    while j1 < n:
                        j1 += n
                    j1 %= n
                elif j1 >= n:
                    j1 %= n

                pix += g[k] * vinH[int(j1)]

            vout[i] += pix

        return vout

    @staticmethod
    def replaceArray(inlist: np.ndarray, val, index: int, axis: int=0) -> np.ndarray:
        if axis == 0:
            y = index
            tmp1 = np.insert(inlist, y, val, axis=0)
            outlist = np.delete(tmp1, y+1, axis=0)
        elif axis == 1:
            x = index
            tmp1 = np.insert(inlist, x, val, axis=1)
            outlist = np.delete(tmp1, x+1, axis=1)

        return outlist
