from math import exp

import cv2
import numpy as np

__all__ = ('YoloV3TinyParser', )


def overlapped_ratio(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b

    ax2 = ax + aw
    ay2 = ay + ah

    bx2 = bx + bw
    by2 = by + bh

    ix = max(0, min(ax2, bx2) - max(ax, bx))
    iy = max(0, min(ay2, by2) - max(ay, by))

    sa = (ay2 - ay) * (ax2 - ax)
    sb = (by2 - by) * (bx2 - bx)
    si = ix * iy

    su = sa + sb - si
    return max(0, si / su)


class Layer:
    __slots__ = 'loc', 'row', 'col', 'n', 'nwh', 'w', 'h', 'wh', 'output'

    def __init__(self, output):
        self.loc = self.row = self.col = self.n = self.nwh = -1
        self.w, self.h = output.shape[-2:]
        self.wh = self.w * self.h
        self.output = output.flatten()


class YoloV3TinyParser:
    def __init__(self,
                 frame_size,
                 input_size,
                 classes=1,
                 anchors=(10, 14, 23, 27, 37, 58, 81, 82, 135, 169, 344, 319),
                 threshold=.3):
        fw, fh = frame_size
        iw, ih = input_size
        self.input_size = input_size
        self.frame_scale = (fw / iw, fh / ih)
        self.classes = classes
        self.anchors = anchors
        self.threshold = threshold

    def reshape_input(self, frame):
        nchw = cv2.resize(frame,
                          self.input_size,
                          interpolation=cv2.INTER_NEAREST)
        nchw = nchw[np.newaxis, :, :, :]  # HWC to NHWC
        return nchw.transpose((0, 3, 1, 2))  # NHWC to NCHW

    def parse_output(self, output):
        return self.cleanup_results(self.get_yolo_detections(Layer(output)))

    # int get_yolo_detections(l, w, h, netw, neth, thresh, *map, relative, *dets)
    def get_yolo_detections(self, l):
        results = []
        iw, ih = self.input_size

        for i in range(l.wh):
            l.loc = i
            l.row = i // l.h
            l.col = i % l.w
            for n in range(3):
                l.n = n
                l.nwh = n * l.wh

                # int obj_index  = entry_index(l, 0, n*l.w*l.h + i, 4);
                obj_index = self.entry_index(l, 4)
                objectness = l.output[obj_index]
                if objectness < self.threshold:
                    continue

                # int box_index  = entry_index(l, 0, n*l.w*l.h + i, 0);
                box_index = self.entry_index(l, 0)
                box_position = self.get_yolo_box(box_index, l)

                for j in range(self.classes):
                    # int class_index = entry_index(l, 0, n*l.w*l.h + i, 4 + 1 + j);
                    class_index = self.entry_index(l, 5 + j)
                    prob = objectness * l.output[class_index]
                    if prob < self.threshold:
                        continue

                    results.append(
                        (j, prob, self.original_position(*box_position)))

        return results

    # int entry_index(l, batch, location, entry)
    def entry_index(self, l, entry):
        return l.nwh * (5 + self.classes) + entry * l.wh + l.loc

    # box get_yolo_box(*x, *biases, n, index, i, j, lw, lh, w, h, stride)
    def get_yolo_box(self, index, l):
        offset = 2 * 3 if l.w == 13 else 0
        anchors = self.anchors

        x = (l.col + l.output[index + 0 * l.wh]) / l.w * self.input_size[0]
        y = (l.row + l.output[index + 1 * l.wh]) / l.h * self.input_size[1]
        w = exp(l.output[index + 2 * l.wh]) * anchors[offset + 2 * l.n]
        h = exp(l.output[index + 3 * l.wh]) * anchors[offset + 2 * l.n + 1]

        return x, y, w, h

    def cleanup_results(self, results):
        trashs = set()

        for i, curr in enumerate(results):
            for j, result in enumerate(results[i + 1:]):
                if overlapped_ratio(curr[2], result[2]) < .5:
                    continue

                if curr[1] < result[1]:
                    results[i], results[j] = results[j], results[i]

                trashs.add(result)

        return list(filter(lambda x: x not in trashs, results))

    def original_position(self, x, y, w, h):
        x, y = x - w // 2, y - h // 2
        ws, hs = self.frame_scale
        return int(x * ws), int(y * hs), int(w * ws), int(h * hs)
