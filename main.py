from train import run


if __name__ == "__main__":    
    INPUT_ID = "1670766294"    

    INPUT_DEP = "서울"
    INPUT_DES = "전주"

    YEAR = 2018
    MONTH = 2
    DATE = 14
    HOUR_MIN = [14, 00]
    HOUR_MAX = [17, 00]

    run(INPUT_ID, INPUT_DEP, INPUT_DES, YEAR, MONTH, DATE, HOUR_MIN, HOUR_MAX)