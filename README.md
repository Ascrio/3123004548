# 3123004548软件工程第二次作业
<center>

| PSP2 1    | Personal Software Process Stages | 预估耗时（分钟） | 实际耗时（分钟） |
|---|---|---|---|
| Planning    | 计划    |15    |10    |
| Estimate    | 估计这个任务需要多少时间 | 330   | 355   |
| Development    | 开发    | 15   |15    |
| Analysis    | 需求分析（包括学习新技术） | 30   |30    |
| Design Spec    | 生成设计文档 | 10   | 10   |
| Design Review    | 设计复审 | 15   | 15   |
| Coding Standard   | 代码规范（为目前的开发制定合适的规范） | 10   | 20   |
| Design    | 具体设计 | 30   | 50   |
| Coding    | 具体编码 | 120   | 100   |
| Code Review    | 代码复审 |5    | 10   |
| Test    | 测试（自我测试，修改代码，提交修改） |15    | 30   |
| Reporting    | 报告    | 15   | 10   |
| Test Report    | 测试报告 | 15   | 10   |
| Size Measurement    | 计算工作量 | 20    | 25   |
| Postmortem & Process Improvement Plan | 事后总结，并提出过程改进计划 | 15   | 20   |

</center>

# 模块接口的设计与实现过程
 ## 设计概述

采用基于余弦相似度算法的词袋模型，设计了该论文查重功能，并通过DocumentComparator类来封装整个查重算法功能，并采用面向对象的方式组织代码，确保模块化和可维护性

 ## 函数设计以及调用模块展示
 ### 核心函数DocumentComparator类包括以下函数

 1._ init _():初始化jieba分词器
 
 2.fetch_document_data(): 读取文档内容
 
 3.process_content(): 对内容进行分词和预处理，同时构建词汇表
 
 4.compute_document_similarity(): 余弦相似度算法计算两个文档的相似度
 
 5.execute_comparison(): 执行完整的比较流程

 ### 辅助函数primary_function()则负责处理命令行参数和程序流程
 ### 各函数之间调用模块关系如下

<img width="5722" height="5824" alt="diagram" src="https://github.com/user-attachments/assets/3fb6d80d-f320-40e4-8548-63a4266eb713" />

 ## 算法设计于与流程展示

 1.对指定的文本进行jieba分词器处理，将文本处理成词语序列，同时过滤处理文本中出现的符号

 2.读取源文档和目标文档，并对两个文档进行分词和过滤处理

 3.使用gensim构建词袋模型(Bag-of-Words Model)

 4.计算文本余弦相似度，并将结果标准化到[0,1]范围

 5.输出结果至文件

 核心函数DocumentComparator 流程图如下

<img width="2663" height="6533" alt="4e4ac3f0d27a53bf62d2b7fc46da9462" src="https://github.com/user-attachments/assets/c7543c01-3c7c-4f70-8c60-fc16c0baf788" />

 算法的关键点在于文本分词以及词袋模型的构建，文本分词为文档转换成词频向量做了铺垫，而词袋模型的构建是文本查重算法实现的基础核心
 
 该算法实现简单，无需复杂的语义分析，适合处理大量文档，且对词序不敏感能够实现检测内容重复而非结构化抄袭，同时不依赖词典库

 # 模块接口的性能改进

 最初代码采用基于给定停用词列表的simhash算法，经运行后得出性能分析图如下
 
 <img width="2586" height="1356" alt="image" src="https://github.com/user-attachments/assets/2d06fa83-27f5-4662-841b-0ae07f6c93b7" />

 后经研究发现，代码对停用词列表高度依赖且算法因为反复查看停用词导致算法的时间成本耗费很大，同时存在多处函数开销极大的情况(如_find_and_load函数)

 同时，该算法存在无法区分差距较大的文本，导致即使文本完全不同，也有50%以上的相似度，如下图所示

<img width="1074" height="225" alt="image" src="https://github.com/user-attachments/assets/a625b142-94c6-4e72-8209-45bd688732c0" />
  
 经过代码改进，性能图如下

 <img width="2568" height="1362" alt="image" src="https://github.com/user-attachments/assets/cec5e924-4b20-4e4a-8a87-4b9a710dec9e" />

 可见，函数平均时间耗费有所降低，且函数利用得到有效提升

 同时，对于差异较大的文本，该算法能够完全区分并且以此给出较低的相似度

 <img width="1014" height="185" alt="image" src="https://github.com/user-attachments/assets/f97e6a30-04ee-4bd2-9e0d-45c8f49001b9" />

 在改进版的算法中，虽然消耗最大的函数依旧为_find_and_load函数，但是函数的平均开销相比前者有所降低，性能得到一定改进

 # 模块部分单元测试展示

 为了测试代码稳定性，设计了18处测试代码paperchecker.py，经测试改进代码已全部通过

 <img width="2386" height="1270" alt="image" src="https://github.com/user-attachments/assets/6b74e581-ee79-4f0c-a9a5-644da9d9bab4" />

 考虑篇幅限制，此处仅展示3处测试代码

 ## 测试一：对于完全相同的文本，相似度应为1
 
 ``` python
 def test_similarity_calculation_identical(self):
        text1 = "这是一个完全相同的测试文本"
        text2 = "这是一个完全相同的测试文本"
        processed1 = self.comparator.process_content(text1)
        processed2 = self.comparator.process_content(text2)
        similarity = self.comparator.compute_document_similarity(processed1, processed2)
        self.assertAlmostEqual(similarity, 1.0, delta=0.1)
 ```
 ## 测试二：对于完全不同的文本，相似度应小于0.4
 
 ``` python
 def test_similarity_calculation_different(self):
        text1 = "这是第一个测试文本，关于人工智能和机器学习"
        text2 = "恐惧是生物的本能，勇气是人类的赞歌"
        processed1 = self.comparator.process_content(text1)
        processed2 = self.comparator.process_content(text2)
        similarity = self.comparator.compute_document_similarity(processed1, processed2)
        self.assertLess(similarity, 0.4)
 ```
 ## 测试三：对于一个有文本的文件和一个没有文本的文件，相似度应为0

 ```python
    def test_one_empty_file_processing(self):
        content = "这是一个有内容的文件"
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_file1 = f.name
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            temp_file2 = f.name
        processed1 = self.comparator.process_content(content)
        processed2 = self.comparator.process_content("")
        similarity = self.comparator.compute_document_similarity(processed1, processed2)
        self.assertEqual(similarity, 0.0)
        os.unlink(temp_file1)
        os.unlink(temp_file2)
 ```
 测试结束后，以覆盖率(pycharm自带功能)运行代码，结果如下图所示

 <img width="872" height="100" alt="f7a92ba751826db10221f3e8a3df46c1" src="https://github.com/user-attachments/assets/4d36a7a8-5f96-4679-839b-ed08130d902f" />

 # 模块部分异常处理说明

 ## 异常一：文档读取阶段异常
 目标：当用户传入的文档路径无效（如文件不存在、无权限、编码错误等），避免程序因 FileNotFoundError、UnicodeDecodeError等异常而中断
 处理方式：使用 try-except捕获所有可能的读取异常，打印具体错误信息，并返回空字符串 ""作为兜底内容
 ```python
 def fetch_document_data(self, document_location):
    try:
        with open(document_location, 'r', encoding='UTF-8') as file_obj:
            return file_obj.read()
    except Exception as error:
        print(f"文档读取异常 {document_location}: {error}")
        return ""
 ```
 对应代码测试片段如下
 ```python
 class TestDocumentFetcher(unittest.TestCase):
    def test_fetch_nonexistent_file(self):
        comparator = DocumentComparator()
        result = comparator.fetch_document_data("dummy_nonexistent_file_12345.txt")
        self.assertEqual(result, "")  # 应返回空字符串
 ```
 ## 异常二：内容处理阶段异常
 目标：对读取到的原始内容进行分词和过滤，但如果传入的内容为空（比如上个阶段读取失败返回了 ""），则直接返回空列表，避免后续处理出错。
 处理方式​​：首先判断 content_data是否为空，如果是，则返回空列表 []，而不是继续分词。
 ```python
 def process_content(self, content_data):
    if not content_data:  # 处理空字符串（包括空文件）
        return []
    segmented_data = jieba.lcut(content_data)
    filtered_result = []
    for segment in segmented_data:
        if re.match(r"[a-zA-Z0-9\u4e00-\u9fa5]", segment):  # 保留中/英文字符和数字
            filtered_result.append(segment)
    return filtered_result
 ```
 对应代码测试片段如下
 ```python
 def test_process_empty_content(self):
    comparator = DocumentComparator()
    result = comparator.process_content("")
    self.assertEqual(result, [])  # 空内容应返回空列表
 ```
