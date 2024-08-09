from robocorp.tasks import task
from robocorp import workitems
from classes.ExcelManager import ExcelManager
import logging

@task
def workItemsCreation_task():
    # Set the work items
    ExcelManager.setWorkItems(arg_strExcelPath='./input/workitems.xlsx')


@task
def main_task():
    for item in workitems.outputs:
        logging.info(item.payload['search-phrase'])

