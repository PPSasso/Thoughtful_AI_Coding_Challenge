from robocorp.tasks import task
from robocorp import workitems, log
from classes.ExcelManager import ExcelManager
from classes.BrowserManager import BrowserManager


@task
def workItemsCreation_task():
    # Set the work items
    ExcelManager.setWorkItems(arg_strExcelPath='./input/workitems.xlsx')


@task
def main_task():
    var_wbWebBrowser = BrowserManager()

    for item in workitems.inputs:
        var_wbWebBrowser.startWebBrowser(item.payload['website'])
        log.console_message('\nStarting the search on: '+str(item.payload['search_phrase']), "regular")
        var_wbWebBrowser.searchForNews(arg_strSearchPhrase=item.payload['search_phrase'],
                                       arg_strTopic=item.payload['category_section_topic'],
                                       arg_strTimeSpan=item.payload['timespan'])





    
    

