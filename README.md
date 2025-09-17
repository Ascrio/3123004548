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

 1.__init__():初始化jieba分词器
 2.fetch_document_data(): 读取文档内容
 3.process_content(): 对内容进行分词和预处理，同时构建词汇表
 4.compute_document_similarity(): 余弦相似度算法计算两个文档的相似度
 5.execute_comparison(): 执行完整的比较流程

 ### 辅助函数primary_function()则负责处理命令行参数和程序流程

 ### 各函数之间调用模块关系如下

 ## 算法设计
