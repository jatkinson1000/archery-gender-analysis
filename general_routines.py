# Author        : Jack Atkinson
#                 @jatkinson1000
#
# Date Created  : 2022-07-18
# Last Modified : 2022-07-18
#
# Summary       : AGB Gender investigation for indoor competition.  general routines
#

import numpy as np
import pandas as pd
from scipy.stats import ttest_ind


def read_from_files(flist, datapath='./data/', fname_fmt='.csv', f_pref='', f_suff='Scores'):

    if not isinstance(flist, list):
        flist = [flist]

    li_df = []
    fields = ['Division', 'Class', 'Score', '10', '9', 'Category Rank']
    for f_id in flist:
        dataset = pd.read_csv(f'{datapath}{f_pref}{f_id}{f_suff}{fname_fmt}', usecols=fields)
        # Drop any zero/DNS scores as cause issues with analysis.
        dataset = dataset.drop(dataset[dataset.Score == 0].index)
        dataset["Event"] = f_id
        li_df.append(dataset)
    # Combine all events into a single dataset
    df_comb = pd.concat(li_df, axis=0, ignore_index=True)

    return df_comb


def calc_separate_rank_percentiles(df_in):

    # Generate seperate gender category rank based on score and then 10s
    df_in["Sep rank"] = (df_in.groupby(['Event', 'Division', 'Class'])["Score"].rank(ascending=False, method='min')
                         + df_in.groupby(['Event', 'Division', 'Class', 'Score'])["10"].rank(ascending=False, method='average')
                         - 1)
    # Get separate percentile
    df_in['Sep pc'] = 100 * ((df_in['Sep rank'] - 1)
                             / (df_in.groupby(['Event', 'Division', 'Class'])['Score'].transform('count') - 1))

    return df_in


def calc_mixed_rank_percentiles(df_in):

    # Check we have generated separate rank and percentile already, if not do so first
    if ('Sep rank' not in df_in.columns) or 'Sep pc' not in df_in.columns:
        df_in = calc_separate_rank_percentiles(df_in)

    # Generate mixed gender category rank based on score and then 10s and percentile
    df_in["Mixed rank"] = (df_in.groupby(['Event', 'Division'])["Score"].rank(ascending=False, method='min')
                           + df_in.groupby(['Event', 'Division', 'Score'])["10"].rank(ascending=False, method='average')
                           - 1)
    df_in['Mixed pc'] = 100 * ((df_in['Mixed rank'] - 1)
                               / (df_in.groupby(['Event', 'Division'])['Score'].transform('count') - 1))

    return df_in


def calc_delta_sep_mixed(df_in):

    # Check we have generated separate rank and percentile already, if not do so first
    if ('Mixed rank' not in df_in.columns) or 'Mixed pc' not in df_in.columns:
        df_in = calc_mixed_rank_percentiles(df_in)

    # Calculate position changes as a result of mixing categories
    df_in['Delta rank'] = df_in["Sep rank"] - df_in["Mixed rank"]
    df_in['Delta pc'] = df_in["Sep pc"] - df_in["Mixed pc"]

    return df_in


def get_pos_changes(df_in, fpref=''):

    # Check we have generated separate rank and percentile already, if not do so first
    if 'Delta rank' not in df_in.columns:
        df_in = calc_delta_sep_mixed(df_in)

    # Group by event, division, class, take top 3
    df_in = df_in.sort_values(by=['Event', 'Division', 'Class', 'Score', '10'],
                              ascending=[False, True, True, False, False], ignore_index=True)
    delta_pos = (df_in.groupby(['Event', 'Division', 'Class'])
                 [['Event', 'Division', 'Class', 'Sep rank', 'Mixed rank', 'Delta rank']].head(3))

    with open(f'./results/{fpref}delta_pos.txt', 'w') as f:
        f.write(delta_pos.to_string(index=False))

    return delta_pos


def set_rank_band(data, band_edges=None):
    if band_edges is None:
        band_edges = [1, 6, 11, 21, 51, np.inf]

    cat_lab = [f'>{band_edges[i-1]-1}' if band_edges[i] == np.inf else f'{band_edges[i-1]}-{band_edges[i]-1}'
               for i in range(1, len(band_edges))]
    cat_sc = (2*np.asarray(band_edges) - 1)/2

    Qm = pd.cut(data["Sep rank"],
                cat_sc,
                labels=cat_lab,
                include_lowest=True)
    data['Rank band'] = Qm

    return data


def conduct_t_test(data, fpath='./results/', fpref=''):

    if 'Rank band' not in data.columns:
        data = set_rank_band(data)

    # Conduct ttest for all scores for each event and bowstyle(Division)
    groups_ed = data.groupby(['Event', 'Division'])
    with open(f'{fpath}{fpref}t_test_results_all.txt', 'w') as f:
        f.write(groups_ed.apply(lambda df: ttest_ind(df.loc[df['Class'] == 'M']['Score'],
                                                     df.loc[df['Class'] == 'W']['Score'],
                                                     equal_var=False)[1]).to_string())

    groups_edc = data.groupby(['Event', 'Division', 'Class'])
    with open(f'{fpath}{fpref}all_stats.txt', 'w') as f:
        f.write(groups_edc['Score'].aggregate(['mean', 'std', 'max', 'min', 'count']).to_string())

    # Conduct ttest for separate bands within each event and bowstyle(Division)
    groups_edb = data.groupby(['Event', 'Division', 'Rank band'])
    with open(f'{fpath}{fpref}t_test_results_bands.txt', 'w') as f:
        f.write(groups_edb.apply(lambda df: ttest_ind(df.loc[df['Class'] == 'M']['Score'],
                                                      df.loc[df['Class'] == 'W']['Score'],
                                                      equal_var=False)[1]).to_string())

    groups_edcb = data.groupby(['Event', 'Division', 'Rank band', 'Class'])
    with open(f'{fpath}{fpref}score_band_stats.txt', 'w') as f:
        f.write(groups_edcb['Score'].aggregate(['mean', 'std', 'max', 'min', 'count']).to_string())

    return None


#
#
# def conduct_chi_sq(data, chisq_df):
#     for cat in ['R', 'C', 'B', 'L']:
#         try:
#             data_cat_m, data_cat_f = get_mf_db(data, cat)
#
#             data_cat = pd.concat([data_cat_m, data_cat_f], ignore_index=True)
#             data_cat = set_award(data_cat, cat)
#             # use data_cat_m["Sep Rank"].nsmallest(1).max() for resolving ties
#             contigency = pd.crosstab(data_cat['Class'], data_cat['Award'])
#             print(cat)
#             print(contigency)
#             print(chi2_contingency(contigency))
#
#         except IndexError:
#             # Bowstyle not in results
#             pass
#         except ValueError:
#             # Bowstyle not in results
#             pass
#
#     return chisq_df
