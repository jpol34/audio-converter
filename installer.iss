[Setup]
AppName=ConvertAudio
AppVersion=1.0
DefaultDirName={pf}\ConvertAudio
DefaultGroupName=ConvertAudio
OutputBaseFilename=ConvertAudioInstaller

[Files]
Source: "dist\ConvertAudio.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\ConvertAudio"; Filename: "{app}\ConvertAudio.exe"
Name: "{commondesktop}\ConvertAudio"; Filename: "{app}\ConvertAudio.exe"; Tasks: desktopicon
