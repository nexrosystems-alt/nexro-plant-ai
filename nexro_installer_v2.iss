; ═══════════════════════════════════════════════════════════════════════════════
;   NEXRO PLANT AI — Instalador profesional
;   Inno Setup 6.7.x
;   Nexro Systems © 2026
; ═══════════════════════════════════════════════════════════════════════════════

#define AppName      "Nexro Plant AI"
#define AppVersion   "3.0 Pro"
#define AppPublisher "Nexro Systems"
#define AppURL       "https://nexrosystems-alt.github.io/nexro-systems"
#define AppExeName   "Nexro Plant AI.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppCopyright=Copyright 2026 {#AppPublisher}

DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
AllowNoIcons=yes

OutputDir=D:\NEXRO_APP\instalador
OutputBaseFilename=Nexro Plant AI Setup v3.0
SetupIconFile=D:\NEXRO_APP\nexro.ico
UninstallDisplayIcon={app}\{#AppExeName}
UninstallDisplayName={#AppName}

Compression=lzma2/ultra64
SolidCompression=yes

MinVersion=10.0
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

WizardStyle=modern
WizardSizePercent=120
DisableWelcomePage=no
DisableDirPage=no
DisableProgramGroupPage=yes
PrivilegesRequired=admin
DisableFinishedPage=no

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon";        Description: "Crear icono en el Escritorio";      GroupDescription: "Iconos adicionales:"
Name: "startmenuicon";      Description: "Crear acceso en el menu Inicio";    GroupDescription: "Iconos adicionales:"
Name: "launchafterinstall"; Description: "Abrir Nexro Plant AI al terminar";  GroupDescription: "Al finalizar:"

[Files]
Source: "D:\NEXRO_APP\dist\Nexro Plant AI.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\NEXRO_APP\nexro.ico";               DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autodesktop}\{#AppName}";                              Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\nexro.ico"; Tasks: desktopicon
Name: "{autoprograms}\{#AppName}\{#AppName}";                  Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\nexro.ico"
Name: "{autoprograms}\{#AppName}\Desinstalar {#AppName}";      Filename: "{uninstallexe}"

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Abrir {#AppName}"; Flags: nowait postinstall skipifsilent; Tasks: launchafterinstall

[UninstallRun]
Filename: "taskkill"; Parameters: "/F /IM ""{#AppExeName}"""; Flags: runhidden; RunOnceId: "KillApp"

[UninstallDelete]
Type: filesandordirs; Name: "{app}\.cache"
Type: files;          Name: "{app}\historial.json"

[Code]
procedure InitializeWizard();
begin
  WizardForm.WelcomeLabel2.Caption :=
    'Este asistente instalara Nexro Plant AI 3.0 Pro en tu equipo.' + #13#10 + #13#10 +
    'Sistema de diagnostico inteligente de enfermedades en cultivos' + #13#10 +
    'mediante Inteligencia Artificial (YOLOv8).' + #13#10 + #13#10 +
    '  88 enfermedades detectables' + #13#10 +
    '  20 cultivos soportados' + #13#10 +
    '  93.7% de precision' + #13#10 +
    '  Funciona 100% sin internet' + #13#10 + #13#10 +
    'Nexro Systems 2026  |  nexrosystems@gmail.com';
end;
