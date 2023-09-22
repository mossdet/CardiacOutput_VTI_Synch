import os


def get_table_destination_path():
    path = os.path.dirname(os.path.abspath(__file__))
    cutIdx = path.rfind(os.path.sep)
    workspacePath = path[:cutIdx]

    tables_path = workspacePath + os.path.sep + 'Tables' + os.path.sep
    os.makedirs(tables_path, exist_ok=True)

    return tables_path
