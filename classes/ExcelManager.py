from RPA.Robocorp.WorkItems import WorkItems
import pandas as pd
import logging

logger = logging.getLogger(__name__)

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

        logger.info("Reading the work items excel file..")

        # Initialize WorkItems instance
        var_wiWorkItems = WorkItems()
        var_wiWorkItems.get_input_work_item()

        # Reads the excel file
        var_dfWorkItems = pd.read_excel(arg_strExcelPath)

        logger.info(f"{len(var_dfWorkItems)} workitems were identified")

        logger.info("Creating new workitems")

        #iterates over the dataframe and adds each row as a new work item
        for index, row in var_dfWorkItems.iterrows():
            var_wiNewWorkItem = var_wiWorkItems.create_output_work_item()  # Create a new work item
            var_wiNewWorkItem.payload = (row.to_dict())
            var_wiWorkItems.save_work_item() # Saves the new work item


        logger.info("Workitems created successfully!")