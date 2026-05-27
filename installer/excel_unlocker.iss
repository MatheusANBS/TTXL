[Setup]
AppName=Excel Sheet Unlocker
AppVersion=1.0.0
AppPublisher=Matheuss
DefaultDirName={localappdata}\ExcelSheetUnlocker
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\excel_unlocker_gui.exe
Compression=lzma
SolidCompression=yes
OutputDir=..\installer_output
OutputBaseFilename=ExcelSheetUnlocker_Setup
SetupIconFile=..\assets\icon.ico

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Files]
Source: "..\dist\excel_unlocker_gui.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Excel Sheet Unlocker"; Filename: "{app}\excel_unlocker_gui.exe"; IconFilename: "{app}\excel_unlocker_gui.exe"
Name: "{commondesktop}\Excel Sheet Unlocker"; Filename: "{app}\excel_unlocker_gui.exe"; IconFilename: "{app}\excel_unlocker_gui.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\excel_unlocker_gui.exe"; Description: "Launch Excel Sheet Unlocker"; Flags: nowait postinstall
