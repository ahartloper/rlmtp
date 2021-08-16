"""@package create_latex_photos
Functions to write a LaTeX file containing figures in the specified directory.

Can be called as a script or by using the latex_photo_compiler function.
"""
import os
import sys
import errno


def latex_figure_string(name, image_rel_path):
    """ Creates the LaTeX code for the figure located at image_rel_path. """
    # Note: the max image size is 6cm x 6cm.
    # Note: the name is only used locally in the LaTeX document.
    name_no_ext = name[0:-4]
    label_string = 'fig:{0}'.format(name_no_ext)
    caption_string = name_no_ext.replace('_', ' ')
    fig_strings = [r'\begin{figure}',
                   r'\centering',
                   r'\includegraphics[width=6cm,height=6cm,keepaspectratio]{{{0}}}'.format(image_rel_path),
                   r'\caption{{{0}}}'.format(caption_string),
                   r'\label{{{0}}}'.format(label_string),
                   r'\end{figure}']
    fig_final_string = '\n'.join(fig_strings)
    return fig_final_string


def dir_maker(directory):
    """ Makes directory if it doesn't exist, else does nothing. """
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return


def latex_photo_compiler(input_dir, output_dir):
    """ Creates a LaTeX file with all the photo files in input_dir as figures.

    :param str input_dir: Directory containing photos, ends with '/'.
    :param str output_dir: Directory where the .tex file will be created, ends with '/'.
    :return:

    - The file created is 'output_dir/photo_summary.tex', this file will be overwritten if it exists.
    - Only files ending in 'png', 'PNG', and 'jpg' will be included.
    """
    # Get the relative path from the input to the output directory
    dir_maker(output_dir)
    image_relpath = os.path.relpath(input_dir, output_dir)
    # Set the extensions that will be considered as images to include in the LaTeX file
    valid_extensions = ['png', 'PNG', 'jpg']

    # Get all the files in the input folder
    file_names = os.listdir(input_dir)
    image_files = [f for f in file_names if f[-3:] in valid_extensions]
    image_file_paths = [image_relpath + '/' + f for f in image_files]

    # Start the LaTeX document
    out_file_name = 'photo_summary.tex'
    out_path = output_dir + out_file_name
    make_latex_doc(image_file_paths, out_path)

    # Print a completion message
    print('Finished creating the file {0}'.format(output_dir + out_file_name))
    return


def make_latex_doc(image_paths, output_path, paper_type='a4paper', doc_type='article'):
    """ Writes the LaTeX document to file. """

    # Start the LaTeX document
    with open(output_path, 'w') as figure_tex_file:
        # Create the preamble
        figure_tex_file.write(r'\documentclass[{{{0}}}]{{{1}}}'.format(paper_type, doc_type))
        figure_tex_file.write('\n')
        figure_tex_file.write(r'\usepackage{graphicx}')
        figure_tex_file.write('\n')
        figure_tex_file.write(r'\begin{document}')
        figure_tex_file.write('\n')
        figure_tex_file.write('\n')

        for im_path in image_paths:
            filename = os.path.basename(im_path)
            latex_fig = latex_figure_string(filename, im_path)
            figure_tex_file.write(latex_fig)
            figure_tex_file.write('\n')
            figure_tex_file.write('\n')

        # End the LaTeX document
        figure_tex_file.write(r'\end{document}')
    return


# If called as a script
if __name__ == '__main__':
    # Get the input and output directories from the script call
    number_of_inputs = len(sys.argv) - 1  # -1 to discount the name of the script
    if number_of_inputs == 2:
        in_dir = sys.argv[1]
        out_dir = sys.argv[2]
        latex_photo_compiler(in_dir, out_dir)
    else:
        print('Incorrect input arguments. Usage: \n create_latex_photos.py photos_folder/ output_folder/')
