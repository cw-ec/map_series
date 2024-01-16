from components import DissolveData

"""
This tool dissolves the given input dataset by the given inputs field(s).

This tool takes the following input parameters:

    in_data: This parameter is the path to the dataset that the dissolve isto be done on
    out_gdb: 
    diss_fields:  

"""

DissolveData(
    in_data="..\\data\\PD_A.gdb\\EGD_RLS_PDA",
    out_gdb="..\\data\\diss_tests.gdb",
    diss_fields=["ADV_UID", "SITE_AREA_UID"]
)
