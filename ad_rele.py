import LaurentJSON as LJ
import config
import time

L_IP24 = config.Laurent_IP_Pool24
L_Pass = config.Laurent_Pass

def switch_rele():
    code = 404
    while code == 404:
        code = LJ.check_ip(f"{L_IP24}/cmd.cgi?psw={L_Pass}&cmd=REL,1,1")
        time.sleep(0.1)
        print("Включил реле")
    code = 404
    while code == 404:
        code = LJ.check_ip(f"{L_IP24}/cmd.cgi?psw={L_Pass}&cmd=REL,1,0")
        time.sleep(1)
        print("Выключил реле")

def l24_xml():
    l24_xml = LJ.l2_xml_read_all(L_IP24)
    if l24_xml == "N/A":
        l24_xml = ('N', 'NNNN', 'NNNNNN', 'NNNNNNNNNNNN', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N')
    return l24_xml

while True:
    print(type(l24_xml()[3][0]))
    print(l24_xml()[3][0])
    if l24_xml()[3][0] == "0":
        switch_rele()
        time.sleep(600)
    elif l24_xml()[3][0] == "1":
        time.sleep(20)