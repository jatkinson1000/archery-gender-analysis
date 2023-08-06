# Author        : Jack Atkinson
#                 @jatkinson1000
#
# Date Created  : 2022-07-14
# Last Modified : 2022-07-30
#
# Summary       : AGB Gender investigation for indoor competition.  plotting routines
#

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
import numpy as np


def scatter_scores(data, fsave=True, fpath='./results/'):
    """ function scatter_scores
    plot a scatter of scores comparing 2 genders for a specific category

    Parameters
    ----------
    data : pandas dataframe
        pandas dataframe containing AGB tournament data
    fsave : bool
        string identifying file to save image to. Displays plot if None.

    Returns
    -------
    None
        Plots to screen

    """

    for event in data["Event"].unique():

        data_event = data[data["Event"] == event]
        cat = data_event["Division"].unique()
        cat = sorted(cat, key=lambda x: ['R', 'C', 'B', 'L'].index(x[0]))

        fig, ax = plt.subplots(1, len(cat), figsize=(5*len(cat), 5), sharey='row')
        for i, cat_i in enumerate(cat):
            data_cat_m = data_event[(data_event['Class'] == f'M')
                                    & (data_event['Division'] == f'{cat_i}')]
            data_cat_f = data_event[(data_event['Class'] == f'W')
                                    & (data_event['Division'] == f'{cat_i}')]
            ax[i].scatter(100 * (data_cat_m['Sep rank'] - 1) / (len(data_cat_m) - 1),
                          data_cat_m['Score'], c='c', label='male')
            ax[i].scatter(100 * (data_cat_f['Sep rank'] - 1) / (len(data_cat_f) - 1),
                          data_cat_f['Score'], c='r', label='female')

            ax[i].invert_xaxis()
            ax[i].set_title(cat_i)
            ax[i].set_xlabel('Split Ranking Position')
            ax[i].legend(loc='lower right')

        ax[0].set_ylabel('Score')
        plt.suptitle(event)

        if fsave:
            plt.savefig(f'{fpath}{event}_scores.png')
        else:
            plt.show()


def scatter_mixed_scores(data, fsave=True, fpath='./results/'):
    """ function scatter_scores
    plot a scatter of scores comparing 2 genders for a specific category

    Parameters
    ----------
    data : pandas dataframe
        pandas dataframe containing AGB tournament data
    fsave : bool
        string identifying file to save image to. Displays plot if None.

    Returns
    -------
    None
        Plots to screen

    """
    for event in data["Event"].unique():

        data_event = data[data["Event"] == event]
        cat = data_event["Division"].unique()
        cat = sorted(cat, key=lambda x: ['R', 'C', 'B', 'L'].index(x[0]))

        fig, ax = plt.subplots(1, len(cat), figsize=(5*len(cat), 5), sharey='row')
        for cat_i, ax_i in zip(cat, ax.ravel()):
            data_cat_m = data_event[(data_event['Class'] == f'M')
                                    & (data_event['Division'] == f'{cat_i}')]
            data_cat_f = data_event[(data_event['Class'] == f'W')
                                    & (data_event['Division'] == f'{cat_i}')]

            ax_i.scatter(data_cat_m['Mixed rank'], data_cat_m['Score'], c='c', s=2, label='male')
            ax_i.scatter(data_cat_f['Mixed rank'], data_cat_f['Score'], c='r', s=2, label='female')

            ax_i.invert_xaxis()
            ax_i.set_title(cat_i)
            ax_i.set_xlabel('Mixed Ranking Position')
            ax_i.legend(loc='lower right')

        ax[0].set_ylabel('Score')
        plt.suptitle(event)

        if fsave:
            plt.savefig(f'{fpath}{event}_scores_mixed.png')
        else:
            plt.show()


def mixed_split_percentile(data, fsave=True, fpath='./results/'):

    for event in data["Event"].unique():

        data_event = data[data["Event"] == event]
        cat = data_event["Division"].unique()
        cat = sorted(cat, key=lambda x: ['R', 'C', 'B', 'L'].index(x[0]))

        fig, ax = plt.subplots(1, len(cat), figsize=(5*len(cat), 5), sharey='row')
        for cat_i, ax_i in zip(cat, ax.ravel()):
            data_cat_m = data_event[(data_event['Class'] == f'M')
                                    & (data_event['Division'] == f'{cat_i}')]
            data_cat_f = data_event[(data_event['Class'] == f'W')
                                    & (data_event['Division'] == f'{cat_i}')]
            n_mixed = len(data_cat_m) + len(data_cat_f)

            ax_i.scatter(100*(data_cat_m['Sep rank']-1)/(len(data_cat_m)-1),
                          100*((data_cat_m['Mixed rank']-1)/(n_mixed-1)), c='c', label=f'male ({len(data_cat_m)})')
            ax_i.scatter(100*(data_cat_f['Sep rank']-1)/(len(data_cat_f)-1),
                          100*((data_cat_f['Mixed rank']-1)/(n_mixed-1)), c='r', label=f'female ({len(data_cat_f)})')

            ax_i.plot([-10, 110], [-10, 110], 'k')

            ax_i.set_title(cat_i)
            ax_i.set_xlabel('Split Qualification Percentile')

            ax_i.invert_yaxis()
            ax_i.invert_xaxis()

            if cat_i in 'RC':
                # Insert axis
                axins2 = zoomed_inset_axes(ax_i, zoom=2, loc='upper left', borderpad=2.5)
                axins2.scatter(100*(data_cat_m['Sep rank']-1)/(len(data_cat_m)-1),
                               100*((data_cat_m['Mixed rank']-1)/(n_mixed-1)), c='c', label=f'male ({len(data_cat_m)})')
                axins2.scatter(100*(data_cat_f['Sep rank']-1)/(len(data_cat_f)-1),
                               100*((data_cat_f['Mixed rank']-1)/(n_mixed-1)), c='r', label=f'female ({len(data_cat_f)})')
                axins2.plot([-10, 110], [-10, 110], 'k')

                # sub-region of the original image
                x1, x2, y1, y2 = -1.0, 16.0, -1.0, 16.0
                axins2.set_xlim(x1, x2)
                axins2.set_ylim(y1, y2)
                # fix the number of ticks on the inset axes
                # axins2.yaxis.get_major_locator().set_params(nbins=7)
                # axins2.xaxis.get_major_locator().set_params(nbins=7)
                axins2.tick_params(labelleft=True, labelbottom=True)
                axins2.invert_yaxis()
                axins2.invert_xaxis()
                axins2.set_aspect('equal')

                # draw a bbox of the region of the inset axes in the parent axes and
                # connecting lines between the bbox and the inset axes area
                patch, pp1, pp2 = mark_inset(ax_i, axins2, loc1=2, loc2=1, fc="none", ec="0.0")
                pp1.loc1 = 2
                pp1.loc2 = 4
                pp2.loc1 = 4
                pp2.loc2 = 2

            ax_i.set_xlim([105, -5])
            ax_i.set_ylim([105, -5])
            ax_i.set_aspect('equal')
            ax_i.legend(loc='lower right')

        ax[0].set_ylabel('Mixed Qualification Percentile')
        plt.suptitle(event)

        if fsave:
            plt.savefig(f'{fpath}{event}_percentile_scatter.png')
        else:
            plt.show()


def plot_pos_changes(delta_pos, fid='', fpath='./results/'):
    gen = ['M', 'W']
    gen_c = ['c', 'r']
    pos_c = ['gold', 'silver', 'saddlebrown']

    # generate list of bowstyles for this event and sort as desired
    cat = delta_pos["Division"].unique()
    cat = sorted(cat, key=lambda x: ['R', 'C', 'B', 'L'].index(x[0]))

    fig, ax = plt.subplots(1, len(cat), figsize=(3*len(cat), 4.5), sharey='row')
    for j, cat_j in enumerate(cat):
        for i, gen_i in enumerate(gen):
            for pos in range(1, 4):
                dr_cr = delta_pos.loc[(delta_pos['Class'] == f'{gen[i]}')
                                      & (delta_pos['Sep rank'] == pos)
                                      & (delta_pos['Division'] == f'{cat_j}')]['Delta rank']

                dr_err = [[dr_cr.median() - dr_cr.min()],
                          [dr_cr.max() - dr_cr.median()]]
                ax[j].scatter(dr_cr.median(), 3*(4-pos)-i-1, c=gen_c[i])
                ax[j].errorbar(dr_cr.median(), 3*(4-pos)-i-1, xerr=dr_err, c=pos_c[pos-1],
                               capsize=5.0)

            xmin = delta_pos.loc[delta_pos['Division'] == f'{cat_j}']['Delta rank'].min()
            ax[j].set_xlim([(np.floor(xmin/5))*5-1, 1])
            ax[j].set_ylim([0, 9])
            ax[j].axvline(0.0, c='k', ls='--', alpha=0.1)
            ax[j].axvline(-1.0, ymin=1/3, c='k', ls='--', alpha=0.1)
            ax[j].axvline(-2.0, ymin=2/3, c='k', ls='--', alpha=0.1)
            # ax[j].axvline(-3.0, ymin=2/3, c='k', ls='--', alpha=0.1)
            ax[j].set_title(cat_j)

        plt.suptitle(f'Position Changes for {fid}')
        fig.supxlabel('Change in position, split -> mixed gender')

        y = [1.5, 4.5, 7.5]
        labels = ['Bronze', 'Silver', 'Gold']
        ax[0].set_yticks(y, labels, rotation='vertical', va='center')

    plt.savefig(f'{fpath}{fid}position_changes.png')

    return None
