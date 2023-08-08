# A Simplified version of mABs production pipeline

This repository enables you to reproduce a sample of Python data processing steps (from final PCR to Gibson Assembly, refer to [1] for more details) of the pipeline for mABs production. It includes following scripts:

`05_PCR3.py`, `06_cELE.py`, `07_GiAS.py`, together with mock data needed for the run. 

### Why only some steps?

The smaller, isolated version of the pipeline contains only analysis steps that are necessary to exemplify the design principles described in [1]. It serves as a proof-of-concept, i.e., it acts as a smaller-scale demonstration of the core functionality and key steps of the full data processing pipeline. It is easier to run and modify, allowing adjustments to your needs. It serves as a demonstration of main concepts and is less overwhelming than a full pipeline. 

However, if you wish to download the whole pipeline and reproduce other data processing steps as described in [1], please go back to the root directory of this repository and follow the instructions provided in README.md
## Table of contents
* [Setup](#setup)
* [Reproducing the pipeline run “as is”](#reproducing-the-pipeline-as-is)
* [Adjusting the pipeline to your own needs](#adjusting-the-pipeline-to-your-own-needs)
* [References](#references)
  
## Setup

1. You can download the simplified pipeline version from the [releases page](https://github.com/Malwoiniak/mABpy/archive/refs/tags/v1.0.0.zip). This will download the source code of simplified pipeline (dir `mABpy-1.0.0/`)

3. In terminal, navigate to the `mABpy-1.0.0/simplified_pipeline` directory of the extracted repository
4. Follow the setup steps (from step 5.) described [here](https://github.com/Malwoiniak/mABpy/tree/main#setup) to finish the installation

## Reproducing the pipeline run “as is”

You can follow the [tutorial](link) to get you through the instructions on reproducing **all** pipeline steps. Otherwise, see below for the description on reproducing sample steps. 

**Note that** plate numbers used in this example are arbitrary and were selected to match the barcode values in downstream files, ensuring consistency throughout pipeline run. 

**Also, note that** scripts needs to be run in the order described below due to their dependency on proceeding modules.

### 05_PCR3.py

This script prepares the samples for a final PCR step (PCR3) and capillary electrophoresis (cELE), before cloning by Gibson Assembly (GiAS).

#### Input files

+ From `Input/` directory: `PCR3_primer.xlsx` (contains plate location of the primers specific for the sequenced H and L chains, with overhangs for Gibson Assembly) and `sorter.xlsx` (contains the list of plate grids on 384-well plate)

+ From ` PCR3_Store_Lists/` directory: ` PCR3_StoreList_20230713-120500.xlsx` (contains the samples waiting for their turn in PCR3 reaction). It’s the latest file in that directory (by modification date) and is dropped there by a **Knime module** that precedes `05_PCR3.py` module

+ From `04_Parse_Out/ID_Dictionary` directory: `ID_Dictionary.xlsx` (contains the unique IDs and sequencing identifiers of all the samples present in the database). This file is automatically exported from the database every time the proceeding **Knime module** is run. 

#### Usage

05_PCR3.py takes three arguments:

| Argument         | Description                               | Required | Default Value |
|------------------|-------------------------------------------|----------|---------------|
| `-s SPECPCRPLATE ` | Last plate number used for PCR3 | Yes      | None |
| `-e CELE_PLATE ` | Last plate number used for capillary electrophoresis | Yes | None |
| `-c SPECPCR_COPY_PLATE ` | Last plate number used for a copy plate (a plate that stores diluted PCR3 product) | Yes | None |

1.	In terminal, move to the `Scripts/` directory of the project
2.	Run the script passing the plate numbers:

`python 05_PCR3.py –s 60 -e 381 –c 28`

#### Output files

+ In `05_PCR3_Out/` directory, files:
 
    `BAOsPCR3p00061_TemplatePickList.xslx`, `BAOsPCR3p00061_PrimerPickList.xlsx`, `BAOsPCR3p00062_TemplatePickList.xslx`, `BAOsPCR3p00062_PrimerPickList.xlsx`,

    These are the pipetting protocols for [ECHO Acoustic Liquid Handler](https://www.beckman.com/liquid-handlers/echo-650-series) (machine-readable files for dispensing volumes of primers and templates for PCR3 reaction).

+ In `PCR3_Store_Lists/` directory, file `PCR3_StoreList_date-time.xlsx`. It’s a new store list of leftover samples that will now wait for the next round of PCR3

+ In `05_PCR3_Out/Intermed_Files/` directory, file `PCR3_Intermed_date-time.xlsx`. It’s an intermediate file that contains combined information on all samples that will be run in this PCR3 and capillary electrophoresis (cELE) round. 

### 06_cELE.py

#### Input files

+ In `05_PCR3_Out/Intermed_Files/` directory, file `PCR3_Intermed_date-time.xlsx`, latest in that directory (by modification date). It’s an output of `05_PCR3.py`

+ In `Experimental_Data/cELE/` directory, folders with corresponding cELE results (here: `Experimental_Data/cELE/baoscelep00382` and `Experimental_Data/cELE/baoscelep00383`), containing peak tables ([Fragment Analyzer’s](https://www.agilent.com/en/product/automated-electrophoresis/fragment-analyzer-systems/fragment-analyzer-systems) redouts), here: `2023 07 20 14H 00M Peak Table.csv` and `2023 07 20 15H 25M Peak Table.csv`

#### Usage

1.	In terminal, move to the `Scripts/` directory of the project
2.	Run the script:

`python 06_cELE.py`

#### Output files

+ In `06_cELE2_Out/` directory, file `cele2_Intermed_date-time.xlsx`. It’s an intermediate file that contains information on all samples that were run in current PCR3 and cELE round, together with analysed cELE data. The script assigns a ‘Y’ in col `Decision_Cele_SpecPCR` if the cELE band is within a size threshold (in base pairs, defined in `config.py`)

### 07_GiAS.py

#### Input files

+ In `06_cELE2_Out/` directory, file `cele2_Intermed_date-time.xlsx`. latest in that directory (by modification date). It’s an output of `06_ cELE2.py`

#### Usage

07_GiAS.py takes one argument:

| Argument         | Description                               | Required | Default Value |
|------------------|-------------------------------------------|----------|---------------|
| `-g GIBSON_PLT` | Last plate number used for Gibson Assembly | Yes      | None |

1.	In terminal, move to the `Scripts/` directory of the project
2.	Run the script passing the plate numbers:

`python 07_GiAS.py –g 61 `

3.	Enter user’s input: 

a.	Linear plasmids’ (per chain) wells on the plate suitable for ECHO Acoustic Liquid Handler, from which a transfer of linearized plasmids of heavy and light mAB chains are transferred to Gibson Assembly plate, here: E6, F6, G6 (1st plate), M6, N6, O6(2nd plate)
b.	Gibson Assembly master mix wells on the same plate, from which a transfer of master mix to Gibson Assembly plate is done, here: A6, B6, C6 (1st plate), I6, J6, K6 (2nd plate)

#### Output files

+ In `07_GiAS_Out/` directory, files:
 
    `BAOsGiAsp00062_MM_Spotting.xslx`, `BAOsGiAsp00062_PCR_Spotting.xlsx`, `BAOsGiAsp00062_Pla_Spotting.xlsx`, `BAOsGiAsp00063_MM_Spotting.xslx`, `BAOsGiAsp00063_PCR_Spotting.xlsx`, `BAOsGiAsp00063_Pla_Spotting.xlsx`,

These are the pipetting protocols for ECHO Acoustic Liquid Handler (machine-readable files for dispensing volumes of master mix, PCR3 product and linearized plasmids for Gibson Assembly reaction).

+ `07_GiAS_Out/07_GiAS_imports/` directory, file `GiAS_import_date-time.xlsx`. It’s a database import file, containing all information on processed samples (from PCR3 to Gibson Assembly, together with `Unique_IDs` needed for the connection with upstream samples’ information in the database).

#### Other files needed by scripts

| Filename | Description                               |
|------------------|-------------------------------------------|
| `Scripts/config.py` | A configuration file to host all parameters (modifiable), used by all pipeline scripts. It includes directories, filenames, machine parameters or threshold settings, among others|
| `Scripts/utils/plt_manipulators.py` | An utility module that provides reusable and generic functionalities, here: functions related to manipulation of plate grids|
| `Scripts/utils/spotting_lists.py` | An utility module that provides reusable and generic functionalities, here: functions related to manipulation of pipetting protocols for automated sample handling|

## Adjusting the pipeline to your own needs

### Adjusting the parameters
There are several parameters residing in `config.py` file that can be adjusted to individual needs by simply modifying the variables:
+  volumes used in pipetting protocols (e.g., `primer_vol`, `template_vol` for PCR3 reactions) that can be modified depending of the reaction volumes
+ column names of any input/output/intermediate files used throughout the workflow (e.g., `cols_peak` of cELE readout files) can be adapted to other files’ layouts
+ filenames and directories
+ file formats: for example, it is possible to modify the variable `all_cele_parsed` to search through files with a chosen extension (here `.xlsx`)
+ Upper/lower thresholds of cELE band size can be set by modifying variables `treshold_upper_bp` and `treshold_lower_bp`

You can also add:
+ Your own parameters to `config.py`
+ Your own data processing functions to the modules in `utils/` directory
+ Your own data processing scripts downstream or upstream in the pipeline. You can use existing modules from `utils/` in your scripts by passing your own arguments (e.g., your custom barcodes).

You should modify `requirements.txt` based on the packages used by your own scripts.

### Adjusting the pipeline to manual (low-throughput) workflows

The number of samples that can be processed at once can be adjusted to accommodate low-throughput workflows. This can be done by modifying the `chunk_96` in `config.py` (here set to handle samples in 96-well format). The script will calculate the number of plates (chunks containing a designated number of samples) automatically. 

### Adapting the pipeline to other database systems

This pipeline is designed to fit our own database system. Therefore, the scripts handle the flow of samples through the set of interconnected tables in the backend of the database. For that purpose, most of the files contain the unique IDs per sample, as well as (non-unique) FK_IDs (foreign keys). If your system works in similar way and you can provide unique IDs to connect your data across the tables, the scripts could (theoretically) be adjusted to your needs. 

Please have a look at the file `Dictionary_IDs.xlsx` in dir `04_Parse_Out/ID_Dictionary` and the files in dir `PCR3_Store_Lists` to get a better understanding how the connection is handled. 

Columns `aBASE_ID`, `Seq1_Name_heavy`, `Seq1_Name_kappa`, `Seq1_Name_Lambda` in `Dictionary_IDs.xlsx` and col `Seq1_Name` in `PCR3_Store_Lists` are the ones that take care of the connection. `aBASE_ID` becomes a foreign key in the intermediate files in dir `05_PCR3_Out`. To get a glimpse on how the samples are being merged, please inspect [code lines 108 to 113](simplified_pipeline/Scripts/05_PCR3.py#L108-L113) and [code lines 135 to 138](simplified_pipeline/Scripts/05_PCR3.py#L135-L138) in `05_PCR3.py` script. Although a full reuse of the script to accommodate your database system probably would not be possible, you can get to know how we do it and hopefully get some ideas for your pipelines.

## References

[1] Preprint on Biorxiv and [DOI](link)
