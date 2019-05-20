import xlrd
import xlwt
from xlutils.copy import copy

class excel():
    def title( self, src , dst , title ):
        src = xlrd.open_workbook( src , formatting_info=True )
        xls = copy( src )
        sheet = xls.get_sheet(0)
        style = xlwt.Style.easyxf("font: name 宋体, height 0x00F0; align: wrap on, vert centre, horiz center")
        sheet.write( 1,0,title,style )
        return xls