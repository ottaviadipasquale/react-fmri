# REACT: Receptor-Enriched Analysis of functional Connectivity by Targets

[![DOI](https://zenodo.org/badge/362894234.svg)](https://zenodo.org/badge/latestdoi/362894234)

![Graphical abstract](https://user-images.githubusercontent.com/79755700/116727558-a0c38700-a9dc-11eb-8ecc-28b3446b9d11.jpg)

The `react-fmri` software package allows to estimate target-enriched functional 
connectivity maps from functional MRI data using Positron Emission Tomography 
(PET) templates as spatial priors of the density distribution of 
neurotransmitters in the brain.

This software is coded in pure Python, its code is available on 
[Github](https://github.com/ottaviadipasquale/react-fmri), it can be installed 
via [Pypi](https://pypi.org/project/react-fmri/)
and it is released under 
[MIT License](https://github.com/ottaviadipasquale/react-fmri/blob/main/LICENSE).

It is implemented as a two-step multivariate regression analysis:
 * **Step 1**: the PET maps are used as a set of spatial regressors to estimate the 
 functional connectivity in terms of fitting the BOLD fluctuations across voxels 
 with respect to the dominant fluctuation within each of these maps. The same 
 resolution is required for the PET maps (i.e., spatial regressors) and the fMRI 
 images (i.e., input data). Both fMRI data and the PET maps will be demeaned at 
 this stage, before estimating the BOLD fluctuations, in order to obtain a good 
 fit. This step requires a mask that restricts the analysis to the voxels for 
 which the neurotransmitter density information is available. This mask can 
 either be estimated independently or by using the `react_masks` command 
 provided in this package.
 * **Step 2**: The BOLD fluctuations estimated in Step 1 are used as a set of 
 temporal regressors to estimate the subject-specific target-enriched functional
 connectivity maps. At this stage, the fMRI data (i.e., input data) and the BOLD 
 fluctuations (i.e., design matrix) will be demeaned before estimating the 
 functional maps; the design matrix columns will also be normalised to unit 
 standard deviation. This stage requires a binary grey matter mask, which can 
 be estimated independently or by using the `react_masks` command provided in 
 this package.


## Usage
### To normalize the PET atlases: `react_normalize`

```shell_script
react_normalize original_pet_atlas.nii.gz pet_atlas.nii.gz
```

* Input data (required to be in standard space):
    - `original_pet_atlas.nii.gz` is a 3D or 4D volume including one or more 
    PET atlases to be used for the estimation of the target-enriched functional 
    maps. Of note, the regions used as reference regions in the kinetic model 
    for the quantification of the PET data should be masked out from the 
    respective PET volume. An example is the 
    [pet_atlas.nii.gz](https://github.com/ottaviadipasquale/react-fmri/blob/main/data/pet_atlas.nii.gz) 
    file provided in the `data` directory, where the cerebellum was masked 
    out as it was used as reference region. All values < 0 will be set at 0. 
* Output: 
The command will normalize each PET atlas included in the original_pet_atlas.nii.gz
file by shifting the minimum value to zero and rescaling the resulting values by 
the span between the minimum and the maximum values of the image. Then, it will 
generate:
    - `pet_atlas.nii.gz`: normalised version of  `original_pet_atlas.nii.gz`. 
    The order of the PET atlases is the same as the one in the original file.
The optional argument -v will output the min and max values for each PET map.

### To create the masks: `react_masks`

```shell_script
react_masks subject_list.txt pet_atlas.nii.gz gm_mask.nii.gz out_masks
```

* Input data (required to be all in the same standard space and with the same 
resolution):
    - `subject_list.txt` is a text file that specifies which functional MRI 
    data are to be used for the creation of the masks. Typically, it includes 
    all the subjects of the dataset. An example is the 
    [subject_list.txt](https://github.com/ottaviadipasquale/react-fmri/blob/main/data/subject_list.txt) 
    file provided in the `data` directory.
    - `pet_atlas.nii.gz` is a 3D or 4D volume including one or more PET 
    atlases to be used for the estimation of the target-enriched functional 
    maps. Of note, the regions used as reference regions in the kinetic model 
    for the quantification of the PET data should be masked out from the 
    respective PET volume. An example is the 
    [pet_atlas.nii.gz](https://github.com/ottaviadipasquale/react-fmri/blob/main/data/pet_atlas.nii.gz) 
    file provided in the `data` directory, where the cerebellum was masked 
    out as it was used as reference region.
    - `gm_mask.nii.gz` is a grey matter mask. A grey matter image, 
    [gm_mask.nii.gz](https://github.com/ottaviadipasquale/react-fmri/blob/main/data/gm_mask.nii.gz), 
    is provided in the `data` directory and can be used as input in this 
    command. It was estimated by thesholding the probabilistic grey matter image 
    provided by FSL at the intensity value of 77 in order to retain all voxels 
    with a probability of at least 30% of being grey matter. The resulting 
    thresholded image was then binarised.
* Output: 
The command will create two masks to be used as input in the `react` command. 
First, the script estimates a *dataset-specific mask* by intersecting all the 
subject-specific masks specified by the user in the subject_list.txt file and a 
*PET-specific mask* by intersecting all the PET atlases provided by the user in 
the pet_atlas.nii.gz file. Then, it will generate two masks:
    - `mask_stage1.nii.gz`: intersection of the dataset-specific mask, 
    PET-specific mask and grey matter mask `gm_mask.nii.gz`;
    - `mask_stage2.nii.gz`: intersection of the dataset-specific mask and the 
    grey matter mask `gm_mask.nii.gz`.

Once the two masks are generated, they can be used in `react` for the estimation 
of the subject-specific target-enriched functional maps.


### To run the target-enriched fMRI analysis: `react`

```shell_script
react subject001_fmri.nii.gz mask_stage1.nii.gz mask_stage2.nii.gz pet_atlas.nii.gz REACT/subject001
```

* Input data (required to be all in the same standard space and with the same 
resolution):
    - `fmri_subject001.nii.gz` is the subject-specific 4D fMRI data set.
    - `mask_stage1.nii.gz` is the mask used in the step 1 of the multivariate 
    regression analysis.
    - `mask_stage2.nii.gz` is the mask used in the step 2 of the multivariate 
    regression analysis.
    - `pet_atlas.nii.gz` is a 3D or 4D volume including one or more PET 
    atlases to be used for the estimation of the target-enriched functional 
    maps. Of note, the regions used as reference regions in the kinetic model 
    for the quantification of the PET data should be masked out from the 
    respective PET volume. An example is the 
    [pet_atlas.nii.gz](https://github.com/ottaviadipasquale/react-fmri/blob/main/data/pet_atlas.nii.gz) 
    file provided in the `data` directory, where the cerebellum was masked 
    out as it was used as reference region. We recommend to rescale each PET 
    image in the [0,1] range after removing the reference region. This step can 
    be done using the `react_normalize` command.
    
* Output: The command will run the two-step multivariate regression analysis and 
generate: 
    - `REACT/subject001_react_stage1.txt`: subject-specific time series 
    associated to the PET atlases used as spatial regressors;
    - `REACT/subject001_react_stage2.nii.gz`: subject-specific functional 
    connectivity maps associated to the PET atlases provided as regressors. 
    If the number of PET atlases is higher than 1, the 4D file 
    `subject001_react_stage2.nii.gz` will be split into 3D files, e.g.:
        - `subject001_react_stage2_map0.nii.gz`
        - `subject001_react_stage2_map1.nii.gz`
        - `subject001_react_stage2_map2.nii.gz`

## Requirements
* python3
* numpy >= 1.15
* scipy >= 0.19.1
* nibabel >= 3.0.0
* scikit-learn >= 0.22

## Installation
You can install the `react-fmri` software package using Pypi by typing in your 
terminal:

```shell script
pip install react-fmri
``` 

However, we recommend to use REACT in a dedicated environment. If you are 
familiar with the Anaconda Python distribution, here's how you can safely 
install REACT without interfering with other local software.
```shell script
conda create -n react-fmri python=3
conda activate react-fmri
pip install react-fmri
```
Then you will need to activate the `react-fmri` environment for using REACT.
```shell script
conda activate react-fmri
react_masks ...
react ...
```

## Getting help
For help requests and bug reporting please use the 
[Github issues](https://github.com/ottaviadipasquale/react-fmri/issues/new) 
system.

## Comparison with FSL
The `react-fmri` package is entirely based on Python and does not need FSL to 
run. If you want to check that the results matches with the FSL output 
(i.e., using the scripts from the original REACT paper) you just need to run 
the following commands:

```shell_script
fsl_glm -i subject001_fmri.nii.gz -d pet_atlas.nii.gz -o REACT/subject001_stage1.txt -m mask_stage1.nii.gz --demean
fsl_glm -i subject001_fmri.nii.gz -d REACT/subject001_stage1.txt -o REACT/subject001_stage2 -m mask_stage2.nii.gz --demean --des_norm
```

## How to cite REACT
* **Primary Reference**: O. Dipasquale, P. Selvaggi, M. Veronese, 
A.S. Gabay, F. Turkheimer, M.A. Mehta, "Receptor-Enriched 
Analysis of functional connectivity by targets (REACT): A novel, multimodal 
analytical approach informed by PET to study the pharmacodynamic response of the 
brain under MDMA", Neuroimage 2019, 195, 252-260, 
https://doi.org/10.1016/j.neuroimage.2019.04.007.

* **Other References**:
    * O. Dipasquale, D. Martins, A. Sethi, M. Veronese, S. Hesse, M. Rullmann, 
    O. Sabri, F. Turkheimer, N.A. Harrison, M.A. Mehta, M. Cercignani, "Unravelling
    the effects of methylphenidate on the dopaminergic and noradrenergic functional 
    circuits", Neuropsychopharmacology 2020, 45 (9), 1482-1489,
    https://doi.org/10.1038/s41386-020-0724-x
    
    * M. Cercignani, O. Dipasquale, I. Bogdan, T. Carandini, J. Scott, W. Rashid, 
    O. Sabri, S. Hesse, M. Rullmann, L. Lopiano, M. Veronese, D. Martins, M. Bozzali,
    "Cognitive fatigue in multiple sclerosis is associated with alterations in the 
    functional connectivity of monoamine circuits", Brain Communications 2021, 
    3 (2), fcab023, https://doi.org/10.1093/braincomms/fcab023
    
    * D. Martins, M. Veronese, F.E. Turkheimer, M.A. Howard, S.C.R. Williams, 
    O. Dipasquale, "A candidate neuroimaging biomarker for detection of 
    neurotransmission-related functional alterations and prediction of 
    pharmacological analgesic response in chronic pain", BioRxiv, 
    https://doi.org/10.1101/2021.02.17.431572
    
* **Github Repository**: Ottavia Dipasquale and Matteo Frigo, "REACT-fMRI Python 
package", 2021, https://github.com/ottaviadipasquale/react-fmri/,
[DOI:10.5281/zenodo.4730559](https://zenodo.org/badge/latestdoi/362894234).



## Developers
* [Ottavia Dipasquale](https://ottaviadipasquale.github.io) - original REACT 
implementation in FSL
* [Matteo Frigo](https://matteofrigo.github.io) - porting to Python
