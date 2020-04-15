class BuilderException(Exception):
    pass

class MissingRequirementsFile(BuilderException):
    pass

class MissingNotebookFile(BuilderException):
    pass

class EnvironmentVarName(BuilderException):
    pass

