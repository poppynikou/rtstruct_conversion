import nibabel as nib
import numpy as np 
from utils import get_image_objects

def calc_couch_slices(sagital_voxel_size):

    # this is the thickness in mm of the UCLH couch 
    UCLH_couch_thickness = 20*0.976562

    # calculate the number of slices this corresponds to in the image 
    no_slices = UCLH_couch_thickness/sagital_voxel_size

    return int(no_slices)


def create_mask(couch_path, body_path, mask_path):

    '''
    :param couch_path: string. path to binary/boolean image of the couch. 
    :param body_path:  string. path to binary/boolean image of the body. 
    :param mask_path: string. path to binary/boolean image of the mask. 1s in region you want to mask. 
    '''

    # read in couch info 
    Couch_Img, Couch_Affine, Couch_Header = get_image_objects(couch_path)
    Couch_Img_copy = Couch_Img.copy()
    Couch_Img_copy = np.array(Couch_Img_copy, dtype = np.bool8)

    # find indexes where the couch mask is non zero 
    indexes = np.nonzero(Couch_Img_copy)

    # find the sagital size at which to define the mask at 
    # this is based on UCLH couch size in mm 
    sagital_voxel_size = Couch_Header['pixdim'][1]
    no_slices = calc_couch_slices(sagital_voxel_size)
    sagital_slice = indexes[1][0] - no_slices

    # create the binary mask, and mask the couch region 
    shape = Couch_Header['dim'][1:4]
    Binary_Mask = np.zeros(shape= shape)
    Binary_Mask[:,sagital_slice:shape[1],:] = 1

    # import body image info 
    Body_Img, _, _ = get_image_objects(body_path)
    del _
    Body_Img_copy = Body_Img.copy()
    Body_Img_copy = np.array(Body_Img_copy, dtype = np.bool8)

    # mask out region infront on the body 
    bodyindexes = np.nonzero(Body_Img_copy)
    body_sagital_slice = min(bodyindexes[1]) - 20
    Binary_Mask[:,0:body_sagital_slice,:] = 1

    # save the mask 
    NewniftiObj = nib.Nifti1Image(Binary_Mask, Couch_Affine, Couch_Header)
    nib.save(NewniftiObj, mask_path)


def mask_img(img_path, mask_path, masked_img_path, masking_value = np.NaN):

    '''
    :param img_path: string. path to the image you want to mask
    :param mask_path: string. path to binary/boolean image of the mask. 1s in region you want to mask. 
    must be the same size as the image you want to mask 
    :param masked_img_path: string. path in which you want to save the masked image. 
    :param masking_value: Nan or integer. The value which you want to mask the image with 
    '''

    CT_Img, CT_Affine, CT_Header = get_image_objects(img_path)
    CT_Img_copy = CT_Img.copy()
    CT_Img_copy = np.array(CT_Img_copy, dtype = np.float32)

    Mask_Img, _, _ = get_image_objects(mask_path)
    del _
    Mask_Img_copy = Mask_Img.copy()
    Mask_Img_copy = np.array(Mask_Img_copy, dtype=np.bool8)

    CT_Img_copy[Mask_Img_copy] = masking_value

    newNiftiObj = nib.Nifti1Image(CT_Img_copy, CT_Affine, CT_Header)
    nib.save(newNiftiObj, masked_img_path)

