import os
import time
import numpy as np
import pandas as pd
import py_parser
import lint_engine
import constants
import logging


logger = logging.getLogger("ForensicLogger")
logger.setLevel(logging.INFO)


file_handler = logging.FileHandler("forensics.log")
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)


def getCSVData(dic_, dir_repo):
   
    try:
        temp_list = []
        for TEST_ML_SCRIPT in dic_:
            logger.info(f"Processing script: {TEST_ML_SCRIPT}")

            
            data_load_counta = lint_engine.getDataLoadCount(TEST_ML_SCRIPT)
            logger.info(f"Data load count (a): {data_load_counta}")
            data_load_countb = lint_engine.getDataLoadCountb(TEST_ML_SCRIPT)
            data_load_countc = lint_engine.getDataLoadCountc(TEST_ML_SCRIPT)

            model_load_counta = lint_engine.getModelLoadCounta(TEST_ML_SCRIPT)
            model_load_countb = lint_engine.getModelLoadCountb(TEST_ML_SCRIPT)
            model_load_countc = lint_engine.getModelLoadCountc(TEST_ML_SCRIPT)
            model_load_countd = lint_engine.getModelLoadCountd(TEST_ML_SCRIPT)

         
            data_load_count = data_load_counta + data_load_countb + data_load_countc
            model_load_count = (
                model_load_counta
                + model_load_countb
                + model_load_countc
                + model_load_countd
            )
            total_event_count = data_load_count + model_load_count

            logger.info(f"Total event count for {TEST_ML_SCRIPT}: {total_event_count}")
            temp_list.append((dir_repo, TEST_ML_SCRIPT, total_event_count))
        return temp_list
    except Exception as e:
        logger.error(f"Error in getCSVData: {e}")
        raise


def getAllPythonFilesinRepo(path2dir):

    try:
        valid_list = []
        for root_, _, filenames in os.walk(path2dir):
            for file_ in filenames:
                full_path_file = os.path.join(root_, file_)
                if (
                    os.path.exists(full_path_file)
                    and file_.endswith(constants.PY_FILE_EXTENSION)
                    and py_parser.checkIfParsablePython(full_path_file)
                ):
                    valid_list.append(full_path_file)
        logger.info(f"Found {len(valid_list)} Python files in {path2dir}")
        return np.unique(valid_list)
    except Exception as e:
        logger.error(f"Error in getAllPythonFilesinRepo: {e}")
        raise


def getFileList(input_dir):
   
    try:
        logger.info(f"Scanning directory: {input_dir}")
        files = [
            f.path
            for f in os.scandir(input_dir)
            if os.path.isfile(f.path) and f.name.endswith(constants.PY_FILE_EXTENSION)
        ]
        logger.info(f"Retrieved {len(files)} files from {input_dir}")
        return files
    except Exception as e:
        logger.error(f"Error in getFileList: {e}")
        raise


def writeToCSV(dataframe, output_path):
   
    try:
        if dataframe.empty:
            logger.warning(f"No data available to write to CSV at {output_path}. Skipping file generation.")
            return
        dataframe.to_csv(output_path, header=constants.CSV_HEADER, index=False, encoding=constants.UTF_ENCODING)
        logger.info(f"Successfully wrote CSV to {output_path}")
    except Exception as e:
        logger.error(f"Error writing to CSV: {e}")
        raise


def runFameML(inp_dir, csv_fil):
 
    try:
        start_time = time.time()
        logger.info(f"Starting runFameML with directory: {inp_dir}")

 
        df_list = []
        for subfolder in [f.path for f in os.scandir(inp_dir) if f.is_dir()]:
            logger.info(f"Processing subfolder: {subfolder}")
            python_files = getAllPythonFilesinRepo(subfolder)
            if not python_files.size:  
                logger.warning(f"No Python files found in {subfolder}.")
            csv_data = getCSVData(python_files, subfolder)
            df_list.extend(csv_data)

       
        full_df = pd.DataFrame(df_list, columns=["Directory", "Script", "Total Events"])
        writeToCSV(full_df, csv_fil)

        end_time = time.time()
        duration = round(end_time - start_time, 2)
        logger.info(f"Completed runFameML in {duration} seconds")
    except Exception as e:
        logger.error(f"Error in runFameML: {e}")
        raise


if __name__ == "__main__":
    
    try:
        dir_path = os.getcwd()
        csv_output = os.path.join(dir_path, "output.csv")

        logger.info("Script started")
        runFameML(dir_path, csv_output)
        logger.info("Script finished successfully")
    except Exception as main_exception:
        logger.error(f"Error in main execution: {main_exception}")
