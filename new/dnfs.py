import pyergast_utils   # custom file contained
from pyergast import pyergast
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO)


def main(drivers: list, STARTYEAR: int, STOPYEAR: int) -> pd.DataFrame:
    '''Returns a shape (x,3) pandas dataframe with:
    driverId, total race starts, total DNFs'''
    # create the out table
    out = pd.DataFrame(0, index=drivers, columns=['Finishes', 'DNFs'])
    for year in range(STARTYEAR, STOPYEAR + 1):
        for race in range(1, pyergast_utils.races_in_season(year) + 1):
            out = count_dnfs_finishes(out, year, race)
        logging.info(f'{year} completed.')
    return out


def count_dnfs_finishes(out: pd.DataFrame, year: int, race: int) -> pd.DataFrame:
    result = pyergast.get_race_result(year=year, race=race)
    # now we look for NaNs and determine DNFs that way...
    # ASSUMPTION : no finishing time = no finish
    for _, driver_result in result.iterrows():
        # fetch vars from the col
        curr_driver = driver_result[5]  # eg. driverId
        status = driver_result[11]
        if pyergast_utils.is_dnf(status):
            out.DNFs[curr_driver] += 1
            if logging.DEBUG >= logging.root.level:  # test to list all labels reckoned as DNFs
                logging.debug(f'{status} reckognized as a DNF')
        else:
            out.Finishes[curr_driver] += 1
    return out


if __name__ == '__main__':
    drivers = pyergast_utils.all_drivers()
    STOPYEAR = pyergast_utils.curr_year()
    STARTYEAR = 1950
    out = main(drivers, STARTYEAR, STOPYEAR)
    pyergast_utils.labeled_scatter(out, drivers)
