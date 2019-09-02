import glob
import os


def clear_csv_folder():
    files = glob.glob('./csv/*.csv')

    for x in files:
        os.remove(x)

def order_scalar(source,target_order = 1):
    x = str(round(1/source,0))
    scalar = len(x) * target_order
    return(scalar)
