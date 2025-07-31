import logging
import os


class AppLogger:
    @staticmethod
    def get_logger(name = 'AppLogger', log_dir = 'logs', level=logging.INFO):
        """
        Retrieves or creates a named logger instance, configuring it to write
        to a specific log file in the 'logs' directory.

        Args:
            name (str): The name of the logger (e.g., '__name__' of the module).
                        This name will also be used to derive the log file name.
            log_dir (str): The directory where logs should be stored, relative to the project root.
            level (int): The minimum logging level for this logger.

        Returns:
            logging.Logger: The configured logger instance.
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.propagate = False

        # Determine the project root dynamically
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.dirname(current_file_dir)
        project_root = os.path.dirname(src_dir)

        full_log_dir_path = os.path.join(project_root, log_dir)

        # Create the log directory if it doesn't exist
        if not os.path.exists(full_log_dir_path):
            os.makedirs(full_log_dir_path)

        log_file_name = f"{name.replace('.', '_')}.log"
        log_file_path = os.path.join(full_log_dir_path, log_file_name)

    
        if not logger.handlers:
            # File handler
            file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
            file_handler.setLevel(level)
           
            file_formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s:%(lineno)d - %(message)s')

            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)


        return logger
