import mysql.connector
from prettytable import PrettyTable
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageTemplate, Frame
from reportlab.platypus.flowables import PageBreak
from reportlab.platypus import Paragraph
from reportlab.lib import styles
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

from email import encoders


db_config = {
    "host": "localhost",
    "user": "xatovate",
    "password": "###",
    "database": "username_pass"
}

db = mysql.connector.connect(**db_config)
cursor = db.cursor()



print ('enter the number  ')
print( '\033[95m 1 : insert new password \033[0m \n\033[93m 2 :  update passwords \033[0m \n\033[91m 3 : Delete password \033[0m \n\033[92m 4 : send email \033[0m\n\033[30m q for quit \033[0m')

while True:
    userInput = input()
    
    if userInput == 'q':
         break

    try:
        userInput = int(userInput)
        if userInput not in [1 , 2 , 3 ]:
             print('enter just 1 ,  2 , 3 or q for quit')
        else:
             break 
        
    except ValueError:
        print("Invalid input. Please enter an integer.")

if userInput == 1 :
     
     while True:
          username = input('Enter your username: ')
          password = input('Enter your password: ')

          if username and password:  
               description = input('Enter the description: ')
               break
          else:
               print("Both username and password cannot be empty. Please enter both.")

     query = '''
     INSERT INTO username_pass (username, password, description)
     VALUES (%s, %s, %s)
     '''

     cursor.execute(query, (username, password, description))
     db.commit()


     cursor.execute("SELECT id , username, password , description FROM username_pass")
     result = cursor.fetchall()

     table = PrettyTable()
     table.field_names = ["ID" , "Username", "Password" , "Description"]
     table_data = [table.field_names]

     for row in result:
         table.add_row(row)
         table_data.append([row[0], row[1] , row[2] ,  row[3]]) 


     # Create a PDF
     pdf_filename = "username_pass.pdf"
     document = SimpleDocTemplate(pdf_filename, pagesize=letter)
     doc = SimpleDocTemplate(pdf_filename, pagesize=letter)  


     def footer(canvas, doc):
          canvas.saveState()
          footer_text = "Created by Salehmhosseini"
          footer = Paragraph(footer_text, styles.getSampleStyleSheet()['Normal'])
          w, h = footer.wrap(doc.width, doc.bottomMargin)
          footer.drawOn(canvas, (doc.pagesize[0] - w) / 2, h - 10)
          
     page_template = PageTemplate(id='main_template', frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 40, id='normal')])
     page_template.afterDrawPage = footer
     document.addPageTemplates([page_template])
     
     # Create a table with the table data
     table = Table(table_data)
     table.setStyle(TableStyle([
         ('BACKGROUND', (0, 0), (-1, 0), (0.7, 0.7, 0.7)),
         ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
         ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),
         ('GRID', (0, 0), (-1, -1), 1, (0.7, 0.7, 0.7))
     ]))

     # Build the PDF
     document.build([table])

     print(f"PDF file '{pdf_filename}'\033[92m created successfully. \033[0m")

if userInput == 2 :
     
     cursor.execute("SELECT id , username, password , description FROM username_pass")
     result = cursor.fetchall()

     table = PrettyTable()
     table.field_names = ["ID" , "Username", "Password" , "Description"]
     table_data = [table.field_names]

     for row in result:
          table.add_row(row)
     
     print(table)
     
     cursor.execute("SELECT id FROM username_pass")

     idList = [row[0] for row in cursor.fetchall()]
     
     while True :
          userPassId =  input('please enter your id : ')
          
          if int(userPassId) in idList :
               break
          
          else : 
               print('id not found')
     cursor.execute(f"SELECT username FROM username_pass WHERE id = {userPassId} ")
     print('Your username is : ',cursor.fetchall()[0][0] )
     new_username = input('enter the new username or enter for continue : ')
     if new_username :
          
          update_query = f"UPDATE username_pass SET username = '{new_username}' WHERE id = {userPassId}"
          cursor.execute(update_query)
          
     cursor.execute(f"SELECT password FROM username_pass WHERE id = {userPassId} ")
     print('Your password is : ',cursor.fetchall()[0][0] )
     new_password = input('enter the new password or enter for continue : ')

     if new_password :
     
          update_query = f"UPDATE username_pass SET password = '{new_password}' WHERE id = {userPassId}"
          cursor.execute(update_query)
          
          
     cursor.execute(f"SELECT description FROM username_pass WHERE id = {userPassId} ")
     print('Your description is : ',cursor.fetchall()[0][0] )
     new_description = input('enter the new description or enter for continue : ')

     if new_description :
     
          update_query = f"UPDATE username_pass SET description = '{new_description}' WHERE id = {userPassId}"
          cursor.execute(update_query)
          
     cursor.execute("SELECT id , username, password , description FROM username_pass")
     result = cursor.fetchall()

     table = PrettyTable()
     table.field_names = ["ID" , "Username", "Password" , "Description"]
     table_data = [table.field_names]

     for row in result:
         table.add_row(row)
         table_data.append([row[0], row[1] , row[2] ,  row[3]]) 


     # Create a PDF
     pdf_filename = "username_pass.pdf"
     document = SimpleDocTemplate(pdf_filename, pagesize=letter)
     doc = SimpleDocTemplate(pdf_filename, pagesize=letter)  


     def footer(canvas, doc):
          canvas.saveState()
          footer_text = "Created by Salehmhosseini"
          footer = Paragraph(footer_text, styles.getSampleStyleSheet()['Normal'])
          w, h = footer.wrap(doc.width, doc.bottomMargin)
          footer.drawOn(canvas, (doc.pagesize[0] - w) / 2, h - 10)
          
     page_template = PageTemplate(id='main_template', frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 40, id='normal')])
     page_template.afterDrawPage = footer
     document.addPageTemplates([page_template])
     
     # Create a table with the table data
     table = Table(table_data)
     table.setStyle(TableStyle([
         ('BACKGROUND', (0, 0), (-1, 0), (0.7, 0.7, 0.7)),
         ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
         ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),
         ('GRID', (0, 0), (-1, -1), 1, (0.7, 0.7, 0.7))
     ]))

     # Build the PDF
     document.build([table])

     print(f"PDF file '{pdf_filename}'\033[92m created successfully. \033[0m")
     
     
if userInput == 3 :
     
          
     cursor.execute("SELECT id , username, password , description FROM username_pass")
     result = cursor.fetchall()

     table = PrettyTable()
     table.field_names = ["ID" , "Username", "Password" , "Description"]
     table_data = [table.field_names]

     for row in result:
          table.add_row(row)
     
     print(table)
     
     cursor.execute("SELECT id FROM username_pass")

     idList = [row[0] for row in cursor.fetchall()]
     
     while True :
          userPassId =  input('please enter your id : ')
          
          if int(userPassId) in idList :
               break
          
          else : 
               print('id not found')
     print(f'your choosen id is : \033[1m{userPassId}\033[0m')
     
     while True : 
          
          user_answer = input("\033[1m Are you sure to delete this?? \033[0m  (y/n)")
          if user_answer == 'y' :
               cursor.execute(f"DELETE FROM username_pass WHERE id = {userPassId}")
               db.commit()
               print('\033[92m Record successfully deleted \033[0m')
               break
          elif user_answer == 'n' :
               break 
          
          
     cursor.execute("SELECT id , username, password , description FROM username_pass")
     result = cursor.fetchall()

     table = PrettyTable()
     table.field_names = ["ID" , "Username", "Password" , "Description"]
     table_data = [table.field_names]

     for row in result:
         table.add_row(row)
         table_data.append([row[0], row[1] , row[2] ,  row[3]]) 


     # Create a PDF
     pdf_filename = "username_pass.pdf"
     document = SimpleDocTemplate(pdf_filename, pagesize=letter)
     doc = SimpleDocTemplate(pdf_filename, pagesize=letter)  


     def footer(canvas, doc):
          canvas.saveState()
          footer_text = "Created by Salehmhosseini"
          footer = Paragraph(footer_text, styles.getSampleStyleSheet()['Normal'])
          w, h = footer.wrap(doc.width, doc.bottomMargin)
          footer.drawOn(canvas, (doc.pagesize[0] - w) / 2, h - 10)
          
     page_template = PageTemplate(id='main_template', frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 40, id='normal')])
     page_template.afterDrawPage = footer
     document.addPageTemplates([page_template])
     
     # Create a table with the table data
     table = Table(table_data)
     table.setStyle(TableStyle([
         ('BACKGROUND', (0, 0), (-1, 0), (0.7, 0.7, 0.7)),
         ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
         ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),
         ('GRID', (0, 0), (-1, -1), 1, (0.7, 0.7, 0.7))
     ]))

     # Build the PDF
     document.build([table])

     print(f"PDF file '{pdf_filename}'\033[92m created successfully. \033[0m")
          
          
     
     
         

# TODO it's not work , fix it to send the username_pass.pdf file with email wheh the user type 4     
if userInput == 4 :
          
     # Email configuration
     sender_email = "practical.mail.me@gmail.com"
     receiver_email = "######"
     subject = "PDF Attachment"
     body = "temp text"

     # Attach the PDF file
     file_path = "username_pass.pdf"

     
     msg = MIMEMultipart()
     msg['From'] = sender_email
     msg['To'] = receiver_email
     msg['Subject'] = subject
     msg.attach(MIMEText(body, 'plain'))

     # Attach the PDF file
     attachment = open(file_path, 'rb')
     pdf = MIMEBase('application', 'octet-stream')
     pdf.set_payload((attachment).read())
     encoders.encode_base64(pdf)
     pdf.add_header('Content-Disposition', "attachment; filename=pdf_file.pdf")
     msg.attach(pdf)

     # Establish an SMTP connection
     smtp_server = "smtp.gmail.com"
     smtp_port = 587
     smtp_username = '######'
     smtp_password = "######"

     server = smtplib.SMTP(smtp_server, smtp_port)
     server.starttls()
     server.login(smtp_username, smtp_password)

     # Send the email
     server.sendmail(sender_email, receiver_email, msg.as_string())
     server.quit()