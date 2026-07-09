# run.py
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from src.database.data_loader import DataLoader

def print_line():
    print("=" * 60)

def show_dataset_info(table_name, df):

    print_line()

    print(f"表名：{table_name}")

    print_line()

    print(f"数据量：{df.shape}")

    print("\n字段信息：")

    print(df.dtypes)

    print("\n前5行数据：")

    print(df.head())

    print("\n缺失值统计：")

    print(df.isnull().sum())

def main():
    print_line()
    print("淘宝电商用户增长分析平台")

    print_line()
    loader = DataLoader()
    data = loader.load_all()
    print("\n数据库读取成功\n")
    for table_name, df in data.items():
        show_dataset_info(table_name, df)
    print_line()
    print("数据加载完成")
    print_line()
if __name__ == "__main__":
    main()

