"""
Runs all the processing files for the material database.

This file executes step "Update the database" in the instructions "instructions.md" file.
"""
from generate_database_summary import gen_db_summary
from generate_all_clean_data import gen_clean_data
from generate_yield_properties import gen_yield_props
from generate_mechanical_props_table import gen_mech_props_tab

gen_db_summary()
gen_clean_data()
gen_yield_props()
gen_mech_props_tab()
