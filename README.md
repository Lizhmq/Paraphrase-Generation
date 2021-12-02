## Paraphrase Generation

仓库整理了Paraphrase Generation的三个baseline模型：
pointer-generator network, reinforcement learning, DiPS.

#### Pointer-Generator

Pointer-Generator是论文"Get To The Point: Summarization with Pointer-Generator Networks(ACL 17)"提出的模型，是copy-generate模型的SOTA工作。其代码开源在[Github/abisee](https://github.com/abisee/pointer-generator)，原版本是python2环境，[Github/becxer](https://github.com/becxer/pointer-generator/)是其python3版fork，这个仓库的代码取自python3版本。

#### Reinforcement Learning

Reinforcement-Paraphrase-Genration是论文"An Empirical Comparison on Imitation Learning and Reinforcement Learning for Paraphrase Generation(EMNLP 19)"的工作，代码开源在[Github/wyu-du](https://github.com/wyu-du/Reinforce-Paraphrase-Generation)。论文中对比了Reinforce算法和Dagger算法在复述生成任务上的表现，方法是先用交叉熵loss预训练，再用Reinforce/Dagger进行fine-tuning.

#### DiPS

DiPS是论文"Submodular optimization-based diverse paraphrasing and its effectiveness in data augmentation(NAACL 19)"提出的工作，代码开源在[Github/malllabiisc](https://github.com/malllabiisc/DiPS)，其采用普通的训练方式，在decoding时用定义的启发式函数为评估做beam search。

## 运行方式

#### 数据获取

数据集的获取见[paraphrasing-datasets](https://github.com/Lizhmq/Paraphrasing-Datasets)，按照[paraphrasing-datasets](https://github.com/Lizhmq/Paraphrasing-Datasets)的指示运行make_datafiles.py可以得到处理后的数据。

运行后：

pointer-generator和RL需要预处理过的数据，将processed目录复制到pointer-generator或RL的data目录下即可。

注：pointer-generator处理数据时需要在target sentence前后加上\<s>和\</s>，取消make_datafiles.py中get_arg_abs函数中的注释即可。而RL工作不需要。

DiPS需要将切词后的数据按照(train/val/test)/(src/tgt).txt分开放置，执行DiPS/process.py可以完成。

#### 运行环境

前两个模型的运行环境如下：

```
# python3
torch
tensorflow-gpu==1.15
pyrouge
nltk
```

DiPS的运行环境参照github介绍安装requirements.txt中的内容。注：其中pkg-resources==0.0.0在Arnold环境下pip3安装失败，删去这个包的需求后可以正常运行，因此在DiPS/requirements.txt删去了这一行。

#### 运行脚本

更多信息可参考引用的Github仓库。

**pointer-generator**

超参数可修改run_summarization.py或通过命令行运行参数修改。

```
# training
python3 run_summarization.py --mode=train --data_path=/path/to/chunked/train_* --vocab_path=/path/to/vocab --log_root=/path/to/a/log/directory --exp_name=myexperiment
# concurrent eval
python3 run_summarization.py --mode=eval --data_path=/path/to/chunked/val_* --vocab_path=/path/to/vocab --log_root=/path/to/a/log/directory --exp_name=myexperiment
# decoding
python3 run_summarization.py --mode=decode --data_path=/path/to/chunked/val_* --vocab_path=/path/to/vocab --log_root=/path/to/a/log/directory --exp_name=myexperiment
```

注：pointer-generator的代码比较陈旧，训练时可能出现Nan，详情见引用Github仓库。

**Reinforcement Learning**

训练算法（预训练/强化训练）和其他超参数通过config.py修改。

```
# pretraining
python3 train.py
# fine-tuning
python3 train.py -m ../log_xxxxxx/best_model/model_best_xxxxxx
# decoding
python3 -u decode.py ../log_xxxxxx/best_model/model_best_xxxxxx
```

**DiPS**

超参数可修改args.py或通过命令行运行参数修改。

```
# training
python3 -m src.main -mode train -gpu 0 -use_attn -bidirectional -dataset quora -run_name <run_name>
# Create dictionary for submodular subset selection
python3 -m src.create_dict -model trained -run_name <run_name> -gpu 0
# decoding
python3 -m src.main -mode decode -selec submod -dataset <dataset> -run_name <run_name> -beam_width 10 -gpu 0
```

#### 结果

[NMT-Eval](https://github.com/Lizhmq/nmt-eval)包含计算BLEU,ROUGE指标的脚本和保存的模型、生成输出。
