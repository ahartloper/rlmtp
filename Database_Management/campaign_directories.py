"""
This file contains all the locations of all the campaign directories.

The contents of this file are used in the various Python scripts.
Add entries to the lists as necessary so that they are processed by these scripts.

- Additional data that follows the RLMTP storage protocol should be inserted into
    the campaign_dirs_rlmtp list.
- Additional data that does not follow the RLMTP storage protocol should be inserted into
    the campaign_dirs_nonrlmtp list.

Adding to this file:
1. Add a new line to either "campaign_dirs_rlmtp" or "campaign_dirs_nonrlmtp".
2. Make sure that there is a comma at the end of the line (proper array format)
"""

# The input_root directory contains the following campaign_dirs
input_root = './RESSLab_Material_DB'

# Data in these directories follow the RLMTP protocol
# The data in these folders are in raw format and need to be filtered/reduced
campaign_dirs_rlmtp = [
    # S355
    # Sections
    'S355J2_HEB500/flange',
    'S355J2_HEB500/web',
    'S355J2_HEM300/flange',
    'S355J2_IPE400/flange',
    'S355J2_IPE400/web',
    'S355J2_IPE300',
    'S355J2_HEM320/WP3_HEM320_D_CRM20',
    'S355J2_HEM320/WP3_HEM320_C_CRM20',
    'S355J2_IPE360/WP3_IPE360_D_CRM8',
    'S355J2_IPE360/WP3_IPE360_C_CRM8',
    'S355J2_IPE270/flange',
    'S355J2_HEA160/S355J2_HEA160_FLANGE_DATA',
    'S355J2_HEM500/S355J2_HEM500_FLANGE_DATA',
    'S355J2_HEM500/S355J2_HEM500_WEB_DATA',
    'S355J2_IPE200/S355J2_IPE200_FLANGE_DATA',
    'S355J2_IPE330/S355J2_IPE330_RBS_C_CRM8',
    'S355J2_IPE330/S355J2_IPE330_RBS_D_CRM8',
    # Plates
    'S355J2_Plates/WP3_PLT15_CRM12',
    'S355J2_Plates/S355_J2_N_Base_metal_15mm_plate_SELIMCAN_MASTER_THESIS',
    'S355J2_Plates/S355_J2_N_HAZ_10_C_s_15mm_plate_SELIMCAN_MASTER_THESIS',
    'S355J2_Plates/S355_J2_N_HAZ_12_5_C_s_15mm_plate_SELIMCAN_MASTER_THESIS',

    # S235/275
    'S235275_Plates/S235275_Plate15',

    # S690
    'S690QL/Base metal',
    'S690QL/Heat affected zone',
    'S690/S690_11mm',
    'S690/S690_19mm',

    # SM/SN490
    'SM490A_H498x432x45_70/SM490A_H498x432x45_70_FLANGE',
    'SM490A_H498x432x45_70/SM490A_H498x432x45_70_WEB',
    'SN490B_HY650x300x16x25/SN490B_HY650x300x16x25_FLANGE',
    'SN490B_HY650x300x16x25/SN490B_HY650x300x16x25_WEB',

    # Fe-SMA
    'Fe-SMA/Fe-SMA_Cyclic-Calib'
]

# Data in these directories do not following the RLMTP protocol
# The data in these folders are already filtered/reduced, just need to copy
campaign_dirs_nonrlmtp = [
    'S690QL/25mm',
    'S460NL/25mm',
    'S355J2_Plates/S355J2_N_25mm',
    'S355J2_Plates/S355J2_N_50mm',
    'HYP400',
    'BCR295',
    'BCP325',
    'A500',
    'A992_Gr50/A992_W14X82_flange',
    'A992_Gr50/A992_W14X82_web'
]
