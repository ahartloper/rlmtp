"""
This file contains all the locations of all the campaign directories.

The contents of this file are used in the various Python scripts.
Add entries to the lists as necessary so that they are processed by these scripts.

Additional data that follows the RLMTP storage protocol should be inserted into to the campaign_dirs_rlmtp list.
Additional data that does not follow the RLMTP storage protocol should be inserted into to the campaign_dirs_nonrlmtp list.
"""

# The input_root directory contains the following campaign_dirs
input_root = './RESSLab_Material_DB'

# Data in these directories follow the RLMTP protocol
# The data in these folders are in raw format and need to be downsampled
campaign_dirs_rlmtp = [
    # S355
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
    'S355J2_Plates/WP3_PLT15_CRM12',
    'S355J2_Plates/S355J2_Base_metal_15mm',
    'S355J2_Plates/S355J2_Welded_metal_15mm',

    # S235/275
    'S235275_Plates/S235275_Plate15',

    # S690
    'S690QL/Base metal',
    'S690QL/Heat affected zone',
    'S690/S690_11mm',
    'S690/S690_19mm',

    # Fe-SMA
    'FE-SMA/FE-SMA_Cyclic-Calib'
]

# Data in these directories do not following the RLMTP protocol
# The data in these folders are already processed, just need to copy
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
