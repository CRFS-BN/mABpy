# mABpy
[![DOI](https://zenodo.org/badge/676124646.svg)](https://zenodo.org/badge/latestdoi/676124646)
> A Python data processing pipeline for high-throughput production of monoclonal antibodies
> 
This repository holds the python modules of the data processing pipeline for the production of monoclonal antibodies (mABs) from patient-derived, single B-cells, as described in [Gain efficiency with simple and automated data processing: Examples from a high-throughput workflow for the production of monoclonal antibodies](link_to_preprint)
## Table of contents
* [General info](#general-info)
* [Setup](#setup)
* [Reproducing the pipeline run](#reproducing-the-pipeline-run)
* [Contact](#contact)
* [References](#references)
## General info

This project contains the scripts that run the data processing concerned with wet-lab workflow steps from final PCR to purified plasmid pairs, as well as later wet-lab steps from HEK cell transfection to harvest and quantification of produced antibodies (refer to [1] for more details). 

The pipeline is customised to a high-throughput, semi-automated mABs production workflow and associated database. Therefore, the scripts are highly specific to the data processing and documentation performed in the mABs workflow in our lab. 

The code published here is thought to serve as **guidance in building similar pipelines in other setups**. We encourage the reader to get familiar with our paper before reproducing any pipeline steps. 

We recommend reproducing a [simplified, template pipeline](simplified_pipeline) that contains sample data processing steps. Within the simplified pipeline you can also find hints on how to adjust it to your own requirements. However, if you wish to download the whole pipeline, follow the steps below.
## Setup

### Installation instructions

Bodypy requires Python (3.7+), together with the following packages: pandas and numpy. You can install the necessary dependencies by following a few simple steps:

1.	Download the full pipeline [here](https://github.com/Malwoiniak/mABpy/archive/refs/heads/main.zip)
2.	Alternatively, you can clone the repository by running:

`git clone https://github.com/Malwoiniak/mABpy.git`

3.	Extract the contents of the zip files, if necessary.
4.	In terminal, navigate to the root directory of the extracted repository
5.	Create and activate a virtual environment, for example by using the Python build-in venv module:

**Linux/MacOS**
```
# Create a virtual environment named 'my_venv'
python3 -m venv my_venv

# Activate the virtual environment
source my_venv/bin/activate
```
**Windows**
```
# Create a virtual environment named 'my_venv'
python -m venv my_venv

# Activate the virtual environment
my_venv\Scripts\activate
```

6.	Install the project dependencies:

`(my_venv)$ pip install -r requirements.txt`

## Reproducing the pipeline run

The best way to reproduce the pipeline is to follow the comprehensive instructions in this [tutorial](link_to_manual). Below you can find an example explanation on how to run the script `05_PCR3.py`, which prepares the samples for a final PCR step (PCR3) and capillary electrophoresis (cELE), before cloning by Gibson Assembly (GiAS).

After downloading the pipeline, you will note that there are already some output files produced on each pipeline step. They serve as example of a complete pipeline run. Your files will be added to each step’s directory after the run. 
### What do you need?

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

    These are the pipetting protocols for automated liquid handler (machine-readable files for dispensing volumes of primers and templates for PCR3 reaction).

+ In `PCR3_Store_Lists/` directory, file `PCR3_StoreList_date-time.xlsx`. It’s a new store list of leftover samples that will now wait for the next round of PCR3

+ In `05_PCR3_Out/Intermed_Files/` directory, file `PCR3_Intermed_date-time.xlsx`. It’s an intermediate file that contains combined information on all samples that will be run in this PCR3 and cELE round. 

## Contact

Malwina Kotowicz: m_kotowicz@hotmail.com, feel free to contact me!

## References

[1] Preprint on Biorxiv and [DOI](link)

