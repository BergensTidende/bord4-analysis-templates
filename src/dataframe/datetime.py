"""
  Collection of utility functions to do with datetime for faster analysis
"""

def split_into_ymd(_df, date_column):
    """Utility function to split a date column into year, month and day

    Args:
        __df (dataframe): The dataframe to split
        date_column (_type_): The column to split

    Returns:
        dataframe: The dataframe with the split columns
    """

    _df[date_column] = _df[date_column].dt.year.fillna(0).astype('int')
    _df[date_column] = _df[date_column].dt.month.fillna(0).astype('int')
    _df[date_column] = _df[date_column].dt.day.fillna(0).astype('int')

    return _df


def split_into_hms(_df, date_column):
    """Utility function to split a date column into hour, minute and second

    Args:
        __df (dataframe): The dataframe to split
        date_column (_type_): The column to split

    Returns:
        dataframe: The dataframe with the split columns
    """

    _df[date_column] = _df[date_column].dt.hour.fillna(0).astype('int')
    _df[date_column] = _df[date_column].dt.minute.fillna(0).astype('int')
    _df[date_column] = _df[date_column].dt.second.fillna(0).astype('int')

    return _df


def add_month_name(_df, month_col="month", short_name=False, start_index=1):
    """
    Utility function to add the month name to a dataframe

    Args:
        _df (dataframe): the dataframe to add the month name to
        month_col (str, optional): The month column. Defaults to "month".
        short_name (bool, optional): should we use short month name?. Defaults to False.
        start_index (int, optional): The numner for January. Defaults to 1.

    Returns:
        dataframe: the dataframe with the month name added
    """
    lst_month = ["januar", "februar", "mars", "april", "mai", "juni",
                 "juli", "august", "september", "oktober", "novemeber", "desember"]

    if short_name:
        lst_month = ["jan", "feb", "mar", "apr", "mai", "jun", "jul", "aug", "sep", "okt", "nov", "des"]

    if start_index == 1:
        lst_month.insert(0, "")

    _df["month_name"] = _df[month_col].apply(lambda x: lst_month[int(x)])

    return _df