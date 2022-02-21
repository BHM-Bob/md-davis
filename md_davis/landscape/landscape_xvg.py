#!/usr/bin/env python3

import click

from md_davis.landscape.landscape import Landscape
from md_davis.xvg import Xvg


def landscape_xvg(x, y, name, label, common=False, temperature=None,
                  output='landscapes.html',
                  save=None, title=None, shape=(100, 100), begin=0, end=None,
                  limits=None,
                  orthographic=False, layout=None, width=None, height=None,
                  font=None,
                  font_size=None, dtick=None,
                  axis_labels=None,
                  columns=None):
    """Plot free energy landscapes from .xvg files generated by GROMACS"""

    # TODO: Add checks to ensure the correct number of arguments are passed

    if limits is not None:
        limits = eval(limits)

    input_data = {}
    landscapes = []
    for f1, f2, name, label in zip(x, y, name, label):
        data1 = Xvg(f1)
        data2 = Xvg(f2)

        time = data1.data[begin:end, 0]
        x_data = data1.data[begin:end, 1]
        y_data = data2.data[begin:end, 1]

        if len(time) < 1 or len(x_data) < 1 or len(y_data) < 1:
            raise ValueError('Invalid value for begin or end')

        if common:
            input_data[name] = [time, x_data, y_data, label]
        else:
            print(f'Generating Landscape for {name}')
            landscape = Landscape.landscape(
                name=name,
                time=time,
                x_data=x_data,
                y_data=y_data,
                shape=shape,
                label=label,
                temperature=temperature,
                limits=limits,
            )
            landscapes.append(landscape)

    if common and len(input_data) > 0:
        landscapes = Landscape.common_landscapes(
            data=input_data,
            shape=shape, temperature=temperature,
            limits=limits,
        )

    if save:
        for ls in landscapes:
            ls.save(filename=save,
                    name=ls.name,
                    xlabel='RMSD',
                    ylabel='Radius of Gyration')

    Landscape.plot_landscapes(
        landscapes=landscapes,
        title=title,
        filename=output,
        axis_labels=axis_labels,
        width=width,
        height=height,
        othrographic=orthographic,
        dtick=eval(dtick) if dtick else None,
        layout=eval(layout) if layout else None,
        font_family=font,
        font_size=font_size,
    )


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(name='landscape_xvg', context_settings=CONTEXT_SETTINGS)
@click.option('-x', type=click.Path(exists=True), multiple=True, required=True,
              help='Data to plot on x-axis')
@click.option('-y', type=click.Path(exists=True), multiple=True, required=True,
              help='Data to plot on y-axis')
@click.option('-n', '--name', type=str, multiple=True, required=True,
              help='Names of each landscape object')
@click.option('-l', '--label', type=str, multiple=True, required=True,
              help='Label to show in plots')
@click.option('-c', '--common', is_flag=True,
              help='Use common ranges for all the landscapes')
@click.option('-T', '--temperature', type=float,
              help='Temperature of the system. If this option is provided the '
              'energy landscape is calculated using Boltzmann inversion, '
              'else only the histogram is evaluated')
@click.option('-o', '--output', type=str, default='landscapes.html',
              help='Name for the output HTML file containing the plots')
@click.option('--shape', nargs=2, default=[100, 100], type=int,
              metavar="('X-bins', 'Y-bins')",
              help='Number of bins in the X and Y direction')
@click.option('-b', '--begin', type=int, metavar='<int>', default=0,
              help='Starting index for the data to include')
@click.option('-e', '--end', type=int, metavar='<int>',
              help='Last index for the data to include')
@click.option('--limits', help='A dictionary containing the limits for '
                               'x, y, and x axes')
@click.option('-s', '--save', metavar='FILENAME',
              help='Name for HDF5 file to save the landscapes')
@click.option('--title', type=str, metavar='<str>', help='Title for the figure')
@click.option('--orthographic/--perspective', default=False,
              help='Orthographic projection for 3D plots')
@click.option('--width', type=int, metavar='<int>', help='Width of the plot')
@click.option('--height', type=int, metavar='<int>', help='Height of the plot')
@click.option('--font', type=str, metavar='<str>', help='Font style')
@click.option('--font_size', type=int, metavar='<int>',
              help='Size of text and labels in the plot')
@click.option('--dtick', help='Tick interval on each axes')
@click.option('--axis_labels', default=None,
              help='A dictionary of strings specifying the labels for '
                   "the x, y and z-axis. For example: "
                   "dict(x='RMSD (in nm)', y='Rg (in nm)', "
                   "z='Free Energy (kJ mol<sup>-1</sup>)<br> ')")
@click.option('--layout', help='Layout of subplots')
@click.option('--columns', help='Columns to use (start from second column = 1)')
def main(x, y, name, label, common=False, temperature=None,
         output='landscapes.html',
         save=None, title=None, shape=(100, 100), begin=0, end=None,
         limits=None,
         orthographic=False, layout=None, width=None, height=None, font=None,
         font_size=None, dtick=None,
         axis_labels=None,
         columns=None):
    """ Wrapper function for Click """
    landscape_xvg(x=x, y=y, name=name, label=label, common=common,
                  temperature=temperature, output=output, save=save,
                  title=title, shape=shape, begin=begin, end=end, limits=limits,
                  orthographic=orthographic, layout=layout, width=width,
                  height=height, font=font, font_size=font_size, dtick=dtick,
                  axis_labels=axis_labels, columns=columns)


if __name__ == '__main__':
    main()
