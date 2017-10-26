from openpyxl import Workbook
from openpyxl import Workbook
from openpyxl.chart import (
    AreaChart,
    Reference,
    Series,
)
#创建一个工作簿
wb = Workbook()
#活取一个活动的工作表
ws = wb.active

#按行优先迭代
ws['C9'] = 'test'
print(tuple(ws.rows))

#按列优先迭代
print(tuple(ws.columns))