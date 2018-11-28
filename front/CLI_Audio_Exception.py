class CLI_Audio_Exception(Exception):
    """Parent class for other excpetions"""
    pass

class CLI_Audio_File_Exception(CLI_Audio_Exception):
    """Raised when audio file cannot be played"""
    pass

class CLI_Audio_Screen_Size_Exception(CLI_Audio_Exception):
    """Raised when screen size is too small on startup"""
    pass
