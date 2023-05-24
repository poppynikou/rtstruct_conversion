'''
TO DO 
Add in checks for folders which:
- make sure there are CT_ folders
- make sure there is more than X CBCT_ folderss
- makes sure the dates on the CT and CBCT files are real dates which make sense
- makes sure the first CBCT is after the first CT in chronological order

- we can reaplce the CT_CBCT_slice threshold by just identifying the index in the list with the max slices . reduces number of inputs from a person
- also shouldnt have to insert number of patients, should just be able to list folders within the base directory 
- could reduce even more, by adding contour names and associations section into the function 

'''
