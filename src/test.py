import os

from utils.utils import VcfTool

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    vcf_tool = VcfTool(
        vcf_path=os.path.join(BASE_DIR, "src", "static", "NA12877_API_10.vcf.gz")
    )
    df = vcf_tool.get_dataframe()
    print(df.head())
