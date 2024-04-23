import argparse

# 创建 ArgumentParser 对象
parser = argparse.ArgumentParser(description="一个简单的示例程序。")

# 添加参数
parser.add_argument('echo', help="回显输入的字符串")
parser.add_argument('--verbosity', help="增加输出的详细程度",
                    type=int, choices=[0, 1, 2])

# 解析命令行参数
args = parser.parse_args()

# 使用参数
if args.verbosity == 2:
    print("输出非常详细...")
elif args.verbosity == 1:
    print("输出较详细...")
else:
    print(args.echo)
