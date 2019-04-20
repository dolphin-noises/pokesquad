import pkgutil


class FileParser:
    @staticmethod
    def parse(file):
        file_data = pkgutil.get_data(__package__, file)
        file_list = file_data.decode().split('\r\n')
        file_split = []
        for x in file_list:
            file_split.append(x.split('|'))
        return file_split