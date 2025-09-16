# Kyrelix 1.0.1 – Gestor de Procesos y Generador de SS

**Kyrelix** es una herramienta avanzada para **monitorear procesos**, **generar informes completos** y **analizar aplicaciones recientes** en Windows.  
Desarrollada en **Python** con **Tkinter**, ofrece una interfaz moderna, filtrado dinámico, captura de pantalla, creación de PDF con gráficos y gestión de procesos en tiempo real.

---

## 🆕 Novedades de la versión 1.0.1
- **Informe en PDF**: ahora se genera un archivo PDF con:
  - Gráfico de barras de los procesos activos en el momento de la captura.
  - Screenshot automático de la pantalla.
- **Ajustes de interfaz**:
  - Mejor contraste en campos de entrada en modo oscuro.
  - Colores de estado renombrados a **Disponible** (verde) y **Eliminado** (rojo) para mayor claridad.
- **Pequeñas optimizaciones** en la búsqueda en tiempo real y en la apertura de carpetas con rutas que contienen espacios.

---

## 🏗 Arquitectura General

```
+----------------------------------------------------------+
|                        Kyrelix GUI                       |
|----------------------------------------------------------|
| Panel Izquierdo      | Panel Derecho                     |
|--------------------- |-----------------------------------|
| [Mostrar todos]      | [Buscar proceso]                  |
| [Abrir ubicación]    | Treeview con lista de procesos    |
| [Cambiar tema]       | Mostrar detalles del proceso      |
| [Generar informe]    |                                   |
| [Apps recientes]     |                                   |
+----------------------------------------------------------+
```

- **Panel Izquierdo:** Botones de acción rápida.
- **Panel Derecho:** Árbol de procesos (`TreeView`) y búsqueda en tiempo real.
- **Ventanas adicionales:**  
  - **Informe SS:** Genera JSON, screenshot y PDF con gráfico.  
  - **Apps recientes:** Lista de aplicaciones abiertas con doble clic para abrir la carpeta.

---

## ⚙ Funcionalidades Detalladas

| Función | Descripción | Widgets Clave | Notas |
|---------|------------|---------------|-------|
| Mostrar todos los procesos | Lista todos los procesos activos en el sistema. | `ttk.Treeview`, `Button` | Filtrado dinámico por nombre, PID, ejecutable o ruta. |
| Abrir ubicación | Abre la carpeta contenedora del ejecutable seleccionado. | `Button`, `subprocess.Popen` | Maneja rutas con espacios y muestra error si no existe. |
| Cambiar tema | Alterna entre tema oscuro y claro. | `Button`, `Style` | Actualiza todos los widgets compatibles dinámicamente. |
| Generar informe | Crea un informe JSON + screenshot + PDF con gráfico de procesos. | `Button`, `Toplevel`, `Entry`, `ImageGrab`, `matplotlib`, `reportlab` | Archivos guardados en `Informe_SS/`. |
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
    |       +--> Guardar informe JSON + screenshot + PDF
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
- **Pillow (ImageGrab)** – Captura de pantalla
- **matplotlib** – Gráficos de procesos en el PDF
- **reportlab** – Generación de PDF
- **subprocess & os** – Manejo de archivos y apertura de carpetas
- **socket** – Obtención del hostname
- **json** – Guardado de informes
- **datetime** – Formateo de fechas

### Instalación de Dependencias
```bash
pip install psutil Pillow matplotlib reportlab
```
(O usa `requirements.txt`)

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
  - Columnas: Nombre, Ejecutable, PID, Hora, Estado, Ubicación
  - Colores de estado: verde (`Disponible`), rojo (`Eliminado`)
- **Ventana de informe**
  - Campo de PC (readonly)
  - Nickname del jugador (editable)
  - Selección de proceso sospechoso
  - Generación de JSON, captura de pantalla y PDF
- **Ventana Apps recientes**
  - Lista con scroll
  - Filtrado en tiempo real
  - Doble clic para abrir ubicación

---

## 📝 Seguridad y Consideraciones

- No requiere privilegios de administrador.
- Solo captura procesos accesibles por el usuario actual.
- Informes guardados localmente en `Informe_SS/`.
- Compatible con Windows 10 y 11.

---

## 📦 Estructura de Archivos

```
Kyrelix/
├── main.py            # Script principal
├── kyrelix.ico        # Icono del ejecutable
├── requirements.txt   # Dependencias de Python
├── Informe_SS/        # Carpeta generada con los informes
└── screenshots/       # Screenshots del ejecutable
```

---

## ✨ Autor

**ilyVyzer_** – [GitHub](https://github.com/iVyz3r)  
Especialista en herramientas de monitoreo y soporte para entornos de videojuegos.

**Discord** – an4rchvyzer (!         ilyVyzer_)

---

## 🔗 Recursos

- [Tkinter Docs](https://docs.python.org/3/library/tk.html)
- [psutil Docs](https://psutil.readthedocs.io/)
- [Pillow Docs](https://pillow.readthedocs.io/)
- [matplotlib Docs](https://matplotlib.org/stable/contents.html)
- [ReportLab Docs](https://www.reportlab.com/documentation/)
