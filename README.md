# REACT: Receptor-Enriched Analysis of functional Connectivity by Targets

The `react-fmri` software package allows to estimate target-enriched functional connectivity maps from functional MRI data using Positron Emission Tomography (PET) templates as spatial priors of the density distribution of neurotransmitters in the brain.

It is a two-step multivariate regression analysis:
 * Step 1: the PET maps are used as a set of spatial regressors to estimate the functional connectivity in terms of fitting the BOLD fluctuations across voxels with respect to the dominant fluctuation within each of these maps. The same resolution is required for the PET maps (i.e., spatial regressors) and the fMRI images (i.e., input data). Both fMRI data and the PET maps will be demeaned at this stage, before estimating the BOLD fluctuations, in order to obtain a good fit. This step requires a mask that restricts the analysis to the voxels for which the neurotransmitter density information is available. This mask can either be estimated independently or by using the `react_masks` command provided in this package.
 * Step 2: The BOLD fluctuations estimated in step 1 are used as a set of temporal regressors to estimate the subject-specific target-enriched functional connectivity maps. At this stage, the fMRI data (i.e., input data) and the BOLD fluctuations (i.e., design matrix) will be demeaned before estimating the functional maps; the design matrix columns will also be normalised to unit standard deviation. This stage requires a binary grey matter mask, which can be estimated independently or by using the `react_masks` command provided in this package.


## Usage
### To create the masks: `react_masks`

```shell_script
react_masks subject_list.txt pet_atlas.nii.gz gm_mask.nii.gz out_masks
```

* Input data (required to be all in the same standard space and with the same resolution):
- **subject_list.txt** is a text file that specifies which functional MRI data are to be used for the creation of the masks. Typically, it includes all the subjects of the dataset. An example is the [subject_list.txt]() file provided in the `examples` directory.
- **pet_atlas.nii.gz** is a 3D or 4D volume including one or more PET atlases to be used for the estimation of the target-enriched functional maps. Of note, the regions used as reference regions in the kinetic model for the quantification of the PET data should be masked out from the respective PET volume. An example is the [pet_atlas.nii.gz]() file provided in the `examples` directory, where the cerebellum was masked out as it was used as reference region.
- **gm_mask.nii.gz** is a grey matter mask. A grey matter image, [gm_mask.nii.gz](), is provided in the `examples` directory and can be used as input in this command. It was estimated by thesholding the probabilistic grey matter image provided by FSL at the intensity value of 77 in order to retain all voxels with a probability of at least 30% of being grey matter. The resulting thresholded image was then binarised.
* Output: 
The command will create two masks to be used as input in the `react` command. First, the script estimates a *dataset-specific mask* by intersecting all the subject-specific masks specified by the user in the subject_list.txt file and a *PET-specific mask* by intersecting all the PET atlases provided by the user in the pet_atlas.nii.gz file. Then, it will generate two masks:
- `mask_stage1.nii.gz`: intersection of the dataset-specific mask, PET-specific mask and grey matter mask gm_mask.nii.gz;
- `mask_stage2.nii.gz`: intersection of the dataset-specific mask and the grey matter mask gm_mask.nii.gz.

Once the two masks are generated, they can be used in `react` for the estimation of the subject-specific target-enriched functional maps.

### To run the target-enriched fMRI analysis: `react`

```shell_script
react subject001_fmri.nii.gz mask_stage1.nii.gz mask_stage2.nii.gz pet_atlas.nii.gz REACT/subject001
```

* Input data (required to be all in the same standard space and with the same resolution):
- **fmri_subject001.nii.gz** is the subject-specific 4D fMRI data set.
- **mask_stage1.nii.gz** is the mask used in the step 1 of the multivariate regression analysis.
- **mask_stage2.nii.gz** is the mask used in the step 2 of the multivariate regression analysis.
- **pet_atlas.nii.gz** is a 3D or 4D volume including one or more PET atlases to be used for the estimation of the target-enriched functional maps. Of note, the regions used as reference regions in the kinetic model for the quantification of the PET data should be masked out from the respective PET volume. An example is the [pet_atlas.nii.gz]() file provided in the `examples` directory, where the cerebellum was masked out as it was used as reference region.
* Outputs: 
The command will run the two-step multivariate regression analysis and generate: 
- `REACT/subject001_react_stage1.txt`: subject-specific time series associated to the PET atlases used as spatial regressors;
- `REACT/subject001_react_stage2.nii.gz`: subject-specific functional connectivity maps associated to the PET atlases provided as regressors. If the number of PET atlases is higher than 1, the 4D file subject001_react_stage2.nii.gz will be split into 3D files, e.g.:
	- subject001_react_stage2_IC0.nii.gz
	- subject001_react_stage2_IC1.nii.gz
	- subject001_react_stage2_IC2.nii.gz
- `REACT/subject001_react_stage2_Z.nii.gz`: if the optional argument --out_z is specified, the Fisher z-transformation will be applied to the `REACT/subject001_react_stage2.nii.gz` functional connectivity maps, producing a 4D file named `REACT/subject001_react_stage2_Z.nii.gz`


## Installation ... {MATTEO}
You can install the react-fmri software package using pypi by typing in your terminal:

* python3 -m pip install react-fmri 


### Dependencies
Recommended to use Anaconda Python distribution.
* numpy >=1.13
* scipy
* ... {MATTEO}


## Getting help
Write me an email or open an issue on github.

## Comparison with FSL
The `react-fmri` package is entirely based on python. If you want to check that the results match with the
FSL output (i.e., using the scripts from the original REACT paper) you just need to run the following commands:

```shell_script
fsl_glm -i subject001_fmri.nii.gz -d pet_atlas.nii.gz -o REACT/subject001_stage1.txt -m mask_stage1.nii.gz --demean
fsl_glm -i subject001_fmri.nii.gz -d REACT/subject001_stage1.txt -o REACT/subject001_stage2 -m mask_stage2.nii.gz --demean --des_norm
```

## How to cite REACT
* Primary Reference: Ottavia Dipasquale, Pierluigi Selvaggi, Mattia Veronese, Anthony S.Gabay, Federico Turkheimer, Mitul A. Mehta, "Receptor-Enriched Analysis of functional connectivity by targets (REACT): A novel, multimodal analytical approach informed by PET to study the pharmacodynamic response of the brain under MDMA", Neuroimage, Volume 195, 2019, Pages 252-260, ISSN 1053-8119, https://doi.org/10.1016/j.neuroimage.2019.04.007.
* Github Repository: 
