# 🌿 Nexro Plant AI — v3.0 Pro

**Sistema comercial de diagnóstico fitosanitario con IA**

---

## 📦 Archivos que necesitas en `D:\NEXRO_APP\`

```
D:\NEXRO_APP\
├── app.py              ← Archivo principal (ejecuta este)
├── nexro_data.py       ← Base de datos (88 enfermedades, 20 cultivos)
├── nexro_utils.py      ← Excel, PDF, historial, validaciones
  └── best.pt             ← Archivo descarga drive: https://drive.google.com/file/d/1RN4aJteiDmR7s0rTcQ8WlkCCnIcC6y4D/view?usp=drive_link
```

---

## ⚡ Instalación rápida (solo 1 vez)

Abre Anaconda Prompt, activa tu entorno y ejecuta:

```bash
conda activate nexro_app
pip install openpyxl reportlab
```

> Ya tienes `pyqt6`, `ultralytics`, `pillow`, `opencv-python-headless`.
> Solo faltan `openpyxl` (para Excel) y `reportlab` (para PDF).

---

## ▶️ Cómo ejecutar

```bash
cd D:\NEXRO_APP
python app.py
```

---

## 🚀 Qué hace la app

### 🏠 Pantalla Inicio
- Hero profesional con "IA" resaltado correctamente en la misma línea
- 5 stats chips (88 enfermedades · 20 cultivos · 93.7% · <2s · 79K+)
- Botones **Analizar imagen** y **Ver catálogo**
- Guía visual de cómo tomar la foto (✅/❌)

### 🔬 Pantalla Análisis
- **Drag & Drop** — arrastra la imagen directo
- **Validación automática** de tamaño (mínimo 100px, warning si <224 o >4000)
- **Barra animada** de confianza (800ms suave)
- Alerta de gravedad con color dinámico
- 3 cards: Descripción / Tratamiento / Prevención
- Top 5 otras posibilidades con mini-cards
- **3 botones de exportación**:
  - 💾 Guardar imagen (jpg/png)
  - 📊 Excel profesional (con imagen embebida)
  - 📄 PDF profesional

### 📚 Pantalla Catálogo
- **Buscador en vivo** por enfermedad, cultivo o síntoma
- **Filtro por gravedad** (Sana / Media / Alta / Muy alta)
- Cards clickables de los 20 cultivos
- Modal de detalle con info completa por enfermedad
- **Descarga Excel completo** (2 hojas: por cultivo y todas las enfermedades)

### 🗂 Pantalla Historial
- Últimos 15 análisis guardados automáticamente
- Thumbnail + nombre + fecha + confianza + gravedad
- Persiste entre sesiones (archivo `historial.json`)
- Botón para limpiar

---

## ⌨️ Atajos de teclado

| Atajo | Acción |
|---|---|
| `Ctrl+O` | Cargar imagen |
| `Ctrl+S` | Guardar imagen analizada |
| `Ctrl+E` | Exportar a Excel |
| `Ctrl+P` | Exportar a PDF |
| `Ctrl+Q` | Salir |
| `Ctrl+1/2/3/4` | Cambiar entre pantallas |
| `F1` | Acerca de |

---

## 📊 Excel generado — lo que contiene

1. **Header corporativo** con logo y fecha
2. **Resumen ejecutivo** (enfermedad, cultivo, confianza, gravedad)
3. **Diagnóstico detallado** (descripción / tratamiento / prevención)
4. **Top 5 otras posibilidades** con porcentajes
5. **Imagen embebida** del análisis
6. **Footer con contacto** de Nexro Systems

El formato es profesional, con colores por gravedad, listo para enviar a clientes.

---

## 💡 Características Pro

- ✨ Splash screen al arrancar
- ✨ Validación de imagen antes de analizar
- ✨ Historial persistente en JSON
- ✨ Menú contextual (⋮) con todas las opciones
- ✨ Barra de progreso animada
- ✨ Sombras suaves en botones principales
- ✨ About dialog con specs del modelo
- ✨ Status bar dinámico que muestra el resultado
- ✨ Responsive (se adapta al tamaño de ventana)
- ✨ Tema dark consistente en toda la app

---

## 📦 Próximo paso: Empaquetar a .exe

Cuando estés satisfecho con la app, puedes generar el ejecutable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Nexro Plant AI" ^
    --add-data "best.pt;." ^
    --add-data "nexro_data.py;." ^
    --add-data "nexro_utils.py;." ^
    --icon=nexro.ico ^
    app.py
```

Esto te genera un `Nexro Plant AI.exe` de ~300MB que puedes distribuir o vender.

---

**Nexro Systems © 2026**
📧 nexrosystems@gmail.com · 📱 +57 321 521 7396
