# -*- coding: utf-8 -*-
"""HashTag_Modeling사본.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JdS5BG4cSz1wN3t2xMzc58ykog6VheqN
"""

import pandas as pd
diary = pd.read_csv("C:/Users/user/Documents/EWHA/log/log/modelling/diary.csv", encoding='utf-8')

diary.head()

"""## HashTag Modelling"""

from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq,
)
from tokenizers import Tokenizer
from typing import Dict, List, Optional
from torch.utils.data import Dataset

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from IPython.display import display
from typing import Dict
import torch

model_name = "gogamza/kobart-base-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# max input
max(diary['요약'].map(lambda x: len(x)).to_list())

# max output
max(diary['해시태그'].map(lambda x: len(x)).to_list())

class HashTagMakerDataset(Dataset):
  def __init__(self,
               df: pd.DataFrame,
               tokenizer: Tokenizer
               ):
    self.df = df
    self.tokenizer = tokenizer

  def __len__(self):
    return len(self.df)

  def __getitem__(self, index):
    row = self.df.iloc[index, :]
    text1 = row[1]
    text2 = row[2]

    encoder_text = text1
    decoder_text = text2
    model_inputs = self.tokenizer(encoder_text, max_length=181, truncation=True)

    with self.tokenizer.as_target_tokenizer():
      labels = tokenizer(decoder_text, max_length=43, truncation=True)
    model_inputs['labels'] = labels['input_ids']
    del model_inputs['token_type_ids']

    return model_inputs

# Train, Test split - 현재는 이 과정 skip
from sklearn.model_selection import train_test_split

df_train, df_test = train_test_split(diary, test_size=0.1, random_state=42) # train, test 분리
print(len(df_train), len(df_test))

train_dataset = HashTagMakerDataset(df_train, tokenizer)
test_dataset = HashTagMakerDataset(df_test, tokenizer)

model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

data_collator = DataCollatorForSeq2Seq(tokenizer = tokenizer, model = model)

model_path = "C:/Users/user/Documents/EWHA/log/log/modelling/"

training_args = Seq2SeqTrainingArguments(
    output_dir=model_path,
    overwrite_output_dir=True,
    num_train_epochs=24,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    eval_steps=500,
    save_steps=1000,
    warmup_steps=300,
    prediction_loss_only=True,
    evaluation_strategy="steps",
    save_total_limit=3
    )

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

# GPU 사용 가능 -> 가장 빠른 번호 GPU, GPU 사용 불가 -> CPU 자동 지정 예시
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)
model.to(device)

print(model.device)

trainer.train()

trainer.save_model(model_path)

evaluation_results = trainer.evaluate(eval_dataset=test_dataset)

evaluation_results

loss = evaluation_results["eval_loss"]
print("평가 손실:", loss)

# 테스트할 문장
test_sentence = "명절을 맞아 고향에 돌아와 가족과 함께 보낸 특별하고 따뜻한 하루였다. 가족의 사랑과 고향의 소중함을 깨달았다."

# 입력 문장을 토큰화하여 인코딩
input_ids = tokenizer.encode(test_sentence, return_tensors="pt").to(device)

# 모델에 입력 전달하여 디코딩
output = model.generate(input_ids)

# 디코딩된 출력을 토크나이저를 사용하여 텍스트로 변환
decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)

# 결과 출력
print("입력 문장:", test_sentence)
print("모델 출력:", decoded_output)

def make_tag(text):
  # 입력 문장을 토큰화하여 인코딩
  input_ids = tokenizer.encode(text, return_tensors="pt").to(device)

  # 모델에 입력 전달하여 디코딩
  output = model.generate(input_ids).to(device)

  # 디코딩된 출력을 토크나이저를 사용하여 텍스트로 변환
  decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)

  # 결과 출력
  print("입력 문장:", text)
  print("모델 출력:", decoded_output)

make_tag(diary.iloc[-2,1])

make_tag(diary.iloc[-10,1])

make_tag(diary.iloc[-45,1])