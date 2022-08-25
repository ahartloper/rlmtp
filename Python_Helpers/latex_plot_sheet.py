import os
import rlmtp

root_dir = 'Clean_Data'
output_dir = 'Python_helpers/All_Plots'
rlmtp.dir_maker(output_dir)


def sort_split(s):
    if 'LP' in s:
        try:
            return int(s.split('_')[0].split('LP')[-1])
        except:
            return s
    else:
        return s


all_pdf_files = []
for root, dirs, files in os.walk(root_dir, topdown=False):
    print(root)
    rel_dp = os.path.relpath(root, output_dir)
    pdf_files = [f for f in files if os.path.splitext(f)[1] == '.pdf']
    pdf_files.sort(key=sort_split)
    all_pdf_files += [os.path.join(rel_dp, f) for f in pdf_files]

outpath = os.path.join(output_dir, 'latex_figures_file.tex')
rlmtp.create_latex_photos.make_latex_doc(all_pdf_files, outpath)
