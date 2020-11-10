"""@package fracture_strain
Functions to compute the fracture strain.
"""
from numpy import log
from .readers import ACCEPTED_READER_INPUTS


def compute_fracture_strain(d_initial, d_final):
    """ Returns the fracture strain.

    :param float d_initial: Initial measured diameter of the specimen.
    :param float d_final: Final diameter measured after fracture of the specimen.
    :return float: Fracture diameter.
    """
    return 2. * log(d_final / d_initial)


def process_fracture_strains(df):
    """ Returns the fracture strains for the provided data.

    :param pd.DataFrame df: Contains the measured initial and fractured diameters.
    :return pd.Series: The fracture strains for all the entries.
    """
    d_initial = df[ACCEPTED_READER_INPUTS['reduced_dia_m'][0]]
    d_final = 0.5 * (df[ACCEPTED_READER_INPUTS['fractured_dia_top_m'[0]]]
                     + df[ACCEPTED_READER_INPUTS['fractured_dia_bot_m'[0]]])
    return compute_fracture_strain(d_initial, d_final)
