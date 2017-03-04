import log_bin
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def log_bin_and_plot(df, a=1.7, font_size=10, **kwargs):
    log_binned_df = pd.DataFrame()

    for i, col in enumerate(df):
        if isinstance(a, list):
            factor = a[i]
        elif isinstance(a, (int, float)):
            factor = a
        else:
            raise ValueError("a must be integer, float, or list!")
        x, y = log_bin.log_bin(df[col].dropna()[df[col] != 0], a=factor, datatype='integer')
        additional = pd.DataFrame({col: y}, index=x)
        log_binned_df = pd.concat([log_binned_df, additional], axis=1)
    ax = plt.figure().gca()
    for col in log_binned_df:
        column = log_binned_df[col]
        # drop zeros before plotting
        if kwargs:
            column[column != 0].dropna().plot(**kwargs, ax=ax)
        else:
            column[column != 0].dropna().plot(style='--', ax=ax, loglog=True)
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

def deg_dist_theory(m, k):
    return 2 * m * (m + 1) / (k * (k + 1) * (k + 2))

def deg_dist_ra_theory(m, k):
    return 1. / (m + 1) * ((m / (m + 1))**(k - m))

def deg_dist_cumulative(m, ks):
    y = deg_dist_theory(m, ks)
    return np.cumsum(y[::-1])[::-1]

def get_model_df(df, columns, model=deg_dist_theory, mlist=None, index=True):
    if mlist is None:
        mlist = columns
    new_df = pd.DataFrame()
    for c, m in zip(columns, mlist):
        if index:
            ks = df.index.values
        else:
            min, max = df[c].dropna().index.min(), df[c].dropna().index.max()
            ks = np.linspace(min, max, num=1000)
        p = model(m, ks)
        additional = pd.DataFrame(p, index=ks, columns=[m])
        new_df = pd.concat([new_df, additional], axis=1)
    return new_df