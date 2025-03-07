# Use this script to verify multi core process produces exact
# same output as single core script.
# Like yeah, we're comparing list of floats, we're that sure!

from multi_core import main_process as mc
from single_core import main_process as sc
from multi_core_w_pool import main_process as mcp

if __name__ == "__main__":
    mc_list = mc()
    sc_list = sc()
    mcp_list = mcp()

    assert mc_list == sc_list
    assert mc_list == mcp_list
    print("They ALL match!!")
