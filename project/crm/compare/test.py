import hashlib
import codecs


def file_lines_hash_dict(file):
    """将文件的每一行转成hash的字典"""
    hash_dict = {}
    with codecs.open(file, 'r', encoding='gb18030', errors='ignore') as file:
        for i, line in enumerate(file, start=1):
            try:
                # 计算每一行hash value
                line_hash = hashlib.md5(line.encode('gb18030')).hexdigest()
                # 保存hash value和行号
                hash_dict[i] = line_hash
            except Exception as err:
                print("md5 encode error")

    return hash_dict


a = file_lines_hash_dict("test_utf8.txt")
b = file_lines_hash_dict("test_gbk.txt")
print(a)
print(b)