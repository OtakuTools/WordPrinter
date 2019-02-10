from docx import Document
from docx.shared import Inches
from docx.shared import RGBColor

document = Document()

document.add_heading('Document Title', 0)

p = document.add_paragraph('A plain paragraph having some ')
p.add_run('bold,').bold = True
p.add_run('highlight,').font.highlight_color = 7 # YELLOW
p.add_run('color,').font.color.rgb = RGBColor(0xff, 0x00, 0x00)
p.add_run('underline').font.underline = True
run = p.add_run(' and some ')
run.font.color.rgb = RGBColor(0xff, 0x00, 0x00)
run.font.highlight_color = 7 # YELLOW

p.add_run('italic.').italic = True

document.add_heading('Heading, level 1', level=1)
document.add_paragraph('Intense quote', style='Intense Quote')

document.add_paragraph(
    'first item in unordered list', style='List Bullet'
)
document.add_paragraph(
    'first item in ordered list', style='List Number'
)

records = (
    (3, '101', 'Spam'),
    (7, '422', 'Eggs'),
    (4, '631', 'Spam, spam, eggs, and spam')
)

table = document.add_table(rows=1, cols=3)
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Qty'
hdr_cells[1].text = 'Id'
hdr_cells[2].text = 'Desc'
for qty, id, desc in records:
    row_cells = table.add_row().cells
    row_cells[0].text = str(qty)
    row_cells[1].text = id
    row_cells[2].text = desc

document.add_page_break()

document.save('demo.docx')

for p in document.paragraphs:
    for r in p.runs:
        print( r.text )
        print( "    bold:" + str(r.bold) )
        print( "    italic:" + str(r.italic) )
        print( "    color:" + str(r.font.color.rgb))

print("----------------------------")
for p in document.paragraphs:
    for r in p.runs:
        if str(r.font.color.rgb) == 'FF0000' or r.font.highlight_color == 7:
            print( r.text )