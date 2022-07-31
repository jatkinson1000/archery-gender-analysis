# Author        : Jack Atkinson
#                 @jatkinson1000
#
# Date Created  : 2022-07-14
# Last Modified : 2022-07-30
#
# Summary       : AGB Gender investigation for indoor competition.  Main script
#

import plotting_routines as plot
import general_routines as gr

if __name__ == "__main__":
    dataset_id = 'Nimes_'
    data_in = ["Nimes15",
               "Nimes16",
               "Nimes17",
               "Nimes18",
               "Nimes19",
               "Nimes20",
               "Nimes21",
               # "Euro19",
               "Nimes22"]

    # dataset_id = 'AGB_NI_'
    # data_in = ["AGBNI21",
    #            "AGBNI19",
    #            "AGBNI18",
    #            "AGBNI17",
    #            "AGBNI16",
    #            "AGBNI15",
    #            "AGBNI14",
    #            "AGBNI11"]

    df_all = gr.read_from_files(data_in, datapath='./data/', fname_fmt='.csv', f_pref='', f_suff='Scores')

    # Calculate split and mixed gender rankings and percentiles, and the position changes that result for individuals
    df_all = gr.calc_mixed_rank_percentiles(df_all)
    df_all = gr.calc_delta_sep_mixed(df_all)

    # Save the raw dataset
    df_out = df_all.sort_values(by=['Event', 'Division', 'Class', 'Score', '10'],
                                ascending=[False, True, True, False, False], ignore_index=True)
    with open(f'./results/{dataset_id}raw_data.txt', 'w') as f:
        f.write(df_out.to_string(index=False,
                                 columns=['Event', 'Division', 'Class', 'Score', '10', '9', 'Sep rank', 'Mixed rank']))

    # Scatter all scores against separate percentile position
    plot.scatter_scores(df_all, fsave=True)
    # Scatter mixed scores against mixed percentile position (but showing gender)
    plot.scatter_mixed_scores(df_all, fsave=True)
    # Scatter change in percentile when going from separate to mixed gender competition
    plot.mixed_split_percentile(df_all, fsave=True)

    # Examine the effect on medalists across all events and plot
    delta_pos = gr.get_pos_changes(df_all, fpref=dataset_id)
    plot.plot_pos_changes(delta_pos, fid=dataset_id)

    # Conduct a t_test on the data by event and write to file along with key stats
    ttest = gr.conduct_t_test(df_all, fpref=dataset_id)


# Plot error bars of t test probability
# comment on what it tells about the overlapping ranges of ability - smaller pool of women so 50th
# should be worse than men's 50th...
