#!/usr/bin/env python3


class DcmRead:

    def __init__(self, path):
        self.path = path
        
        from pydicom import dcmread

        ds = dcmread(self.path)
        
        self.original = ds.pixel_array
        self.ipp = ds.ImagePositionPatient

    def __eq__(self, other):
        return self.ipp == other.ipp
    


class DcmFilter(DcmRead):

    def __init__(self, path, sigma):

        DcmRead.__init__(self, path)
        
        if sigma is not None:
            self.sigma = sigma
        else:
            self.sigma = 3

        from scipy.ndimage import gaussian_filter

        self.filtered = gaussian_filter(self.original, self.sigma)


class DcmRotate(DcmRead):

    def __init__(self, path, angle):

        DcmRead.__init__(self, path)
        
        if angle is not None:
            self.angle = angle
        else:
            self.angle = 180

        from numpy import rot90

        self.rotated = rot90(self.original, round(self.angle / 90.))
        
        
def check_ipp(dcm1, dcm2):

    return dcm1.ipp==dcm2.ipp



