from loguru import logger
import LaurentJSON as LJ
import platform
import requests
import json
import re

# Включение логирования
if platform.system() == "Windows":
    logger.add("log\LaurentJSON.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB", compression="zip")
else:
    logger.add("/home/bots/BotPiP/log/LaurentJSON.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB", compression="zip")


@logger.catch
def check_ip(L_IP):
    try:
        result = requests.get(f"http://{L_IP}", timeout=1).status_code
    except Exception as err:
        result = 404
    return result


@logger.catch
def switch_rele(L_Version, L_IP, L_Pass, L_Rele):
    if L_Version == "L2":
        if LJ.l2_xml_read_all(L_IP)[3][L_Rele - 1] == "0":
            requests.get(f"http://{L_IP}/cmd.cgi?psw={L_Pass}&cmd=REL,{L_Rele},1")
        elif LJ.l2_xml_read_all(L_IP)[3][L_Rele - 1] == "1":
            requests.get(f"http://{L_IP}/cmd.cgi?psw={L_Pass}&cmd=REL,{L_Rele},0")
    elif L_Version == "L5":
        if LJ.l5_json_read_all(L_IP, L_Pass)[8][L_Rele - 1] == "0":
            print(L_Version)
            print(LJ.l5_json_read_all(L_IP, L_Pass)[8][L_Rele - 1])
            print(f"http://{L_IP}/cmd.cgi?psw={L_Pass}&cmd=REL,{L_Rele},1")
            requests.get(f"http://{L_IP}/cmd.cgi?psw={L_Pass}&cmd=REL,{L_Rele},1")
        elif LJ.l5_json_read_all(L_IP, L_Pass)[8][L_Rele - 1] == "1":
            print(L_Version)
            print(LJ.l5_json_read_all(L_IP, L_Pass)[8][L_Rele - 1])
            print(f"http://{L_IP}/cmd.cgi?psw={L_Pass}&cmd=REL,{L_Rele},0")
            requests.get(f"http://{L_IP}/cmd.cgi?psw={L_Pass}&cmd=REL,{L_Rele},0")


@logger.catch
def set_rele(L_IP, L_Pass, L_Rele, L_Set):
    requests.get(f"http://{L_IP}/cmd.cgi?psw={L_Pass}&cmd=REL,{L_Rele},{L_Set}")


@logger.catch
def l5_json_read_all(L_IP, L_Pass):
    CheckIP = check_ip(L_IP)
    if CheckIP == 200:
        laurent = requests.get(f"http://{L_IP}/json_sensor.cgi?psw={L_Pass}")
        l_json = json.loads(laurent.content)
        fw = l_json["fw"]
        sys_time = l_json["sys_time"]
        rtc_y = l_json["rtc_y"]
        rtc_m = l_json["rtc_m"]
        rtc_d = l_json["rtc_d"]
        rtc_dw = l_json["rtc_dw"]
        rtc_h = l_json["rtc_h"]
        rtc_min = l_json["rtc_min"]
        rele = l_json["rele"]
        in_ = l_json["in"]
        io_in = l_json["io_in"]
        io_out = l_json["io_out"]
        io_dir = l_json["io_dir"]
        out = l_json["out"]
        adc = l_json["adc"]
        onew_temp = l_json["onew_temp"]
        pwm = l_json["pwm"]
        dth11_con = l_json["dth11_con"]
        dth11_vld = l_json["dth11_vld"]
        dth11_hum = l_json["dth11_hum"]
        dth11_tmp = l_json["dth11_tmp"]
        impl_in = l_json["impl_in"]
        impl_io = l_json["impl_io"]
        return (fw,
                sys_time,
                rtc_y,
                rtc_m,
                rtc_d,
                rtc_dw,
                rtc_h,
                rtc_min,
                rele,
                in_,
                io_in,
                io_out,
                io_dir,
                out, adc,
                onew_temp,
                pwm,
                dth11_con,
                dth11_vld,
                dth11_hum,
                dth11_tmp,
                impl_in,
                impl_io)
    else:
        result = "N/A"
        return result

# l5_json_read_all("172.16.1.22", "Laurent")


@logger.catch
def l2_xml_read_all(L_IP):
    CheckIP = check_ip(L_IP)
    if CheckIP == 200:
        raw_html = requests.get(f"http://{L_IP}/state.xml")
        content_html = raw_html.content
        decode_html = content_html.decode('utf-8').replace(u'\u2212', '-')
        match_systime = re.findall("<systime>(.*?)</systime>", str(decode_html))
        systime = match_systime[0]
        match_rele = re.findall("<rele>(.*?)</rele>", str(decode_html))
        rele = match_rele[0]
        match_in = re.findall("<in>(.*?)</in>", str(decode_html))
        in_ = match_in[0]
        match_in = re.findall("<out>(.*?)</out>", str(decode_html))
        out = match_in[0]
        match_adc1 = re.findall("<adc1>(.*?)</adc1>", str(decode_html))
        adc1 = match_adc1[0]
        match_adc2 = re.findall("<adc2>(.*?)</adc2>", str(decode_html))
        adc2 = match_adc2[0]
        match_temp = re.findall("<temp>(.*?)</temp>", str(decode_html))
        temp = match_temp[0]
        match_count1 = re.findall("<count1>(.*?)</count1>", str(decode_html))
        count1 = match_count1[0]
        match_count2 = re.findall("<count2>(.*?)</count2>", str(decode_html))
        count2 = match_count2[0]
        match_count3 = re.findall("<count3>(.*?)</count3>", str(decode_html))
        count3 = match_count3[0]
        match_count4 = re.findall("<count4>(.*?)</count4>", str(decode_html))
        count4 = match_count4[0]
        match_pwm = re.findall("<pwm>(.*?)</pwm>", str(decode_html))
        pwm = match_pwm[0]
        return systime, rele, in_, out, adc1, adc2, temp, count1, count2, count3, count4, pwm
    else:
        result = "N/A"
        return result
