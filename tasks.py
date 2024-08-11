from robocorp.tasks import task
from robocorp import workitems, log
from classes.ExcelManager import ExcelManager
from classes.BrowserManager import BrowserManager
import time


@task
def workItemsCreation_task():
    # Set the work items
    ExcelManager.setWorkItems(arg_strExcelPath='./input/workitems.xlsx')


@task
def main_task():
    var_wbWebBrowser = BrowserManager()
        
    for item in workitems.inputs:
        for attempt in range(3): # tries to execute the process 3 times.
            try:
                log.console_message(f'\nStarting execution attempt numer {attempt}', "regular")
                var_wbWebBrowser.startWebBrowser(item.payload['website'])
                log.console_message('\nStarting the search on: '+str(item.payload['search_phrase']), "regular")
                var_dfCapturedNews = var_wbWebBrowser.searchForNews(arg_strSearchPhrase=item.payload['search_phrase'],
                                                                    arg_strTopic=item.payload['category_section_topic'],
                                                                    arg_strTimeSpan=item.payload['timespan'])
                break
            except Exception as e:
                log.console_message(f'\nAttempt {attempt} failed: {e}', "error")
                if attempt > 2:
                    raise Exception(f"All attempts failed after retrying {attempt} times.")
                else:
                    time.sleep(5) # Waits a bit before retrying

        ExcelManager.saveNewsFile(var_dfCapturedNews, f"news_on_{str(item.payload['search_phrase'])}.xlsx")
                
                

        





    
    

