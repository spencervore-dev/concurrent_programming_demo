# Use this script to verify multi core process produces exact
# same output as single core script.
# Like yeah, we're comparing list of floats, we're that sure!

from multi_core import main_process as mc
from single_core import main_process as sc

if __name__ == "__main__":
    mc_list = mc()
    sc_list = sc()

    assert mc_list == sc_list
    print("They match!!")
