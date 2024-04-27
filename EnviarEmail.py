import smtplib
from tkinter import *
from tkinter import messagebox
from tkinter import Text, filedialog
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from PIL import Image
import io
import base64
import icon
import tempfile

temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.ico')
temp_file.write(base64.b64decode(icon.icon))
temp_file.close()

icon_image = Image.open(io.BytesIO(base64.b64decode(icon.icon)))

cor_background = "#C5D8D1"
janela_principal = Tk()
janela_principal.title("Enviar Emails")
janela_principal.configure(bg=cor_background)
janela_principal.state("zoomed")
janela_principal.iconbitmap(temp_file.name)

texto_titulo = Label(janela_principal, text="Enviar E-mails", bg=cor_background, font=("Arial", 16))
texto_titulo.pack(pady=(50, 10), fill="x")  # Centraliza verticalmente
texto_titulo.configure(font=("Arial", 16))

def enviar_email(assunto, destinatario, mensagem, password, remetente, anexo):
    
    destinatarios = destinatario.split()
    
    corpo_email = "<p>{0}</p>".format(mensagem.replace("\n", "<br>"))
    
    msg = MIMEMultipart()
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = ", ".join(destinatarios)
    msg.attach(MIMEText(mensagem, 'plain'))
    
    if anexo:
        nome_arquivo = os.path.basename(anexo)
        with open(anexo, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        # Codifica o arquivo em base64
        encoders.encode_base64(part)        
        # Adiciona o cabeçalho do anexo
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {nome_arquivo}",
        )

        # Adiciona o anexo ao e-mail
        msg.attach(part)

    
    try:
    
        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(msg['From'], password)
        s.sendmail(msg['From'], destinatarios, msg.as_string(). encode ('utf-8'))
        s.quit()
        
        messagebox.showinfo("Sucesso", "E-mail enviado com sucesso!")
    
    except smtplib.SMTPAuthenticationError:
        
        messagebox.showerror("Falha ao enviar E-mail", "Error: Por favor, preencha os campos corretamente.")
    
def enviar():
    
    assunto = assunto_entry.get()
    destinatario = destinatario_entry.get()
    mensagem = mensagem_entry.get("1.0", "end-1c")
    password = password_entry.get()
    remetente = remetente_entry.get()
    anexo = anexo_entry.get()
    
    enviar_email(assunto, destinatario, mensagem, password, remetente, anexo)
    
def selecionar_anexo():
    arquivo = filedialog.askopenfilename()
    anexo_entry.delete(0, END)
    anexo_entry.insert(0, arquivo)
    
cor_borda = "#12263A"
cor_fundo_entry = "#06BCC1"

frame_para = Frame(janela_principal, bg=cor_background)
frame_para.pack(pady=(10, 5))
texto_destinatario = Label(frame_para, text="Para", bg=cor_background, font=("Arial", 13))
texto_destinatario.pack(side=TOP, padx=(10, 5))
destinatario_entry = Entry(frame_para, width=40, font=("Arial", 13), bd=0, highlightbackground=cor_borda, highlightcolor=cor_borda, highlightthickness=2, bg=cor_fundo_entry)
destinatario_entry.pack(side=BOTTOM, padx=5)

frame_assunto = Frame(janela_principal, bg=cor_background)
frame_assunto.pack(pady=2)
texto_titulo_email = Label(frame_assunto, text="Assunto", bg=cor_background, font=("Arial", 13))
texto_titulo_email.pack(side=TOP, padx=(10, 5))
assunto_entry = Entry(frame_assunto, width=40, font=("Arial", 13), bd=0, highlightbackground=cor_borda, highlightcolor=cor_borda, highlightthickness=2, bg=cor_fundo_entry)
assunto_entry.pack(side=BOTTOM, padx=5)

frame_mensagem = Frame(janela_principal, bg=cor_background)
frame_mensagem.pack(pady=2)
texto_mensagem = Label(frame_mensagem, text="Mensagem", bg=cor_background, font=("Arial", 13))
texto_mensagem.pack(side=TOP, padx=(10, 5))
mensagem_entry = Text(frame_mensagem, width=40, height=10, font=("Arial", 13), bd=0, highlightbackground=cor_borda, highlightcolor=cor_borda, highlightthickness=2, bg=cor_fundo_entry, wrap=NONE)
mensagem_entry.pack(side=BOTTOM, padx=5)
scrollbar_vertical = Scrollbar(frame_mensagem, command=mensagem_entry.yview)
mensagem_entry.config(yscrollcommand=scrollbar_vertical.set)

frame_email_remetente = Frame(janela_principal, bg=cor_background)
frame_email_remetente.pack(pady=2)
texto_email_remetente = Label(frame_email_remetente, text="E-mail do Remetente", bg=cor_background, font=("Arial", 13))
texto_email_remetente.pack(side=TOP, padx=(10, 5))
remetente_entry = Entry(frame_email_remetente, width=40, font=("Arial", 13), bd=0, highlightbackground=cor_borda, highlightcolor=cor_borda, highlightthickness=2, bg=cor_fundo_entry)
remetente_entry.pack(side=BOTTOM, padx=5)

frame_senha_app = Frame(janela_principal, bg=cor_background)
frame_senha_app.pack(pady=2)
texto_senha_app = Label(frame_senha_app, text="Senha do E-mail Remetente", bg=cor_background, font=("Arial", 13))
texto_senha_app.pack(side=TOP, padx=(10, 5))
password_entry = Entry(frame_senha_app, width=40, font=("Arial", 13), bd=0, highlightbackground=cor_borda, highlightcolor=cor_borda, highlightthickness=2, bg=cor_fundo_entry)
password_entry.pack(side=BOTTOM, padx=5)

frame_botoes = Frame(janela_principal, bg=cor_background)
frame_botoes.pack(pady=2)
botao_enviar = Button(frame_botoes, text="Enviar", command=enviar, bg=cor_fundo_entry, bd=3, font=("Arial", 13))
botao_enviar.pack(side=TOP, padx=(10, 5))
botao_anexo = Button(frame_botoes, text="Anexar Arquivo", command=selecionar_anexo, bg=cor_fundo_entry, bd=3, font=("Arial", 13))
botao_anexo.pack(side=BOTTOM, padx=5, pady=5)

anexo_entry = Entry(janela_principal, width=40, font=("Arial", 13), bd=0, highlightbackground="#12263A", highlightcolor="#12263A", highlightthickness=2, bg="#06BCC1")
anexo_entry.pack(pady=2)

for widget in janela_principal.winfo_children():
    widget.pack_configure(anchor="n")
    
janela_principal.mainloop()