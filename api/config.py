"""API Configs"""
import operator

OPERATIONS_DICT = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv
    }


CSV = 'csv'
XLSX = 'xlsx'
SUPPORTED_FORMATS = (CSV, XLSX)
