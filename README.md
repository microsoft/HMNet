# HMNet
This is the official code for the Microsoft's paper of HMNet model at EMNLP 2020. It is implemented under PyTorch framework. The related [paper](https://www.microsoft.com/en-us/research/uploads/prod/2020/04/MeetingNet_EMNLP_full.pdf) to cite is:

```
@Article{zhu2020a,
author = {Zhu, Chenguang and Xu, Ruochen and Zeng, Michael and Huang, Xuedong},
title = {A Hierarchical Network for Abstractive Meeting Summarization with Cross-Domain Pretraining},
year = {2020},
month = {November},
url = {https://www.microsoft.com/en-us/research/publication/end-to-end-abstractive-summarization-for-meetings/},
journal = {Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing},
}
```

# Finetune HMNet

It is recommended to run our model inside a docker:

Build docker image
```
cd Docker
sudo docker build . -t hmnet
```

Run container from image
```
sudo nvidia-docker run -it hmnet /bin/bash
```

Get the pretrained HMNet ready at `ExampleInitModel/HMNet-pretrained`. Please see [document](./ExampleInitModel/HMNet-pretrained/README.md).

Finetune on AMI dataset
```
CUDA_VISIBLE_DEVICES="0,1,2,3" mpirun -np 4 --allow-run-as-root python PyLearn.py train ExampleConf/conf_hmnet_AMI
```

The training log/model/settings could be found at `ExampleConf/conf_hmnet_AMI_conf~/run_1`

### Data paths

- `ExampleRawData/meeting_summarization/AMI_proprec`: The preprocessed AMI dataset. The `*.json` files point to the path to each split. Each folder (`train`, `dev` or `test`) contains the compressed chunks of data in the format for [infinibatch](https://github.com/microsoft/infinibatch).

- `ExampleRawData/meeting_summarization/ICSI_proprec`: Same as above for ICSI dataset.

- `ExampleInitModel/transfo-xl-wt103`: Here we only used the vocabulary from Transformer-XL, provided by [Huggingface](https://huggingface.co/transformers/model_doc/transformerxl.html).

# Evaluation

## Step 1: specify the model path

In `ExampleConf/conf_eval_hmnet_AMI`, for the line 
```
PYLEARN_MODEL ###
```

Replace `###` to the real checkpoint path. Use the relative path w.r.t the location of this configuration file. 

## Step 2: run the evaluate pipeline

```
CUDA_VISIBLE_DEVICES="0,1,2,3" mpirun -np 4 --allow-run-as-root python PyLearn.py evaluate ExampleConf/conf_eval_hmnet_AMI
```

The decoding results could be found at `ExampleConf/conf_eval_hmnet_AMI_conf~/run_1`

##  [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct)

## Trademarks
This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow Microsoft's Trademark & Brand Guidelines. Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos are subject to those third-party's policies.

<!-- BEGIN MICROSOFT SECURITY.MD V0.0.3 BLOCK -->

## Security

Microsoft takes the security of our software products and services seriously, which includes all source code repositories managed through our GitHub organizations, which include [Microsoft](https://github.com/Microsoft), [Azure](https://github.com/Azure), [DotNet](https://github.com/dotnet), [AspNet](https://github.com/aspnet), [Xamarin](https://github.com/xamarin), and [our GitHub organizations](https://opensource.microsoft.com/).

If you believe you have found a security vulnerability in any Microsoft-owned repository that meets Microsoft's [Microsoft's definition of a security vulnerability](https://docs.microsoft.com/en-us/previous-versions/tn-archive/cc751383(v=technet.10)), please report it to us as described below.

## Reporting Security Issues

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them to the Microsoft Security Response Center (MSRC) at [https://msrc.microsoft.com/create-report](https://msrc.microsoft.com/create-report).

If you prefer to submit without logging in, send email to [secure@microsoft.com](mailto:secure@microsoft.com).  If possible, encrypt your message with our PGP key; please download it from the the [Microsoft Security Response Center PGP Key page](https://www.microsoft.com/en-us/msrc/pgp-key-msrc).

You should receive a response within 24 hours. If for some reason you do not, please follow up via email to ensure we received your original message. Additional information can be found at [microsoft.com/msrc](https://www.microsoft.com/msrc).

Please include the requested information listed below (as much as you can provide) to help us better understand the nature and scope of the possible issue:

  * Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
  * Full paths of source file(s) related to the manifestation of the issue
  * The location of the affected source code (tag/branch/commit or direct URL)
  * Any special configuration required to reproduce the issue
  * Step-by-step instructions to reproduce the issue
  * Proof-of-concept or exploit code (if possible)
  * Impact of the issue, including how an attacker might exploit the issue

This information will help us triage your report more quickly.

If you are reporting for a bug bounty, more complete reports can contribute to a higher bounty award. Please visit our [Microsoft Bug Bounty Program](https://microsoft.com/msrc/bounty) page for more details about our active programs.

## Preferred Languages

We prefer all communications to be in English.

## Policy

Microsoft follows the principle of [Coordinated Vulnerability Disclosure](https://www.microsoft.com/en-us/msrc/cvd).

<!-- END MICROSOFT SECURITY.MD BLOCK -->
