from utils import * 

'''
Script which converts the CT and CBCT DICOM objects into NIFTI objects
The images from one patient must be stored into one folder 
The code finds unique instances of series UIDs and links them with the series dates in the dicom headers
It then sorts your folder into the following architecture:
HN_x:
    -CT_date
        -DICOM
        -NIFTI
    -CBCT_date
        -DICOM
        -NIFTI
'''

#### --- USER INPUTS --- ####
'''
Base_path: string. folder in which the HN_x folders are stored.
hn_contournames_path: string. path where the excel file is stored which contains the contours you want to convert and their associated contour options. 
'''

Base_path = 'D:/test_data'
hn_contournames_path = 'Contour_Naming.xlsx'

# get the contour names and the associations in a usable format 
contour_names, associations = get_contour_names_and_associations(hn_contournames_path)

#do the conversion 
DICOM_CONVERT(Base_path, contour_names, associations)

# check the dicom conversions have worked 
check_DICOM_conversions(Base_path)