from openpyxl import load_workbook
from openpyxl.styles import PatternFill
'''
class excel():
    def title( self, src , dst , title ):
        src = xlrd.open_workbook( src , formatting_info=True )
        xls = copy( src )
        sheet = xls.get_sheet(0)
        style = xlwt.Style.easyxf("font: name 宋体, height 0x00F0; align: wrap on, vert centre, horiz center")
        sheet.write( 1,0,title,style )
        return xls
'''

class excel:
    def title( self, src , dst , title ):
        xlsx = load_workbook( filename = src )
        xlsx.active['A2'] = title
        xlsx.active['A2'].fill = PatternFill( fill_type=None )
        return xlsx