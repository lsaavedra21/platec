import tkinter as tk
import os
from tkinter import ttk, messagebox
from datetime import datetime

class LoginApp:
    def __init__(self, master):

        # Verifica se o arquivo log.txt existe e, se não existir, cria um novo
        if not os.path.exists("log.txt"):
            with open("log.txt", "w") as file:
                file.write("")

        self.master = master
        self.master.title("Controle de Login")

        # Define um estilo para os widgets
        self.style = ttk.Style()

        # Define um estilo para os botões com efeito 3D
        self.style.configure("TButton", relief="raised", font=("Helvetica", 10))

        # Define um estilo para os radio buttons
        self.style.configure("TRadiobutton", font=("Helvetica", 10))

        # Define um estilo para os labels
        self.style.configure("TLabel", font=("Helvetica", 10))

        # Define um estilo para os entry fields
        self.style.configure("TEntry", font=("Helvetica", 10))

        # Define um estilo para o Treeview
        self.style.configure("Treeview", font=("Helvetica", 10))

        self.user_type = tk.StringVar(value="Interno")  # Opção padrão
        self.radio_interno = ttk.Radiobutton(master, text="Interno", variable=self.user_type, value="Interno", command=self.update_fields, style="TRadiobutton")
        self.radio_interno.grid(row=0, column=0, pady=5, padx=5)
        self.radio_external = ttk.Radiobutton(master, text="Externo", variable=self.user_type, value="Externo", command=self.update_fields, style="TRadiobutton")
        self.radio_external.grid(row=0, column=1, pady=5, padx=5)

        self.label_user = ttk.Label(master, text="Digite seu código de usuário:", style="TLabel")
        self.label_user.grid(row=1, column=0, pady=5, padx=5)

        self.entry_user = ttk.Entry(master, style="TEntry")
        self.entry_user.grid(row=1, column=1, pady=5, padx=5)

        self.label_company = ttk.Label(master, text="Nome da Empresa:", style="TLabel")
        self.label_company.grid(row=2, column=0, pady=5, padx=5)
        self.entry_company = ttk.Entry(master, style="TEntry")
        self.entry_company.grid(row=2, column=1, pady=5, padx=5)

        self.login_button = ttk.Button(master, text="Login", command=self.login, style="TButton")
        self.login_button.grid(row=3, column=0, columnspan=2, pady=5, padx=5)

        self.logout_button = ttk.Button(master, text="Logout", command=self.logout, state=tk.DISABLED, style="TButton")
        self.logout_button.grid(row=4, column=0, columnspan=2, pady=5, padx=5)

        # Configuração das cabeçalhos do Treeview
        self.tree = ttk.Treeview(master, columns=("Ação", "Tipo de Usuário", "Usuário/Nome", "Empresa", "Registro"), show="headings", style="Treeview")

        # Configuração das colunas do Treeview
        self.tree.column("Ação", width=70, anchor="center")
        self.tree.column("Tipo de Usuário", width=100, anchor="center")
        self.tree.column("Usuário/Nome", width=150, anchor="center")
        self.tree.column("Empresa", width=150, anchor="center")
        self.tree.column("Registro", width=150, anchor="center")

        # Configuração dos cabeçalhos do Treeview
        self.tree.heading("Ação", text="Ação")
        self.tree.heading("Tipo de Usuário", text="Tipo de Usuário")
        self.tree.heading("Usuário/Nome", text="Usuário/Nome")
        self.tree.heading("Empresa", text="Empresa")
        self.tree.heading("Registro", text="Registro")

        # Cria uma scrollbar vertical
        self.scroll_y = ttk.Scrollbar(master, orient="vertical", command=self.tree.yview)
        self.scroll_y.grid(row=0, column=3, rowspan=5, sticky="ns")

        # Configura a scrollbar para rolar o Treeview
        self.tree.configure(yscrollcommand=self.scroll_y.set)

        self.tree.grid(row=0, column=2, rowspan=5, pady=5, padx=5, sticky="nsew")

        self.logged_in_user = None  # Armazena o código de usuário logado

        self.update_fields()  # Atualiza os campos de entrada com base na seleção inicial

        self.load_last_logs()  # Carrega os últimos logs ao iniciar a aplicação

        # Define uma função de fechamento para chamar logout antes de fechar a janela
        def on_closing():
            if self.logged_in_user:
                self.logout()
            self.master.destroy()

        # Configura o protocolo de fechamento para chamar a função on_closing
        self.master.protocol("WM_DELETE_WINDOW", on_closing)

    def load_last_logs(self):
        # Abre o arquivo de texto em modo de leitura
        with open("log.txt", "r") as file:
            # Lê as primeiras 10 linhas do arquivo
            lines = file.readlines()[:10]

        # Adiciona os registros ao Treeview na ordem correta
        for line in lines:
            log_data = line.strip().split(" - ")
            self.tree.insert("", tk.END, values=log_data)

    def update_fields(self):
        if self.user_type.get() == "Interno":
            self.label_user.config(text="Digite seu código de usuário: (LB ou PM)")
            self.label_company.grid_forget()
            self.entry_company.grid_forget()
        else:  # Se selecionado "Externo"
            self.label_user.config(text="Nome:")
            self.entry_user.grid(row=1, column=1, pady=5, padx=5)
            self.label_company.grid(row=2, column=0, pady=5, padx=5)
            self.entry_company.grid(row=2, column=1, pady=5, padx=5)

    def login(self):
        user_type = self.user_type.get()
        if user_type == "Interno":
            user_code = self.entry_user.get().upper()  # Convertendo para maiúsculas
            if not (user_code.startswith("LB") or user_code.startswith("PM")) or not user_code[2:].isdigit() or len(
                    user_code) != 7:
                messagebox.showerror("Erro",
                                     "Código de usuário interno inválido. Deve começar com 'LB' ou 'PM'.")
                return
        else:  # Usuário externo
            user_name = self.entry_user.get()
            company_name = self.entry_company.get()
            if len(user_name) < 3 or len(company_name) < 3:
                messagebox.showerror("Erro", "O nome do usuário e o nome da empresa devem ser preenchidos.")
                return
        self.logged_in_user = self.entry_user.get()  # Armazena o código de usuário logado
        user_info = self.logged_in_user
        company_info = self.entry_company.get() if user_type == "Externo" else "Renault"  # Nome da empresa para usuário externo
        login_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log_message = f"Login - {user_type} - {user_info} - {company_info} - {login_time}\n"
        self.tree.insert("", 0, values=log_message.strip().split(" - "))
        self.login_button.config(state=tk.DISABLED)
        self.logout_button.config(state=tk.NORMAL)
        self.write_to_file(log_message)  # Escreve no arquivo de texto

        # Desativa os campos de entrada e os radio buttons
        self.entry_user.config(state=tk.DISABLED)
        self.entry_company.config(state=tk.DISABLED)
        self.radio_interno.config(state=tk.DISABLED)
        self.radio_external.config(state=tk.DISABLED)

    def logout(self):
        if self.logged_in_user:  # Verifica se há um usuário logado
            user_info = self.logged_in_user  # Usa o código de usuário logado durante o logout
            logout_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            user_type = self.user_type.get()
            company_info = self.entry_company.get() if user_type == "Externo" else "Renault"  # Nome da empresa para usuário externo
            log_message = f"Logout - {user_type} - {user_info} - {company_info} - {logout_time}\n"
            self.tree.insert("", 0, values=log_message.strip().split(" - "))
            self.logged_in_user = None  # Reseta o usuário logado para None
            self.login_button.config(state=tk.NORMAL)
            self.logout_button.config(state=tk.DISABLED)
            self.write_to_file(log_message)  # Escreve no arquivo de texto

            # Ativa os campos de entrada e os radio buttons
            self.entry_user.config(state=tk.NORMAL)
            self.entry_company.config(state=tk.NORMAL)
            self.radio_interno.config(state=tk.NORMAL)
            self.radio_external.config(state=tk.NORMAL)

    def write_to_file(self, log_message):
        # Abre o arquivo de texto em modo de leitura e escrita
        with open("log.txt", "r+") as file:
            # Lê todos os dados existentes
            data = file.read()
            # Retorna o cursor para o início do arquivo
            file.seek(0)
            # Escreve o novo registro no início do arquivo
            file.write(log_message.strip() + "\n" + data)

    def __del__(self):
        pass

def main():
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
