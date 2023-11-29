from  pydicom import dcmread
import os 

path = 'D:\GSTT_HN\DICOM'

patients = os.listdir(path)

for patient in patients:

    path_to_CBCT_folder = os.path.join(path, patient, patient, 'CBCT')

    dicom_files = os.listdir(path_to_CBCT_folder)

    for dicom_file in dicom_files:
        
        dcm_file_path = os.path.join(path, patient, patient, 'CBCT', dicom_file)
        
        ds = dcmread(dcm_file_path)

        if ds[0x08, 0x70].value  == 'GE MEDICAL SYSTEMS':

            print(patient)
            print(ds[0x08, 0x22].value)


