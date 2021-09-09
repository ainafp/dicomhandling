from dicomhandling import DcmRotate

path = '.'
angle = 270

dcm_rotate = DcmRotate (path, angle)

# dcm_rotate.original should contain the NumPy array with the original image
# dcm_rotate.rotated should contain the NumPy array with the rotated image
# dcm_rotate.ipp should store the 3 item list containing the ImagePositionPatient


