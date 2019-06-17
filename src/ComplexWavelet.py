import numpy as np
import copy

class ComplexWavelet:
    def analysis(img: ndarray , n: int, length: int):
        nx, ny = img.shape

        outRe = copy.copy(img)
        outIm = copy.copy(img)

        re = 0
        im = 1

    def split(img: ndarray, type1: int, type2: int, length: int) -> ndarray:
        nx, ny = img.shape
        out = np.zeros(nx*ny)

        if nx >= 1:
            rowi = [0.0] * nx
            rowo = [0.0] * nx
            for y in ny:
                rowi = img[y,;]
                if type1 == 0:
                    split1D()
                elif type1 == 1:
                    split1D()
                out = np.insert(out, y, rowo)
        elif:
            out = copy.copy(img)

        if ny > 1:
            coli = [0.0] * ny
            colo = [0.0] * ny
            for x in nx:
                coli = img[;,x]
                if type2 == 0:
                    split1D()
                elif
                    split1D()
                out = np.insert(out, x, colo, axis=1)

        return out



