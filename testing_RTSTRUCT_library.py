from DicomRTTool.ReaderWriter import DicomReaderWriter
import SimpleITK as sitk 

DICOM_path = ''

dicom_Reader = DicomeReaderWriter(description='Examples', arg_max=True)
dicom_Reader.walk_through_folders(DICOM_path)
all_rois = dicom_Reader.return_rois(print_rois=True)

img_path = ''
roi_path = ''

dicom_Reader.get_images_and_mask()

image = dicom_Reader.ArrayDicom
mask = dicom_Reader.mask

dicom_sitk_handle = dicom_Reader.dicom_handle
mask_sitk_handle = dicom_Reader.annotation_handle

sitk.WriteImage(dicom_sitk_handle, img_path)
sitk.WriteImage(mask_sitk_handle, roi_path)
