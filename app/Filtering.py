# For this part of the assignment, You can use inbuilt functions to compute the fourier transform
# You are welcome to use fft that are available in numpy and opencv
import numpy as np
import math as math

class Filtering:
    image = None
    filter = None
    cutoff = None
    order = None

    def __init__(self, image, filter_name, cutoff, order=0):

        self.image = image
        if filter_name == 'ideal_l':
            self.filter = self.get_ideal_low_pass_filter
        elif filter_name == 'ideal_h':
            self.filter = self.get_ideal_high_pass_filter
        elif filter_name == 'butterworth_l':
            self.filter = self.get_butterworth_low_pass_filter
        elif filter_name == 'butterworth_h':
            self.filter = self.get_butterworth_high_pass_filter
        elif filter_name == 'gaussian_l':
            self.filter = self.get_gaussian_low_pass_filter
        elif filter_name == 'gaussian_h':
            self.filter = self.get_gaussian_high_pass_filter

        self.cutoff = cutoff
        self.order = order


    def get_ideal_low_pass_filter(self, shape, cutoff):

        (p, q) = shape
        mask = np.array([[1 if math.sqrt(math.pow((u - (p / 2)), 2) + math.pow((v - (q / 2)), 2)) <= cutoff else 0 for v in range(q)] for u in range(p)])
        return mask


    def get_ideal_high_pass_filter(self, shape, cutoff):

        mask = 1 - self.get_ideal_low_pass_filter(shape, cutoff)
        return mask

    def get_butterworth_low_pass_filter(self, shape, cutoff, order):

        (p, q) = shape
        mask = np.array([[(1 / (1 + math.pow((math.sqrt(math.pow((u - (p / 2)), 2) + math.pow((v - (q / 2)), 2))/cutoff), 2 * order))) for v in range(q)] for u in range(p)])

        return mask

    def get_butterworth_high_pass_filter(self, shape, cutoff, order):

        mask = 1 - self.get_butterworth_low_pass_filter(shape, cutoff, order)
        return mask

    def get_gaussian_low_pass_filter(self, shape, cutoff):

        (p, q) = shape
        mask = np.array([[math.exp(-1 * (math.pow(math.sqrt(math.pow((u - (p / 2)), 2) + math.pow((v - (q / 2)), 2)), 2)/(2 * math.pow(cutoff, 2)))) for v in range(q)] for u in range(p)])
        return mask

    def get_gaussian_high_pass_filter(self, shape, cutoff):

        mask = 1 - self.get_gaussian_low_pass_filter(shape, cutoff)
        return mask

    def post_process_image(self, image):

        min_gray_level = np.min(image)
        max_gray_level = np.max(image)
        (h, w) = image.shape

        fsimage = np.array([[(((255 - 1) / (max_gray_level - min_gray_level)) * (image[i][j] - min_gray_level)) for j in range(w)] for i in range(h)], dtype=np.uint8)

        return fsimage


    def filtering(self):

        if self.order > 0:
            mask = self.filter(self.image.shape, self.cutoff, self.order)
        else:
            mask = self.filter(self.image.shape, self.cutoff)

        image_fft = np.fft.fft2(self.image)
        shifted_fft = np.fft.fftshift(image_fft)
        compressed_fft = np.uint8(np.log(np.absolute(shifted_fft)) * 10)

        filtered_dft = shifted_fft * mask
        compressed_filtered_fft = np.uint8(np.log(np.absolute(filtered_dft)) * 10)

        inverse_shift = np.fft.ifftshift(filtered_dft)
        inverse_fft = np.fft.ifft2(inverse_shift)
        magnitude = np.absolute(inverse_fft)
        fsimage = self.post_process_image(magnitude)

        return [fsimage, compressed_fft, compressed_filtered_fft]
