import log_bin
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
import random

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

def get_deg_dist_from_file(folder, n, m):
    filename = "{0}_{1}.txt".format(n, m)
    filepath = folder + filename
    return pd.read_csv(filepath)

def visualize_ccdf(df, m, ax=None):
    if ax is None:
        ax = plt.figure().gca()
    column_to_plot = 1 - df[m].cumsum(skipna=True)
    column_to_plot = column_to_plot.dropna().head(-1)
    column_to_plot.plot(style='-', logy=True, ax=ax)
    last_k = column_to_plot.index[-1]
    ks = np.arange(m, last_k)
    a = deg_dist_theory(m, ks)
    theory_ccdf = 1 - pd.Series(a, index=ks).cumsum(skipna=True)
    theory_ccdf.dropna().plot(logy=True, style='--', ax=ax)

# modified from log_bin.py file provided by James Clough 2015
def log_bin_from_freq_count(values, freqs, bin_start=1., first_bin_width=1., a=2.,
                            datatype="integer", drop_zeros=True, debug_mode=False):
    # create array of the edges of the bins beginning with the left edge of the
    # leftmost bin, and ending with the right edge of the rightmost
    bin_width = first_bin_width
    bins = [bin_start]
    new_edge = bin_start
    min_x, max_x = min(values), max(values)
    while new_edge <= max_x:
        last_edge = new_edge
        new_edge = last_edge + bin_width
        bins.append(new_edge)
        bin_width *= a

    # find how many datapoints are in each bin
    # counts[i] is how many points are there in the bin whose left edge is bins[i]
    indices = np.digitize(values, bins[1:])
    counts = [0. for x in bins[1:]]
    for num, i in enumerate(indices):
        counts[i] += freqs[num]

    bin_indices = list(range(len(bins) - 1))
    if datatype == 'float':
        widths = [bins[i + 1] - bins[i] for i in bin_indices]
        centres = [np.sqrt(bins[i + 1] * bins[i]) for i in bin_indices]
    else:
        widths = [np.ceil(bins[i + 1]) - np.ceil(bins[i]) for i in bin_indices]
        integers_in_each_bin = [list(range(int(np.ceil(bins[i])), int(np.ceil(bins[i + 1])))) for i in bin_indices]
        centres = [log_bin.geometric_mean(x) for x in integers_in_each_bin]

    widths = np.array(widths)
    counts /= widths

    # print out some values to help with debugging
    if debug_mode:
        print('DATA - %s' % data[:10])
        print('BINS - %s' % bins[:10])
        print('INDICES - %s' % indices[:10])
        print('COUNTS - %s' % counts[:10])
        print('WIDTHS - %s' % widths[:10])
        try:
            print('INTEGERS IN EACH BIN - %s' % integers_in_each_bin[:10])
        except:
            pass
        print('CENTRES - %s' % centres[:10])

    return centres, counts

def log_bin_freq_and_plot(df, a=1.7, font_size=10, **kwargs):
    log_binned_df = pd.DataFrame()

    for i, col in enumerate(df):
        if isinstance(a, list):
            factor = a[i]
        elif isinstance(a, (int, float)):
            factor = a
        else:
            raise ValueError("a must be integer, float, or list!")
        x, y = log_bin_from_freq_count(df[col].dropna()[df[col] != 0].index.values, df[col].dropna()[df[col] != 0].values, a=factor, datatype='integer')
        additional = pd.DataFrame({col: y}, index=x)
        log_binned_df = pd.concat([log_binned_df, additional], axis=1)
    ax = plt.figure().gca()
    for col in log_binned_df:
        column = log_binned_df[col]
        # drop zeros before plotting
        if kwargs:
            column[column != 0].dropna().plot(**kwargs, ax=ax, fontsize=font_size)
        else:
            column[column != 0].dropna().plot(style='--', ax=ax, loglog=True, fontsize=font_size)
    ax.set_ylabel(u'$P(k)$', fontsize=font_size)
    ax.set_xlabel(u'$k$', fontsize=font_size)
    return log_binned_df

def largest_degree(N, m):
    D = 1 + 4 * N * m * (m+1)
    return (-1 + np.sqrt(D))/2

def largest_degree_ra(N, m):
    return np.log(N) / (np.log(m+1) - np.log(m)) + m

class ba_degree_dist(scipy.stats.rv_discrete):
    def _pmf(self, k, m):
        return deg_dist_theory(m, k)

class ba_degree_dist_float(scipy.stats.rv_continuous):
    def _pdf(self, k, m):
        return deg_dist_theory(m, k)

def generate_synthetic_data2(m, simulated_dataset, number_of_nodes):
    # simulated_dataset is a pandas dataframe series
    # returns a pandas series
    simulated_dataset.sort_index()
    simulated_dataset = simulated_dataset.dropna()
    N = simulated_dataset.sum()
    ccdf = 1. - simulated_dataset.cumsum()
    n = ccdf[ccdf < 1. / number_of_nodes].sum()
    k1 = ccdf[ccdf >= 1. / number_of_nodes].index[0]
    dist = ba_degree_dist(a=m, b=k1, name='dist')

    result_degrees = []
    for i in range(number_of_nodes):
        if random.random() < n / N:
            result_degrees.append(dist.rvs(size=1, m=m)[0])
        else:
            r = random.uniform(0, N)
            row = np.digitize(r, simulated_dataset.cumsum().values)
            result_degrees.append(simulated_dataset.head(row + 1).index[-1])
    return result_degrees

def generate_synthetic_data(m, data):
    N = len(data)
    maximum = max(data)
    dist = ba_degree_dist(a=m, b=maximum, name='dist')
    print(dist)
    return dist.rvs(size=100000, m=m)


def convert_deg_dist_to_degrees(degrees, counts):
    assert(len(degrees) == len(counts))
    # converts a degree distribution to a list of degrees
    result = []
    for i in range(len(degrees)):
        extra = [degrees[i]] * int(counts[i])
        result.extend(extra)
    return result

# def generate_synthetic_data(m, simulated_dataset, number_of_nodes):
#     simulated_dataset.sort_index()
#     simulated_dataset = simulated_dataset.dropna()
#     N = simulated_dataset.sum()
#     ccdf = 1. - simulated_dataset.cumsum()
#     n = ccdf[ccdf < 1. / number_of_nodes].sum()
#     k1 = ccdf[ccdf >= 1. / number_of_nodes].index[0]
#     dist = ba_degree_dist(a=0, b=k1, name='dist')
#
#     result_degrees = []
#     for i in range(number_of)

def deg_dist_cdf(k, m, range_start, range_end):
    values = []
    k_range = np.arange(range_start, range_end)
    total = deg_dist_theory(m, k_range).sum()
    for value in k:
        start_to_value = np.arange(range_start, value+1)
        cumulative = deg_dist_theory(m, start_to_value).sum()
        normalized = cumulative / total
        values.append(normalized)
    return np.array(values)