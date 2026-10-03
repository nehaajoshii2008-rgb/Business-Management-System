Set WshShell = CreateObject("WScript.Shell")
strDesktop = WshShell.SpecialFolders("Desktop")
Set objShortcut = WshShell.CreateShortcut(strDesktop & "\ISBMS Business Management System.lnk")

strAppPath = WshShell.CurrentDirectory & "\Launch_ISBMS.vbs"
strIconPath = WshShell.CurrentDirectory & "\inventory\static\images\bms_icon.ico"

objShortcut.TargetPath = strAppPath
objShortcut.WorkingDirectory = WshShell.CurrentDirectory
objShortcut.Description = "ISBMS - Business Management System Desktop Software"
objShortcut.IconLocation = strIconPath
objShortcut.Save

WScript.Echo "Success! Desktop Shortcut 'ISBMS Business Management System' has been created on your Windows Desktop."
