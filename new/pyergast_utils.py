from pyergast import pyergast
import pandas as pd  # pyergast returns pandas dataframes
import json  # file manip
import logging
import re
STARTYEAR = 1950
pd.options.plotting.backend = 'plotly'
'''General toolset for stats work with the Ergast developer API.
F1 records keeping database 1950-current'''


def curr_year() -> int:
    # gets the year of the last event that is scheduled to happen
    # should be the same season as the last seasons with records.
    return int(list(pyergast.get_schedule()['season'])[0])


def all_drivers() -> list:
    # return all drivers with records, result is cached and loaded when needed
    try:
        with open('all_drivers.json', 'r') as f:
            drivers = json.load(f)
            return drivers
    except FileNotFoundError:
        logging.info('Cached all_drivers not found, creating one...')
        pd_frame = pyergast.get_drivers()  # automatically gets all current!
        drivers = list(pd_frame['driverId'])
        # after creating, safe the file
        with open('all_drivers.json', 'w') as f:
            json.dump(drivers, f)
        return drivers  # after saving the list return it!

    # WONTDO: automatic flushing, if the cached file is old delete manually


def races_in_season(year: int) -> int:
    out = pyergast.get_schedule(year)
    return out.shape[0]


def is_dnf(status: str) -> bool:
    return not bool(re.match(r'Finished|\+[0-9]', status))


def labeled_scatter(data: pd.DataFrame, drivers: list) -> None:
    # Expecting data in shape (n,2) with set axis for labels
    fig = data.plot.scatter(x='Finishes', y='DNFs', hover_data=[drivers])
    fig.show()


if __name__ == '__main__':
    raise NotImplementedError
