from pathlib import Path
import sys


sys.path.append(str(Path(__file__).resolve().parents[1]))

from tools.size_parser import SizeParser


parser = SizeParser()

for value in [
    "1000x600x20",
    "1200*700*18",
    "1800脳900脳20",
    "invalid",
]:
    print(value)
    print(parser.parse_size(value))
