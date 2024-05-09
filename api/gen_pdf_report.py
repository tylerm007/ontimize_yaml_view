import json 
import contextlib
import logging
from api.exression_parser import parsePayload
from base64 import b64encode
from sqlalchemy.sql import text
import safrs
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageTemplate, Frame, Spacer
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO
    

app_logger = logging.getLogger(__name__)

db = safrs.DB 
session = db.session 
def gen_report(api_clz, project_dir, payload) -> any:
        ''' Report PDF POC https://docs.reportlab.com/
        pip install reportlab 
        Ontimize Payload:
        {"title":"","groups":[],
        "entity":"Customer",
        "path":"/Customer",
        "service":"Customer",
        "vertical":true,
        "functions":[],
        "style":{"grid":false,"rowNumber":false,"columnName":true,"backgroundOnOddRows":false,"hideGroupDetails":false,"groupNewPage":false,"firstGroupNewPage":false},
        "subtitle":"",
        "columns":[{"id":"Id","name":"Id"},{"id":"CompanyName","name":" Company Name*"}],
        "orderBy":[],
        "language":"en",
        "filters":{"columns":["Id","CompanyName","Balance","CreditLimit","OrderCount","UnpaidOrderCount","Client_id","ContactName","ContactTitle","Address","City","Region","PostalCode","Country","Phone","Fax"],
        "sqltypes":{"Id":1111,"CompanyName":1111,"Balance":8,"CreditLimit":8,"OrderCount":4,"UnpaidOrderCount":4,"Client_id":4,"ContactName":1111,"ContactTitle":1111,"Address":1111,"City":1111,"Region":1111,"PostalCode":1111,"Country":1111,"Phone":1111,"Fax":1111},
        "filter":{},
        "offset":0,
        "pageSize":20},
        "advQuery":true}
        '''

        filter, columns, sqltypes, offset, pagesize, orderBy, data = parsePayload(payload)
        if len(payload) == 3:
            return jsonify({})
        
        entity = payload["entity"]
        columns = "*"
        rows = get_rows(api_clz, entity, columns)
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        
        def add_page_number(canvas, doc):
            page_num = canvas.getPageNumber()
            text = "Page %s" % page_num
            canvas.drawRightString(letter[0] - inch, inch, text)

        page_template = PageTemplate(id='my_page_template', frames=[], onPage=add_page_number)
        #doc.addPageTemplates([page_template])
        
        content = []

        # Add title
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        title = payload["title"] if payload["title"] != '' else f"{entity.upper()} Report"
        content.append(Paragraph(title, title_style))
        content.append(Spacer(1, 0.2 * inch)) 
        # Column Header
        data = []
        col_data = []
        for column in columns:
            col_data.append(column['name'])
            
        # Define table data (entity)
        data.append(col_data)
        
        for row in rows['data']:
            r = []
            for col in columns:
                r.append(row[col["id"]])
            data.append(r)

        # Create table
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        content.append(table)
        
        # Build PDF document
        doc.build(content)  

        with open(f"{project_dir}/{entity}.pdf", "wb") as binary_file:
            binary_file.write(buffer.getvalue())
        
        output =  b64encode(buffer.getvalue())
        
        return {"code": 0,"message": "","data": [{"file":str(output)[2:-1] }],"sqlTypes": None}
    
def get_rows(clz, entity, columns) -> any:
    sql = f"SELECT {columns} FROM {entity}"
    return session.query(text(sql)).all()