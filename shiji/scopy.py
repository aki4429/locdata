# vim:fileencoding=utf-8

import shutil
import glob

filename = glob.glob("../../../../obic_new/seizoshiji*.csv")[-1]

shutil.copy(filename, '.')

print(filename, "をカレントディレクトリーにコピーしました。")


