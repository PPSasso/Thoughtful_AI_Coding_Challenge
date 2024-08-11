from RPA.Browser.Selenium import Selenium
from RPA.Browser.Selenium import By
from robocorp import log
import pandas as pd
import time
import urllib.request
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta


class BrowserManager:
    """
    Class responsible for all the interactions with the web browser. Each instance of this object relates to a single web browser.
    """

    def __init__(self) -> None:
        # Creates the browser that will be used throughout the methods
        self.var_browser = Selenium()
        self.var_browser.open_available_browser()


    def startWebBrowser(self,arg_strURL):
        """
        Goes to the address given through the methods arguments
        
        Parameters:
            arg_strURL (str): The URL of the page that is to be opened

        Returns:
            None
        """
        log.console_message(f"\nOpening '{arg_strURL}'", "regular")
        self.var_browser.go_to(arg_strURL)

    def searchForNews(self, arg_strSearchPhrase:str, arg_strTopic:str, arg_strTimeSpan:str) -> pd.DataFrame:
        """
        Search for the newest articles about the 'search phrase' that are within the 'Topic' within the 
        'Time Span' ammount of months. The results are stored in a pandas dataframe.
        
        Parameters:
            arg_strSearchPhrase (str): The phrase that will be searched in the news website
            arg_strTopic (str): The topic of the articles captured
            var_strTimeSpan (str): The max timespan, in months, of said articles.
            
        Returns:
            arg_dfCapturedNews (DataFrame): All of the results that fall within parameters
        """
        
        # Search in the sites search bar
        self.var_browser.click_button("//button[@data-element='search-button']")
        self.var_browser.input_text("//input[@data-element='search-form-input']", arg_strSearchPhrase, True)
        self.var_browser.click_button("//button[@data-element='search-submit-button']")

        # Wait for it to load
        time.sleep(5)

        log.console_message(f"\nFiltering the topic to '{arg_strTopic}'", "regular")

        # Filter it by topic
        self.var_browser.click_button("//div[@class='search-filter'][//p[text() = 'Topics']]//button[@class='button see-all-button']")
        self.var_browser.click_button(f"//label[@class='checkbox-input-label'][span[text()='{arg_strTopic.capitalize()}']]/input")

        # Wait for it to load
        time.sleep(5)

        log.console_message(f"\nSorting articles from oldest to newest.", "regular")

        # Sort it by 'Newest'
        self.var_browser.select_from_list_by_label(f"//label[@class='select-label']/select",'Newest')

        # Wait for it to load
        time.sleep(5)

        # Set the df output's columns
        var_listDfColumns = ['Title', 'Date', 'Description', 'Picture_filename', 'Search_Phrase_Appearances', 'Mentions_money']
        var_dfOutputNews = pd.DataFrame(columns=var_listDfColumns)

        var_intCount = 0 # Just a limit to captured news. Can be adjusted in the while condition.
        var_booTimespanLimit = False

        log.console_message(f"\nExtracting data...", "regular")

        # While there are News within the timespan set via workitem
        while(not var_booTimespanLimit and var_intCount < 10):

            # Identify all the visible news on the current page
            var_listNewsList = self.var_browser.find_elements("//ul[@class='search-results-module-results-menu']/li")
            
            for index, article in enumerate(var_listNewsList):
                try:
                    # Capture the News Date
                    var_strDate:str = article.find_element(By.XPATH, ".//p[@class='promo-timestamp']").text

                    # Validates if the article is within the timespan from the current workitem
                    var_strFormatedDate = ' '.join([var_strDate[0:3], var_strDate.split(' ')[1], var_strDate.split(' ')[2]])
                    var_dtArticleDateTime = datetime.strptime(var_strFormatedDate, r'%b %d, %Y')
                    var_dtDateLimit = datetime.now() - relativedelta(months=arg_strTimeSpan)
                    if var_dtArticleDateTime < var_dtDateLimit:
                        var_booTimespanLimit = True # if the articles are too old, the process stop reading them
                        break

                    # Capture the News title
                    var_strTitle = article.find_element(By.XPATH, ".//div[@class='promo-title-container']/h3").text
                    
                    # Capture the News Description
                    try:
                        var_strDescription = article.find_element(By.XPATH, ".//p[@class='promo-description']").text
                    except:
                        var_strDescription = 'No description'
                        pass

                    # Capture and save the News Image
                    var_strImageURL:str = article.find_element(By.XPATH, ".//div[@class='promo-media']/a/picture/img").get_attribute('src')
                    var_strImageExtension = var_strImageURL.split('.')[-1]
                    if len(var_strImageExtension) > 4 : var_strImageExtension = 'jpg'
                    var_strImageFileName = f'{arg_strSearchPhrase}Image{index+(var_intCount*10)}.{var_strImageExtension}'
                    urllib.request.urlretrieve(var_strImageURL, f'./output/{var_strImageFileName}')

                    # See how many times the search phrase has been mentioned in the title and on the description
                    var_matchListTitle = re.findall(arg_strSearchPhrase, var_strTitle)
                    var_matchListDescription = re.findall(arg_strSearchPhrase, var_strDescription)
                    var_intSearchPhraseCount = 0
                    var_intSearchPhraseCount += (len(var_matchListTitle)+len(var_matchListDescription))

                    # Validates if the article mentions money in the title or description
                    var_matchListMoneyTitle = re.findall(r'\$\d[\d\.\,]*|\d[\d\.\,]*\ ?(?:dollars)|\d[\d\.\,]*\ ?(?:USD)', var_strTitle)
                    var_matchListMoneyDescr = re.findall(r'\$\d[\d\.\,]*|\d[\d\.\,]*\ ?(?:dollars)|\d[\d\.\,]*\ ?(?:USD)', var_strDescription)
                    var_booMoneyMentioned = True if (len(var_matchListMoneyTitle) + len(var_matchListMoneyDescr)) > 0 else False

                    var_dfNewRow = pd.DataFrame({'Title':[var_strTitle],
                                                    'Date':[var_dtArticleDateTime.strftime('%m/%d/%Y')],
                                                    'Description':[var_strDescription], 
                                                    'Picture_filename':[var_strImageFileName], 
                                                    'Search_Phrase_Appearances':[str(var_intSearchPhraseCount)], 
                                                    'Mentions_money':[str(var_booMoneyMentioned)]})
                    var_dfOutputNews = pd.concat([var_dfOutputNews,var_dfNewRow], ignore_index=True)
                except:
                    continue

            log.console_message(f"\nNext page...", "regular")

            # Goes to the next page of news
            self.var_browser.find_element("//div[@class='search-results-module-next-page']/a").click()

            var_intCount+=1

        log.console_message(f"\nNews articles extracted successfully!", "regular")
        
        return var_dfOutputNews

        