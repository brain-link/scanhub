### What is a MAP (MONAI Application Package)?

A MONAI Application Package (MAP) is a specialized containerized application or service designed for medical AI applications. It is self-descriptive, meaning it contains all the necessary information about its structure, purpose, and requirements. MAPs are highly portable and are built to run consistently whether executed locally or deployed in a clinical environment. They adhere to Open Container Initiative standards and are compatible with Kubernetes, making them versatile and easy to integrate into various hosting environments.

#### How ScanHub Uses MAPs

In the ScanHub platform, MAPs serve as plugins for post-acquisition processing steps. For example, a MAP could be designed to reconstruct an acquired MRI k-space with respect to the specific sequence used during the scan. This allows for a seamless and efficient workflow, from data acquisition to post-processing and analysis.

For more details on MAPs, you can visit the [official MONAI guidelines](https://github.com/Project-MONAI/monai-deploy/blob/main/guidelines/monai-application-package.md).
