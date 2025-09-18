import os
import jieba
import gensim
import re
import sys
class DocumentComparator:
    def __init__(self):
        jieba.initialize()  # 初始化jieba分词器
    def fetch_document_data(self, document_location):
        try:
            with open(document_location, 'r', encoding='UTF-8') as file_obj:
                return file_obj.read()
        except Exception as error:
            print(f"文档读取异常 {document_location}: {error}")
            return ""
    def process_content(self, content_data):
        if not content_data:  # 处理空字符串（包括空文件）
            return []
        segmented_data = jieba.lcut(content_data)  # 使用jieba进行中文分词
        filtered_result = []
        for segment in segmented_data:
            if re.match(r"[a-zA-Z0-9\u4e00-\u9fa5]", segment):  # 保留中/英文字符和数字
                filtered_result.append(segment)
        return filtered_result
    def compute_document_similarity(self, processed_data_1, processed_data_2):
        if not processed_data_1 and not processed_data_2:  # 处理两个文档都为空的情况
            return 1.0
        if not processed_data_1 or not processed_data_2:  # 处理任一文档为空的情况
            return 0.0
        documents_collection = [processed_data_1, processed_data_2]  # 准备文档集合用于构建词典
        try:
            vocabulary = gensim.corpora.Dictionary(documents_collection)  # 创建词典
            document_corpus = [vocabulary.doc2bow(doc) for doc in documents_collection]  # 创建文档向量
            similarity_measure = gensim.similarities.Similarity(
                'SimilarityMeasure', document_corpus, num_features=len(vocabulary)
            )  # 计算相似度
            test_corpus_data = vocabulary.doc2bow(processed_data_1)  # 将第一个文档转换为词袋模型
            similarity_score = similarity_measure[test_corpus_data][1]  # 计算与第二个文档的相似度
            return similarity_score
        except Exception as error:
            print(f"相似度计算异常: {error}")
            return 0.0
    def execute_comparison(self, source_doc_path, target_doc_path, result_output_path):
        if not os.path.exists(source_doc_path):  # 检查源文档是否存在
            print(f"源文档不存在: {source_doc_path}")
            return False
        if not os.path.exists(target_doc_path):  # 检查目标文档是否存在
            print(f"目标文档不存在: {target_doc_path}")
            return False
        source_content = self.fetch_document_data(source_doc_path)  # 读取源文档内容
        target_content = self.fetch_document_data(target_doc_path)  # 读取目标文档内容
        processed_source = self.process_content(source_content)  # 处理源文档内容
        processed_target = self.process_content(target_content)  # 处理目标文档内容
        similarity_value = self.compute_document_similarity(processed_source, processed_target)  # 计算相似度
        similarity_value = max(0.0, min(1.0, similarity_value))  # 确保在 [0,1] 范围内
        print(f"文档相似度: {similarity_value:.4f}")
        try:
            with open(result_output_path, 'w', encoding="utf-8") as output_file:
                output_file.write(f"{similarity_value:.4f}")  # 输出结果到文件
            print(f"结果输出至: {result_output_path}")
            return True
        except Exception as error:
            print(f"结果写入异常: {error}")
            return False
def primary_function():
    if len(sys.argv) != 4:  # 检查命令行参数数量
        print("执行命令: python main.py <源文档路径> <目标文档路径> <输出文件路径>")
        print("示例: python main.py original.txt modified.txt comparison_result.txt")
        sys.exit(1)
    original_document = sys.argv[1]  # 获取源文档路径参数
    modified_document = sys.argv[2]  # 获取目标文档路径参数
    output_document = sys.argv[3]  # 获取输出文件路径参数
    comparator = DocumentComparator()  # 创建文档比较器实例
    operation_status = comparator.execute_comparison(original_document, modified_document, output_document)  # 执行比较
    sys.exit(0 if operation_status else 1)  # 根据操作状态退出程序
if __name__ == '__main__':
    primary_function()  # 程序入口点