from robocorp import workitems
import pandas as pd
import logging

class ExcelManager:
    """
    Class responsible for managing all excel related tasks.

    """

    @classmethod
    def setWorkItems(cls, arg_strExcelPath:str=None):
        """
        Reads the 'workitems.xlsx' file from '\input' and creates a workitem for each row.

        Parameters:
            arg_strExcelPath (str): The Path of the excel file containing the work items that are to be added to the queue
        
        Returns:
            None

        """

        logging.info("Reading the work items excel file..")

        # Reads the excel file
        var_dfWorkItems = pd.read_excel(arg_strExcelPath)

        logging.info(f"{len(var_dfWorkItems)} workitems were identified")

        logging.info("Creating new workitems")

        #iterates over the dataframe and adds each row as a new work item
        for index, row in var_dfWorkItems.iterrows():
            workitems.outputs.create(row.to_dict())


        logging.info("Workitems created successfully!")