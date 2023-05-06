from DataBase import DataBase
from FindMeaning import FindMeaning

if __name__ == '__main__':
    dark = DataBase('today', FindMeaning)
    print(dark.data)
