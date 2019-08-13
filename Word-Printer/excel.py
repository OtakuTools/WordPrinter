from openpyxl import load_workbook
from openpyxl.styles import PatternFill,Font

class excel:
    def title( self, title ):
        for worksheet in self.xlsx.worksheets:
            if worksheet['A2'].fill.fgColor.rgb == 'FFFFFF00':
                worksheet['A2'] = title
                worksheet['A2'].fill = PatternFill( fill_type=None )
                worksheet['A2'].font = Font( name=worksheet['A2'].font.name ,color=None )

    def replace( self , project ):
        for worksheet in self.xlsx.worksheets:
            for row in worksheet.rows:
                for curCell in row:
                    if curCell.fill.fgColor.rgb == 'FFFFFF00':
                        print( str(curCell.font.color) )
                        if curCell.font.color.rgb == 'FFFF0000':
                            curCell.value = title
                        elif curCell.font.color.rgb == 'FFD30000':
                            curCell.value = "客户名称：" + project.BasicInfo.PartyA.company
                        else:
                            pass
                        curCell.fill = PatternFill( fill_type=None )
                        curCell.font = Font( name=curCell.font.name ,color=None )

    def run( self, src , dst , titleName , project):
        self.xlsx = load_workbook( filename = src )
        self.title( titleName )
        self.replace( project )
        return self.xlsx