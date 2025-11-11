# criar_atalho.py
import os
import sys
import win32com.client

def criar_atalho():
    # Caminhos absolutos
    pasta_projeto = os.path.dirname(os.path.abspath(__file__))
    main_py = os.path.join(pasta_projeto, 'main.py')
    python_exe = sys.executable  # Ex: C:\Python313\python.exe

    # Verifica se main.py existe
    if not os.path.exists(main_py):
        print(f"ERRO: main.py não encontrado em {main_py}")
        return

    # Área de trabalho
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    atalho_path = os.path.join(desktop, "Paciência Yukon.lnk")

    # Cria o atalho
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(atalho_path)
    
    shortcut.Targetpath = python_exe
    shortcut.Arguments = f'"{main_py}"'  # Aspas para caminhos com espaço
    shortcut.WorkingDirectory = pasta_projeto  # ESSENCIAL!
    shortcut.IconLocation = python_exe  # Ícone do Python
    shortcut.Description = "Jogo Paciência Yukon"
    
    shortcut.save()
    
    print(f"SUCESSO! Atalho criado em:\n{atalho_path}")
    print(f"   Python: {python_exe}")
    print(f"   Script: {main_py}")
    print(f"   Pasta: {pasta_projeto}")

if __name__ == "__main__":
    criar_atalho()