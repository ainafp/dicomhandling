from dicomhandling import DcmFilter

path = '.'
sigma = 3

dcm_filter = DcmFilter(path, sigma)

# dcm_filter.original should contain the NumPy array with the original image
# dcm_filter.filtered should contain the NumPy array with the filtered image
# dcm_filter.ipp should store the 3 item list containing the ImagePositionPatient


