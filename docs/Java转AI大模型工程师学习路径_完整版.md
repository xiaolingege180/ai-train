# Java转AI大模型工程师完整学习路径（详细版）

> 适用于有Java全栈基础的工程师转型  
> 预计周期：16-20周  
> 每日投入：工作日2-3小时，周末6-8小时

---

## 前言：你的优势与定位

### 为什么Java程序员转AI有优势？

| 你的现有技能 | 在AI领域的价值 |
|-------------|---------------|
| Spring Boot/微服务 | 搭建模型推理服务、API网关、限流熔断 |
| MySQL/Redis/MQ | RAG系统的向量数据库选型、缓存策略、异步队列 |
| Docker/K8s | 模型部署、弹性扩缩容、多卡调度 |
| 业务理解能力 | 把模型需求翻译成技术方案，避免算法与业务脱节 |

### 目标岗位定位

**首选方向（发挥工程优势）：**
- AI应用工程师（大模型应用开发）
- LLM后端工程师（推理优化、服务部署）
- AI Infra工程师（分布式训练框架、K8s调度）

**次要方向（需要补算法理论）：**
- 大模型算法工程师（预训练、微调）

---

## 第一阶段：基础补课（第1-6周）

### Week 1：Python熟练度速成

**学习目标：**
- 忘记Java思维，建立Pythonic编程习惯
- 熟练常用的数据结构和语法特性

**学习资源：**
1. 廖雪峰Python3教程（重点：函数式编程、装饰器）
2. Python Cookbook（第1、4、7章）

**实践任务：**

**任务1：重写Java工具类**
```python
from typing import List, Callable, TypeVar

T = TypeVar('T')
R = TypeVar('R')

def filter_and_transform(data: List[T], 
                         filter_fn: Callable[[T], bool],
                         transform_fn: Callable[[T], R]) -> List[R]:
    return [transform_fn(x) for x in data if filter_fn(x)]

# 使用示例
data = ["apple", "banana", "cherry"]
result = filter_and_transform(
    data,
    lambda x: len(x) > 5,
    lambda x: x.upper()
)
print(result)  # ['BANANA', 'CHERRY']
```

**任务2：装饰器实战**
```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.2f}s")
        return result
    return wrapper

@timer
def train_model(epochs):
    time.sleep(1)

train_model(10)  # 输出: train_model took 1.00s
```

**验收标准：**
- [ ] 能写列表/字典推导式
- [ ] 理解装饰器原理
- [ ] 会用yield实现惰性求值

---

### Week 2-3：深度学习基础

**学习目标：**
- 理解神经网络基本原理
- 熟练使用PyTorch框架

**学习资源：**
- 吴恩达《深度学习》前3门课
- PyTorch官方60分钟入门

**核心概念：**

| 概念 | 说明 |
|------|------|
| 反向传播 | 链式法则计算梯度 |
| ReLU | 激活函数，计算快 |
| Adam | 自适应优化器 |
| Batch Norm | 标准化层输入 |

**实践任务：**

从零实现神经网络：
```python
import torch
import torch.nn as nn

class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x
```

---

### Week 4-6：Transformer核心原理

**学习目标：**
- 深入理解Attention机制
- 能从头实现Transformer

**学习资源：**
- 论文：《Attention Is All You Need》
- 代码：The Annotated Transformer

**Self-Attention实现：**
```python
import torch
import torch.nn as nn
import math

class SelfAttention(nn.Module):
    def __init__(self, d_model):
        super().__init__()
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
    
    def forward(self, x, mask=None):
        Q = self.W_q(x)
        K = self.W_k(x)
        V = self.W_v(x)
        
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_model)
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        
        attention_weights = torch.softmax(scores, dim=-1)
        output = torch.matmul(attention_weights, V)
        return output, attention_weights
```

**Multi-Head Attention：**
```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        assert d_model % num_heads == 0
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
    
    def split_heads(self, x):
        batch_size, seq_len, _ = x.size()
        return x.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
    
    def forward(self, query, key, value, mask=None):
        Q = self.split_heads(self.W_q(query))
        K = self.split_heads(self.W_k(key))
        V = self.split_heads(self.W_v(value))
        
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        
        attention_weights = torch.softmax(scores, dim=-1)
        output = torch.matmul(attention_weights, V)
        
        output = output.transpose(1, 2).contiguous().view(query.size(0), -1, self.d_model)
        return self.W_o(output), attention_weights
```

**输出物：**
- [ ] 博客：《从零实现Transformer》
- [ ] 完整可运行代码

---

## 第二阶段：LLM实战（第7-14周）

### Week 7-9：大模型微调（Fine-tuning）

**LoRA原理：**
```
原始参数：W ∈ R^(d×k)
LoRA参数：W' = W + BA，其中B∈R^(d×r), A∈R^(r×k), r<<d
```

**关键超参数：**
- r（rank）：8, 16, 32, 64
- lora_alpha：缩放因子，通常=2*r
- target_modules：q_proj, v_proj等

**完整代码：**
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import BitsAndBytesConfig

# 1. 加载模型
model_name = "Qwen/Qwen2-7B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

# 2. 4bit量化
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
)

# 3. 配置LoRA
model = prepare_model_for_kbit_training(model)
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)

# 4. 训练
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    optim="paged_adamw_8bit",
)

trainer = Trainer(model=model, args=training_args, train_dataset=dataset)
trainer.train()

# 5. 保存
model.save_pretrained("./lora_weights")
```

---

### Week 10-12：RLHF与对齐

**RLHF三阶段：**
1. SFT：有监督微调
2. Reward Modeling：训练奖励模型打分
3. PPO：用强化学习优化策略

**PPO训练代码：**
```python
from trl import PPOTrainer, PPOConfig

ppo_config = PPOConfig(
    model_name="your-sft-model",
    learning_rate=1e-5,
    batch_size=8,
)

ppo_trainer = PPOTrainer(
    config=ppo_config,
    model=model,
    ref_model=ref_model,
    tokenizer=tokenizer,
)

for epoch in range(3):
    for batch in dataloader:
        queries = batch['query']
        response_tensors = ppo_trainer.generate(queries)
        rewards = reward_model(queries, response_tensors)
        stats = ppo_trainer.step(queries, response_tensors, rewards)
```

---

### Week 13-14：推理优化

**量化对比：**

| 精度 | 模型大小 | 推理速度 | 质量损失 |
|-----|---------|---------|---------|
| FP16 | 14GB | 1x | 0% |
| INT8 | 7GB | 1.5x | <1% |
| INT4 | 3.5GB | 2x | <3% |

**vLLM部署：**
```bash
pip install vllm

python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2-7B-Instruct \
    --tensor-parallel-size 1 \
    --max-num-seqs 256 \
    --port 8000
```

---

## 第三阶段：工程落地（第15-20周）

### Week 15-17：RAG系统开发

```python
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# 1. 加载文档
loader = PyPDFLoader("document.pdf")
documents = loader.load()

# 2. 分块
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
chunks = text_splitter.split_documents(documents)

# 3. 创建向量库
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-zh")
vectorstore = Chroma.from_documents(chunks, embeddings)

# 4. 检索
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
docs = retriever.get_relevant_documents("查询问题")
```

---

### Week 18-20：Agent开发

```python
import openai

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取城市天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                },
                "required": ["city"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)
```

---

## 第四阶段：求职准备（第21-24周）

### 必备项目
1. **领域大模型**：完整数据→训练→评估流程
2. **RAG知识库**：线上可访问Demo
3. **Agent助手**：多工具调用自动化

### 面试必会

**手撕代码：**
- Multi-Head Attention
- Layer Normalization
- KV Cache优化
- Beam Search

**系统设计：**
- 高并发LLM服务平台
- RAG系统存储架构
- 模型版本管理

---

## 附录：资源汇总

### 推荐课程
| 课程 | 平台 | 优先级 |
|-----|------|-------|
| 吴恩达深度学习 | Coursera | ⭐⭐⭐⭐⭐ |
| 李宏毅机器学习 | B站 | ⭐⭐⭐⭐⭐ |

### 推荐论文
1. 《Attention Is All You Need》
2. 《LoRA: Low-Rank Adaptation》
3. 《Training language models to follow instructions》

---

**祝转型顺利！**
