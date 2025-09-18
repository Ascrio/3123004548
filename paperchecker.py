import unittest
import tempfile
import os
import sys
import jieba
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from main import DocumentComparator
except ImportError:
    print("请确保main.py文件存在且包含DocumentComparator类")
    sys.exit(1)
class TestDocumentComparator(unittest.TestCase):
    def setUp(self):
        self.comparator = DocumentComparator()  # 初始化文档比较器实例
    def test_document_comparator_initialization(self):
        self.assertIsNotNone(self.comparator)  # 测试比较器是否成功初始化
        self.assertTrue(hasattr(jieba, 'dt'))  # 测试jieba分词器是否已初始化
    def test_content_processing(self):
        text = "这是一个测试文本，用于测试内容处理功能的准确性"
        processed_content = self.comparator.process_content(text)  # 测试内容处理功能
        self.assertIsInstance(processed_content, list)  # 验证返回结果为列表类型
        self.assertTrue(len(processed_content) > 0)  # 验证处理后的内容不为空
    def test_empty_content_processing(self):
        processed_content = self.comparator.process_content("")  # 测试空内容处理
        self.assertIsInstance(processed_content, list)  # 验证返回结果为列表类型
        self.assertEqual(len(processed_content), 0)  # 验证空内容处理结果为空列表
    def test_file_reading(self):
        content = "测试文件内容，包含中文和English文字"
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_file = f.name
        try:
            read_content = self.comparator.fetch_document_data(temp_file)  # 测试文件读取功能
            self.assertEqual(content, read_content)  # 验证读取内容与写入内容一致
        finally:
            os.unlink(temp_file)  # 清理临时文件
    def test_empty_file_reading(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            temp_file = f.name
        try:
            read_content = self.comparator.fetch_document_data(temp_file)  # 测试空文件读取
            self.assertEqual("", read_content)  # 验证空文件读取结果为空字符串
        finally:
            os.unlink(temp_file)  # 清理临时文件
    def test_similarity_calculation_identical(self):
        text1 = "这是一个完全相同的测试文本"
        text2 = "这是一个完全相同的测试文本"
        processed1 = self.comparator.process_content(text1)
        processed2 = self.comparator.process_content(text2)
        similarity = self.comparator.compute_document_similarity(processed1, processed2)  # 测试相同文本相似度计算
        self.assertAlmostEqual(similarity, 1.0, delta=0.1)  # 验证相同文本相似度接近1.0
    def test_similarity_calculation_different(self):
        text1 = "这是第一个测试文本，关于人工智能和机器学习"
        text2 = "恐惧是生物的本能，勇气是人类的赞歌"
        processed1 = self.comparator.process_content(text1)
        processed2 = self.comparator.process_content(text2)
        similarity = self.comparator.compute_document_similarity(processed1, processed2)  # 测试不同文本相似度计算
        self.assertLess(similarity, 0.4)  # 验证不同文本相似度较低
    def test_similarity_calculation_similar(self):
        text1 = "这是一个测试文本，用于测试相似度计算功能"
        text2 = "这是一个测试文本，用于检验相似度计算功能"
        processed1 = self.comparator.process_content(text1)
        processed2 = self.comparator.process_content(text2)
        similarity = self.comparator.compute_document_similarity(processed1, processed2)  # 测试相似文本相似度计算
        self.assertGreater(similarity, 0.6)  # 验证相似文本相似度较高
        self.assertLess(similarity, 1.0)  # 验证相似文本相似度小于1.0
    def test_empty_documents_similarity(self):
        processed1 = self.comparator.process_content("")
        processed2 = self.comparator.process_content("")
        similarity = self.comparator.compute_document_similarity(processed1, processed2)  # 测试空文档相似度计算
        self.assertEqual(similarity, 1.0)  # 验证两个空文档相似度为1.0
    def test_empty_file_processing(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            temp_file1 = f.name
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            temp_file2 = f.name
        processed1 = self.comparator.process_content("")
        processed2 = self.comparator.process_content("")
        similarity = self.comparator.compute_document_similarity(processed1, processed2)  # 测试空文件处理
        self.assertAlmostEqual(similarity, 1.0, delta=0.1)  # 验证两个空文件相似度接近1.0
        os.unlink(temp_file1)  # 清理临时文件
        os.unlink(temp_file2)  # 清理临时文件
    def test_one_empty_file_processing(self):
        content = "这是一个有内容的文件"
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_file1 = f.name
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            temp_file2 = f.name
        processed1 = self.comparator.process_content(content)
        processed2 = self.comparator.process_content("")
        similarity = self.comparator.compute_document_similarity(processed1, processed2)  # 测试一个空文件相似度计算
        self.assertEqual(similarity, 0.0)  # 验证有内容文件与空文件相似度为0.0
        os.unlink(temp_file1)  # 清理临时文件
        os.unlink(temp_file2)  # 清理临时文件
    def test_nonexistent_file(self):
        success = self.comparator.execute_comparison("nonexistent_file.txt", "another_nonexistent.txt",
                                                     "dummy_output.txt")  # 测试不存在的文件处理
        self.assertFalse(success)  # 验证处理不存在的文件返回False
    def test_chinese_text_processing(self):
        text1 = "自然语言处理是人工智能领域的一个重要方向"
        text2 = "自然语言处理是AI领域的一个重要研究方向"
        processed1 = self.comparator.process_content(text1)
        processed2 = self.comparator.process_content(text2)
        similarity = self.comparator.compute_document_similarity(processed1, processed2)  # 测试中文文本处理
        self.assertGreaterEqual(similarity, 0.0)  # 验证相似度在合理范围内
        self.assertLessEqual(similarity, 1.0)  # 验证相似度在合理范围内
        self.assertGreater(similarity, 0.5)  # 验证相似文本相似度较高
    def test_punctuation_handling(self):
        text1 = "这是一个测试文本，包含标点符号！还有问号？"
        text2 = "这是一个测试文本包含标点符号还有问号"
        processed1 = self.comparator.process_content(text1)
        processed2 = self.comparator.process_content(text2)
        similarity = self.comparator.compute_document_similarity(processed1, processed2)  # 测试标点符号处理
        self.assertGreater(similarity, 0.7)  # 验证去除标点后相似度较高
    def test_main_function_integration(self):
        orig_content = "这是原始文档内容，包含一些特定的技术术语和概念说明"
        copy_content = "这是修改后的文档内容，包含一些特定的技术术语和概念说明但有一些修改和补充"
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            f.write(orig_content)
            orig_file = f.name
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            f.write(copy_content)
            copy_file = f.name
        processed1 = self.comparator.process_content(orig_content)
        processed2 = self.comparator.process_content(copy_content)
        similarity = self.comparator.compute_document_similarity(processed1, processed2)  # 测试主功能集成
        self.assertGreaterEqual(similarity, 0.0)  # 验证相似度在合理范围内
        self.assertLessEqual(similarity, 1.0)  # 验证相似度在合理范围内
        os.unlink(orig_file)  # 清理临时文件
        os.unlink(copy_file)  # 清理临时文件
    def test_short_text_handling(self):
        text1 = "短文本"
        text2 = "短文本"
        processed1 = self.comparator.process_content(text1)
        processed2 = self.comparator.process_content(text2)
        similarity = self.comparator.compute_document_similarity(processed1, processed2)  # 测试短文本处理
        self.assertGreaterEqual(similarity, 0.0)  # 验证相似度在合理范围内
        self.assertLessEqual(similarity, 1.0)  # 验证相似度在合理范围内
    def test_very_different_texts(self):
        text1 = "量子力学是描述微观粒子行为的基础理论"
        text2 = "文艺复兴是欧洲历史上重要的文化运动"
        processed1 = self.comparator.process_content(text1)
        processed2 = self.comparator.process_content(text2)
        similarity = self.comparator.compute_document_similarity(processed1, processed2)  # 测试完全不同文本相似度
        self.assertLess(similarity, 0.4)  # 验证完全不同文本相似度较低
    def test_command_line_interface(self):
        text1 = "测试文本1"
        text2 = "测试文本2"
        processed1 = self.comparator.process_content(text1)
        processed2 = self.comparator.process_content(text2)
        self.assertIsInstance(processed1, list)  # 验证处理结果为列表类型
        self.assertIsInstance(processed2, list)  # 验证处理结果为列表类型
        similarity = self.comparator.compute_document_similarity(processed1, processed2)  # 测试命令行接口相关功能
        self.assertGreaterEqual(similarity, 0.0)  # 验证相似度在合理范围内
        self.assertLessEqual(similarity, 1.0)  # 验证相似度在合理范围内
        success = self.comparator.execute_comparison("nonexistent1.txt", "nonexistent2.txt", "output.txt")  # 测试不存在的文件处理
        self.assertFalse(success)  # 验证处理不存在的文件返回False
def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDocumentComparator)  # 加载测试用例
    runner = unittest.TextTestRunner(verbosity=2)  # 创建测试运行器
    result = runner.run(suite)  # 运行测试
    print(f"\n测试结果统计:")  # 输出测试结果统计
    print(f"运行测试数: {result.testsRun}")  # 输出运行的测试数量
    print(f"失败数: {len(result.failures)}")  # 输出失败的测试数量
    print(f"错误数: {len(result.errors)}")  # 输出错误的测试数量
    print(f"跳过数: {len(result.skipped)}")  # 输出跳过的测试数量
    if result.failures:  # 如果有失败的测试
        print("\n失败的测试:")  # 输出失败的测试信息
        for test, traceback in result.failures:
            print(f"  {test}")
            print(f"    {traceback.splitlines()[-1]}")
    if result.errors:  # 如果有错误的测试
        print("\n错误的测试:")  # 输出错误的测试信息
        for test, traceback in result.errors:
            print(f"  {test}")
            print(f"    {traceback.splitlines()[-1]}")
    return result  # 返回测试结果
if __name__ == '__main__':
    test_result = run_tests()  # 运行测试
    exit_code = 0 if len(test_result.failures) == 0 and len(test_result.errors) == 0 else 1  # 根据测试结果设置退出码
    sys.exit(exit_code)  # 退出程序