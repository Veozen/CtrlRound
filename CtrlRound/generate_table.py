import itertools
import pandas as pd
import numpy as np

def generate_random_table(n_dim, n_cat, scale=1):
    """
    generate a pandas dataframe with random values
    """
    #generate n_dim columns each with n_cat values
    sets = [set(range(n_cat)) for _ in range(n_dim)]
    cartesian_product = list(itertools.product(*sets))
    df = pd.DataFrame(cartesian_product, columns=[*range(n_dim)])
     #generate random values between 0 and scale
    df["value"] = np.random.rand(len(df)) * scale
    return df
  




