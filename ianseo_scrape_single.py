# Author        : Jack Atkinson
#                 @jatkinson1000
#
# Date Created  : 2022-07-18
# Last Modified : 2022-07-18
#
# Summary       : AGB Gender investigation for indoor competition.
#                 Code to scrape results from ianseo pages into a csv for processing
#

import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import product


def get_cat(url_main, url_suffix, div, gen):

    # Old IANSEO Table layout
    try:
        page = requests.get(f'{url_main}/{url_suffix}')
        soup = BeautifulSoup(page.text, 'lxml')
        table1 = soup.find('table', {'class': 'Griglia'})

        table = pd.read_html(str(table1))[0]

    # New IANSEO Table layout
    except ImportError:
        page = requests.get(f'{url_main}/{url_suffix}')
        soup = BeautifulSoup(page.text, 'lxml')
        table = table_to_2d(soup.find('table'))

        # Remove excess headers/rows without useful data
        del table[0]
        del table[2::3]
        del table[2::2]

        table = pd.DataFrame(table[1:], columns=table[0])

    # Add columns relevant for our usage
    table["Event"] = f'{div}{gen}'
    table["Division"] = div
    table["Class"] = gen
    table = table.rename(columns={"Tot.": "Score", "Pos.": "Category Rank"})
    table = table.rename(columns={"Rank": "Category Rank"})

    # Remove disqualified athletes (messes up pandas import and no effect on analysis)
    table[table["Score"] == 'DSQ'] = 0

    return table


def table_to_2d(table_tag):
    # Credit: Martijn Pieters
    # https://stackoverflow.com/questions/48393253/how-to-parse-table-with-rowspan-and-colspan
    rowspans = []  # track pending rowspans
    rows = table_tag.find_all('tr')

    # first scan, see how many columns we need
    colcount = 0
    for r, row in enumerate(rows):
        cells = row.find_all(['td', 'th'], recursive=False)
        # count columns (including spanned).
        # add active rowspans from preceding rows
        # we *ignore* the colspan value on the last cell, to prevent
        # creating 'phantom' columns with no actual cells, only extended
        # colspans. This is achieved by hardcoding the last cell width as 1.
        # a colspan of 0 means “fill until the end” but can really only apply
        # to the last cell; ignore it elsewhere.
        colcount = max(
            colcount,
            sum(int(c.get('colspan', 1)) or 1 for c in cells[:-1]) + len(cells[-1:]) + len(rowspans))
        # update rowspan bookkeeping; 0 is a span to the bottom.
        rowspans += [int(c.get('rowspan', 1)) or len(rows) - r for c in cells]
        rowspans = [s - 1 for s in rowspans if s > 1]

    # it doesn't matter if there are still rowspan numbers 'active'; no extra
    # rows to show in the table means the larger than 1 rowspan numbers in the
    # last table row are ignored.

    # build an empty matrix for all possible cells
    table = [[None] * colcount for row in rows]

    # fill matrix from row data
    rowspans = {}  # track pending rowspans, column number mapping to count
    for row, row_elem in enumerate(rows):
        span_offset = 0  # how many columns are skipped due to row and colspans
        for col, cell in enumerate(row_elem.find_all(['td', 'th'], recursive=False)):
            # adjust for preceding row and colspans
            col += span_offset
            while rowspans.get(col, 0):
                span_offset += 1
                col += 1

            # fill table data
            rowspan = rowspans[col] = int(cell.get('rowspan', 1)) or len(rows) - row
            colspan = int(cell.get('colspan', 1)) or colcount - col
            # next column is offset by the colspan
            span_offset += colspan - 1
            value = cell.get_text()
            for drow, dcol in product(range(rowspan), range(colspan)):
                try:
                    table[row + drow][col + dcol] = value
                    rowspans[col + dcol] = rowspan
                except IndexError:
                    # rowspan or colspan outside the confines of the table
                    pass

        # update rowspan bookkeeping
        rowspans = {c: s - 1 for c, s in rowspans.items() if s > 1}

    return table


if __name__ == "__main__":
    # # Nimes 2015
    # url = 'https://www.ianseo.net/TourData/2015/797'
    # fname = 'Nimes15Scores'

    # # Nimes 2016
    # url = 'https://www.ianseo.net/TourData/2016/1276'
    # fname = 'Nimes16Scores'

    # # Nimes 2017
    # url = 'https://www.ianseo.net/TourData/2017/2013'
    # fname = 'Nimes17Scores'

    # # Nimes 2018
    # url = 'https://www.ianseo.net/TourData/2018/3113'
    # fname = 'Nimes18Scores'

    # # Nimes 2019
    # url = 'https://www.ianseo.net/TourData/2019/4785'
    # fname = 'Nimes19Scores'

    # # Nimes 2020
    # url = 'https://www.ianseo.net/TourData/2020/6255'
    # fname = 'Nimes20Scores'

    # # Nimes 2021
    # url = 'https://www.ianseo.net/TourData/2021/8006'
    # fname = 'Nimes21Scores'

    # # Nimes 2022
    # url = 'https://www.ianseo.net/TourData/2022/9959'
    # fname = 'Nimes22Scores'

    # # AGB NI 2021
    # url = 'https://www.ianseo.net/TourData/2021/9399/'
    # fname = 'AGBNI21Scores'

    # # AGB NI 2019
    # url = 'https://www.ianseo.net/TourData/2019/6526'
    # fname = 'AGBNI19Scores'

    # # AGB NI 2018
    # url = 'https://www.ianseo.net/TourData/2018/4739'
    # fname = 'AGBNI18Scores'

    # # AGB NI 2017
    # url = 'https://www.ianseo.net/TourData/2017/3214'
    # fname = 'AGBNI17Scores'

    # # AGB NI 2016
    # url = 'https://www.ianseo.net/TourData/2016/2192'
    # fname = 'AGBNI16Scores'

    # # AGB NI 2015
    # url = 'https://www.ianseo.net/TourData/2015/1322'
    # fname = 'AGBNI15Scores'

    # # AGB NI 2014
    # url = 'https://www.ianseo.net/TourData/2014/861'
    # fname = 'AGBNI14Scores'

    # # AGB NI 2011
    # url = 'https://www.ianseo.net/TourData/2011/237'
    # fname = 'AGBNI11Scores'

    # Assume recurve and compound always exist and combine into one table
    RM = get_cat(url, 'IQRM.php', div='R', gen='M')
    RW = get_cat(url, 'IQRW.php', div='R', gen='W')
    CM = get_cat(url, 'IQCM.php', div='C', gen='M')
    CW = get_cat(url, 'IQCW.php', div='C', gen='W')
    full_results = pd.concat([RM, RW, CM, CW], ignore_index=True)

    # Try Longbow
    try:
        LM = get_cat(url, 'IQLM.php', div='L', gen='M')
        LW = get_cat(url, 'IQLW.php', div='L', gen='W')
        full_results = pd.concat([full_results, LM, LW], ignore_index=True)
    except ValueError:
        pass
    except AttributeError:
        pass

    # Try Barebow
    try:
        BM = get_cat(url, 'IQBM.php', div='B', gen='M')
        BW = get_cat(url, 'IQBW.php', div='B', gen='W')
        full_results = pd.concat([full_results, BM, BW], ignore_index=True)
    except ValueError:
        pass
    except AttributeError:
        pass

    # Save to file
    full_results.to_csv(f'data/{fname}.csv')
