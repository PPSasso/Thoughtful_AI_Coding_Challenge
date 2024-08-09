from robocorp.tasks import task
from robocorp import workitems
from classes.ExcelManager import ExcelManager
import logging

logger = logging.getLogger(__name__)

@task
def workItemsCreation_task():
    # Set the work items
    ExcelManager.setWorkItems(arg_strExcelPath='./input/workitems.xlsx')


@task
def main_task():
    for item in workitems.outputs:
        logger.info(item.payload['search-phrase'])

