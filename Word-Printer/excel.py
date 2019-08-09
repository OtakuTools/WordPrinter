from openpyxl import load_workbook
from openpyxl.styles import PatternFill

class excel:
    def title( self, src , dst , title ):
        xlsx = load_workbook( filename = src )
        #xlsx.active['A2'] = title
        #xlsx.active['A2'].fill = PatternFill( fill_type=None )
        for worksheet in xlsx.worksheets:
            if worksheet['A2'].fill.fgColor.rgb == 'FFFFFF00':
                    worksheet['A2'] = title
                    worksheet['A2'].fill = PatternFill( fill_type=None )
        return xlsx