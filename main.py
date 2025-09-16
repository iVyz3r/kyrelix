import os
import psutil
import subprocess
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import json
import socket
from PIL import ImageGrab
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet

# --- Funciones ---
def gather_processes():
    procs = []
    for p in psutil.process_iter(['pid','name','exe','create_time']):
        try:
            info = p.info
            pid = info.get('pid')
            name = str(info.get('name') or '')
            exe_path = str(info.get('exe') or '')
            exe_file = os.path.basename(exe_path)
            create_time = datetime.fromtimestamp(info.get('create_time')).strftime('%Y-%m-%d %H:%M:%S') if info.get('create_time') else 'N/A'
            status = "Signed" if os.path.exists(exe_path) else "Deleted"
            procs.append({
                'name': name,
                'exe': exe_file,
                'pid': str(pid),
                'time': create_time,
                'status': status,
                'path': exe_path
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return procs

def show_processes(tree, filter_text=""):
    filter_text = filter_text.lower()
    for row in tree.get_children():
        tree.delete(row)
    
    for p in gather_processes():
        if filter_text:
            if not (filter_text in p['name'].lower() or
                    filter_text in p['exe'].lower() or
                    filter_text in p['pid'] or
                    filter_text in p['path'].lower()):
                continue
        item_id = tree.insert("", tk.END, values=(p['name'], p['exe'], p['pid'], p['time'], p['status'], p['path']))
        if p['status'] == "Signed":
            tree.tag_configure(f"signed_{item_id}", foreground="#55ff55")
            tree.item(item_id, tags=(f"signed_{item_id}",))
        else:
            tree.tag_configure(f"deleted_{item_id}", foreground="#ff5555")
            tree.item(item_id, tags=(f"deleted_{item_id}",))

def open_location(path):
    folder = os.path.dirname(path)
    if os.path.exists(folder):
        subprocess.Popen(f'explorer "{folder}"')
    else:
        messagebox.showerror("Error", "La ubicación no existe")

def open_selected_location(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Aviso", "Selecciona un proceso primero")
        return
    path = tree.item(selected[0])['values'][5]
    open_location(path)

def toggle_theme(root, widgets, dark_mode_flag):
    dark_mode_flag[0] = not dark_mode_flag[0]
    dark = dark_mode_flag[0]
    if dark:
        style.configure("Treeview", background="#2b2b2b", foreground="#ffffff", fieldbackground="#2b2b2b")
        style.configure("Treeview.Heading", background="#1f1f1f", foreground="#ffffff")
        root.configure(bg="#2b2b2b")
        for w in widgets:
            if isinstance(w, (tk.Button, tk.Entry, tk.Label)):
                w.configure(bg="#1f1f1f", fg="#ffffff", insertbackground="#ffffff")
    else:
        style.configure("Treeview", background="#ffffff", foreground="#000000", fieldbackground="#ffffff")
        style.configure("Treeview.Heading", background="#f0f0f0", foreground="#000000")
        root.configure(bg="#f0f0f0")
        for w in widgets:
            if isinstance(w, (tk.Button, tk.Entry, tk.Label)):
                w.configure(bg="#f0f0f0", fg="#000000", insertbackground="#000000")

def search_callback(tree, entry):
    show_processes(tree, entry.get())

def generate_report(tree):
    report_win = tk.Toplevel(root)
    report_win.title("Kyrelix - Generar Informe")
    report_win.geometry("500x350")
    report_win.configure(bg="#2b2b2b")

    tk.Label(report_win, text="Generar Informe", bg="#2b2b2b", fg="#ffffff", font=("Arial", 12, "bold")).pack(pady=5)
    
    tk.Label(report_win, text="Nombre de la PC:", bg="#2b2b2b", fg="#ffffff").pack()
    tk.Label(report_win, text="Bloqueado", fg="#ff5555", bg="#2b2b2b", font=("Arial", 8)).pack()
    pc_name_entry = tk.Entry(report_win, bg="#1f1f1f", fg="#000000")
    pc_name_entry.pack(fill=tk.X, padx=10)
    pc_name_entry.insert(0, socket.gethostname())
    pc_name_entry.config(state="readonly")

    tk.Label(report_win, text="Nickname del jugador:", bg="#2b2b2b", fg="#ffffff").pack() 
    nickname_entry = tk.Entry(report_win, bg="#1f1f1f", fg="#ffffff")
    nickname_entry.pack(fill=tk.X, padx=10)

    selected_process = {"values": None}
    selected_label = tk.Label(report_win, text="No seleccionado", bg="#2b2b2b", fg="#ffffff")
    selected_label.pack(pady=5)

    def select_process():
        sel_win = tk.Toplevel(report_win)
        sel_win.title("Seleccionar proceso")
        sel_win.geometry("600x400")
        sel_win.configure(bg="#2b2b2b")

        columns = ("Nombre", "Ejecutable", "PID", "Hora", "Status", "Ruta")
        tree_sel = ttk.Treeview(sel_win, columns=columns, show="headings")
        scroll_y = ttk.Scrollbar(sel_win, orient="vertical", command=tree_sel.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x = ttk.Scrollbar(sel_win, orient="horizontal", command=tree_sel.xview)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        tree_sel.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        tree_sel.pack(fill=tk.BOTH, expand=True)
        for col in columns:
            tree_sel.heading(col, text=col)
            tree_sel.column(col, width=120, anchor=tk.W)

        for p in gather_processes():
            item_id = tree_sel.insert("", tk.END, values=(p['name'], p['exe'], p['pid'], p['time'], p['status'], p['path']))
            if p['status'] == "Signed":
                tree_sel.tag_configure(f"signed_{item_id}", foreground="green")
                tree_sel.item(item_id, tags=(f"signed_{item_id}",))
            else:
                tree_sel.tag_configure(f"deleted_{item_id}", foreground="red")
                tree_sel.item(item_id, tags=(f"deleted_{item_id}",))

        def select_and_close():
            sel = tree_sel.selection()
            if not sel:
                messagebox.showwarning("Aviso", "Selecciona un proceso")
                return
            selected_process["values"] = tree_sel.item(sel[0])['values']
            selected_label.config(text=f"{selected_process['values'][0]} | PID: {selected_process['values'][2]}")
            sel_win.destroy()

        tk.Button(sel_win, text="Seleccionar", command=select_and_close, bg="#1f1f1f", fg="#ffffff").pack(pady=5)

    def save_report():
        nickname = nickname_entry.get()
        if not nickname:
            messagebox.showwarning("Aviso", "Ingresa el nickname del jugador")
            return
        if not selected_process["values"]:
            messagebox.showwarning("Aviso", "Selecciona un proceso")
            return

        folder = "Informe_SS"
        os.makedirs(folder, exist_ok=True)
                    
        report_data = {
            "PC": pc_name_entry.get(),
            "Nickname": nickname,
            "Proceso": selected_process["values"]
        }
        json_path = os.path.join(folder, "log.json")
        with open(json_path, "w") as f:
            json.dump(report_data, f, indent=4)
        screenshot_path = os.path.join(folder, "screenshot.png")
        ImageGrab.grab().save(screenshot_path)

        procs = gather_processes()
        nombres = [p['name'] for p in procs]
        conteos = [1]*len(procs) 

        plt.figure(figsize=(8,5))
        plt.bar(nombres, conteos, color="#55aaff")
        plt.xticks(rotation=45, ha="right")
        plt.title("Procesos capturados actualmente")
        plt.tight_layout()
        graph_path = os.path.join(folder, "grafico.png")
        plt.savefig(graph_path)
        plt.close()

        pdf_path = os.path.join(folder, "informe.pdf")
        doc = SimpleDocTemplate(pdf_path)
        styles = getSampleStyleSheet()
        content = []
        content.append(Paragraph("<b>Informe SS</b>", styles['Title']))
        content.append(Paragraph(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        content.append(Spacer(1,20))
        content.append(Paragraph(f"PC: {pc_name_entry.get()}", styles['Normal']))
        content.append(Paragraph(f"Nickname: {nickname}", styles['Normal']))
        content.append(Paragraph(f"Proceso seleccionado: {selected_process['values'][0]} (PID {selected_process['values'][2]})", styles['Normal']))
        content.append(Spacer(1,20))
        content.append(RLImage(graph_path, width=400, height=250))
        content.append(Spacer(1,20))
        content.append(RLImage(screenshot_path, width=400, height=250))
        doc.build(content)

        messagebox.showinfo("Éxito", f"Informe generado en '{folder}'")

    tk.Button(report_win, text="Seleccionar proceso", command=select_process, bg="#1f1f1f", fg="#ffffff").pack(pady=5)
    tk.Button(report_win, text="Generar Informe", command=save_report, bg="#1f1f1f", fg="#ffffff").pack(pady=5)

def open_recent_apps():
    recent_win = tk.Toplevel(root)
    recent_win.title("Kyrelix - Apps abiertas recientemente")
    recent_win.geometry("900x500")
    recent_win.configure(bg="#2b2b2b")

    tk.Label(recent_win, text="Apps abiertas recientemente", bg="#2b2b2b", fg="#ffffff", font=("Arial", 12, "bold")).pack(pady=5)

    search_frame = tk.Frame(recent_win, bg="#2b2b2b")
    search_frame.pack(fill=tk.X, pady=5)
    tk.Label(search_frame, text="Buscar:", bg="#2b2b2b", fg="#ffffff").pack(side=tk.LEFT, padx=5)
    search_entry = tk.Entry(search_frame, bg="#1f1f1f", fg="#ffffff", insertbackground="#ffffff")
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    columns = ("Hora", "Ejecutable", "Ubicación", "Abrir", "Status")
    tree_recent = ttk.Treeview(recent_win, columns=columns, show="headings")
    scroll_y = ttk.Scrollbar(recent_win, orient="vertical", command=tree_recent.yview)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    scroll_x = ttk.Scrollbar(recent_win, orient="horizontal", command=tree_recent.xview)
    scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
    tree_recent.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    tree_recent.pack(fill=tk.BOTH, expand=True)

    for col in columns:
        tree_recent.heading(col, text=col)
        tree_recent.column(col, width=150, anchor=tk.W)
        
    for p in gather_processes():
        item_id = tree_recent.insert("", tk.END, values=(p['time'], p['exe'], p['path'], "Abrir", p['status']))
        if p['status'] == "Signed":
            tree_recent.tag_configure(f"signed_{item_id}", foreground="green")
            tree_recent.item(item_id, tags=(f"signed_{item_id}",))
        else:
            tree_recent.tag_configure(f"deleted_{item_id}", foreground="red")
            tree_recent.item(item_id, tags=(f"deleted_{item_id}",))

    def open_path(event):
        sel = tree_recent.selection()
        if sel:
            col = tree_recent.identify_column(event.x)
            if col == "#4": 
                path = tree_recent.item(sel[0])['values'][2]
                open_location(path)

    tree_recent.bind("<Double-1>", open_path)

    def search_recent(event=None):
        filter_text = search_entry.get().lower()
        for row in tree_recent.get_children():
            tree_recent.delete(row)
        for p in gather_processes():
            if filter_text in p['name'].lower() or filter_text in p['exe'].lower():
                item_id = tree_recent.insert("", tk.END, values=(p['time'], p['exe'], p['path'], "Abrir", p['status']))
                if p['status'] == "Signed":
                    tree_recent.tag_configure(f"signed_{item_id}", foreground="green")
                    tree_recent.item(item_id, tags=(f"signed_{item_id}",))
                else:
                    tree_recent.tag_configure(f"deleted_{item_id}", foreground="red")
                    tree_recent.item(item_id, tags=(f"deleted_{item_id}",))

    search_entry.bind("<KeyRelease>", search_recent)


dark_mode_flag = [True]
root = tk.Tk()
root.title("Kyrelix - Gestor de Procesos")
root.geometry("1250x600")

style = ttk.Style()
style.theme_use("default")

main_frame = tk.Frame(root, bg="#2b2b2b")
main_frame.pack(fill=tk.BOTH, expand=True)

btn_frame = tk.Frame(main_frame, bg="#2b2b2b")
btn_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

btn_show = tk.Button(btn_frame, text="Mostrar todos los procesos", command=lambda: show_processes(tree, ""), bg="#1f1f1f", fg="#ffffff")
btn_show.pack(pady=5, fill=tk.X)
btn_open = tk.Button(btn_frame, text="Abrir ubicación del archivo", command=lambda: open_selected_location(tree), bg="#1f1f1f", fg="#ffffff")
btn_open.pack(pady=5, fill=tk.X)
btn_toggle = tk.Button(btn_frame, text="Cambiar tema", command=lambda: toggle_theme(root, [btn_show, btn_open, btn_toggle, btn_report, btn_recent, entry_search, label_text, label_github], dark_mode_flag), bg="#1f1f1f", fg="#ffffff")
btn_toggle.pack(pady=5, fill=tk.X)
btn_report = tk.Button(btn_frame, text="Generar informe", command=lambda: generate_report(tree), bg="#1f1f1f", fg="#ffffff")
btn_report.pack(pady=5, fill=tk.X)
btn_recent = tk.Button(btn_frame, text="Apps abiertas recientemente", command=open_recent_apps, bg="#1f1f1f", fg="#ffffff")
btn_recent.pack(pady=5, fill=tk.X)

right_frame = tk.Frame(main_frame, bg="#2b2b2b")
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

label_text = tk.Label(right_frame, text="Hecho por ilyVyzer_", bg="#2b2b2b", fg="#ffffff", font=("Arial", 12, "bold"))
label_text.pack(pady=(0,2))
label_github = tk.Label(right_frame, text="GitHub: https://github.com/iVyz3r", bg="#2b2b2b", fg="#ffffff", font=("Arial", 10))
label_github.pack(pady=(0,5))

search_frame = tk.Frame(right_frame, bg="#2b2b2b")
search_frame.pack(fill=tk.X, pady=5)
tk.Label(search_frame, text="Buscar:", bg="#2b2b2b", fg="#ffffff").pack(side=tk.LEFT, padx=5)
entry_search = tk.Entry(search_frame, bg="#1f1f1f", fg="#ffffff", insertbackground="#ffffff")
entry_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
btn_search = tk.Button(search_frame, text="Buscar", command=lambda: search_callback(tree, entry_search), bg="#1f1f1f", fg="#ffffff")
btn_search.pack(side=tk.LEFT, padx=5)
entry_search.bind("<KeyRelease>", lambda e: search_callback(tree, entry_search))

columns = ("Nombre del proceso", "Ejecutable", "PID", "Hora de apertura", "Status", "Ubicación")
tree_frame = tk.Frame(right_frame)
tree_frame.pack(fill=tk.BOTH, expand=True)
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
tree.pack(fill=tk.BOTH, expand=True)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180, anchor=tk.W)

style.configure("Treeview", background="#2b2b2b", foreground="#ffffff", fieldbackground="#2b2b2b")
style.configure("Treeview.Heading", background="#1f1f1f", foreground="#ffffff")
root.configure(bg="#2b2b2b")

show_processes(tree)
root.mainloop()
