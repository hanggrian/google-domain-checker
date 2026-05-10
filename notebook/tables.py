from IPython.display import display, HTML
from numpy import arange
from pandas import DataFrame, read_csv


def show(filename: str) -> None:
    data: DataFrame = read_csv(filename)

    data.index = arange(1, len(data) + 1)
    data.loc['Grand Total'] = ['', data['Price'].sum()]

    data['Price'] = data['Price'].map('{:,}'.format)  # pylint: disable=consider-using-f-string
    display(HTML(data.to_html(render_links=True, escape=False)))
