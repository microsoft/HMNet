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

- `ExampleRawData/meeting_summarization/AMI_proprec`: The preprocessed AMI dataset. The `*.json` files point to the path to each split. Each folder (`train`, `dev` or `test`) contains the compressed chunks of data in the format for infinibatch.

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