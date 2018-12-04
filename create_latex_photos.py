import os
import sys


def latex_figure_string(name):
    """ Creates the figure """
    # Note: the max image size is 6cm x 6cm.
    name_no_ext = name[0:-4]
    label_string = 'fig:{0}'.format(name_no_ext)
    caption_string = name_no_ext.replace('_', ' ')
    fig_strings = [r'\begin{figure}',
                   r'\centering',
                   r'\includegraphics[width=6cm,height=6cm,keepaspectratio]{{{0}}}'.format(name),
                   r'\caption{{{0}}}'.format(caption_string),
                   r'\label{{{0}}}'.format(label_string),
                   r'\end{figure}']
    fig_final_string = '\n'.join(fig_strings)
    return fig_final_string


def latex_photo_compiler(input_dir):
    """ Creates a LaTeX file with all the photo files in input_dir as figures.

    :param str input_dir: Directory containing photos, ends with '/'.
    :return:

    - The file created is 'input_dir/photo_summary.tex', this file will be overwritten if it exists.
    - Only files ending in 'png', 'PNG', and 'jpg' will be included.
    """
    # Set the output directory same as the input
    output_dir = input_dir
    # Set the extensions that will be considered as images to include in the LaTeX file
    valid_extensions = ['png', 'PNG', 'jpg']

    # Start the LaTeX document
    doc_type = 'article'
    paper_type = 'a4paper'
    out_file_name = 'photo_summary.tex'
    with open(output_dir + out_file_name, 'w') as photo_tex_file:
        # Create the preamble
        photo_tex_file.write(r'\documentclass[{{{0}}}]{{{1}}}'.format(paper_type, doc_type))
        photo_tex_file.write('\n')
        photo_tex_file.write(r'\usepackage{graphicx}')
        photo_tex_file.write('\n')
        photo_tex_file.write(r'\begin{document}')
        photo_tex_file.write('\n')
        photo_tex_file.write('\n')

        # Get all the files in the input folder and add the figures to the LaTeX file
        file_names = os.listdir(input_dir)
        filtered_files = [f for f in file_names if f[-3:] in valid_extensions]
        for i, fn in enumerate(filtered_files):
            latex_fig = latex_figure_string(fn)
            photo_tex_file.write(latex_fig)
            photo_tex_file.write('\n')
            photo_tex_file.write('\n')

        # End the LaTeX document
        photo_tex_file.write(r'\end{document}')

    # Print a completion message
    print('Finished creating the file {0}'.format(output_dir + out_file_name))
    return


# If called as a script
if __name__ == '__main__':
    # Get the input and output directories from the script call
    number_of_inputs = len(sys.argv) - 1  # -1 to discount the name of the script
    if number_of_inputs == 1:
        in_dir = sys.argv[1]
        latex_photo_compiler(in_dir)
    else:
        print('Incorrect input arguments. Usage: \n create_latex_photos.py photos_folder/ ')
