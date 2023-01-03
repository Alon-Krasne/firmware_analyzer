import os
import re
from collections import Counter
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import List, Union, Dict
import multiprocessing
import argparse


CSV_TITLE = "Path,Occurrences,Token\n"
TOKEN_PATTERN = re.compile(r"<Tkn\d{3}[A-Z]{5}Tkn>")


@dataclass
class FileTokens:
    path: Path
    tokens: Dict[str, int]

    @cached_property
    def sorted_tokens_keys_by_value(self) -> List[str]:
        temp = sorted([(value, token) for token, value in self.tokens.items()], key=lambda x: (x[0], x[1]), reverse=True)
        return [token for value, token in temp]

    def _to_csv_line(self, key) -> str:
        return f"{self.path},{self.tokens[key]},{key}\n"

    def to_csv_lines(self) -> List[str]:
        return [self._to_csv_line(key) for key in self.sorted_tokens_keys_by_value]


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, required=True, help='Directory path of the files to analyze')
    parser.add_argument('--output-csv', type=str, required=True, help='Output path for the CSV results file')
    return parser.parse_args()


def get_all_files(dir_path: Union[Path, str] = Path("./test_files")) -> List[Path]:
    if isinstance(dir_path, str):
        dir_path = Path(dir_path)

    _files = []
    for root, _, file_names in os.walk(dir_path):
        for file_name in file_names:
            _files.append(Path(os.path.join(root, file_name)))
    return _files


def analyze_document_tokens_in_file(file_path: Path) -> FileTokens:
    with open(file_path, "r") as f:
        file_content = f.read()

    appearances = TOKEN_PATTERN.findall(file_content)
    count = Counter(appearances)

    return FileTokens(path=file_path, tokens=dict(count))


def write_results_to_csv(results: List[FileTokens], filename: str = "results.csv"):
    sorted_result = sorted(results, key=lambda x: x.path)
    with open(filename, "w") as f:
        f.write(CSV_TITLE)
        for result in sorted_result:
            f.writelines(result.to_csv_lines())


def analyze_firmware(directory_path: str, csv_output_path: str):
    files_to_process = get_all_files(directory_path)

    with multiprocessing.Pool() as pool:
        res = pool.map_async(analyze_document_tokens_in_file, files_to_process)
        result = res.get()

    write_results_to_csv(results=result, filename=csv_output_path)


if __name__ == '__main__':  # Compare between the main functions time
    args = parse_arguments()
    exit(analyze_firmware(args.input_dir, args.output_csv))
