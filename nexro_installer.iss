; ═══════════════════════════════════════════════════════════════════════════════
;   NEXRO PLANT AI — Script de instalador profesional
;   Inno Setup 6.x
;   Nexro Systems © 2026
; ═══════════════════════════════════════════════════════════════════════════════

#define AppName      "Nexro Plant AI"
#define AppVersion   "3.0 Pro"
#define AppPublisher "Nexro Systems"
#define AppURL       "https://nexrosystems-alt.github.io/nexro-systems"
#define AppExeName   "Nexro Plant AI.exe"
#define AppContact   "nexrosystems@gmail.com"

[Setup]
; ── Identificación única de la app (NO cambiar después del primer release) ──
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}

; ── Info de la app ──────────────────────────────────────────────────────────
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppContact={#AppContact}
AppCopyright=Copyright © 2026 {#AppPublisher}

; ── Instalación ─────────────────────────────────────────────────────────────
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
AllowNoIcons=yes
OutputDir=D:\NEXRO_APP\instalador
OutputBaseFilename=Nexro Plant AI Setup v3.0
SetupIconFile=D:\NEXRO_APP\nexro.ico
UninstallDisplayIcon={app}\{#AppExeName}
UninstallDisplayName={#AppName}

; ── Compresión (LZMA2 = máxima compresión, tarda más pero pesa menos) ───────
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes

; ── Requerimientos del sistema ───────────────────────────────────────────────
MinVersion=10.0
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; ── Apariencia del instalador ────────────────────────────────────────────────
WizardStyle=modern
WizardSizePercent=120
DisableWelcomePage=no
DisableDirPage=no
DisableProgramGroupPage=yes

; ── Privilegios (admin para instalar en Program Files) ──────────────────────
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; ── Reinicio ─────────────────────────────────────────────────────────────────
RestartIfNeededByRun=no
DisableFinishedPage=no

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[CustomMessages]
spanish.WelcomeLabel1=Bienvenido al instalador de {#AppName}
spanish.WelcomeLabel2=Este asistente te guiará para instalar {#AppName} {#AppVersion} en tu equipo.%n%nSistema de diagnóstico inteligente de enfermedades en cultivos con IA.%n%n88 enfermedades · 20 cultivos · 93.7% precisión%n%nSe recomienda cerrar todas las aplicaciones antes de continuar.

[Tasks]
Name: "desktopicon";    Description: "Crear icono en el {cm:DesktopFolder}"; GroupDescription: "Iconos adicionales:"; Flags: checked
Name: "startmenuicon";  Description: "Crear acceso directo en menú Inicio";   GroupDescription: "Iconos adicionales:"; Flags: checked
Name: "launchafterinstall"; Description: "Abrir {#AppName} al terminar la instalación"; GroupDescription: "Al finalizar:"; Flags: checked

[Files]
; ── Archivo principal ────────────────────────────────────────────────────────
Source: "D:\NEXRO_APP\dist\Nexro Plant AI.exe"; DestDir: "{app}"; Flags: ignoreversion

; ── Icono ────────────────────────────────────────────────────────────────────
Source: "D:\NEXRO_APP\nexro.ico"; DestDir: "{app}"; Flags: ignoreversion

; ── README ───────────────────────────────────────────────────────────────────
Source: "D:\NEXRO_APP\README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme; DestName: "Leeme.txt"

[Icons]
; ── Acceso directo en escritorio ─────────────────────────────────────────────
Name: "{autodesktop}\{#AppName}";        Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\nexro.ico"; Tasks: desktopicon; Comment: "Diagnóstico inteligente de cultivos con IA"

; ── Acceso directo en menú Inicio ────────────────────────────────────────────
Name: "{autoprograms}\{#AppName}\{#AppName}";          Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\nexro.ico"; Comment: "Diagnóstico inteligente de cultivos con IA"
Name: "{autoprograms}\{#AppName}\Desinstalar {#AppName}"; Filename: "{uninstallexe}"; IconFilename: "{app}\nexro.ico"

[Run]
; ── Abrir la app al terminar (opcional, según checkbox) ──────────────────────
Filename: "{app}\{#AppExeName}"; Description: "Abrir {#AppName}"; Flags: nowait postinstall skipifsilent; Tasks: launchafterinstall

[UninstallRun]
; ── Al desinstalar, matar el proceso si está abierto ─────────────────────────
Filename: "taskkill"; Parameters: "/F /IM ""{#AppExeName}"""; Flags: runhidden; RunOnceId: "KillApp"

[UninstallDelete]
; ── Limpiar archivos que crea la app (historial, cache) ──────────────────────
Type: filesandordirs; Name: "{app}\.cache"
Type: files;          Name: "{app}\historial.json"

[Code]
// ── Verificar si la app está corriendo antes de instalar ────────────────────
function IsAppRunning(const FileName: string): Boolean;
var
  FSWbemLocator: Variant;
  FWMIService: Variant;
  FWbemObjectSet: Variant;
begin
  Result := False;
  try
    FSWbemLocator := CreateOleObject('WbemScripting.SWbemLocator');
    FWMIService := FSWbemLocator.ConnectServer('', 'root\CIMV2', '', '');
    FWbemObjectSet := FWMIService.ExecQuery(
      Format('SELECT * FROM Win32_Process WHERE Name="%s"', [FileName])
    );
    Result := (FWbemObjectSet.Count > 0);
  except
    Result := False;
  end;
end;

function InitializeSetup(): Boolean;
begin
  Result := True;
  if IsAppRunning('Nexro Plant AI.exe') then
  begin
    MsgBox(
      'Nexro Plant AI está abierto en este momento.' + #13#10 +
      'Por favor ciérralo antes de instalar.',
      mbError, MB_OK
    );
    Result := False;
  end;
end;

// ── Página de bienvenida personalizada ──────────────────────────────────────
procedure InitializeWizard();
begin
  WizardForm.WelcomeLabel2.Caption :=
    'Este asistente instalará Nexro Plant AI 3.0 Pro en tu equipo.' + #13#10 + #13#10 +
    'Sistema de diagnóstico inteligente de enfermedades en cultivos' + #13#10 +
    'mediante Inteligencia Artificial (YOLOv8).' + #13#10 + #13#10 +
    '  ✓  88 enfermedades detectables' + #13#10 +
    '  ✓  20 cultivos soportados' + #13#10 +
    '  ✓  93.7% de precisión' + #13#10 +
    '  ✓  Funciona 100% sin internet' + #13#10 + #13#10 +
    'Nexro Systems © 2026  |  nexrosystems@gmail.com';
end;
