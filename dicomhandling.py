#!/usr/bin/env python3

import sys
import os
import os.path as op
import glob
import matplotlib.pyplot as plt

from pydicom import dcmread
from scipy.ndimage import gaussian_filter
from numpy import rot90



class DcmRead:
    """Read dicom image and save ipp"""

    def __init__(self, path):
        self.path = path
        
        ds = dcmread(self.path)

        self.original = ds.pixel_array
        self.ipp = ds.ImagePositionPatient

    def __eq__(self, other):
        return self.ipp == other.ipp
    


class DcmFilter(DcmRead):
    """Filter image with Gaussian filter"""

    def __init__(self, path, sigma):

        DcmRead.__init__(self, path)
        
        if sigma is not None:
            self.sigma = sigma
        else:
            self.sigma = 3

        self.filtered = gaussian_filter(self.original, self.sigma)


class DcmRotate(DcmRead):
    """Rotate image an angle multiple of 90"""

    def __init__(self, path, angle):

        DcmRead.__init__(self, path)
        
        if angle is not None:
            self.angle = angle
        else:
            self.angle = 180

        self.rotated = rot90(self.original, round(self.angle / 90.))
        
        
def check_ipp(dcm1, dcm2):
    """Check if they are the same image"""
    return dcm1.ipp==dcm2.ipp



class Error(Exception):
    """Base class for other exceptions"""
    pass


class SameImagePositionPatient(Error):
    pass


class IncorrectNumberOfImages(Error):
    pass




sigma = 3 
# sigma could be also passed as an argument


def main(argv):

    path = argv[0]
    images = [im for im in glob.glob(op.join(path, '*')) if not os.path.isdir(im)]

    if len(images)==2 and images[0].lower().endswith('.dcm') and images[1].lower().endswith('.dcm'):

        print('Loading images...')
        dcm1 = DcmRead(images[0])
        dcm2 = DcmRead(images[1])
        same_ipp = check_ipp(dcm1, dcm2)

        if not same_ipp:
            
            print('Filtering images with sigma', sigma, '...')
            dcm1_filter = DcmFilter(images[0], sigma)
            dcm2_filter = DcmFilter(images[1], sigma)

            print('Generating residu images...')
            unfilt_residu = dcm1_filter.original - dcm2_filter.original
            filt_residu = dcm1_filter.filtered - dcm2_filter.filtered

            print('Creating residu folder...')
            folder_residus = op.join(path, 'residus')
            if not op.exists(folder_residus):
                os.makedirs(folder_residus)

            print('Saving unfiltered residu image...')
            plt.figure()
            plt.imshow(unfilt_residu)
            plt.savefig(op.join(folder_residus, "unfiltered_residu.jpg"))
            
            print('Saving filtered residu image...')
            plt.figure()
            plt.imshow(filt_residu)
            plt.savefig(op.join(folder_residus, "filtered_residu.jpg"))
            
        else:

            raise SameImagePositionPatient("The DICOM files appear to be the same. Aborting.")
        
    else:
        
        raise IncorrectNumberOfImages("Incorrect number of images. Aborting.")
        # This also raises in case the extension is not correct. 
        # I would also raise a different exception for this case.
    

if __name__ == "__main__":
    main(sys.argv[1:])
