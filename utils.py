import log_bin
import pandas as pd
import matplotlib.pyplot as plt

def log_bin_and_plot(df, a=1.7, font_size=10):
    log_binned_df = pd.DataFrame()

    for col in df:
        x, y = log_bin.log_bin(df[col].dropna()[df[col] != 0], a=a, datatype='integer')
        additional = pd.DataFrame({str(col) + " (log binned)": y}, index=x)
        log_binned_df = pd.concat([log_binned_df, additional], axis=1)

    ax = plt.figure().gca()
    for col in log_binned_df:
        column = log_binned_df[col]
        # drop zeros before plotting
        column[column != 0].plot(style='--', ax=ax, loglog=True)
    ax.set_ylabel(u'$P(k)$', fontsize=font_size)
    ax.set_xlabel(u'$k$', fontsize=font_size)
    return log_binned_df

def value_counts_and_plot(df, **kwargs):
    degrees_df = pd.DataFrame()
    for col in df:
        result = df[col].value_counts(sort=False, normalize=True)
        degrees_df = pd.concat([degrees_df, result], axis=1)

    if kwargs:
        degrees_df.plot(**kwargs)
    else:
        degrees_df.plot(style='o', loglog=True, alpha=0.8)
    return degrees_df

# drop zeros for each column to plot
def drop_zeros_and_plot(df, **kwargs):
    for col in df:
        column = df[col]
        if kwargs:
            column[column != 0].plot(**kwargs)
        else:
            column[column != 0].plot()
