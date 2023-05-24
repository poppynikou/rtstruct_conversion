from DicomRTTool.ReaderWriter import DicomReaderWriter, ROIAssociationClass
import SimpleITK as sitk 
import os
import shutil 
import pandas as pd
import numpy as np 
   


def DICOM_CONVERT(Base_path, contour_names, associations):

    '''
    function which converts both images and structures at the same time 

    Base_path: string. folder in which the HN_x folders are stored.
    contour_names: list of strings. List of names of contours which you want to save
    associations: list of lists of strings. List of possible associated contour names as contour_names.
    ''' 

    #The number of nested lists in associations should be equal to the length of contour_names
    if len(associations) != len(contour_names):
        raise Exception('Each contour should have a list of associations')


    # for catching patients which didnt work
    file = open("RTSTRUCT_conversion_log.txt", mode="w")

    patient_folders = os.listdir(Base_path)

    for patient_path in patient_folders:


        # indefies the number of unique series UID images within the patient specific folder
        dicom_Reader = DicomReaderWriter()
        dicom_Reader.walk_through_folders(patient_path)#
        indexes = dicom_Reader.images_dictionary

        # records the path of slices for each unique series UID
        no_dicom_slices_path = [len(dicom_Reader.return_files_from_index(img_index)) for img_index in range(0, len(indexes))]
        # records the number of dicom slices associated with each unique series UID
        dicom_slices_path = [dicom_Reader.return_files_from_index(img_index) for img_index in range(0, len(indexes))]


        # loops through the number of unique series UIDs
        for img_index in range(0, len(indexes)):

            # gets image object 
            dicom_Reader.set_index(img_index)

            # determines, based on number of slices, whether image is CT or CBCT
            # the item in the list with the most slices is assumed by default to be the CT 
            if no_dicom_slices_path[img_index] < max(no_dicom_slices_path):
                filename_prefix = 'CBCT'
            else: 
                filename_prefix = 'CT'

            # this returns the series date of the scan 
            series_date = str(dicom_Reader.return_key_info('0008|0021'))
            
            # creates folders within the patient folder for saving images
            # see above for exact folder architecture which is stored 
            image_folder = patient_path + '/'+filename_prefix + '_' + series_date + '/'
            if not os.path.exists(image_folder):
                os.mkdir(image_folder)
            dicom_folder =  image_folder + '/DICOM/'
            if not os.path.exists(dicom_folder):
                os.mkdir(dicom_folder)
            nifti_folder = image_folder + '/NIFTI/'
            if not os.path.exists(nifti_folder):
                os.mkdir(nifti_folder)
            
            # gives name of nifti image
            filename = nifti_folder + filename_prefix + '_' + series_date + '.nii.gz'
            # gets the image object and writes to file
            dicom_Reader.get_images()
            dicom_sitk_handle = dicom_Reader.dicom_handle
            sitk.WriteImage(dicom_sitk_handle, filename)    

            # moves old nifti files into the DICOM folder 
            for dicom_slice_index, dicom_slice in enumerate(dicom_slices_path[img_index]):

                source = dicom_slice
                destination = dicom_folder + filename_prefix + series_date + '_' + str(dicom_slice_index) + '.dcm'
                shutil.move(source, destination)
            
            if filename_prefix == 'CT':

                # create a directory for the structures
                structures_path = image_folder + '/STRUCTURES/'
                if not os.path.exists(structures_path):
                    os.mkdir(structures_path)

                for i, contour_name in enumerate(contour_names):

                    dicom_Reader.set_contour_names_and_associations(contour_names=[contour_name], associations=[ROIAssociationClass(contour_name, associations[i])])
                    path = dicom_Reader.where_is_ROI()
                    print('-----')
                    print(path)
                    dicom_Reader.get_mask()

                    #load mask
                    mask_sitk_handle = dicom_Reader.annotation_handle

                    # saves as boolean mask 
                    roi_name =  structures_path + 'BIN_'+ contour_name + '.nii.gz'
                    sitk.WriteImage(mask_sitk_handle, roi_name)

                # copy file name of RTSTRUCT into the DICOM folder 
                

                # check that there are the correct number of binary files saved in the folder
                # this should catch patients and exceptions which didnt work 
                # check the files which are in the directory are files
                # which start with 'BIN_' and end in '.nii.gz'
                # if not it writes the failed patients and imgs into a file
                if len([name for name in os.listdir(structures_path) if (os.path.isfile(os.path.join(structures_path, name)) & name.startswith('BIN_') & name.endswith('.nii.gz'))]) < len(contour_names):
                    file.write(str(Base_path))

    # if no conversions failed you note this down too 
    if os.path.getsize("RTSTRUCT_conversion_log.txt") == 0:
        file.write('No failed conversions.')


def get_contour_names_and_associations(path):
    '''
    path: string. path to excel file which contains the contour names as a header
    and all the listed associations in columns 

    returns: contour names and associations in list formats
    '''
   
    contour_names_excel = pd.read_excel(path, sheet_name = 'H&N', header =0 , dtype = str,  keep_default_na=False)
    # these are the contour names you want
    contour_names = list(contour_names_excel.columns.values)
    # possible list of associated contour names
    associations = np.transpose(contour_names_excel.to_numpy()).tolist()

    return contour_names, associations


