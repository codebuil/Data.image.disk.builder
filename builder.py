import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import subprocess
import shutil
import os



class BareboneBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Barebone Builder")

        # Janela amarela
        self.root.configure(bg='yellow')

        # Área de texto
        self.text_area = tk.Text(self.root, height=10, width=50)
        self.text_area.pack(pady=10)

        # Botões
        self.build_button = tk.Button(self.root, text="Build", command=self.build_kernel)
        self.build_button.pack(pady=5)

        self.run_button = tk.Button(self.root, text="Run", command=self.run_kernel)
        self.run_button.pack(pady=5)

        self.copy_button = tk.Button(self.root, text="unmount", command=self.copy_file)
        self.copy_button.pack(pady=5)

    def execute_command(self, command,show:bool):
        try:
            
            result = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, text=True)
            self.text_area.insert(tk.END, result)
        except subprocess.CalledProcessError as e:
            if show:
                self.text_area.insert(tk.END,f"Error executing command:\n{e.output}")

    def build_kernel(self):#filename = tk.filedialog.askdirectory(title="Select folder to build")
        self.text_area.delete(1.0, tk.END)

        self.text_area.insert(tk.END,f"writing 40 mega...")
        self.execute_command('dd if=/dev/zero of="data.img" bs=1M count=40',True)
        self.execute_command('sudo mkfs.vfat -n "DATA" -S 512  "data.img"',True)
        self.execute_command('sudo chmod 777 "data.img"',True)
        
    def run_kernel(self):
        self.text_area.delete(1.0, tk.END)
        self.execute_command("mkdir /mnt/isos",False)
        self.execute_command("sudo chmod 777 /mnt/isos",False)
        self.execute_command('sudo mount-t vfat -o loop "data.img" /mnt/isos ',True)
        self.execute_command("nautilus --browser /mnt/isos",True)


    def copy_file(self):
        self.text_area.delete(1.0, tk.END)
        
        if 0==0:
            self.execute_command("sudo umount /mnt/isos",True)
            


if __name__ == "__main__":
    root = tk.Tk()
    builder = BareboneBuilder(root)
    root.mainloop()
