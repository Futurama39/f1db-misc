import pyergast_utils
import dnfs
import pandas as pd


# testing some utils things
def test_list_outs():
    # should return non empty list
    drivers = pyergast_utils.all_drivers()
    assert drivers


def test_plot():
    frame = [[0, 5], [1, 7], [5, 5], [3, 1]]  # shape (4,2)
    out = pd.DataFrame(frame, index=['albono', 'seb', 'nando', 'jamilton'], columns=['Finishes', 'DNFs'])
    pyergast_utils.labeled_scatter(out, ['albono', 'seb', 'nando', 'jamilton'])


def test_max():
    # we're expecting 114 starts and 27 DNFs
    frame = dnfs.main(pyergast_utils.all_drivers(), 2014, 2021)  # outs a pd dataframe
    max = frame.loc['max_verstappen']
    assert max['DNFs'] == 29
    assert max['Finishes'] == 112


if __name__ == '__main__':
    test_max()
