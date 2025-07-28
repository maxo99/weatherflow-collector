import pandas as pd
from colorama import Fore, Style


def style_df(df, color="grey", caption=""):
    """
    Styles a pandas DataFrame with a specified background color.

    Parameters:
    df (pandas.DataFrame): The DataFrame to style.
    color (str): The background color to apply to the DataFrame cells.

    Returns:
    pandas.io.formats.style.Styler: A Styler object with the applied styles.
    """
    return df.style.set_caption(caption).set_properties(
        **{"border": "1.3px solid blue", "color": color}
    )


# Color printing
# inspired by https://www.kaggle.com/code/ravi20076/sleepstate-eda-baseline
def PrintColor(text: str, color=Fore.BLUE, style=Style.BRIGHT):
    """Prints color outputs using colorama using a text F-string"""
    print(style + color + text + Style.RESET_ALL)


# inspired by https://www.kaggle.com/code/rishabh15virgo/cmi-dss-first-impression-data-understanding-eda
def summarize_dataframe(df):
    summary_df = pd.DataFrame(df.dtypes, columns=["dtypes"])
    summary_df["missing#"] = df.isna().sum().values * 100
    summary_df["missing%"] = (df.isna().sum().values * 100) / len(df)
    summary_df["uniques"] = df.nunique().values
    summary_df["first_value"] = df.iloc[0].values
    summary_df["last_value"] = df.iloc[len(df) - 1].values
    summary_df["count"] = df.count().values
    # sum['skew'] = df.skew().values
    desc = pd.DataFrame(df.describe().T)
    summary_df["min"] = desc["min"]
    summary_df["max"] = desc["max"]
    summary_df["mean"] = desc["mean"]
    return summary_df


def check_missing_values(df):
    for col in df.columns:
        msg = "column: {:>10}\t Percent of NaN value: {:.2f}%".format(
            col, 100 * (df[col].isnull().sum() / df[col].shape[0])
        )
        PrintColor(f"\n---> {msg}")
