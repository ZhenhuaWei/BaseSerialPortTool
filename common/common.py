import datetime

def get_datetime():
    """ get current date time, as accurate as milliseconds
        
        Args: None
            
        Returns:
            str type
            eg: "2018-10-01 00:32:39.993176"
            
    """
    return str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))