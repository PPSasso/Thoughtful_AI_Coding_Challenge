from robocorp.tasks import task
from robocorp import workitems, log
from classes.ExcelManager import ExcelManager


@task
def workItemsCreation_task():
    # Set the work items
    ExcelManager.setWorkItems(arg_strExcelPath='./input/workitems.xlsx')


@task
def main_task():
    for item in workitems.inputs:
        log.console_message('\n'+str(item.payload['search_phrase']), "regular")

    log.console_message('\n'+str(workitems.inputs), "regular")
    log.console_message('\n'+str(workitems.outputs), "regular")
    

