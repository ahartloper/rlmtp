# Instructions for adding to the material database

## Steps

1. Add your data following the RLMTP protocol to "RESSLab_Material_DB" in the appropriate location.
1. Update the "campaign_dirs_rlmtp" list by adding a new item with the directory corresponding to Step 1.
1. Generate the "filter_file.txt" for each test using "Python_helpers/create_filter_files.py". Make sure to specify the correct campaign directory.
1. Create the new database by running "generate_database_summary.py".
1. Generate all the clean data by running "generate_all_clean_data.py".
1. Generate the yield properties file by running "generate_yield_properties.py".

## Notes
- Yes, everything must be regenerated after each new addition to the database. This takes time. A better approach may be developed in the future.
- It is pointless to make changes to the "Summarized_Material_DB.csv" file since this file gets overwritten every new generation. If a correction is required, go directly to the "specimen_description.csv" file and fix it there.
