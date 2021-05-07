# Instructions for adding to the material database

## Prerequisites

1. Python3 - You need Python3, I recommend Anaconda Python3.
1. RLMTP - You need the Python package `rlmtp` installed.  
This can be installed as follows: 
```
git clone ssh://git@c4science.ch/source/rlmtp.git
cd rlmtp
pip install .
```

## Steps for adding to the database

1. Add your data following the RLMTP protocol to "RESSLab_Material_DB" in the appropriate location.
1. Update the "campaign_dirs_rlmtp" list by adding a new item with the directory corresponding to Step 1.
1. Generate the "filter_file.txt" for your additions using "Python_helpers/create_filter_files.py". Make sure to specify the correct campaign directory.
1. Create the new database by running "generate_database_summary.py".
1. Generate all the clean data by running "generate_all_clean_data.py".
1. Generate the yield properties file by running "generate_yield_properties.py".

## Notes
- Everything must be generated after each new addition to the database.
    - This should not take long because existing items are not re-processed.
- The processing checks if the "clean" .csv file exists for each file, if the "clean" file exists, the processing skips this entry.
    - If you want to re-process data, the existing "clean" data must be deleted first!
- It is pointless to make changes to the "Summarized_Material_DB.csv" file since this file gets overwritten every new generation. If a correction is required, go directly to the "specimen_description.csv" file and fix it there.
