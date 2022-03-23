import win32process,time
processHandle,threadHandle,processHandleId,threadHandleId = win32process.CreateProcess(r'E:\Program Files (x86)\Notepad++\notepad++.exe', '', None, None, 0, win32process.CREATE_NO_WINDOW,
None, None, win32process.STARTUPINFO())
print(processHandle,threadHandle,processHandleId,threadHandleId)
time.sleep(3)
win32process.TerminateProcess(processHandle,-2)