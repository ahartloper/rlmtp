"""
This file associates campaigns with academic references when applicable.

There are two steps to adding a new reference association:
1. Add the reference to the bibliography using the bibtex format. The file is
    "Database_Management/Database_References.bib".
2. Update the "campaign_reference_map" with the campaigns associated with the new
academic reference key.

For parsing see: https://bibtexparser.readthedocs.io/en/master/index.html
"""

# 2. Map each reference to the campaigns it encompasses
# The key is a unique string, and the value is a list of the campaign directories
campaign_reference_map = {
    'HartloperConstitutiveModelingStructural2021': [
        'S355J2_HEB500/flange',
        'S355J2_HEB500/web'
    ],
    'GrigoriouCharacterizationcyclichardening2017': [
        'S690QL/25mm',
        'S460NL/25mm',
        'S355J2_Plates/S355J2_N_25mm',
        'S355J2_Plates/S355J2_N_50mm'
    ],
    'SuzukiExperimentalEvaluationSteel2021': [
        'HYP400',
        'BCR295',
        'BCP325',
        'A500',
        'A992_Gr50/A992_W14X82_flange',
        'A992_Gr50/A992_W14X82_web'
    ],
    'HerediaRosaExperimentalbehaviorironbased2021': [
        'Fe-SMA/Fe-SMA_Cyclic-Calib',
        'Fe-SMA/Fe-SMA_Cyclic-Ancillary'
    ],
    'OzdenExperimentalinvestigationcyclic2021': [
        'S355J2_Plates/S355_J2_N_HAZ_12_5_C_s_15mm_plate_SELIMCAN_MASTER_THESIS',
        'S355J2_Plates/S355_J2_N_HAZ_10_C_s_15mm_plate_SELIMCAN_MASTER_THESIS',
        'S355J2_Plates/S355_J2_N_Base_metal_15mm_plate_SELIMCAN_MASTER_THESIS',
    ],
    'GarciaMultiaxialfatigueanalysis2020': [
        'S690QL/Base metal',
        'S690QL/Base metal fatigue',
        'S690QL/Heat affected zone',
        'S690QL/Heat affected zone fatigue'
    ],
    'InamasuDevelopmentExperimentalValidation2022': [
        'S355J2_IPE400/flange',
        'S355J2_IPE400/web'
    ],
    'ElJisrRoleCompositeFloor2022': [
        'S355J2_Plates/WP3_PLT15_CRM12',
        'S355J2_IPE360/WP3_IPE360_C_CRM8',
        'S355J2_IPE360/WP3_IPE360_D_CRM8',
        'S355J2_Plates/WP3_PLT15_CRM12',
        'S355J2_HEM320/WP3_HEM320_C_CRM20',
        'S355J2_HEM320/WP3_HEM320_D_CRM20'
    ],
    'SkiadopoulosWeldedmomentconnections2022': [
        'SM490A_H498x432x45_70/SM490A_H498x432x45_70_WEB',
        'SM490A_H498x432x45_70/SM490A_H498x432x45_70_FLANGE',
        'SN490B_HY650x300x16x25/SN490B_HY650x300x16x25_FLANGE',
        'SN490B_HY650x300x16x25/SN490B_HY650x300x16x25_WEB'
    ]
}
