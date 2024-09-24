import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


def conectar_banco():
    try:
        conn = sqlite3.connect('minha_crianca_autista.db')
        cursor = conn.cursor()
        

        cursor.execute('''DROP TABLE IF EXISTS profissionais_diagnostico''')
        cursor.execute('''CREATE TABLE profissionais_diagnostico (
                            id INTEGER PRIMARY KEY,
                            especialidade TEXT NOT NULL)''')  

        cursor.execute('''CREATE TABLE IF NOT EXISTS profissionais_recomendados (
                            id INTEGER PRIMARY KEY,
                            nome TEXT NOT NULL,
                            especialidade TEXT NOT NULL,
                            contato TEXT NOT NULL)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS beneficios (
                            id INTEGER PRIMARY KEY,
                            nome TEXT NOT NULL,
                            descricao TEXT NOT NULL)''')

        conn.commit()
        return conn, cursor
    except Exception as e:
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {e}")
        return None, None


def exibir_profissionais_diagnostico():
    cursor.execute('SELECT especialidade FROM profissionais_diagnostico')
    rows = cursor.fetchall()
    lista_profissionais_diagnostico.delete(0, tk.END)
    for row in rows:
        lista_profissionais_diagnostico.insert(tk.END, f"{row[0]}")

def exibir_profissionais_recomendados():
    cursor.execute('SELECT nome, especialidade, contato FROM profissionais_recomendados')
    rows = cursor.fetchall()
    lista_profissionais_recomendados.delete(0, tk.END)
    for row in rows:
        lista_profissionais_recomendados.insert(tk.END, f"{row[0]} - {row[1]} (Contato: {row[2]})")

def exibir_beneficios():
    cursor.execute('SELECT nome, descricao FROM beneficios')
    rows = cursor.fetchall()
    lista_beneficios.delete(0, tk.END)
    for row in rows:
        lista_beneficios.insert(tk.END, f"{row[0]}: {row[1]}")


def inserir_profissional_diagnostico():
    especialidade = entry_especialidade_diagnostico.get()
    if especialidade:  
        cursor.execute('''INSERT INTO profissionais_diagnostico (especialidade) 
                          VALUES (?)''', (especialidade,))
        conn.commit()
        exibir_profissionais_diagnostico()
        entry_especialidade_diagnostico.delete(0, tk.END)  
    else:
        messagebox.showwarning("Atenção", "O campo especialidade não pode estar vazio.")


def inserir_profissional_recomendado():
    nome = entry_nome_recomendado.get()
    especialidade = entry_especialidade_recomendado.get()
    contato = entry_contato.get()
    if nome and especialidade and contato: 
        cursor.execute('''INSERT INTO profissionais_recomendados (nome, especialidade, contato) 
                          VALUES (?, ?, ?)''', (nome, especialidade, contato))
        conn.commit()
        exibir_profissionais_recomendados()
        entry_nome_recomendado.delete(0, tk.END)  
        entry_especialidade_recomendado.delete(0, tk.END)
        entry_contato.delete(0, tk.END)
    else:
        messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")


def inserir_beneficio():
    nome = entry_nome_beneficio.get()
    descricao = entry_descricao_beneficio.get()
    if nome and descricao: 
        cursor.execute('''INSERT INTO beneficios (nome, descricao) 
                          VALUES (?, ?)''', (nome, descricao))
        conn.commit()
        exibir_beneficios()
        entry_nome_beneficio.delete(0, tk.END)  
        entry_descricao_beneficio.delete(0, tk.END)
    else:
        messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")


def criar_interface():
    root = tk.Tk()
    root.title("Minha Criança Autista")


    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, expand=True)


    guia1 = ttk.Frame(notebook)
    notebook.add(guia1, text="Quais Profissionais?")
    
    global lista_profissionais_diagnostico, entry_especialidade_diagnostico
    lista_profissionais_diagnostico = tk.Listbox(guia1, width=50, height=10)
    lista_profissionais_diagnostico.pack(pady=10)
    tk.Button(guia1, text="Carregar Profissionais", command=exibir_profissionais_diagnostico).pack(pady=5)
    
  
    tk.Label(guia1, text="Especialidade:").pack()
    entry_especialidade_diagnostico = tk.Entry(guia1)
    entry_especialidade_diagnostico.pack()
    
    tk.Button(guia1, text="Adicionar Profissional", command=inserir_profissional_diagnostico).pack(pady=5)


    guia2 = ttk.Frame(notebook)
    notebook.add(guia2, text="Profissionais Recomendados")
    
    global lista_profissionais_recomendados, entry_nome_recomendado, entry_especialidade_recomendado, entry_contato
    lista_profissionais_recomendados = tk.Listbox(guia2, width=50, height=10)
    lista_profissionais_recomendados.pack(pady=10)
    tk.Button(guia2, text="Carregar Recomendados", command=exibir_profissionais_recomendados).pack(pady=5)


    tk.Label(guia2, text="Nome:").pack()
    entry_nome_recomendado = tk.Entry(guia2)
    entry_nome_recomendado.pack()
    
    tk.Label(guia2, text="Especialidade:").pack()
    entry_especialidade_recomendado = tk.Entry(guia2)
    entry_especialidade_recomendado.pack()
    
    tk.Label(guia2, text="Contato:").pack()
    entry_contato = tk.Entry(guia2)
    entry_contato.pack()
    
    tk.Button(guia2, text="Adicionar Profissional", command=inserir_profissional_recomendado).pack(pady=5)

 
    guia3 = ttk.Frame(notebook)
    notebook.add(guia3, text="Possíveis Benefícios")
    
    global lista_beneficios, entry_nome_beneficio, entry_descricao_beneficio
    lista_beneficios = tk.Listbox(guia3, width=50, height=10)
    lista_beneficios.pack(pady=10)
    tk.Button(guia3, text="Carregar Benefícios", command=exibir_beneficios).pack(pady=5)
    

    tk.Label(guia3, text="Nome do Benefício:").pack()
    entry_nome_beneficio = tk.Entry(guia3)
    entry_nome_beneficio.pack()
    
    tk.Label(guia3, text="Descrição do Benefício:").pack()
    entry_descricao_beneficio = tk.Entry(guia3)
    entry_descricao_beneficio.pack()
    
    tk.Button(guia3, text="Adicionar Benefício", command=inserir_beneficio).pack(pady=5)


    root.mainloop()

conn, cursor = conectar_banco()
if conn:
    criar_interface()


