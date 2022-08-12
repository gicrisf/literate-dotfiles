import glob, os
from utils import AttributeDict
import secrets

env = AttributeDict()

# Directories
env.epub_path='./Scaricati'
env.epub_path_converted='./epub'
env.mobi_path_sent = './mobi'

# SMTP settings
env.smtp = secrets.tokindle_smtp
env.port = secrets.tokindle_port
env.username = secrets.tokindle_username
env.password = secrets.tokindle_password
env.my_mail = secrets.tokindle_my_mail
env.kindle_mail = secrets.tokindle_kindle_mail

def main():
    """send to kindle"""
    os.chdir(env.epub_path)
    for file in glob.glob("*.epub"):
        filename, ext = os.path.splitext(file)

        # FILE CONVERSION
        if os.path.exists("{}.mobi".format(filename)):
            print("********{}.mobi already exists********".format(filename))
        else:
            print("********Converting to mobi: {}********".format(filename))
            os.system('ebook-convert \"{0}\" .mobi'.format(file))

        # Move epub to proper directory
        os.system('mv \"{0}\" {1}'.format(file, env.epub_path_converted))

        # Pre-setting send command
        cmd = "calibre-smtp"
        a = f"-a \"{filename}\".mobi"
        s = f"-s \"{filename}\""
        r = f"-r \"{env.smtp}\""
        port = f"--port {env.port}"
        u = f"-u \"{env.username}\""
        p = f"-p \"{env.password}\""
        mail = f"\"{env.my_mail}\""
        kindle_mail = f"\"{env.kindle_mail}\""

        # Run send command
        print("********Sending to {}********".format(env.kindle_mail))
        os.system(f'{cmd} {a} {s} {r} {port} {u} {p} {mail} {kindle_mail} \"\"')

        # Move mobi to proper directory
        os.system('mv \"{0}.mobi\" {1}'.format(filename, env.mobi_path_sent))

if __name__ == '__main__':
    main()
