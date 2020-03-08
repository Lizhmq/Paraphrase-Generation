import os
import subprocess

dataset_path = '../paraphrasing-datasets/'
base_dir = 'data/'
datasets = ["mscoco/", "quora/", "twitter/", "wikianswers/"]
for s in datasets:
    if not os.path.isdir(base_dir + s):
        os.mkdir(base_dir + s)
    for sub in ["train/", "val/", "test/"]:
        if not os.path.isdir(base_dir + s + sub):
            os.mkdir(base_dir + s + sub)

with open("mapping.txt", "w") as f:
    for s in datasets:
        f.write("%s \t %s\n" % (dataset_path + s + "train_src.txt", base_dir + s + "train/src.txt"))
        f.write("%s \t %s\n" % (dataset_path + s + "train_tgt.txt", base_dir + s + "train/tgt.txt"))
        f.write("%s \t %s\n" % (dataset_path + s + "valid_src.txt", base_dir + s + "val/src.txt"))
        f.write("%s \t %s\n" % (dataset_path + s + "valid_tgt.txt", base_dir + s + "val/tgt.txt"))
        f.write("%s \t %s\n" % (dataset_path + s + "test_src.txt", base_dir + s + "test/src.txt"))
        f.write("%s \t %s\n" % (dataset_path + s + "test_tgt.txt", base_dir + s + "test/tgt.txt"))
command = ['java', 'edu.stanford.nlp.process.PTBTokenizer', '-ioFileList', '-preserveLines', 'mapping.txt']
subprocess.call(command)
print("Stanford CoreNLP Tokenizer has finished.")
os.remove("mapping.txt")
