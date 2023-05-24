import nibabel as nib
import numpy as np 

'''
This script takes in the CT image, and the contour of the bed which the patient is lying on 
and created a nan mask, for the registration preprocessing

'''

couch_path = ''
CT_path = ''

NiftiCTObj = nib.load(CT_path)
NiftiCTObj_Img = NiftiCTObj.get_fdata()
NiftiCTObj_Affine = NiftiCTObj.affine
NiftiCTObj_Header = NiftiCTObj.header
NiftiCTObj_Img = np.copy(np.array(NiftiCTObj_Img, dtype = 'float32'))

NiftiMaskObj = nib.load(couch_path)
NiftiMaskObj_Img = NiftiMaskObj.get_fdata()


NiftiCTObj_Img[NiftiMaskObj_Img] == 'NaN'

# this is saved on your other laptop --> check to see exactly how you have written this bit of the code 


# add a few more slices sagitally and then grow
# then add a semi circle on to the block and mask that region too 

