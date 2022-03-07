import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def send_mail(pass_temp, username, name, link):
    # create message object instance
    msg = MIMEMultipart()

    message = """
    <html>
    <body>
        <div style="margin:0;padding-top:0;background-color:#c7cda7;color:#000000">
            <div class="adM"></div>
        
            <center>
                <table width="100%" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td height="34"></td>
                        </tr>
                    </tbody>
                </table>
                <table width="600" class="m_-4899739947963130127mobile" cellpadding="0" cellspacing="0" style="background-color:#f3f2f0;border-radius:3rem">
                    <tbody>
                        <tr>
                            <td style="padding:24px;">
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tbody>
                                        <tr>
                                            <td style="font-size:18px;font-family:'Open Sans',sans-serif;font-weight:bold;padding:8px 0 8px 0">
                                                Querido """ + name + """, su solicitud ha sido aprobada, estos son los datos de su login<br><br>
                                                email: <a href="mailto:""" + username + """ target="_blank">""" + username + """</a><br>
                                                senha: """ + pass_temp + """
                                            </td>
                                        </tr>
                                        
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </tbody>
                </table>


                <table width="600" class="m_-4899739947963130127mobile" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td><img width="100%"></td>
                        </tr>
                    </tbody>
                </table>
                <table width="100%" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td height="24"></td>
                        </tr>
                    </tbody>
                </table>

                <table width="600" class="m_-4899739947963130127mobile" cellpadding="0" cellspacing="0">
                    <tbody>
                       
                        <tr>
                            <td style="font-size:12px;line-height:18px;font-family:'Open Sans',sans-serif;color:#474747;padding:0 16px 0 16px;text-align:center">
                                ©2020 
                            </td>
                        </tr>
                    </tbody>
                </table>
                <table width="100%" cellpadding="0" cellspacing="0">
                    <tbody>
                        <tr>
                            <td height="32"></td>
                        </tr>
                    </tbody>
                </table>
            </center>
            <div class="yj6qo"></div>
            <div class="adL"></div>
        </div>
    </body>
</html>

    """

    # setup the parameters of the message
    password = "suporte@ievo4action"
    msg['From'] = "suporte@ievo4action.com.br"
    msg['To'] = username
    msg['Subject'] = "Solicitud Aprobada"

    # add in the message body
    part_1 = MIMEText(message, 'html')
    msg.attach(part_1)

    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    print
    "successfully sent email to %s:" % (msg['To'])