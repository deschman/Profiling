# -*- coding: utf-8 -*-
"""
Automatically profile table by name, source database type, and DSN.

Params
------
table_name : str
    Fully qualified table name of table in the format of 'SCHEMA.TABLE'.
--data_source_name, -dsn : str, default 'SailfishProd'
    Data source name as defined in user ODBC connections.
--source_type, -sf : str, default 'DB2'
    Source database type for use in database url.
--credential_prompt, -cp : str, default False
    If True, user will be prompted to input credentials to database.
--sample_factor, -sf : int, optional
    One record per sample_factor will be read for the profile.
--compress_columns, -cc : str, optional
    List of columns to take out of the profile separated by spaces. All other
    columns will be compressed if this is specified.
--include_columns, -ic : str, optional
    List of columns to include in the profile separated by spaces. All other
    columns will be excluded from the profile.
--primary_key, -pk : str, optional
    Key used to sort data, which may provide a better profile if a data sample
    is being used.
"""


# %% Imports
# %%% Py3 Standard
# import traceback
import os
import argparse
import traceback

# %%% 3rd Party
import distributed
from pandas_profiling import ProfileReport

# %%% User Defined
from sql_profiling import profile_data


# %% Functions
def main() -> None:
    Profile_Argument_Parser: argparse.ArgumentParser = argparse.ArgumentParser(
        'profile.py')
    Profile_Argument_Parser.add_argument(
        'table_name',
        help="Fully qualified name of table in the format of 'SCHEMA.TABLE'")
    Profile_Argument_Parser.add_argument(
        '--data_source_name',
        '-dsn',
        nargs='?',
        default='SailfishProd',
        help="Data source name as defined in user ODBC connections")
    Profile_Argument_Parser.add_argument(
        '--source_type',
        '-s',
        nargs='?',
        default='DB2',
        help="Source database type for use in database url")
    Profile_Argument_Parser.add_argument(
        '--credential_prompt',
        '-cp',
        nargs='?',
        const=True,
        default=False,
        type=bool,
        choices=[True, False],
        help="If True, user will be prompted to input credentials to database")
    Profile_Argument_Parser.add_argument(
        '--sample_factor',
        '-sf',
        type=int,
        default=1,
        help="One record per sample_factor will be read for the profile")
    Profile_Argument_Parser.add_argument(
        '--compress_columns',
        '-cc',
        nargs='*',
        help="If supplied, profile will include unique values in other columns")
    Profile_Argument_Parser.add_argument(
        '--include_columns',
        '-ic',
        nargs='*',
        help="If supplied, profile will include unique values in other columns")
    Profile_Argument_Parser.add_argument(
        '--primary_key',
        '-pk',
        help="Key used to sort data, which may provide a better profile")

    kwargs: dict = vars(Profile_Argument_Parser.parse_args(os.sys.argv[1:]))

    Profile: ProfileReport = profile_data(**kwargs)
    Profile.to_file(
        os.path.join(os.path.dirname(__file__),
                     f"{kwargs.get('table_name')}.html"),
        False)


# %% Script
if __name__ == '__main__':
    os.sys.argv.append('ODATA_D.VW_FACT_ASSORTMENT_HISTORY_TEST')
    os.sys.argv.append('-ic')
    for c in 'ASSORTMENT_ID ACTIVE_FLAG EFFECTIVE_START_DATETIME EFFECTIVE_END_DATETIME LOCATION_ID LOCATION_NUMBER PRODUCT_ID LINE_CODE ITEM_CODE PRODUCT_LINE_CODE SUB_CODE WAREHOUSE_MANAGEMENT_SYSTEM_CODE PROBLEM_SUPPLIER_FLAG DESTINATION_SEPARATED_ORDER_CODE DESTINATION_SEPARATED_ORDER_CODE_DESCRIPTION ZONE_NUMBER MAXIMUM_ORDER_QUANTITY DISTRIBUTION_CENTER_IMASTER_ORDER_QUANTITY WSCORE_WMS_ON_HAND_QUANTITY CURRENT_ORDER_QUANTITY FACTORY_BACKORDERS_QUANTITY CUSTOMER_BACKORDERS_OPEN_QUANTITY CUSTOMER_BACKORDERS_CREATED_QUANTITY CUSTOMER_BACKORDERS_FILLED_QUANTITY RETURN_QUANTITY_IN_TRANSIT POPULARITY_CODE POPULARITY_CODE_DESCRIPTION POPULARITY_TREND_CODE POPULARITY_TREND_CODE_DESCRIPTION WAREHOUSE_COST_PRICE WAREHOUSE_CORE_PRICE STORE_USER_PRICE STORE_DEALER_PRICE STORE_CORE_PRICE IN_HOUSE_QUANTITY IN_HOUSE_LAST_24_HOURS_QUANTITY ORDER_CUTS_QUANTITY GLOBAL_AVAILABLE_QUANTITY GLOBAL_LINK_DC_AVAILABLE_QUANTITY STORE_ORDERED_QUANTITY ORDERS_CREATED_QUANTITY ORDERS_SHIPPED_QUANTITY STORES_ORDERED_QUANTITY STORE_SHIP_QUANTITY OREILLY_PRIORITY_PARTS_TOTAL_REQUESTS OREILLY_PRIORITY_PARTS_NOT_STOCKED_REQUESTS OREILLY_PRIORITY_PARTS_BAD_DEPTH_REQUESTS ADVANCED_SHIPPING_NOTICE_INTERNAL_COUNT ADVANCED_SHIPPING_NOTICE_EXTERNAL_COUNT STORES_STOCKING_COUNT JOBBER_UNIT_OF_MEASURE_DISTRIBUTION_CENTER_MAX_TOTAL JOBBER_UNIT_OF_MEASURE_DISTRIBUTION_CENTER_QUANTITY_ON_HAND_TOTAL ESSENTIAL_HARDPART_RANKING_CODE LIFE_CYCLE_CODE_FACTOR STORE_AUTO_LOAD_CODE CURRENT_SUPPLIER_CODE CURRENT_SUPPLIER_ACCOUNT_NUMBER CURRENT_SUPPLIER_ID ACTIVITY_CLASS_CODE FORECAST_QUANTITY SEASONAL_FORECAST_QUANTITY RESERVE_QUANTITY COMMITTED_QUANTITY THEORETICAL_UNITS THEORETICAL_DOLLARS BUY_MULTIPLE_QUANTITY JOINT_ORDER_POINT_DAYS LEAD_TIME_IN_USE_IN_DAYS SAFETY_STOCK_DAYS STANDARD_DEVIATION_PERCENT MANUAL_MINIMUM_QUANTITY CAR_QUANTITY REPLENISHMENT_MODIFIER_CODE REPLENISHMENT_MOFIDIER_DESCRIPTION ITEM_CLASS_CODE BPOHEDR_LAST_ORDER_DATE COGS_FILTERED_QUANTITY FSA_OVERSTOCK_UNIT_QUANTITY ACTIVE_PRODUCT_FLAG RECEIVAL_WORK_DOLLARS_ALL_TOTAL RECEIVAL_WORK_DOLLARS_TYPES_TOTAL DISTRIBUTION_CENTER_OUT_OF_STOCK_DAYS BELOW_MIN_ORANGE_QUANTITY BELOW_MIN_ORANGE_TRANSIT_QUANTITY IN_STOCK_GREEN_QUANTITY IN_STOCK_GREEN_TRANSIT_QUANTITY OVERSTOCK_BLUE_QUANTITY OVERSTOCK_BLUE_TRANSIT_QUANTITY OUT_OF_STOCK_RED_QUANTITY OUT_OF_STOCK_RED_TRANSIT_QUANTITY DISTRIBUTION_CENTER_TO_STORE_SELL_QUANTITY DISTRIBUTION_CENTER_MAX_QUANTITY MONTHLY_AVERAGE_LAST_12_MONTHS_QUANTITY MANUAL_OVERRIDE_CODE UPDATE_STATUS_CODE LEAD_TIME_AVERAGE_IN_DAYS MONTH_TO_DATE_LOST_SALES LAST_MONTH_LOST_SALES PREVIOUS_DAY_LOST_SALES PREVIOUS_DAY_SHIPPED_QUANTITY'.split(' '):
        os.sys.argv.append(c)
    os.sys.argv.append('-dsn')
    os.sys.argv.append('SailfishDev')
    os.sys.argv.append('-sf')
    os.sys.argv.append('100000')
    os.sys.argv.append('-pk')
    os.sys.argv.append('ASSORTMENT_ID')
    try:
        client: distributed.Client = distributed.Client()
        main()
    except Exception:
        traceback.print_exc()
    finally:
        input("press enter to close")
