import nibabel as nib
import numpy as np 
from utils_masking import *
'''s
This script takes in the CT image, and the contour of the bed which the patient is lying on 
and created a nan mask, for the registration preprocessing

'''

CT_img_path = 'CT_20151217.nii.gz'
Couch_mask_path = 'BIN_COUCH.nii.gz'
Body_mask_path = 'BIN_BODY.nii.gz'
mask_path = 'MASK.nii.gz'
masked_CT_path = 'MASKED_CT_20151217.nii.gz'

# creates the mask first 
create_mask(Couch_mask_path, Body_mask_path, mask_path)

# masks the image 
mask_img(CT_img_path, mask_path, masked_CT_path, masking_value = np.NaN)