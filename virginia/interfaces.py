from zope.interface import Interface

class IFilesystem(Interface):
    """ Marker interface for a filesystem object
    """

class IDirectory(Interface):
    """ Marker interface for directories
    """

class IFile(Interface):
    """ Marker interface for files
    """

class IStructuredText(Interface):
    """ Marker interface for structured text documents
    """

    


    
