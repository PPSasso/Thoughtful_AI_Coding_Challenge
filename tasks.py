from robocorp.tasks import task
from classes.ExcelManager import ExcelManager

@task
def workItemsCreation_task():

    # Set the work items
    ExcelManager.setWorkItems(arg_strExcelPath='./input/workitems.xlsx')

@task
def main_task():
    message = "Hello"
    message = message + " World!"

workItemsCreation_task()
