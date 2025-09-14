# Kyrelix - Gestor de Procesos y Generador de SS

**Kyrelix** es una herramienta avanzada de monitoreo de procesos, generación de informes SS y análisis de aplicaciones recientes en Windows. Desarrollada en **Python** con **Tkinter**, ofrece una interfaz moderna, filtrado dinámico, captura de pantalla y gestión de procesos en tiempo real.

---

## 🏗 Arquitectura General

```
+----------------------------------------------------------+
|                        Kyrelix GUI                        |
|----------------------------------------------------------|
| Panel Izquierdo      | Panel Derecho                      |
|---------------------|------------------------------------|
| [Mostrar todos]     | [Buscar proceso]                  |
| [Abrir ubicación]   | Treeview con lista de procesos    |
| [Cambiar tema]      | Mostrar detalles del proceso      |
| [Generar informe]   |                                    |
| [Apps recientes]    |                                    |
+----------------------------------------------------------+
```

- **Panel Izquierdo:** Botones de acción rápida.
- **Panel Derecho:** Árbol de procesos (`TreeView`) y búsqueda en tiempo real.
- **Ventanas adicionales:**  
  - **Informe SS:** Genera JSON y screenshot.  
  - **Apps recientes:** Lista de aplicaciones abiertas con doble clic para abrir la carpeta.

---

## ⚙ Funcionalidades Detalladas

| Función | Descripción | Widgets Clave | Notas |
|---------|------------|---------------|-------|
| Mostrar todos los procesos | Lista todos los procesos activos en el sistema. | `ttk.Treeview`, `Button` | Filtrado dinámico por nombre, PID, ejecutable o ruta. |
| Abrir ubicación | Abre la carpeta contenedora del ejecutable seleccionado. | `Button`, `subprocess.Popen` | Muestra error si la ruta no existe. |
| Cambiar tema | Alterna entre tema oscuro y claro. | `Button`, `Style` | Actualiza todos los widgets compatibles dinámicamente. |
| Generar informe | Crea un informe JSON con información del PC, jugador y proceso sospechoso. | `Button`, `Toplevel`, `Entry`, `ImageGrab` | Captura de pantalla incluida, guardado en `Informe_SS/`. |
| Apps recientes | Lista apps abiertas recientemente con búsqueda y doble clic para abrir carpeta. | `Toplevel`, `Treeview`, `Entry` | Scroll horizontal y vertical, colores según estado. |
| Filtrado en tiempo real | Filtra los procesos mientras se escribe en el input. | `Entry`, `Treeview` | Optimizado para grandes cantidades de procesos. |

---

## 📌 Flujo de la Aplicación

```
Inicio -> Panel Principal (Kyrelix GUI)
    |
    +--> Mostrar todos los procesos -> TreeView
    |
    +--> Abrir ubicación del archivo -> Explorador de Windows
    |
    +--> Cambiar tema -> Tema oscuro/claro
    |
    +--> Generar informe SS -> Ventana Informe
    |       |
    |       +--> Seleccionar proceso sospechoso -> Ventana Selección
    |       +--> Guardar informe JSON + screenshot
    |
    +--> Apps recientes -> Ventana Apps Recientes
            |
            +--> Filtrado en tiempo real
            +--> Abrir ubicación doble clic
```

---

## 💻 Tecnologías y Librerías

- **Python 3.x** – Lenguaje principal
- **Tkinter / ttk** – GUI y estilos
- **psutil** – Gestión de procesos
- **PIL (Pillow)** – Captura de pantalla
- **subprocess & os** – Manejo de archivos y apertura de carpetas
- **socket** – Obtención del hostname
- **json** – Guardado de informes
- **datetime** – Formateo de fechas

### Instalación de Dependencias
```bash
pip install psutil Pillow
```
(O simplemente puedes usar requirements.txt)

---

## 🛠 Instalación y Ejecución

1. Clonar repositorio:
```bash
git clone https://github.com/iVyz3r/Kyrelix.git
cd Kyrelix
```

2. Crear entorno virtual (opcional, recomendado):
```bash
python -m venv venv
venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar la aplicación:
```bash
python main.py
```

5. Generar ejecutable con PyInstaller:
```bash
pyinstaller --onefile --windowed --icon=kyrelix.ico main.py
```

---

## 🎨 Interfaz de Usuario

- **Tema oscuro predeterminado** con colores:
  - Fondo: `#2b2b2b`
  - Botones: `#1f1f1f`
  - Texto: blanco
- **Tema claro opcional**:
  - Fondo: blanco
  - Texto: negro
- **Árbol de procesos (`TreeView`)**
  - Columnas: Nombre, Ejecutable, PID, Hora, Status, Ubicación
  - Colores de estado: verde (`Signed`), rojo (`Deleted`)
- **Ventana de informe**
  - InputBox de PC (readonly)
  - Nickname del jugador (editable)
  - Selección de proceso sospechoso
  - Generación de JSON y captura de pantalla automática
- **Ventana Apps recientes**
  - Lista con scroll
  - Filtrado en tiempo real
  - Doble clic para abrir ubicación

---

## 📝 Seguridad y Consideraciones

- No requiere privilegios de administrador.
- Solo captura procesos accesibles por el usuario actual.
- Informes JSON y capturas guardadas localmente en `Informe_SS/`.
- Compatible con Windows 10 y 11.

---

## 📦 Estructura de Archivos

```
Kyrelix/
├── main.py            # Script principal
├── kyrelix.ico        # Icono del ejecutable
├── requirements.txt   # Dependencias de Python
├── Informe_SS/        # Carpeta generada con los informes
└── screenshots/       # Screenshots de el ejecutable
```

---

## ✨ Autor

**ilyVyzer_** – [GitHub](https://github.com/iVyz3r)   
Especialista en herramientas de monitoreo y soporte para entornos de videojuegos.

**Discord** - an4rchvyzer (!         ilyVyzer_)

---

## 🔗 Recursos

- [Tkinter Docs](https://docs.python.org/3/library/tk.html)  
- [psutil Docs](https://psutil.readthedocs.io/)  
- [Pillow Docs](https://pillow.readthedocs.io/)

```
[Pantalla principal]
+----------------------------------------+
| Kyrelix - Gestor de Procesos           |
|----------------------------------------|
| [Mostrar todos] [Abrir ubicación] ...  |
| Treeview: Lista de procesos            |
+----------------------------------------+

[Ventana Informe]
+-----------------------------------------------------------------+
| PC: DESKTOP-123 (Esto estará bloqueado)                         |
| Nickname: Jugador1                                              |
| Proceso seleccionado: Minecraft.exe                             |
| [Generar Informe]                                               |
+-----------------------------------------------------------------+

[Ventana Apps Recientes]
+----------------------------------------+
| Buscar: [      ]                        |
| TreeView: Lista de apps recientes       |
+----------------------------------------+
```

---

## 🔧 Mejoras Futuras

- Exportar informe a PDF con gráficos.
- Historial de procesos capturados.
- Sistema de alertas en tiempo real para procesos sospechosos.
- Integración con bases de datos para análisis histórico.
