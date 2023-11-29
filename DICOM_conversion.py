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
Results_path = 'F:/GSTT_HN/NIFTI/'
Base_path = 'F:/GSTT_HN/DICOM/'
#'T:/GSTT_HN/OneDrive_3_11-16-2023/'
hn_contournames_path = 'Contour_Naming.xlsx'

patients = np.arange(1,33)

for patient in patients:
        # for catching patients which didnt work
        RTSTRUCT_conversion_log = open("RTSTRUCT_conversion_log.txt", mode="a")
    
        PatientNo = 'HN_' + str(patient)
        RTSTRUCT_conversion_log.write('--------------------------------- \n')
        RTSTRUCT_conversion_log.write(str(PatientNo) + '\n')

        base_path = Base_path + PatientNo
        results_path = Results_path + PatientNo

        # get the contour names and the associations in a usable format 
        contour_names, associations = get_contour_names_and_associations(hn_contournames_path)

        #do the conversion 
        DICOM_CONVERT(base_path, contour_names, associations, Results_path, PatientNo)

        # check the dicom conversions have worked 
        #check_DICOM_conversions(results_path)

        # need to add in checks to see which ones failed 
   