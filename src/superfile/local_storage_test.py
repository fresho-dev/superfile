import pathlib
import tempfile
import unittest
from . import superfile


def _create_files(paths: list[str]) -> tempfile.TemporaryDirectory:
  tmpdir = tempfile.TemporaryDirectory()
  root = pathlib.Path(tmpdir.name)
  for fpath in paths:
    fpath = root / fpath
    fpath.parent.mkdir(parents=True, exist_ok=True)
    fpath.touch()
  return tmpdir


class TestLocalStorage(unittest.TestCase):

  def test_write_text_file(self):
    text = "hello world"
    with tempfile.TemporaryDirectory() as tmpdir:
      fpath = tmpdir + "/" + "test.txt"
      with superfile.open(fpath, "w") as f:
        f.write(text)
      with open(fpath, "r") as f:
        self.assertEqual(f.read(), text)

  def test_read_text_file(self):
    text = "hello world"
    with tempfile.TemporaryDirectory() as tmpdir:
      fpath = tmpdir + "/" + "test.txt"
      with open(fpath, "w") as f:
        f.write(text)
      with superfile.open(fpath, "r") as f:
        self.assertEqual(f.read(), text)

  def test_list_all_files_with_prefix(self):
    fpaths = [
        "file_0.txt",
        "subdir/file_1.txt",
        "subdir/subsubdir/file_2.txt",
        "subdir/subsubdir/file_3.txt",
    ]
    with _create_files(fpaths) as tmpdir:
      result = list(superfile.list(tmpdir))
      inputs = [tmpdir + "/" + x for x in fpaths]
      self.assertListEqual(inputs, result)


if __name__ == "__main__":
  unittest.main()