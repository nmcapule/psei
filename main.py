"""."""

from datetime import date, datetime, timedelta
import logging
import investpy
from pandas import DataFrame
import plotext
import click
import rich

_DEFAULT_COUNTRY = "Philippines"
_INPUT_DATEFMT = "%Y-%m-%d"
_INVST_DATEFMT = "%d/%m/%Y"


@click.group()
def cli():
    """Entry point for the CLI commands."""
    pass


@cli.command()
@click.argument("stock", type=click.STRING)
@click.option(
    "--country",
    default=_DEFAULT_COUNTRY,
    type=click.STRING,
    help="Country to get the stock",
)
def inspect(stock: str, country: str):
    """Gets basic information about the stock."""
    info: dict = investpy.get_stock_information(stock, country, as_json=True)
    rich.print(info)


@cli.command()
@click.argument("keyword", type=click.STRING)
@click.option(
    "--country",
    default=_DEFAULT_COUNTRY,
    type=click.STRING,
    help="Country to get the stock",
)
def search(keyword: str, country: str):
    """Search stocks list by keyword."""
    results: list = investpy.search_quotes(text=keyword, countries=[country])
    for res in results:
        rich.print(res)


@cli.command()
@click.argument("stock", type=click.STRING)
@click.option(
    "--country",
    default=_DEFAULT_COUNTRY,
    type=click.STRING,
    help="Country to get the stock",
)
@click.option(
    "--from",
    "from_",
    default=(date.today() - timedelta(days=30)).strftime(_INPUT_DATEFMT),
    type=click.DateTime(),
    help="Retrieve from date",
)
@click.option(
    "--to",
    "to_",
    default=date.today().strftime(_INPUT_DATEFMT),
    type=click.DateTime(),
    help="Retrieve to date",
)
def plot(stock: str, country: str, from_: datetime, to_: datetime):
    """Plots a given stock ticker."""
    _df: DataFrame = investpy.get_stock_historical_data(
        stock=stock,
        country=country,
        from_date=from_.strftime(_INVST_DATEFMT),
        to_date=to_.strftime(_INVST_DATEFMT),
    )
    rich.print(_df)

    dates = plotext.datetimes_to_string(_df.index)

    plotext.candlestick(dates, _df)
    plotext.title("Stock Prices")
    plotext.xlabel("Date")
    plotext.ylabel("Stock Price $")
    plotext.show()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    cli()
