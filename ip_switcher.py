import win32com.shell.shell as shell
from time import sleep

location_ids = [19,9,18,165,172,6,70,74,71,54,202,26,155,168,75,94,204,1,207,2,166,25]


base_command = 'cd C:\Program Files (x86)\ExpressVPN\services\ & ExpressVPN.CLI disconnect & ExpressVPN.CLI connect '
def switch_ip_address(loop_num : int):
    try:
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+ base_command + str(location_ids[loop_num%len(location_ids)]))
        sleep(8)
        return True
    except Exception as err:
        raise Exception(err)