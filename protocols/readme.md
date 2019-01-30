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
- sigma_true: the deduced true stress, equal to sigma [Mpa] * (1 + epsilon)

The sense of sigma, epsilon, e_true, and sigma_true should be such that compressive stresses and strains are negative
and tensile strains are positive.
The sense of all the other measured values is arbitrary.

## Temperature Data File Protocol

This protocol is for the file [specimen_directory]/rawData/Temperature_[test_id].xlsx.
The temperature data file is optional, it provides the data for the measured temperature of the specimen throughout the
loading.

File format:
- Line 2: Time 1 - sampling rate 1, [Time 1 - sampling rate 2], Load, Extenso, Temperature
- Line 3: Unit, [Unit], Unit, Unit
- Line 5: DD.MM.yy HH:MM:SS, [DD.MM.yy HH:MM:SS], DD.MM.yy HH:MM:SS, DD.MM.yy HH:MM:SS
- Line 50: start of data, [start of data], start of data, start of data

Notes:
- There can be 4 or 5 columns in the data depending on the number of sampling rates used. The time data in 2 column is
optional depending on the number of sampling rates. A maximum of two rates can be used.
- The Temperature data MUST be associated with the time data that is contained in the first column (i.e., the sampling
rate in line 6 must be equal in the temperature and first columns).
- The standard unit of measurement for time is seconds, and degrees C for temperature.


## Filter Protocol

This protocol is for the file [specimen_directory]/filter_info.csv.
The filter_info file is optional, it provides the specific values to filter and reduce the stress-strain data to be
amenable for material parameter fitting.

File format:
- Line 1: window length, [optional] polyfit_order
- Line 2: anchor_start, [anchor_i], anchor_end

Where polyfit_order is the order of line to fit between points (default is 1), anchor_start is the index of the first
data point to include, anchor_end is the index of the last data point to include and [anchor_i] are the optional anchor
points corresponding to the 0-indexed data between the start and end anchor points.
Note that only the data bounded by anochor_start and anchor_end will be included in the processed output.

## Specimen Description Protocol

This protocol is for the file [specimen_directory]/specimen_description.csv.
The specimen_description file is optional, it's purpose is to keep a record the specimen properties, testing personnel,
testing machine, PID parameters, etc.,.

The format of this file is not line specific, the order below is only recommended.
The first entry in each line is a specific keyword, and the entries given in brackets are the associated values.
Only the keywords in the list below are recognized, any other keywords will not be parsed when processing the file.
Empty lines are allowed, and will be ignored.

File format:
- steel_grade, [grade]
- add_spec, [additional_spec]
- fy_n, [fy]
- fu_n, [fu]
- specimen_id, [tag]
- specimen_source, [source]
- outer_dia_n, [M-]
- gage_length_n, [L]
- reduced_dia_m, [d1], [d2], [d3]
- pid_force, [p], [i], [d]
- pid_disp, [p], [i], [d]
- pid_extenso, [p], [i], [d]
- date, [dd-mm-yyyy]
- personnel, [name]
- location, [location]
- setup, [setup]
- ambient_temp, [temperature]

Where:
- grade is the steel grade (e.g, S355)
- additional_spec are any additional specifications for the steel (e.g., J2+N)
- fy is the nominal yield stress in megapascals (e.g., 355)
- fu is the nominal tensile stress in megapascals (e.g., 490)
- tag is an identifier for the specific specimen (e.g., C2)
- source is where the steel came from (e.g., HEB500 web, 25 mm plate)
- M- is the nominal outer diameter of the specimen (e.g., M8, M20)
- L is the nominal length of the reduced parallel section in millimeters
- d1, d2, d3 are the measured diameters of the reduced parallel section in millimeters
- p, i, d are the proportional (p = K_p), integral (i = T_i), and derivative (d = T_d) constants for the PID controller
(force = force control, disp = cross-head displacement control, extenso = extensometer control)
- dd-mm-yyyy is the day-month-year when the test is conducted
- name is the name of the test personnel
- location is the laboratory where the test was conducted (e.g., EPFL RESSLab)
- setup is the name of the test machine (e.g., w+b)
- temperature is the ambient room temperature when the test begins
