from robocorp.tasks import task
from robocorp import workitems
from classes.ExcelManager import ExcelManager

@task
def workItemsCreation_task():
    # Set the work items
    ExcelManager.setWorkItems(arg_strExcelPath='./input/workitems.xlsx')
    print()


@task
def main_task():
    for item in workitems.outputs:
        print(item.payload['search-phrase'])

