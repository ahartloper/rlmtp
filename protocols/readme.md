# rlmtp Protocols

The various protocols that are assumed in rlmtp for storing data are summarized in this file.


## Specimen Directory Protocol

This protocol specifies the layout of the specimen directory.
Following this template will allow you to use the automatic processing functions within rlmtp.
Optional values are given in brackets ([]), and optional files are also given in brackets
(e.g., [Temperature_[test_id].xlsx]).

```
[specimen_directory]
    +-- [filter_info.csv]
    +-- [specimen_description.csv]
    +-- [specimen_pid.csv]
    +-- Excel
    |   +-- testData_[test_id].xlsx
    |   +-- stiffnessTest_[test_id].xlsx
    +-- Latex
    |   +-- [associated LaTeX files]
    +-- Matlab
    |   +-- [Matlab postprocessing files]
    +-- Photos
    |   +-- [photos taken during the test]
    |   +-- [photos extracted from videos]
    +-- rawData
    |   +-- stiffnessTest_[test_id].lid
    |   +-- stiffnessTest_[test_id].lia.xlsx
    |   +-- testData_[test_id].lid
    |   +-- testData_[test_id].lia.xlsx
    |   +-- [Temperature_[test_id].xlsx]
    +-- Videos
    |   +-- [videos taken during the test]
```

Notes:
- The choice of name for specimen_directory is arbitrary
- The filter_info file is optional, but required if you want to filter the results

## Test Data File Protocol

This protocol is for the file [specimen_directory]/Excel/testData_[test_id].xlsx.
The test data file contains partially processed results from Dion7 (the testData file in the rawData directory).

### Lines and columns in the Excel file

The following lines and columns in the testData Excel file must conform to the following specification:

- Line 7 has the following columns (A7 through J7):
```
S/No, System Date, C_1_Temps[s], C_1_Force[kN], C_1_{Ext_Channel}[mm], C_1_Déplacement[mm], sigma [Mpa], epsilon, e_true, sigma_true
```
{Ext_Channel} is either Angle or Deform1.
Each of these columns are the title of a particular data channel in Dion7.

- The data for each channel associated with its column starts on the following line (Line 8).

### Data channel specifics

Now the specifics of each channel are given.
- S/No: the increment number
- System Data: the [day].[month].[year] [hour]:[min]:[sec].[ms] of each measurement, the [ms] may not be included for
all measurements.
- C_1_Temps[s]: the time in seconds elapsed since the recording started
- C_1_Force[kN]: the measured force in kilonewtons
- C_1_{Ext_Channel}[mm]: the displacement measured from the extensometer in millimeters, the channel name may vary
based on the model
- C_1_Déplacement[mm]: the measured cross-head displacement in millimeters
- sigma [Mpa]: the deduced stress in megapascals, equal to C_1_Force[kN] / deduced_area
- epsilon: the deduced engineering strain, equal to C_1_{Ext_Channel}[mm] / gage_length
- e_true: the deduced true strain, equal to ln(1 + epsilon)
- sigma_true: the deduced true stress, equal to sigma [Mpa] * (1 - epsilon)

The sense of e_true and sigma_true should be such that compressive stresses and strains are negative and tensile strains
 are positive.
The sense of all the other measured values is arbitrary.

## Temperature Data File Protocol

To complete...

## Filter Protocol

This protocol is for the file [specimen_directory]/filter_info.csv.
The filter_info file provides the specific values to filter and reduce the stress-strain data to be amenable for
material parameter fitting.

File format:
- Line 1: window length, [optional] polyfit order
- Line 2: anchor_start, [anchor_i], anchor_end

[anchor_i] are the optional anchor points corresponding to the 0-indexed data.

## Specimen Description Protocol

To complete...

## Specimen PID Information Protocol

To complete...
