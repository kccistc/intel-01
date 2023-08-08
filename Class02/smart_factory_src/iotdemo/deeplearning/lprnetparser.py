import cv2
import numpy as np

__all__ = ('LPRNetParser', )


class LPRNetParser:
    def __init__(self, input_size, code_table=None):
        self.input_size = input_size
        self.code_table = code_table
        if code_table is None:
            self.code_table = [
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "배", "다",
                "호", "마", "라", "러", "A", "B", "C", "D", "E", "F", "G", "H",
                "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                "U", "V", "W", "X", "Y", "Z", "_", ""
            ]

    def reshape_input(self, frame):
        nchw = cv2.resize(frame,
                          self.input_size,
                          interpolation=cv2.INTER_NEAREST)
        nchw = nchw[np.newaxis, :, :, :]  # HWC to NHWC
        return nchw.transpose((0, 3, 1, 2))  # NHWC to NCHW

    def parse_output(self, output):
        code_table = self.code_table
        results = []

        for key in output[0]:
            if key < 0:
                break

            results.append(code_table[key])

        return ''.join(results)
