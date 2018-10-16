import datetime


def daterange(start_date, end_date):

    datas = []

    for n in range(int((end_date - start_date).days)):
        datas.append(start_date + datetime.timedelta(n))

    return datas
