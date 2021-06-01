"""
Runs all the processing files for the material database.

This file executes step "Update the database" in the "instructions.md" file.
"""
import os
from generate_database_summary import gen_db_summary
from generate_all_clean_data import gen_clean_data
from generate_yield_properties import gen_yield_props
from generate_mechanical_props_table import gen_mech_props_tab

# Directory where summaries will be created
output_dir = 'Database_Summaries'
backup_dir = 'Old'
# Move old summaries to the backup directory (csv files)
dir_csv_contents = [f for f in os.listdir(output_dir) if os.path.splitext(f)[1] == '.csv']
for f in dir_csv_contents:
    os.replace(os.path.join(output_dir, f), os.path.join(output_dir, backup_dir, f))

# Do the processing and generate new summaries
gen_db_summary()
gen_clean_data()
gen_yield_props()
gen_mech_props_tab()
