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
        self.comparator = DocumentComparator()
    def test_document_comparator_initialization(self):
        self.assertIsNotNone(self.comparator)
        self.assertTrue(hasattr(jieba, 'dt'))
    def test_content_processing(self):
        text = "这是一个测试文本，用于测试内容处理功能的准确性"
        processed_content = self.comparator.process_content(text)
        self.assertIsInstance(processed_content, list)  # 主代码返回列表，断言成立
        self.assertTrue(len(processed_content) > 0)
    def test_empty_content_processing(self):
        processed_content = self.comparator.process_content("")
        self.assertIsInstance(processed_content, list)  # 主代码返回空列表，断言成立
        self.assertEqual(len(processed_content), 0)
    def test_file_reading(self):
        content = "测试文件内容，包含中文和English文字"
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_file = f.name
        try:
            read_content = self.comparator.fetch_document_data(temp_file)
            self.assertEqual(content, read_content)
        finally:
            os.unlink(temp_file)
    def test_empty_file_reading(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            temp_file = f.name
        try:
            read_content = self.comparator.fetch_document_data(temp_file)
            self.assertEqual("", read_content)
        finally:
            os.unlink(temp_file)
    def test_similarity_calculation_identical(self):
        text1 = "这是一个完全相同的测试文本"
        text2 = "这是一个完全相同的测试文本"
        processed1 = self.comparator.process_content(text1)
        processed2 = self.comparator.process_content(text2)
        similarity = self.comparator.compute_document_similarity(processed1, processed2)
        self.assertAlmostEqual(similarity, 1.0, delta=0.1)
    def test_similarity_calculation_different(self):
        text1 = "这是第一个测试文本，关于人工智能和机器学习"
        text2 = "这是第二个完全不同的文本，关于历史和文化艺术"
        processed1 = self.comparator.process_content(text1)
        processed2 = self.comparator.process_content(text2)
        similarity = self.comparator.compute_document_similarity(processed1, processed2)
        self.assertLess(similarity, 0.5)
    def test_similarity_calculation_similar(self):
        text1 = "这是一个测试文本，用于测试相似度计算功能"
        text2 = "这是一个测试文本，用于检验相似度计算功能"
        processed1 = self.comparator.process_content(text1)
        processed2 = self.comparator.process_content(text2)
        similarity = self.comparator.compute_document_similarity(processed1, processed2)
        self.assertGreater(similarity, 0.6)
        self.assertLess(similarity, 1.0)
    def test_empty_documents_similarity(self):
        processed1 = self.comparator.process_content("")
        processed2 = self.comparator.process_content("")
        similarity = self.comparator.compute_document_similarity(processed1, processed2)
        self.assertEqual(similarity, 1.0)  # 断言与主代码逻辑一致
    def test_empty_file_processing(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            temp_file1 = f.name
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            temp_file2 = f.name
        try:
            success = self.comparator.execute_comparison(temp_file1, temp_file2, "output.txt")
            self.assertTrue(success)
            with open("output.txt", 'r', encoding='utf-8') as f:
                result = f.read().strip()
            similarity = float(result)
            self.assertAlmostEqual(similarity, 1.0, delta=0.1)
        finally:
            if os.path.exists("output.txt"):
                os.unlink("output.txt")
            os.unlink(temp_file1)
            os.unlink(temp_file2)
    def test_one_empty_file_processing(self):
        content = "这是一个有内容的文件"
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_file1 = f.name
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            temp_file2 = f.name
        try:
            success = self.comparator.execute_comparison(temp_file1, temp_file2, "output.txt")
            self.assertTrue(success)
            with open("output.txt", 'r', encoding='utf-8') as f:
                result = f.read().strip()
            similarity = float(result)
            self.assertEqual(similarity, 0.0)
        finally:
            if os.path.exists("output.txt"):
                os.unlink("output.txt")
            os.unlink(temp_file1)
            os.unlink(temp_file2)
    def test_nonexistent_file(self):
        success = self.comparator.execute_comparison("nonexistent_file.txt", "another_nonexistent.txt", "output.txt")
        self.assertFalse(success)
        if os.path.exists("output.txt"):
            os.unlink("output.txt")
    def test_chinese_text_processing(self):
        text1 = "自然语言处理是人工智能领域的一个重要方向"
        text2 = "自然语言处理是AI领域的一个重要研究方向"
        processed1 = self.comparator.process_content(text1)
        processed2 = self.comparator.process_content(text2)
        similarity = self.comparator.compute_document_similarity(processed1, processed2)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)
        self.assertGreater(similarity, 0.5)
    def test_punctuation_handling(self):
        text1 = "这是一个测试文本，包含标点符号！还有问号？"
        text2 = "这是一个测试文本包含标点符号还有问号"
        processed1 = self.comparator.process_content(text1)
        processed2 = self.comparator.process_content(text2)
        similarity = self.comparator.compute_document_similarity(processed1, processed2)
        self.assertGreater(similarity, 0.7)
    def test_main_function_integration(self):
        orig_content = "这是原始文档内容，包含一些特定的技术术语和概念说明"
        copy_content = "这是修改后的文档内容，包含一些特定的技术术语和概念说明但有一些修改和补充"
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            f.write(orig_content)
            orig_file = f.name
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            f.write(copy_content)
            copy_file = f.name
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            output_file = f.name
        try:
            success = self.comparator.execute_comparison(orig_file, copy_file, output_file)
            self.assertTrue(success)
            with open(output_file, 'r', encoding='utf-8') as f:
                result = f.read().strip()
            similarity = float(result)
            self.assertGreaterEqual(similarity, 0.0)
            self.assertLessEqual(similarity, 1.0)
            if '.' in result:
                decimal_part = result.split('.')[1]
                self.assertEqual(len(decimal_part), 4)
        finally:
            for f in [orig_file, copy_file, output_file]:
                if os.path.exists(f):
                    os.unlink(f)
    def test_short_text_handling(self):
        text1 = "短文本"
        text2 = "短文本"
        processed1 = self.comparator.process_content(text1)
        processed2 = self.comparator.process_content(text2)
        similarity = self.comparator.compute_document_similarity(processed1, processed2)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)
    def test_very_different_texts(self):
        text1 = "量子力学是描述微观粒子行为的基础理论"
        text2 = "文艺复兴是欧洲历史上重要的文化运动"
        processed1 = self.comparator.process_content(text1)
        processed2 = self.comparator.process_content(text2)
        similarity = self.comparator.compute_document_similarity(processed1, processed2)
        print(f"完全不同文本的相似度: {similarity:.3f}")
        self.assertLess(similarity, 0.4)
    def test_command_line_interface(self):
        orig_content = "测试命令行接口"
        copy_content = "测试命令行接口功能"
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            f.write(orig_content)
            orig_file = f.name
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            f.write(copy_content)
            copy_file = f.name
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            output_file = f.name
        try:
            original_argv = sys.argv
            sys.argv = ['main.py', orig_file, copy_file, output_file]
            from main import primary_function
            try:
                primary_function()
                self.assertTrue(os.path.exists(output_file))
                with open(output_file, 'r', encoding='utf-8') as f:
                    result = f.read().strip()
                similarity = float(result)
                self.assertGreaterEqual(similarity, 0.0)
                self.assertLessEqual(similarity, 1.0)
            except SystemExit as e:
                self.assertEqual(e.code, 0)
            finally:
                sys.argv = original_argv
        finally:
            for f in [orig_file, copy_file, output_file]:
                if os.path.exists(f):
                    os.unlink(f)
def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDocumentComparator)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    print(f"\n测试结果统计:")
    print(f"运行测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    print(f"跳过数: {len(result.skipped)}")
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"  {test}")
            print(f"    {traceback.splitlines()[-1]}")
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"  {test}")
            print(f"    {traceback.splitlines()[-1]}")
    return result
if __name__ == '__main__':
    test_result = run_tests()
    exit_code = 0 if len(test_result.failures) == 0 and len(test_result.errors) == 0 else 1
    sys.exit(exit_code)