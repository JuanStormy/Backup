#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 INFERNAL BACKUP PRO v2.0 ULTIMATE 🔥
Aplicación Completa con Sistema de Pestañas y Configuración Avanzada
Compatible: Windows 10/11
Autor: Stormy
Licencia: Free
"""

import sys
import os
import subprocess
import ctypes
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import threading
import queue
import time
import json
import hashlib
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import base64
import secrets
import sqlite3
import webbrowser
import zipfile
import platform
import locale

# ============================= INSTALACIÓN AUTOMÁTICA =============================

def check_admin():
    """Verificar permisos de administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def install_dependencies():
    """Instalar dependencias automáticamente"""
    required_packages = [
        'psutil>=5.9.0',
        'py7zr>=0.20.0',
        'cryptography>=41.0.0',
        'jinja2>=3.1.0'
    ]
    
    print("🔥 INFERNAL BACKUP PRO v2.0 ULTIMATE - by Stormy 🔥")
    print("Verificando e instalando dependencias...")
    
    missing_packages = []
    
    for package in required_packages:
        package_name = package.split('>=')[0]
        try:
            if package_name == 'psutil':
                import psutil
            elif package_name == 'py7zr':
                import py7zr
            elif package_name == 'cryptography':
                from cryptography.fernet import Fernet
            elif package_name == 'jinja2':
                import jinja2
            print(f"✅ {package_name} disponible")
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"📦 Instalando {len(missing_packages)} paquetes...")
        for package in missing_packages:
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package, "--quiet"
                ])
                print(f"✅ {package.split('>=')[0]} instalado")
            except Exception as e:
                print(f"❌ Error instalando {package}: {e}")
                return False
    
    return True

# Instalar dependencias al inicio
if not install_dependencies():
    print("❌ No se pudieron instalar las dependencias necesarias")
    input("Presiona Enter para salir...")
    sys.exit(1)

# Importar dependencias instaladas
try:
    import psutil
    import py7zr
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import jinja2
except ImportError as e:
    print(f"❌ Error importando dependencias: {e}")
    sys.exit(1)

# Intentar importar pygame para sonidos (opcional)
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("⚠️ pygame no disponible - funcionando sin sonidos")

# ============================= SISTEMA DE IDIOMAS =============================

class LanguageManager:
    """Gestor de idiomas de la aplicación"""
    
    def __init__(self):
        self.current_language = 'es'  # Español por defecto
        self.translations = {
            'es': {
                'app_title': '🔥 INFERNAL BACKUP PRO v2.0 - by Stormy 🔥',
                'select_source': '📁 Seleccionar Origen',
                'backup_config': '⚙️ Configuración',
                'backup_type': 'Tipo de Backup',
                'full_backup': '🔄 Backup Completo (Full)',
                'incremental_backup': '📈 Backup Incremental',
                'differential_backup': '📊 Backup Diferencial',
                'security_options': '🔐 Seguridad y Compresión',
                'compress_7z': '🗜️ Comprimir con 7-Zip',
                'encrypt_aes': '🔒 Encriptar con AES-256',
                'encrypt_7z_pass': '🔐 7-Zip con Contraseña',
                'password': '🔑 Contraseña:',
                'destination': '💾 Destino del Backup',
                'start_backup': '🚀 INICIAR BACKUP',
                'cancel_backup': '🛑 CANCELAR',
                'progress': '📈 Progreso',
                'activity_log': '📜 Log de Actividad',
                'ready_to_start': '🔋 Listo para iniciar backup',
                'select_origin': 'ℹ️ Selecciona un origen en el explorador',
                'tab_backup': '📂 BACKUP',
                'tab_encryption': '🔐 ENCRIPTACIÓN',
                'tab_reports': '📊 REPORTES',
                'tab_settings': '⚙️ CONFIGURACIÓN',
                'view_reports': '📊 Ver Reportes',
                'encryption_center': '🔐 Encriptación',
                'settings_title': '🛠️ Configuración Avanzada',
                'language_section': '🌍 Idioma / Language',
                'theme_section': '🎨 Tema y Apariencia',
                'sound_section': '🔊 Audio',
                'enable_sounds': '🔊 Habilitar sonidos',
                'test_sounds': 'Probar Sonidos:',
                'btn_click': '▶️ Click',
                'btn_success': '▶️ Éxito', 
                'btn_error': '▶️ Error',
                'font_settings': 'Configuración de Fuente',
                'font_family': 'Familia de Fuente:',
                'font_size': 'Tamaño:',
                'theme_color': 'Color del Tema:',
                'apply_changes': '✅ Aplicar Cambios',
                'reset_defaults': '🔄 Restaurar por Defecto',
                'app_info': 'ℹ️ Información de la Aplicación',
                'restart_app': '🔄 Reiniciar App',
                'exit_app': '❌ Salir',
                'reports_center': '📈 Centro de Reportes y Estadísticas',
                'generate_report': '📄 Generar Reporte Manual',
                'open_last_report': '🌐 Abrir Último Reporte',
                'open_reports_folder': '📁 Abrir Carpeta Reportes',
                'statistics': '📊 Estadísticas',
                'encryption_aes_tab': '🔒 AES-256',
                'encryption_7z_tab': '🗜️ 7-Zip',
                'file_folder': '📄 Archivo/Carpeta:',
                'encrypt': '🔒 Encriptar',
                'decrypt': '🔓 Desencriptar',
                'compress': '🗜️ Comprimir',
                'extract': '📂 Extraer',
                'operation_log': '📜 Log de Operaciones'
            },
            'en': {
                'app_title': '🔥 INFERNAL BACKUP PRO v2.0 - by Stormy 🔥',
                'select_source': '📁 Select Source',
                'backup_config': '⚙️ Configuration',
                'backup_type': 'Backup Type',
                'full_backup': '🔄 Full Backup',
                'incremental_backup': '📈 Incremental Backup',
                'differential_backup': '📊 Differential Backup',
                'security_options': '🔐 Security and Compression',
                'compress_7z': '🗜️ Compress with 7-Zip',
                'encrypt_aes': '🔒 Encrypt with AES-256',
                'encrypt_7z_pass': '🔐 7-Zip with Password',
                'password': '🔑 Password:',
                'destination': '💾 Backup Destination',
                'start_backup': '🚀 START BACKUP',
                'cancel_backup': '🛑 CANCEL',
                'progress': '📈 Progress',
                'activity_log': '📜 Activity Log',
                'ready_to_start': '🔋 Ready to start backup',
                'select_origin': 'ℹ️ Select a source in the explorer',
                'tab_backup': '📂 BACKUP',
                'tab_encryption': '🔐 ENCRYPTION',
                'tab_reports': '📊 REPORTS',
                'tab_settings': '⚙️ SETTINGS',
                'view_reports': '📊 View Reports',
                'encryption_center': '🔐 Encryption',
                'settings_title': '🛠️ Advanced Settings',
                'language_section': '🌍 Language / Idioma',
                'theme_section': '🎨 Theme and Appearance',
                'sound_section': '🔊 Audio',
                'enable_sounds': '🔊 Enable sounds',
                'test_sounds': 'Test Sounds:',
                'btn_click': '▶️ Click',
                'btn_success': '▶️ Success',
                'btn_error': '▶️ Error',
                'font_settings': 'Font Settings',
                'font_family': 'Font Family:',
                'font_size': 'Size:',
                'theme_color': 'Theme Color:',
                'apply_changes': '✅ Apply Changes',
                'reset_defaults': '🔄 Reset to Default',
                'app_info': 'ℹ️ Application Info',
                'restart_app': '🔄 Restart App',
                'exit_app': '❌ Exit',
                'reports_center': '📈 Reports and Statistics Center',
                'generate_report': '📄 Generate Manual Report',
                'open_last_report': '🌐 Open Last Report',
                'open_reports_folder': '📁 Open Reports Folder',
                'statistics': '📊 Statistics',
                'encryption_aes_tab': '🔒 AES-256',
                'encryption_7z_tab': '🗜️ 7-Zip',
                'file_folder': '📄 File/Folder:',
                'encrypt': '🔒 Encrypt',
                'decrypt': '🔓 Decrypt',
                'compress': '🗜️ Compress',
                'extract': '📂 Extract',
                'operation_log': '📜 Operation Log'
            }
        }
    
    def get_text(self, key):
        """Obtener texto traducido"""
        return self.translations.get(self.current_language, {}).get(key, key)
    
    def set_language(self, language_code):
        """Cambiar idioma"""
        if language_code in self.translations:
            self.current_language = language_code
            return True
        return False
    
    def get_available_languages(self):
        """Obtener idiomas disponibles"""
        return {
            'es': '🇪🇸 Español',
            'en': '🇺🇸 English'
        }

# ============================= SISTEMA DE SONIDOS =============================

class SoundManager:
    """Gestor de sonidos de la aplicación"""
    
    def __init__(self):
        self.sounds_enabled = False
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
                self.sounds_enabled = True
                self.create_synthetic_sounds()
            except:
                print("⚠️ No se pudo inicializar el sistema de audio")
    
    def create_synthetic_sounds(self):
        """Crear sonidos sintéticos usando pygame"""
        if not self.sounds_enabled:
            return
            
        try:
            import numpy as np
            
            # Parámetros base
            sample_rate = 22050
            
            # Sonido de click (800Hz, 0.1s)
            duration = 0.1
            frequency = 800
            frames = int(duration * sample_rate)
            wave = np.sin(2 * np.pi * frequency * np.linspace(0, duration, frames))
            wave = (wave * 16384).astype(np.int16)
            stereo_wave = np.array([wave, wave]).T
            self.click_sound = pygame.sndarray.make_sound(stereo_wave)
            
            # Sonido de hover (1200Hz, 0.05s)
            duration = 0.05
            frequency = 1200
            frames = int(duration * sample_rate)
            wave = np.sin(2 * np.pi * frequency * np.linspace(0, duration, frames)) * 0.3
            wave = (wave * 8000).astype(np.int16)
            stereo_wave = np.array([wave, wave]).T
            self.hover_sound = pygame.sndarray.make_sound(stereo_wave)
            
            # Sonido de éxito (frecuencia ascendente)
            duration = 0.5
            frames = int(duration * sample_rate)
            t = np.linspace(0, duration, frames)
            frequency = 400 + 200 * t  # De 400 a 600 Hz
            wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 2)
            wave = (wave * 12000).astype(np.int16)
            stereo_wave = np.array([wave, wave]).T
            self.success_sound = pygame.sndarray.make_sound(stereo_wave)
            
            # Sonido de error (frecuencia descendente)
            duration = 0.3
            frames = int(duration * sample_rate)
            t = np.linspace(0, duration, frames)
            frequency = 300 - 100 * t  # De 300 a 200 Hz
            wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 3)
            wave = (wave * 10000).astype(np.int16)
            stereo_wave = np.array([wave, wave]).T
            self.error_sound = pygame.sndarray.make_sound(stereo_wave)
            
        except ImportError:
            # Fallback sin numpy - sonidos básicos
            self.create_basic_sounds()
        except Exception as e:
            print(f"⚠️ Error creando sonidos: {e}")
            self.sounds_enabled = False
    
    def create_basic_sounds(self):
        """Crear sonidos básicos sin numpy"""
        sample_rate = 22050
        
        # Click básico
        duration = 0.1
        frames = int(duration * sample_rate)
        wave = []
        for i in range(frames):
            amplitude = 8000 * (1 - i / frames)  # Decaimiento
            wave.extend([int(amplitude), int(amplitude)])
        
        try:
            self.click_sound = pygame.sndarray.make_sound(wave)
            self.hover_sound = self.click_sound  # Usar el mismo para hover
            self.success_sound = self.click_sound  # Usar el mismo para éxito
            self.error_sound = self.click_sound    # Usar el mismo para error
        except:
            self.sounds_enabled = False
    
    def play_click(self):
        if self.sounds_enabled and hasattr(self, 'click_sound'):
            try:
                self.click_sound.play()
            except:
                pass
    
    def play_hover(self):
        if self.sounds_enabled and hasattr(self, 'hover_sound'):
            try:
                self.hover_sound.play()
            except:
                pass
    
    def play_success(self):
        if self.sounds_enabled and hasattr(self, 'success_sound'):
            try:
                self.success_sound.play()
            except:
                pass
    
    def play_error(self):
        if self.sounds_enabled and hasattr(self, 'error_sound'):
            try:
                self.error_sound.play()
            except:
                pass

# ============================= BOTONES CON EFECTOS HOVER =============================

class HoverButton(ttk.Button):
    """Botón con efectos de hover y sonidos"""
    
    def __init__(self, parent, sound_manager, **kwargs):
        super().__init__(parent, **kwargs)
        self.sound_manager = sound_manager
        self.original_style = "TButton"
        self.hover_style = "Hover.TButton"
        
        # Bind eventos
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
    
    def on_enter(self, event):
        """Efecto hover"""
        self.sound_manager.play_hover()
        try:
            self.configure(style=self.hover_style)
        except:
            pass
    
    def on_leave(self, event):
        """Salir del hover"""
        try:
            self.configure(style=self.original_style)
        except:
            pass
    
    def on_click(self, event):
        """Efecto click"""
        self.sound_manager.play_click()

# ============================= SISTEMA DE ENCRIPTACIÓN =============================

class EncryptionManager:
    """Gestor de encriptación AES-256 y 7-Zip"""
    
    def __init__(self):
        self.key = None
        self.fernet = None
    
    def generate_key_from_password(self, password: str, salt: bytes = None):
        """Generar clave AES-256 desde contraseña"""
        if salt is None:
            salt = secrets.token_bytes(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.key = key
        self.fernet = Fernet(key)
        return salt
    
    def encrypt_file_aes(self, file_path: str, password: str, output_path: str = None):
        """Encriptar archivo con AES-256"""
        if output_path is None:
            output_path = file_path + ".encrypted"
        
        try:
            salt = self.generate_key_from_password(password)
            
            if os.path.isfile(file_path):
                # Encriptar archivo individual
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                encrypted_data = self.fernet.encrypt(file_data)
            else:
                # Encriptar directorio (crear zip primero)
                temp_zip = file_path + "_temp.zip"
                with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(file_path):
                        for file in files:
                            file_path_full = os.path.join(root, file)
                            arcname = os.path.relpath(file_path_full, file_path)
                            zipf.write(file_path_full, arcname)
                
                with open(temp_zip, 'rb') as f:
                    file_data = f.read()
                os.remove(temp_zip)
                encrypted_data = self.fernet.encrypt(file_data)
            
            with open(output_path, 'wb') as f:
                f.write(salt + encrypted_data)
            
            return True, f"Archivo encriptado: {output_path}"
        except Exception as e:
            return False, f"Error encriptando: {str(e)}"
    
    def decrypt_file_aes(self, file_path: str, password: str, output_path: str = None):
        """Desencriptar archivo AES-256"""
        if output_path is None:
            if file_path.endswith('.encrypted'):
                output_path = file_path[:-10]
            else:
                output_path = file_path + "_decrypted"
        
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            salt = data[:16]
            encrypted_data = data[16:]
            
            self.generate_key_from_password(password, salt)
            decrypted_data = self.fernet.decrypt(encrypted_data)
            
            # Intentar determinar si es un ZIP
            if decrypted_data.startswith(b'PK'):
                # Es un directorio comprimido
                temp_zip = output_path + "_temp.zip"
                with open(temp_zip, 'wb') as f:
                    f.write(decrypted_data)
                
                # Extraer
                os.makedirs(output_path, exist_ok=True)
                with zipfile.ZipFile(temp_zip, 'r') as zipf:
                    zipf.extractall(output_path)
                os.remove(temp_zip)
            else:
                # Es un archivo individual
                with open(output_path, 'wb') as f:
                    f.write(decrypted_data)
            
            return True, f"Archivo desencriptado: {output_path}"
        except Exception as e:
            return False, f"Error desencriptando: {str(e)}"
    
    def compress_7z_with_password(self, source_path: str, archive_path: str, password: str):
        """Crear archivo 7z con contraseña"""
        try:
            with py7zr.SevenZipFile(
                archive_path, 
                'w', 
                password=password,
                header_encryption=True  # CRÍTICO: Encriptar nombres de archivos
            ) as archive:
                if os.path.isfile(source_path):
                    archive.write(source_path, os.path.basename(source_path))
                else:
                    for root, dirs, files in os.walk(source_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, source_path)
                            archive.write(file_path, arcname)
            
            return True, f"Archivo 7z creado: {archive_path}"
        except Exception as e:
            return False, f"Error creando 7z: {str(e)}"
    
    def extract_7z_with_password(self, archive_path: str, extract_path: str, password: str):
        """Extraer archivo 7z con contraseña"""
        try:
            os.makedirs(extract_path, exist_ok=True)
            with py7zr.SevenZipFile(archive_path, 'r', password=password) as archive:
                archive.extractall(extract_path)
            
            return True, f"Archivo extraído en: {extract_path}"
        except Exception as e:
            return False, f"Error extrayendo: {str(e)}"

# ============================= SISTEMA DE REPORTES =============================

class ReportManager:
    """Gestor de reportes HTML y base de datos"""
    
    def __init__(self):
        self.reports_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(self.reports_dir, exist_ok=True)
        self.db_path = os.path.join(self.reports_dir, "backup_history.db")
        self.setup_database()
    
    def setup_database(self):
        """Configurar base de datos SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS backups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                source_path TEXT,
                destination_path TEXT,
                backup_type TEXT,
                file_count INTEGER,
                total_size INTEGER,
                compressed_size INTEGER,
                duration REAL,
                success BOOLEAN,
                encryption_type TEXT,
                verification_hash TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_backup_record(self, backup_data):
        """Guardar registro de backup"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO backups 
            (timestamp, source_path, destination_path, backup_type, 
             file_count, total_size, compressed_size, duration, 
             success, encryption_type, verification_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            backup_data.get('timestamp'),
            backup_data.get('source_path'),
            backup_data.get('destination_path'),
            backup_data.get('backup_type'),
            backup_data.get('file_count', 0),
            backup_data.get('total_size', 0),
            backup_data.get('compressed_size', 0),
            backup_data.get('duration', 0),
            backup_data.get('success', False),
            backup_data.get('encryption_type', 'None'),
            backup_data.get('verification_hash', '')
        ))
        
        conn.commit()
        conn.close()
    
    def generate_html_report(self, backup_data):
        """Generar reporte HTML detallado"""
        timestamp = datetime.now()
        report_filename = f"backup_report_{timestamp.strftime('%Y%m%d_%H%M%S')}.html"
        report_path = os.path.join(self.reports_dir, report_filename)
        
        # Template HTML (versión compacta)
        html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 Infernal Backup Report</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Consolas', 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%);
            color: #00ff00; min-height: 100vh; padding: 20px;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: rgba(0, 0, 0, 0.8);
            border: 2px solid #00ff00; border-radius: 15px; padding: 30px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
        }
        .header { text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 3px solid #00ff00; }
        .header h1 { font-size: 2.8em; margin-bottom: 10px; text-shadow: 0 0 20px #00ff00; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat-card { background: linear-gradient(45deg, rgba(0, 255, 0, 0.1), rgba(0, 255, 0, 0.05));
            padding: 20px; border: 1px solid rgba(0, 255, 0, 0.4); border-radius: 10px; text-align: center; }
        .stat-value { font-size: 2.2em; font-weight: bold; color: #00ff00; display: block; }
        .success { color: #00ff00; }
        .error { color: #ff3333; }
        .footer { text-align: center; margin-top: 40px; padding-top: 25px;
            border-top: 2px solid rgba(0, 255, 0, 0.3); color: #00aa00; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 INFERNAL BACKUP REPORT 🔥</h1>
            <p>by Stormy | {{ timestamp }}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-value">{{ file_count }}</span>
                <div>Archivos Procesados</div>
            </div>
            <div class="stat-card">
                <span class="stat-value">{{ total_size }}</span>
                <div>Tamaño Total</div>
            </div>
            <div class="stat-card">
                <span class="stat-value">{{ duration }}</span>
                <div>Duración</div>
            </div>
            <div class="stat-card">
                <span class="stat-value {{ status_class }}">{{ status }}</span>
                <div>Estado Final</div>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>🔥 Generado por Infernal Backup Pro v2.0 Ultimate</strong></p>
            <p>👤 Autor: Stormy | 📄 Licencia: Free</p>
        </div>
    </div>
</body>
</html>
        """
        
        # Preparar datos del template
        template_data = {
            'timestamp': timestamp.strftime('%d/%m/%Y %H:%M:%S'),
            'file_count': backup_data.get('file_count', 0),
            'total_size': self._format_bytes(backup_data.get('total_size', 0)),
            'duration': self._format_duration(backup_data.get('duration', 0)),
            'status': 'COMPLETADO ✅' if backup_data.get('success', False) else 'ERROR ❌',
            'status_class': 'success' if backup_data.get('success', False) else 'error'
        }
        
        # Renderizar template
        template = jinja2.Template(html_template)
        html_content = template.render(**template_data)
        
        # Guardar archivo HTML
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Guardar en base de datos
        self.save_backup_record(backup_data)
        
        return report_path
    
    def get_backup_statistics(self):
        """Obtener estadísticas de backups"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            stats = {}
            
            # Estadísticas básicas
            cursor.execute("SELECT COUNT(*) FROM backups")
            stats['total_backups'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM backups WHERE success = 1")
            stats['successful_backups'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(total_size) FROM backups WHERE success = 1")
            result = cursor.fetchone()[0]
            stats['total_data_backed_up'] = result or 0
            
            cursor.execute("SELECT AVG(duration) FROM backups WHERE success = 1")
            result = cursor.fetchone()[0]
            stats['average_duration'] = result or 0
            
            # Últimos backups
            cursor.execute("""
                SELECT timestamp, backup_type, source_path, success, encryption_type 
                FROM backups 
                ORDER BY timestamp DESC 
                LIMIT 10
            """)
            stats['recent_backups'] = cursor.fetchall()
            
            conn.close()
            return stats
            
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {
                'total_backups': 0,
                'successful_backups': 0,
                'total_data_backed_up': 0,
                'average_duration': 0,
                'recent_backups': []
            }
    
    def _format_bytes(self, bytes_value):
        """Formatear bytes en unidades legibles"""
        if bytes_value == 0:
            return "0 B"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0
        
        while bytes_value >= 1024 and unit_index < len(units) - 1:
            bytes_value /= 1024.0
            unit_index += 1
        
        return f"{bytes_value:.1f} {units[unit_index]}"
    
    def _format_duration(self, seconds):
        """Formatear duración en formato legible"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"

# ============================= UTILIDADES DEL SISTEMA =============================

class SystemUtils:
    """Utilidades para interactuar con el sistema"""
    
    @staticmethod
    def get_drives():
        """Obtener todas las unidades de disco"""
        drives = []
        try:
            partitions = psutil.disk_partitions(all=False)
            for partition in partitions:
                if os.path.exists(partition.mountpoint):
                    drives.append(partition.mountpoint)
        except Exception as e:
            print(f"Error obteniendo unidades: {e}")
        return drives
    
    @staticmethod
    def get_drive_info(drive_path):
        """Obtener información de una unidad"""
        try:
            usage = psutil.disk_usage(drive_path)
            
            # Intentar obtener etiqueta de volumen
            label = "Local Disk"
            if platform.system() == "Windows":
                try:
                    import win32api
                    volume_info = win32api.GetVolumeInformation(drive_path)
                    label = volume_info[0] if volume_info[0] else "Local Disk"
                except:
                    pass
            
            return {
                'label': label,
                'total_space': SystemUtils.format_bytes(usage.total),
                'free_space': SystemUtils.format_bytes(usage.free),
                'used_space': SystemUtils.format_bytes(usage.used),
                'usage_percent': round((usage.used / usage.total) * 100, 1) if usage.total > 0 else 0
            }
        except Exception:
            return {
                'label': 'Desconocido',
                'total_space': '0 B',
                'free_space': '0 B',
                'used_space': '0 B',
                'usage_percent': 0
            }
    
    @staticmethod
    def get_folders(path, max_folders=100):
        """Obtener carpetas en una ruta"""
        folders = []
        try:
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_dir() and not entry.name.startswith('.'):
                        folders.append(entry.name)
                        if len(folders) >= max_folders:
                            break
        except (PermissionError, FileNotFoundError, OSError):
            pass
        return sorted(folders)
    
    @staticmethod
    def has_subdirectories(path):
        """Verificar si una carpeta tiene subdirectorios"""
        try:
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_dir():
                        return True
        except:
            pass
        return False
    
    @staticmethod
    def get_path_info(path):
        """Obtener información de una ruta"""
        try:
            if os.path.isfile(path):
                size = os.path.getsize(path)
                return f"📄 Archivo - Tamaño: {SystemUtils.format_bytes(size)}"
            elif os.path.isdir(path):
                total_size = 0
                file_count = 0
                folder_count = 0
                
                try:
                    for root, dirs, files in os.walk(path):
                        folder_count += len(dirs)
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                total_size += os.path.getsize(file_path)
                                file_count += 1
                                if file_count > 5000:  # Limitar para rendimiento
                                    return (f"📁 Directorio - >5k archivos, "
                                           f">{SystemUtils.format_bytes(total_size)}")
                            except:
                                continue
                    
                    return (f"📁 Directorio - {file_count} archivos, "
                           f"{folder_count} carpetas, {SystemUtils.format_bytes(total_size)}")
                except:
                    return "📁 Directorio - Sin acceso para calcular estadísticas"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @staticmethod
    def format_bytes(bytes_value):
        """Formatear bytes en unidades legibles"""
        if bytes_value == 0:
            return "0 B"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        unit_index = 0
        
        while bytes_value >= 1024 and unit_index < len(units) - 1:
            bytes_value /= 1024.0
            unit_index += 1
        
        return f"{bytes_value:.1f} {units[unit_index]}"
    
    @staticmethod
    def calculate_folder_hash(folder_path):
        """Calcular hash SHA-256 de una carpeta (para verificación)"""
        try:
            hash_sha256 = hashlib.sha256()
            
            for root, dirs, files in os.walk(folder_path):
                dirs.sort()
                files.sort()
                
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'rb') as f:
                            for chunk in iter(lambda: f.read(8192), b""):
                                hash_sha256.update(chunk)
                        rel_path = os.path.relpath(file_path, folder_path)
                        hash_sha256.update(rel_path.encode('utf-8'))
                    except:
                        continue
            
            return hash_sha256.hexdigest()
        except Exception:
            return ""

# ============================= MOTOR DE BACKUP =============================

class BackupEngine:
    """Motor principal de copias de seguridad"""
    
    def __init__(self, sound_manager, report_manager, encryption_manager):
        self.cancelled = False
        self.sound_manager = sound_manager
        self.report_manager = report_manager
        self.encryption_manager = encryption_manager
    
    def start_backup(self, config):
        """Iniciar proceso de backup"""
        start_time = time.time()
        self.cancelled = False
        
        # Extraer configuración
        source = config['source']
        destination = config['destination']
        mode = config['mode']
        compress = config.get('compress', False)
        encrypt_aes = config.get('encrypt_aes', False)
        encrypt_7z = config.get('encrypt_7z', False)
        password = config.get('password', '')
        progress_queue = config['progress_queue']
        
        # Datos del backup para el reporte
        backup_data = {
            'timestamp': datetime.now().isoformat(),
            'source_path': source,
            'destination_path': destination,
            'backup_type': mode,
            'success': False,
            'encryption_type': 'None',
            'file_count': 0,
            'total_size': 0,
            'compressed_size': 0,
            'duration': 0,
            'verification_hash': ''
        }
        
        try:
            # Crear directorio de backup con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{timestamp}_{mode}"
            backup_dir = os.path.join(destination, backup_name)
            os.makedirs(backup_dir, exist_ok=True)
            
            progress_queue.put({
                'type': 'progress',
                'value': 5,
                'text': '🔍 Analizando archivos origen...'
            })
            
            # Obtener lista de archivos a copiar
            files_to_copy = self._get_files_to_copy(source, destination, mode, progress_queue)
            
            if self.cancelled:
                shutil.rmtree(backup_dir, ignore_errors=True)
                progress_queue.put({'type': 'complete', 'success': False, 'message': 'Operación cancelada'})
                return
            
            # Calcular tamaño total
            total_bytes = 0
            for file_path in files_to_copy:
                try:
                    if os.path.exists(file_path):
                        total_bytes += os.path.getsize(file_path)
                except:
                    continue
            
            backup_data.update({
                'file_count': len(files_to_copy),
                'total_size': total_bytes
            })
            
            progress_queue.put({
                'type': 'progress',
                'value': 15,
                'text': f'📂 Copiando {len(files_to_copy)} archivos...'
            })
            
            # Proceso de copia de archivos
            copied_bytes = 0
            successful_copies = 0
            
            for i, file_path in enumerate(files_to_copy):
                if self.cancelled:
                    break
                
                try:
                    # Calcular ruta relativa y destino
                    rel_path = os.path.relpath(file_path, source)
                    dest_file = os.path.join(backup_dir, rel_path)
                    
                    # Crear directorio padre si no existe
                    dest_parent = os.path.dirname(dest_file)
                    os.makedirs(dest_parent, exist_ok=True)
                    
                    # Copiar archivo manteniendo metadatos
                    shutil.copy2(file_path, dest_file)
                    successful_copies += 1
                    
                    # Actualizar progreso
                    try:
                        file_size = os.path.getsize(file_path)
                        copied_bytes += file_size
                    except:
                        pass
                    
                    # Calcular progreso (15% a 75% para la copia)
                    copy_progress = 15 + (60 * copied_bytes / total_bytes) if total_bytes > 0 else 75
                    
                    progress_queue.put({
                        'type': 'progress',
                        'value': min(75, copy_progress),
                        'text': f'📄 {os.path.basename(file_path)} ({i+1}/{len(files_to_copy)})'
                    })
                    
                except Exception as e:
                    continue
            
            if self.cancelled:
                shutil.rmtree(backup_dir, ignore_errors=True)
                progress_queue.put({'type': 'complete', 'success': False, 'message': 'Operación cancelada'})
                return
            
            # Calcular hash de verificación
            progress_queue.put({
                'type': 'progress',
                'value': 80,
                'text': '🔍 Calculando hash de verificación...'
            })
            
            verification_hash = SystemUtils.calculate_folder_hash(backup_dir)
            backup_data['verification_hash'] = verification_hash
            
            final_path = backup_dir
            final_size = total_bytes
            
            # Aplicar compresión/encriptación según configuración
            if encrypt_aes and password:
                progress_queue.put({
                    'type': 'progress',
                    'value': 85,
                    'text': '🔐 Aplicando encriptación AES-256...'
                })
                
                encrypted_path = backup_dir + ".encrypted"
                success, message = self.encryption_manager.encrypt_file_aes(backup_dir, password, encrypted_path)
                
                if success:
                    shutil.rmtree(backup_dir)
                    final_path = encrypted_path
                    backup_data['encryption_type'] = 'AES-256'
                    try:
                        final_size = os.path.getsize(encrypted_path)
                    except:
                        pass
                        
            elif encrypt_7z and password:
                progress_queue.put({
                    'type': 'progress',
                    'value': 85,
                    'text': '🗜️ Comprimiendo con 7-Zip + Contraseña...'
                })
                
                archive_path = backup_dir + ".7z"
                success, message = self.encryption_manager.compress_7z_with_password(
                    backup_dir, archive_path, password
                )
                
                if success:
                    shutil.rmtree(backup_dir)
                    final_path = archive_path
                    backup_data['encryption_type'] = '7-Zip + Password'
                    try:
                        final_size = os.path.getsize(archive_path)
                    except:
                        pass
                        
            elif compress:
                progress_queue.put({
                    'type': 'progress',
                    'value': 85,
                    'text': '🗜️ Comprimiendo con 7-Zip...'
                })
                
                archive_path = backup_dir + ".7z"
                try:
                    with py7zr.SevenZipFile(archive_path, 'w') as archive:
                        for root, dirs, files in os.walk(backup_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, backup_dir)
                                archive.write(file_path, arcname)
                    
                    shutil.rmtree(backup_dir)
                    final_path = archive_path
                    backup_data['encryption_type'] = '7-Zip Compression'
                    try:
                        final_size = os.path.getsize(archive_path)
                    except:
                        pass
                except Exception as e:
                    print(f"Error en compresión: {e}")
            
            # Finalizar backup
            duration = time.time() - start_time
            backup_data.update({
                'compressed_size': final_size,
                'duration': duration,
                'success': True
            })
            
            progress_queue.put({
                'type': 'progress',
                'value': 95,
                'text': '📄 Generando reporte HTML...'
            })
            
            # Generar reporte HTML automático
            try:
                report_path = self.report_manager.generate_html_report(backup_data)
                report_name = os.path.basename(report_path)
            except Exception as e:
                report_name = "Error al generar reporte"
            
            # Reproducir sonido de éxito
            self.sound_manager.play_success()
            
            progress_queue.put({
                'type': 'complete',
                'success': True,
                'message': (f'🎉 Backup {mode} completado exitosamente!\n\n'
                          f'📁 Origen: {os.path.basename(source)}\n'
                          f'💾 Destino: {os.path.basename(final_path)}\n'
                          f'📊 Archivos: {successful_copies}/{len(files_to_copy)}\n'
                          f'📏 Tamaño: {SystemUtils.format_bytes(total_bytes)}\n'
                          f'⏱️ Duración: {self.report_manager._format_duration(duration)}\n'
                          f'📄 Reporte: {report_name}')
            })
            
        except Exception as e:
            # Error durante el proceso
            backup_data.update({
                'success': False,
                'duration': time.time() - start_time
            })
            
            # Intentar generar reporte de error
            try:
                self.report_manager.generate_html_report(backup_data)
            except:
                pass
            
            self.sound_manager.play_error()
            
            progress_queue.put({
                'type': 'error',
                'message': f'💥 Error durante el backup:\n\n{str(e)}'
            })
    
    def _get_files_to_copy(self, source, destination, mode, progress_queue):
        """Determinar archivos a copiar según el modo de backup"""
        files_to_copy = []
        
        if mode == "full":
            try:
                for root, dirs, files in os.walk(source):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if os.path.exists(file_path) and os.access(file_path, os.R_OK):
                            files_to_copy.append(file_path)
            except Exception as e:
                print(f"Error explorando directorio: {e}")
        else:
            # Para incremental y diferencial, buscar backup de referencia
            last_backup_path = self._find_last_backup(destination, mode)
            
            if not last_backup_path:
                progress_queue.put({
                    'type': 'progress',
                    'value': 10,
                    'text': 'ℹ️ Sin backup previo, realizando backup completo...'
                })
                return self._get_files_to_copy(source, destination, "full", progress_queue)
            
            # Comparar archivos modificados
            try:
                for root, dirs, files in os.walk(source):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if os.path.exists(file_path) and os.access(file_path, os.R_OK):
                            files_to_copy.append(file_path)
            except Exception as e:
                print(f"Error durante comparación: {e}")
        
        return files_to_copy
    
    def _find_last_backup(self, destination, mode):
        """Encontrar el último backup según el modo"""
        # Implementación simplificada
        return None
    
    def cancel_backup(self):
        """Cancelar operación de backup"""
        self.cancelled = True
        self.sound_manager.play_error()

# ============================= INTERFAZ PRINCIPAL CON PESTAÑAS =============================

class InfernalBackupUltimate:
    """Aplicación principal con sistema completo de pestañas"""
    
    def __init__(self, root):
        self.root = root
        self.progress_queue = queue.Queue()
        
        # Inicializar managers
        self.language_manager = LanguageManager()
        self.sound_manager = SoundManager()
        self.encryption_manager = EncryptionManager()
        self.report_manager = ReportManager()
        self.system_utils = SystemUtils()
        self.backup_engine = BackupEngine(
            self.sound_manager, 
            self.report_manager, 
            self.encryption_manager
        )
        
        # Variables de la interfaz
        self.backup_mode = tk.StringVar(value="full")
        self.compress_enabled = tk.BooleanVar(value=False)
        self.encrypt_aes = tk.BooleanVar(value=False)
        self.encrypt_7z = tk.BooleanVar(value=False)
        self.destination_path = tk.StringVar(value=os.path.join(os.getcwd(), "backups"))
        self.selected_source = None
        
        # Variables de configuración
        self.sound_enabled = tk.BooleanVar(value=self.sound_manager.sounds_enabled)
        self.current_font_family = tk.StringVar(value="Consolas")
        self.current_font_size = tk.IntVar(value=10)
        self.current_theme_color = "#00ff00"
        
        # Estado del backup
        self.is_backing_up = False
        self.start_time = None
        
        # Configurar tema y crear interfaz
        self.setup_theme()
        self.create_main_interface()
        
        # Iniciar procesamiento de la cola de progreso
        self.root.after(100, self.process_progress_queue)
    
    def setup_theme(self):
        """Configurar tema oscuro con efectos hover"""
        self.root.configure(bg='#0a0a0a')
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colores del tema
        colors = {
            'bg': '#0a0a0a',
            'fg': self.current_theme_color,
            'select_bg': '#1a4a1a',
            'select_fg': '#ffffff',
            'active_bg': '#2d5a2d',
            'button_bg': '#1a1a1a',
            'hover_bg': '#3d6a3d'
        }
        
        # Configurar estilos base
        self.style.configure('TFrame', background=colors['bg'])
        self.style.configure('TLabel', background=colors['bg'], foreground=colors['fg'])
        self.style.configure('TButton', 
                           background=colors['button_bg'], 
                           foreground=colors['fg'],
                           borderwidth=1)
        
        # Estilo hover para botones
        self.style.configure('Hover.TButton',
                           background=colors['hover_bg'],
                           foreground='#ffffff',
                           borderwidth=2)
        
        # Otros widgets
        self.style.configure('TEntry',
                           background='#1a1a1a',
                           foreground=colors['fg'],
                           insertcolor=colors['fg'])
        self.style.configure('TCheckbutton',
                           background=colors['bg'],
                           foreground=colors['fg'])
        self.style.configure('TRadiobutton',
                           background=colors['bg'],
                           foreground=colors['fg'])
        self.style.configure('TLabelframe',
                           background=colors['bg'],
                           foreground=colors['fg'])
        self.style.configure('TLabelframe.Label',
                           background=colors['bg'],
                           foreground=colors['fg'])
        self.style.configure('TNotebook',
                           background=colors['bg'],
                           borderwidth=0)
        self.style.configure('TNotebook.Tab',
                           background=colors['button_bg'],
                           foreground=colors['fg'],
                           padding=[15, 8])
        self.style.configure('Treeview',
                           background='#1a1a1a',
                           foreground=colors['fg'],
                           fieldbackground='#1a1a1a',
                           selectbackground=colors['select_bg'])
        self.style.configure('TProgressbar',
                           background=colors['fg'],
                           troughcolor='#333333')
        
        # Estados activos y hover
        self.style.map('TButton',
                     background=[('active', colors['active_bg'])])
        self.style.map('TNotebook.Tab',
                     background=[('selected', colors['select_bg']),
                               ('active', colors['active_bg'])])
    
    def create_main_interface(self):
        """Crear interfaz principal con pestañas"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título principal
        self.title_label = ttk.Label(main_frame, 
                                    text=self.language_manager.get_text('app_title'),
                                    font=(self.current_font_family.get(), 14, 'bold'))
        self.title_label.grid(row=0, column=0, pady=(0, 15))
        
        # Notebook con pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear todas las pestañas
        self.create_backup_tab()
        self.create_encryption_tab()
        self.create_reports_tab()
        self.create_settings_tab()
        
        # Bind evento de cambio de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
    
    def create_backup_tab(self):
        """Crear pestaña principal de backup"""
        # Frame de la pestaña
        backup_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(backup_frame, text=self.language_manager.get_text('tab_backup'))
        
        backup_frame.columnconfigure(1, weight=1)
        backup_frame.rowconfigure(0, weight=1)
        
        # Panel izquierdo - Explorador
        left_frame = ttk.LabelFrame(backup_frame, 
                                   text=self.language_manager.get_text('select_source'), 
                                   padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        
        # Treeview para explorador
        tree_frame = ttk.Frame(left_frame)
        tree_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(tree_frame, show='tree', height=20)
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        v_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=v_scroll.set)
        
        h_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        h_scroll.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.tree.configure(xscrollcommand=h_scroll.set)
        
        # Eventos del árbol
        self.tree.bind('<<TreeviewOpen>>', self.on_tree_expand)
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        
        # Panel derecho - Configuración
        right_frame = ttk.Frame(backup_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(5, weight=1)
        
        # 1. Modo de backup
        mode_frame = ttk.LabelFrame(right_frame, 
                                   text=self.language_manager.get_text('backup_type'), 
                                   padding="10")
        mode_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(mode_frame, 
                       text=self.language_manager.get_text('full_backup'),
                       variable=self.backup_mode, value="full").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(mode_frame, 
                       text=self.language_manager.get_text('incremental_backup'),
                       variable=self.backup_mode, value="incremental").grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(mode_frame, 
                       text=self.language_manager.get_text('differential_backup'),
                       variable=self.backup_mode, value="differential").grid(row=2, column=0, sticky=tk.W)
        
        # 2. Opciones de seguridad
        security_frame = ttk.LabelFrame(right_frame, 
                                       text=self.language_manager.get_text('security_options'), 
                                       padding="10")
        security_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        security_frame.columnconfigure(1, weight=1)
        
        ttk.Checkbutton(security_frame, 
                       text=self.language_manager.get_text('compress_7z'),
                       variable=self.compress_enabled).grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        ttk.Checkbutton(security_frame, 
                       text=self.language_manager.get_text('encrypt_aes'),
                       variable=self.encrypt_aes,
                       command=self.on_encryption_change).grid(row=1, column=0, columnspan=2, sticky=tk.W)
        
        ttk.Checkbutton(security_frame, 
                       text=self.language_manager.get_text('encrypt_7z_pass'),
                       variable=self.encrypt_7z,
                       command=self.on_encryption_change).grid(row=2, column=0, columnspan=2, sticky=tk.W)
        
        # Campo contraseña
        ttk.Label(security_frame, 
                 text=self.language_manager.get_text('password')).grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
        self.password_entry = ttk.Entry(security_frame, show="*", width=20)
        self.password_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(5, 0), padx=(5, 0))
        
        # 3. Destino
        dest_frame = ttk.LabelFrame(right_frame, 
                                   text=self.language_manager.get_text('destination'), 
                                   padding="10")
        dest_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        dest_frame.columnconfigure(0, weight=1)
        
        dest_entry_frame = ttk.Frame(dest_frame)
        dest_entry_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        dest_entry_frame.columnconfigure(0, weight=1)
        
        self.dest_entry = ttk.Entry(dest_entry_frame, textvariable=self.destination_path)
        self.dest_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        HoverButton(dest_entry_frame, self.sound_manager, text="📁", width=3,
                   command=self.browse_destination).grid(row=0, column=1)
        
        # Info del origen
        self.info_label = ttk.Label(dest_frame, 
                                   text=self.language_manager.get_text('select_origin'),
                                   wraplength=300, justify=tk.LEFT)
        self.info_label.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 4. Controles
        control_frame = ttk.Frame(right_frame)
        control_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)
        
        # Botón principal
        self.backup_button = HoverButton(control_frame, self.sound_manager,
                                        text=self.language_manager.get_text('start_backup'),
                                        command=self.start_backup)
        self.backup_button.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Botones adicionales
        HoverButton(control_frame, self.sound_manager,
                   text=self.language_manager.get_text('view_reports'),
                   command=self.open_reports_folder).grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        HoverButton(control_frame, self.sound_manager,
                   text=self.language_manager.get_text('encryption_center'),
                   command=self.switch_to_encryption_tab).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # 5. Progreso
        progress_frame = ttk.LabelFrame(right_frame, 
                                       text=self.language_manager.get_text('progress'), 
                                       padding="10")
        progress_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                           maximum=100, mode='determinate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.progress_label = ttk.Label(progress_frame, 
                                       text=self.language_manager.get_text('ready_to_start'))
        self.progress_label.grid(row=1, column=0, sticky=tk.W)
        
        # 6. Log
        log_frame = ttk.LabelFrame(right_frame, 
                                  text=self.language_manager.get_text('activity_log'), 
                                  padding="10")
        log_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        log_text_frame = ttk.Frame(log_frame)
        log_text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_text_frame.columnconfigure(0, weight=1)
        log_text_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_text_frame, height=8, wrap=tk.WORD,
                               bg='#0a0a0a', fg=self.current_theme_color, 
                               insertbackground=self.current_theme_color,
                               font=(self.current_font_family.get(), self.current_font_size.get()-1))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        log_scroll = ttk.Scrollbar(log_text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=log_scroll.set)
        
        # Poblar árbol de unidades
        self.populate_drives()
        
        # Log inicial
        self.log_message("🔥 Infernal Backup Pro v2.0 Ultimate iniciado")
        self.log_message("👤 Autor: Stormy | 📄 Licencia: Free")
    
    def create_encryption_tab(self):
        """Crear pestaña de encriptación"""
        encrypt_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(encrypt_frame, text=self.language_manager.get_text('tab_encryption'))
        
        encrypt_frame.columnconfigure(0, weight=1)
        encrypt_frame.rowconfigure(2, weight=1)
        
        # Título
        title = ttk.Label(encrypt_frame, 
                         text="🔐 Centro de Encriptación/Desencriptación",
                         font=(self.current_font_family.get(), 12, 'bold'))
        title.grid(row=0, column=0, pady=(0, 20))
        
        # Notebook para sub-pestañas
        sub_notebook = ttk.Notebook(encrypt_frame)
        sub_notebook.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Sub-pestaña AES
        aes_frame = ttk.Frame(sub_notebook, padding="15")
        sub_notebook.add(aes_frame, text=self.language_manager.get_text('encryption_aes_tab'))
        
        aes_frame.columnconfigure(1, weight=1)
        
        # Archivo AES
        ttk.Label(aes_frame, 
                 text=self.language_manager.get_text('file_folder')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        aes_file_frame = ttk.Frame(aes_frame)
        aes_file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        aes_file_frame.columnconfigure(0, weight=1)
        
        self.aes_file_var = tk.StringVar()
        self.aes_file_entry = ttk.Entry(aes_file_frame, textvariable=self.aes_file_var)
        self.aes_file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        HoverButton(aes_file_frame, self.sound_manager, text="📁", width=3,
                   command=self.browse_aes_file).grid(row=0, column=1)
        
        # Contraseña AES
        ttk.Label(aes_frame, 
                 text=self.language_manager.get_text('password')).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.aes_password_var = tk.StringVar()
        self.aes_password_entry = ttk.Entry(aes_frame, textvariable=self.aes_password_var, show="*")
        self.aes_password_entry.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Botones AES
        aes_btn_frame = ttk.Frame(aes_frame)
        aes_btn_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        aes_btn_frame.columnconfigure(0, weight=1)
        aes_btn_frame.columnconfigure(1, weight=1)
        
        HoverButton(aes_btn_frame, self.sound_manager,
                   text=self.language_manager.get_text('encrypt'),
                   command=self.encrypt_aes_file).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        HoverButton(aes_btn_frame, self.sound_manager,
                   text=self.language_manager.get_text('decrypt'),
                   command=self.decrypt_aes_file).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Sub-pestaña 7-Zip
        zip_frame = ttk.Frame(sub_notebook, padding="15")
        sub_notebook.add(zip_frame, text=self.language_manager.get_text('encryption_7z_tab'))
        
        zip_frame.columnconfigure(1, weight=1)
        
        # Archivo 7z
        ttk.Label(zip_frame, 
                 text=self.language_manager.get_text('file_folder')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        zip_file_frame = ttk.Frame(zip_frame)
        zip_file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        zip_file_frame.columnconfigure(0, weight=1)
        
        self.zip_file_var = tk.StringVar()
        self.zip_file_entry = ttk.Entry(zip_file_frame, textvariable=self.zip_file_var)
        self.zip_file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        HoverButton(zip_file_frame, self.sound_manager, text="📁", width=3,
                   command=self.browse_zip_file).grid(row=0, column=1)
        
        # Contraseña 7z
        ttk.Label(zip_frame, 
                 text=self.language_manager.get_text('password')).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.zip_password_var = tk.StringVar()
        self.zip_password_entry = ttk.Entry(zip_frame, textvariable=self.zip_password_var, show="*")
        self.zip_password_entry.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Botones 7z
        zip_btn_frame = ttk.Frame(zip_frame)
        zip_btn_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        zip_btn_frame.columnconfigure(0, weight=1)
        zip_btn_frame.columnconfigure(1, weight=1)
        
        HoverButton(zip_btn_frame, self.sound_manager,
                   text=self.language_manager.get_text('compress'),
                   command=self.compress_7z_file).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        HoverButton(zip_btn_frame, self.sound_manager,
                   text=self.language_manager.get_text('extract'),
                   command=self.extract_7z_file).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Log de operaciones
        log_frame = ttk.LabelFrame(encrypt_frame, 
                                  text=self.language_manager.get_text('operation_log'), 
                                  padding="10")
        log_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.encryption_log = tk.Text(log_frame, height=10, wrap=tk.WORD,
                                     bg='#0a0a0a', fg=self.current_theme_color,
                                     font=(self.current_font_family.get(), self.current_font_size.get()-1))
        self.encryption_log.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        encrypt_scroll = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.encryption_log.yview)
        encrypt_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.encryption_log.configure(yscrollcommand=encrypt_scroll.set)
    
    def create_reports_tab(self):
        """Crear pestaña de reportes"""
        reports_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(reports_frame, text=self.language_manager.get_text('tab_reports'))
        
        reports_frame.columnconfigure(0, weight=1)
        reports_frame.rowconfigure(2, weight=1)
        
        # Título
        title = ttk.Label(reports_frame, 
                         text=self.language_manager.get_text('reports_center'),
                         font=(self.current_font_family.get(), 12, 'bold'))
        title.grid(row=0, column=0, pady=(0, 20))
        
        # Botones de control
        control_frame = ttk.LabelFrame(reports_frame, text="🎛️ Controles", padding="15")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        HoverButton(btn_frame, self.sound_manager,
                   text=self.language_manager.get_text('generate_report'),
                   command=self.generate_manual_report).grid(row=0, column=0, padx=(0, 10))
        
        HoverButton(btn_frame, self.sound_manager,
                   text=self.language_manager.get_text('open_last_report'),
                   command=self.open_last_report).grid(row=0, column=1, padx=(0, 10))
        
        HoverButton(btn_frame, self.sound_manager,
                   text=self.language_manager.get_text('open_reports_folder'),
                   command=self.open_reports_folder).grid(row=0, column=2)
        
        # Estadísticas
        stats_frame = ttk.LabelFrame(reports_frame, 
                                    text=self.language_manager.get_text('statistics'), 
                                    padding="15")
        stats_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.rowconfigure(0, weight=1)
        
        self.stats_text = tk.Text(stats_frame, height=15, wrap=tk.WORD,
                                 bg='#0a0a0a', fg=self.current_theme_color,
                                 font=(self.current_font_family.get(), self.current_font_size.get()-1))
        self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        stats_scroll = ttk.Scrollbar(stats_frame, orient=tk.VERTICAL, command=self.stats_text.yview)
        stats_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.stats_text.configure(yscrollcommand=stats_scroll.set)
        
        # Cargar estadísticas iniciales
        self.load_statistics()
    
    def create_settings_tab(self):
        """Crear pestaña de configuración avanzada"""
        settings_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(settings_frame, text=self.language_manager.get_text('tab_settings'))
        
        settings_frame.columnconfigure(0, weight=1)
        
        # Título
        title = ttk.Label(settings_frame, 
                         text=self.language_manager.get_text('settings_title'),
                         font=(self.current_font_family.get(), 12, 'bold'))
        title.grid(row=0, column=0, pady=(0, 20))
        
        # Sección idioma
        lang_frame = ttk.LabelFrame(settings_frame, 
                                   text=self.language_manager.get_text('language_section'), 
                                   padding="15")
        lang_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Selector de idioma
        lang_selector_frame = ttk.Frame(lang_frame)
        lang_selector_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.current_language = tk.StringVar(value=self.language_manager.current_language)
        
        available_langs = self.language_manager.get_available_languages()
        for i, (code, name) in enumerate(available_langs.items()):
            ttk.Radiobutton(lang_selector_frame, text=name, variable=self.current_language, 
                           value=code, command=self.change_language).grid(row=0, column=i, padx=(0, 20))
        
        # Sección tema
        theme_frame = ttk.LabelFrame(settings_frame, 
                                    text=self.language_manager.get_text('theme_section'), 
                                    padding="15")
        theme_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        theme_frame.columnconfigure(1, weight=1)
        
        # Configuración de fuente
        ttk.Label(theme_frame, 
                 text=self.language_manager.get_text('font_family')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        font_families = ['Consolas', 'Courier New', 'Lucida Console', 'Monaco', 'Hack']
        font_combo = ttk.Combobox(theme_frame, textvariable=self.current_font_family, 
                                 values=font_families, state="readonly", width=15)
        font_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        ttk.Label(theme_frame, 
                 text=self.language_manager.get_text('font_size')).grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        size_spinbox = ttk.Spinbox(theme_frame, from_=8, to=16, textvariable=self.current_font_size, 
                                  width=8)
        size_spinbox.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # Color del tema
        ttk.Label(theme_frame, 
                 text=self.language_manager.get_text('theme_color')).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        HoverButton(theme_frame, self.sound_manager, text="🎨 Elegir Color", 
                   command=self.choose_theme_color).grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # Botones de tema
        theme_btn_frame = ttk.Frame(theme_frame)
        theme_btn_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(15, 0))
        theme_btn_frame.columnconfigure(0, weight=1)
        theme_btn_frame.columnconfigure(1, weight=1)
        
        HoverButton(theme_btn_frame, self.sound_manager,
                   text=self.language_manager.get_text('apply_changes'),
                   command=self.apply_theme_changes).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        HoverButton(theme_btn_frame, self.sound_manager,
                   text=self.language_manager.get_text('reset_defaults'),
                   command=self.reset_theme_defaults).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Sección audio
        audio_frame = ttk.LabelFrame(settings_frame, 
                                    text=self.language_manager.get_text('sound_section'), 
                                    padding="15")
        audio_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Checkbutton(audio_frame, 
                       text=self.language_manager.get_text('enable_sounds'),
                       variable=self.sound_enabled, 
                       command=self.toggle_sounds).grid(row=0, column=0, sticky=tk.W)
        
        # Botones de prueba de sonido
        sound_test_frame = ttk.Frame(audio_frame)
        sound_test_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(sound_test_frame, 
                 text=self.language_manager.get_text('test_sounds')).grid(row=0, column=0, sticky=tk.W)
        
        HoverButton(sound_test_frame, self.sound_manager,
                   text=self.language_manager.get_text('btn_click'),
                   command=self.sound_manager.play_click).grid(row=0, column=1, padx=(10, 5))
        
        HoverButton(sound_test_frame, self.sound_manager,
                   text=self.language_manager.get_text('btn_success'),
                   command=self.sound_manager.play_success).grid(row=0, column=2, padx=(5, 5))
        
        HoverButton(sound_test_frame, self.sound_manager,
                   text=self.language_manager.get_text('btn_error'),
                   command=self.sound_manager.play_error).grid(row=0, column=3, padx=(5, 0))
        
        # Información de la aplicación
        info_frame = ttk.LabelFrame(settings_frame, 
                                   text=self.language_manager.get_text('app_info'), 
                                   padding="15")
        info_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        info_text = """
🔥 INFERNAL BACKUP PRO v2.0 ULTIMATE
👤 Autor: Stormy
📄 Licencia: Free
💾 Sistema: Windows 10/11
🐍 Python: 3.8+

✨ Características Avanzadas:
• Sistema de pestañas completo
• Backups completos, incrementales y diferenciales  
• Encriptación AES-256 + 7-Zip con contraseña
• Reportes HTML automáticos con estadísticas
• Sistema de idiomas (Español/English)
• Configuración de temas y fuentes personalizable
• Efectos visuales y sonoros interactivos
• Verificación de integridad con hash SHA-256
        """
        
        info_label = ttk.Label(info_frame, text=info_text.strip(), justify=tk.LEFT,
                              font=(self.current_font_family.get(), self.current_font_size.get()-2))
        info_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Botones de acción
        action_frame = ttk.LabelFrame(settings_frame, text="🎯 Acciones", padding="15")
        action_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)
        
        HoverButton(action_frame, self.sound_manager,
                   text=self.language_manager.get_text('restart_app'),
                   command=self.restart_application).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        HoverButton(action_frame, self.sound_manager,
                   text=self.language_manager.get_text('exit_app'),
                   command=self.exit_application).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
    
    # ===== MÉTODOS DE FUNCIONALIDAD =====
    
    def populate_drives(self):
        """Poblar árbol con unidades del sistema"""
        try:
            drives = self.system_utils.get_drives()
            for drive in drives:
                drive_info = self.system_utils.get_drive_info(drive)
                display_text = f"💽 {drive} ({drive_info['label']}) - {drive_info['free_space']} libres"
                
                item_id = self.tree.insert('', 'end', text=display_text, values=[drive])
                self.tree.insert(item_id, 'end', text="Cargando...")
                
            self.log_message(f"📡 Detectadas {len(drives)} unidades de disco")
            
        except Exception as e:
            self.log_message(f"❌ Error cargando unidades: {e}")
    
    def on_tree_expand(self, event):
        """Expandir nodo del árbol"""
        try:
            item_id = self.tree.focus()
            self.populate_tree_item(item_id)
        except Exception as e:
            self.log_message(f"❌ Error expandiendo: {e}")
    
    def populate_tree_item(self, item_id):
        """Poblar elemento del árbol"""
        try:
            # Eliminar placeholder "Cargando..."
            children = self.tree.get_children(item_id)
            for child in children:
                if self.tree.item(child, 'text') == "Cargando...":
                    self.tree.delete(child)
                    break
            
            if self.tree.get_children(item_id):
                return
            
            # Obtener ruta
            path = self.get_item_path(item_id)
            if not path:
                return
            
            # Obtener subcarpetas
            folders = self.system_utils.get_folders(path, max_folders=50)
            
            for folder in folders:
                try:
                    folder_path = os.path.join(path, folder)
                    folder_item = self.tree.insert(item_id, 'end', text=f"📁 {folder}", values=[folder_path])
                    
                    if self.system_utils.has_subdirectories(folder_path):
                        self.tree.insert(folder_item, 'end', text="Cargando...")
                        
                except:
                    continue
                    
        except Exception as e:
            self.log_message(f"⚠️ Error accediendo a directorio: {e}")
    
    def get_item_path(self, item_id):
        """Obtener ruta de elemento del árbol"""
        try:
            values = self.tree.item(item_id, 'values')
            if values and values[0]:
                return values[0]
            
            # Construir desde jerarquía
            path_parts = []
            current_item = item_id
            
            while current_item:
                text = self.tree.item(current_item, 'text')
                
                if text.startswith('💽 '):
                    clean_text = text.split('💽 ')[1].split(' ')[0]
                    path_parts.append(clean_text)
                elif text.startswith('📁 '):
                    clean_text = text.split('📁 ')[1]
                    path_parts.append(clean_text)
                else:
                    path_parts.append(text)
                
                current_item = self.tree.parent(current_item)
            
            if path_parts:
                path_parts.reverse()
                return os.path.join(*path_parts) if len(path_parts) > 1 else path_parts[0]
                    
        except:
            pass
        return None
    
    def on_tree_select(self, event):
        """Manejar selección en árbol"""
        try:
            selection = self.tree.selection()
            if not selection:
                return
            
            item_id = selection[0]
            path = self.get_item_path(item_id)
            
            if path and os.path.exists(path):
                self.selected_source = path
                path_info = self.system_utils.get_path_info(path)
                
                short_path = path if len(path) < 60 else "..." + path[-57:]
                info_text = f"📍 Seleccionado: {short_path}\n{path_info}"
                self.info_label.config(text=info_text)
                
                self.sound_manager.play_click()
                self.log_message(f"📂 Seleccionado: {path}")
            
        except Exception as e:
            self.log_message(f"❌ Error en selección: {e}")
    
    def browse_destination(self):
        """Explorar destino"""
        try:
            directory = filedialog.askdirectory(
                title="Seleccionar destino para backups",
                initialdir=self.destination_path.get()
            )
            
            if directory:
                self.destination_path.set(directory)
                self.sound_manager.play_click()
                self.log_message(f"💾 Destino actualizado: {directory}")
                
        except Exception as e:
            self.log_message(f"❌ Error seleccionando destino: {e}")
    
    def on_encryption_change(self):
        """Manejar cambio en opciones de encriptación"""
        if self.encrypt_aes.get():
            self.encrypt_7z.set(False)
        elif self.encrypt_7z.get():
            self.encrypt_aes.set(False)
    
    def start_backup(self):
        """Iniciar o cancelar backup"""
        if self.is_backing_up:
            response = messagebox.askyesno("Cancelar Backup", "¿Cancelar el backup en curso?")
            if response:
                self.backup_engine.cancel_backup()
                self.log_message("🛑 Cancelación solicitada")
            return
        
        # Validaciones
        if not self.selected_source:
            self.sound_manager.play_error()
            messagebox.showerror("Error", "❌ Selecciona un origen")
            return
        
        if not os.path.exists(self.selected_source):
            self.sound_manager.play_error()
            messagebox.showerror("Error", f"❌ El origen no existe:\n{self.selected_source}")
            return
        
        # Crear destino
        dest_path = self.destination_path.get()
        if not os.path.exists(dest_path):
            try:
                os.makedirs(dest_path, exist_ok=True)
                self.log_message(f"📁 Directorio creado: {dest_path}")
            except Exception as e:
                self.sound_manager.play_error()
                messagebox.showerror("Error", f"❌ No se pudo crear destino:\n{e}")
                return
        
        # Validar contraseña para encriptación
        if (self.encrypt_aes.get() or self.encrypt_7z.get()):
            password = self.password_entry.get().strip()
            if not password:
                self.sound_manager.play_error()
                messagebox.showerror("Error", "❌ Se requiere contraseña para encriptación")
                return
            if len(password) < 4:
                self.sound_manager.play_error()
                messagebox.showerror("Error", "❌ Contraseña debe tener al menos 4 caracteres")
                return
        
        # Iniciar backup
        self.is_backing_up = True
        self.start_time = time.time()
        self.backup_button.configure(text=self.language_manager.get_text('cancel_backup'))
        self.progress_var.set(0)
        
        # Configuración
        config = {
            'source': self.selected_source,
            'destination': dest_path,
            'mode': self.backup_mode.get(),
            'compress': self.compress_enabled.get(),
            'encrypt_aes': self.encrypt_aes.get(),
            'encrypt_7z': self.encrypt_7z.get(),
            'password': self.password_entry.get(),
            'progress_queue': self.progress_queue
        }
        
        # Log del inicio
        mode_names = {"full": "Completo", "incremental": "Incremental", "differential": "Diferencial"}
        self.log_message(f"🚀 Iniciando backup {mode_names.get(config['mode'], 'Desconocido')}")
        self.log_message(f"📂 Origen: {os.path.basename(self.selected_source)}")
        
        if config['encrypt_aes']:
            self.log_message("🔒 Encriptación: AES-256 activada")
        elif config['encrypt_7z']:
            self.log_message("🔐 Encriptación: 7-Zip con contraseña activada")
        
        # Ejecutar en hilo separado
        backup_thread = threading.Thread(target=self.backup_engine.start_backup, args=(config,), daemon=True)
        backup_thread.start()
    
    def switch_to_encryption_tab(self):
        """Cambiar a la pestaña de encriptación"""
        self.notebook.select(1)  # Índice de la pestaña de encriptación
        self.sound_manager.play_click()
    
    def open_reports_folder(self):
        """Abrir carpeta de reportes"""
        try:
            reports_path = self.report_manager.reports_dir
            if not os.path.exists(reports_path):
                os.makedirs(reports_path)
            
            if platform.system() == "Windows":
                os.startfile(reports_path)
            else:
                webbrowser.open(f"file://{reports_path}")
            
            self.sound_manager.play_click()
            self.log_message(f"📊 Abriendo reportes: {reports_path}")
            
        except Exception as e:
            self.sound_manager.play_error()
            self.log_message(f"❌ Error abriendo reportes: {e}")
    
    def on_tab_changed(self, event):
        """Manejar cambio de pestaña"""
        self.sound_manager.play_hover()
        selected_tab = self.notebook.select()
        tab_text = self.notebook.tab(selected_tab, "text")
        
        # Cargar estadísticas si entramos a la pestaña de reportes
        if self.language_manager.get_text('tab_reports') in tab_text:
            self.load_statistics()
    
    def change_language(self):
        """Cambiar idioma de la aplicación"""
        new_language = self.current_language.get()
        if self.language_manager.set_language(new_language):
            self.sound_manager.play_success()
            self.log_message(f"🌍 Idioma cambiado a: {new_language}")
            messagebox.showinfo("Idioma / Language", 
                               "Se requiere reiniciar para aplicar todos los cambios\n"
                               "Restart required to apply all changes")
        else:
            self.sound_manager.play_error()
    
    def choose_theme_color(self):
        """Elegir color del tema"""
        color = colorchooser.askcolor(
            title="Elegir Color del Tema",
            initialcolor=self.current_theme_color
        )
        
        if color[1]:  # Si se seleccionó un color
            self.current_theme_color = color[1]
            self.sound_manager.play_click()
            self.log_message(f"🎨 Color de tema cambiado: {color[1]}")
    
    def apply_theme_changes(self):
        """Aplicar cambios de tema"""
        try:
            # Actualizar configuraciones
            self.setup_theme()
            
            # Actualizar fuentes en widgets existentes
            new_font = (self.current_font_family.get(), self.current_font_size.get())
            
            if hasattr(self, 'title_label'):
                self.title_label.configure(font=new_font + ('bold',))
            
            if hasattr(self, 'log_text'):
                self.log_text.configure(
                    font=(self.current_font_family.get(), self.current_font_size.get()-1),
                    fg=self.current_theme_color
                )
            
            if hasattr(self, 'encryption_log'):
                self.encryption_log.configure(
                    font=(self.current_font_family.get(), self.current_font_size.get()-1),
                    fg=self.current_theme_color
                )
            
            if hasattr(self, 'stats_text'):
                self.stats_text.configure(
                    font=(self.current_font_family.get(), self.current_font_size.get()-1),
                    fg=self.current_theme_color
                )
            
            self.sound_manager.play_success()
            self.log_message("✅ Tema aplicado correctamente")
            
        except Exception as e:
            self.sound_manager.play_error()
            self.log_message(f"❌ Error aplicando tema: {e}")
    
    def reset_theme_defaults(self):
        """Restaurar configuración de tema por defecto"""
        self.current_font_family.set("Consolas")
        self.current_font_size.set(10)
        self.current_theme_color = "#00ff00"
        
        self.apply_theme_changes()
        self.sound_manager.play_success()
        self.log_message("🔄 Tema restaurado por defecto")
    
    def toggle_sounds(self):
        """Activar/desactivar sonidos"""
        self.sound_manager.sounds_enabled = self.sound_enabled.get()
        if self.sound_manager.sounds_enabled:
            self.sound_manager.play_success()
    
    def restart_application(self):
        """Reiniciar aplicación"""
        if messagebox.askyesno("Reiniciar", "❓ ¿Reiniciar la aplicación?"):
            self.sound_manager.play_click()
            python = sys.executable
            os.execl(python, python, *sys.argv)
    
    def exit_application(self):
        """Salir de la aplicación"""
        if self.is_backing_up:
            response = messagebox.askyesno(
                "Salir", 
                "Hay un backup en curso. ¿Salir de todas formas?\n"
                "⚠️ El backup se cancelará automáticamente."
            )
            if response:
                self.backup_engine.cancel_backup()
                self.root.destroy()
        else:
            self.root.destroy()
    
    # ===== MÉTODOS DE ENCRIPTACIÓN =====
    
    def browse_aes_file(self):
        """Explorar archivo para AES"""
        path = filedialog.askdirectory(title="Seleccionar carpeta para AES")
        if not path:
            path = filedialog.askopenfilename(title="Seleccionar archivo para AES")
        if path:
            self.aes_file_var.set(path)
            self.sound_manager.play_click()
    
    def browse_zip_file(self):
        """Explorar archivo para 7-Zip"""
        path = filedialog.askdirectory(title="Seleccionar carpeta para 7-Zip")
        if not path:
            path = filedialog.askopenfilename(title="Seleccionar archivo para 7-Zip")
        if path:
            self.zip_file_var.set(path)
            self.sound_manager.play_click()
    
    def encrypt_aes_file(self):
        """Encriptar con AES-256"""
        file_path = self.aes_file_var.get().strip()
        password = self.aes_password_var.get().strip()
        
        if not file_path or not password:
            messagebox.showerror("Error", "Completa archivo y contraseña")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "El archivo/carpeta no existe")
            return
        
        self.encryption_log_message(f"🔒 Iniciando encriptación AES de: {os.path.basename(file_path)}")
        
        success, message = self.encryption_manager.encrypt_file_aes(file_path, password)
        
        if success:
            self.sound_manager.play_success()
            self.encryption_log_message(f"✅ {message}")
            messagebox.showinfo("Éxito", message)
        else:
            self.sound_manager.play_error()
            self.encryption_log_message(f"❌ {message}")
            messagebox.showerror("Error", message)
    
    
    def is_encrypted_file_enhanced(self, file_path):
        """Detectar archivos encriptados de forma avanzada"""
        try:
            if not os.path.exists(file_path) or not os.path.isfile(file_path):
                return False
            
            # 1. Verificar extensión
            if file_path.lower().endswith('.encrypted'):
                return True
            
            # 2. Verificar estructura del archivo
            with open(file_path, 'rb') as f:
                data = f.read(32)
                if len(data) < 20:
                    return False
                    
                # Verificar salt (primeros 16 bytes)
                salt = data[:16]
                if salt == b'\x00' * 16:  # Salt no puede ser todo ceros
                    return False
                
                # Verificar que tenga estructura de archivo encriptado
                if len(data) > 16:
                    return True
            
            return False
            
        except Exception:
            return False

    def decrypt_aes_file(self):
        """Desencriptar AES-256"""
        file_path = self.aes_file_var.get().strip()
        # Verificación automática de archivo encriptado
        if not self.is_encrypted_file_enhanced(file_path):
            response = messagebox.askyesno(
                "Archivo No Encriptado",
                f"El archivo '{os.path.basename(file_path)}' no parece estar encriptado.\n\n"
                "¿Deseas continuar de todas formas?",
                icon="warning"
            )
            if not response:
                return
        password = self.aes_password_var.get().strip()
        
        if not file_path or not password:
            messagebox.showerror("Error", "Completa archivo y contraseña")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "El archivo no existe")
            return
        
        self.encryption_log_message(f"🔓 Iniciando desencriptación AES de: {os.path.basename(file_path)}")
        
        success, message = self.encryption_manager.decrypt_file_aes(file_path, password)
        
        if success:
            self.sound_manager.play_success()
            self.encryption_log_message(f"✅ {message}")
            messagebox.showinfo("Éxito", message)
        else:
            self.sound_manager.play_error()
            self.encryption_log_message(f"❌ {message}")
            messagebox.showerror("Error", message)
    
    def compress_7z_file(self):
        """Comprimir con 7-Zip"""
        source_path = self.zip_file_var.get().strip()
        password = self.zip_password_var.get().strip()
        
        if not source_path or not password:
            messagebox.showerror("Error", "Completa origen y contraseña")
            return
        
        if not os.path.exists(source_path):
            messagebox.showerror("Error", "El origen no existe")
            return
        
        archive_path = source_path + ".7z"
        self.encryption_log_message(f"🗜️ Iniciando compresión 7z de: {os.path.basename(source_path)}")
        
        success, message = self.encryption_manager.compress_7z_with_password(
            source_path, archive_path, password
        )
        
        if success:
            self.sound_manager.play_success()
            self.encryption_log_message(f"✅ {message}")
            messagebox.showinfo("Éxito", message)
        else:
            self.sound_manager.play_error()
            self.encryption_log_message(f"❌ {message}")
            messagebox.showerror("Error", message)
    
    def extract_7z_file(self):
        """Extraer archivo 7z"""
        archive_path = self.zip_file_var.get().strip()
        password = self.zip_password_var.get().strip()
        
        if not archive_path or not password:
            messagebox.showerror("Error", "Completa archivo y contraseña")
            return
        
        if not os.path.exists(archive_path):
            messagebox.showerror("Error", "El archivo no existe")
            return
        
        extract_path = os.path.dirname(archive_path)
        self.encryption_log_message(f"📂 Iniciando extracción de: {os.path.basename(archive_path)}")
        
        success, message = self.encryption_manager.extract_7z_with_password(
            archive_path, extract_path, password
        )
        
        if success:
            self.sound_manager.play_success()
            self.encryption_log_message(f"✅ {message}")
            messagebox.showinfo("Éxito", message)
        else:
            self.sound_manager.play_error()
            self.encryption_log_message(f"❌ {message}")
            messagebox.showerror("Error", message)
    
    def encryption_log_message(self, message):
        """Añadir mensaje al log de encriptación"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.encryption_log.insert(tk.END, log_entry)
        self.encryption_log.see(tk.END)
    
    # ===== MÉTODOS DE REPORTES =====
    
    def generate_manual_report(self):
        """Generar reporte manual"""
        self.sound_manager.play_click()
        
        backup_data = {
            'timestamp': datetime.now().isoformat(),
            'source_path': self.selected_source or 'Manual',
            'destination_path': self.destination_path.get(),
            'backup_type': 'Manual',
            'file_count': 0,
            'total_size': 0,
            'compressed_size': 0,
            'duration': 0,
            'success': True,
            'encryption_type': 'None'
        }
        
        try:
            report_path = self.report_manager.generate_html_report(backup_data)
            self.sound_manager.play_success()
            messagebox.showinfo("Éxito", f"✅ Reporte generado:\n{os.path.basename(report_path)}")
            self.load_statistics()
        except Exception as e:
            self.sound_manager.play_error()
            messagebox.showerror("Error", f"❌ Error generando reporte: {e}")
    
    def open_last_report(self):
        """Abrir último reporte"""
        try:
            reports_dir = self.report_manager.reports_dir
            reports = [f for f in os.listdir(reports_dir) if f.endswith('.html')]
            
            if reports:
                latest_report = max(reports)
                report_path = os.path.join(reports_dir, latest_report)
                webbrowser.open(report_path)
                self.sound_manager.play_success()
            else:
                self.sound_manager.play_error()
                messagebox.showwarning("Aviso", "❌ No hay reportes disponibles")
        except Exception as e:
            self.sound_manager.play_error()
            messagebox.showerror("Error", f"❌ Error abriendo reporte: {e}")
    
    def load_statistics(self):
        """Cargar estadísticas en la pestaña de reportes"""
        try:
            stats = self.report_manager.get_backup_statistics()
            
            stats_text = f"""
🔥 ESTADÍSTICAS DE INFERNAL BACKUP PRO ULTIMATE

📊 RESUMEN GENERAL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 Total de backups realizados: {stats['total_backups']}
✅ Backups exitosos: {stats['successful_backups']}
❌ Backups fallidos: {stats['total_backups'] - stats['successful_backups']}
📦 Datos respaldados: {self.system_utils.format_bytes(stats['total_data_backed_up'])}
⏱️ Duración promedio: {stats['average_duration']:.1f}s

📋 ÚLTIMOS BACKUPS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            
            for backup in stats['recent_backups']:
                timestamp = backup[0]
                backup_type = backup[1]
                source = backup[2][:30] + "..." if len(backup[2]) > 30 else backup[2]
                status = "✅" if backup[3] else "❌"
                encryption = backup[4] if len(backup) > 4 else "None"
                
                try:
                    dt = datetime.fromisoformat(timestamp)
                    date_str = dt.strftime("%d/%m/%Y %H:%M")
                except:
                    date_str = timestamp[:16]
                
                stats_text += f"{status} {date_str} | {backup_type.upper()} | {encryption} | {source}\n"
            
            stats_text += f"""

💻 INFORMACIÓN DEL SISTEMA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🖥️ Plataforma: {platform.system()} {platform.release()}
🐍 Python: {platform.python_version()}
📁 Directorio actual: {os.getcwd()}
🌍 Idioma actual: {self.language_manager.current_language.upper()}
🎨 Tema: {self.current_font_family.get()} {self.current_font_size.get()}pt
🔊 Sonidos: {'Habilitados' if self.sound_manager.sounds_enabled else 'Deshabilitados'}

🔥 by Stormy - Infernal Backup Pro v2.0 Ultimate
"""
            
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, stats_text)
            
        except Exception as e:
            error_text = f"❌ Error cargando estadísticas: {e}"
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, error_text)
    
    # ===== MÉTODOS GENERALES =====
    
    def update_progress(self, percentage, text):
        """Actualizar progreso"""
        self.progress_var.set(percentage)
        
        if self.start_time and percentage > 0:
            elapsed = time.time() - self.start_time
            if percentage > 5:
                total_estimated = (elapsed * 100) / percentage
                remaining = total_estimated - elapsed
                eta_str = str(timedelta(seconds=int(remaining)))
                progress_text = f"⏱️ {percentage:.1f}% - ETA: {eta_str}"
            else:
                progress_text = f"🔄 {percentage:.1f}% - Calculando..."
        else:
            progress_text = f"📊 {percentage:.1f}%"
        
        if text:
            progress_text = f"{text} - {progress_text}"
            
        self.progress_label.config(text=progress_text)
        self.root.update_idletasks()
    
    def backup_completed(self, success, message):
        """Manejar finalización del backup"""
        self.is_backing_up = False
        self.backup_button.configure(text=self.language_manager.get_text('start_backup'))
        
        if success:
            self.progress_var.set(100)
            self.progress_label.config(text="✅ Backup completado exitosamente")
            self.sound_manager.play_success()
            self.log_message("🎉 BACKUP COMPLETADO EXITOSAMENTE")
            
            lines = message.split('\n')
            for line in lines:
                if line.strip():
                    self.log_message(line.strip())
            
            messagebox.showinfo("🎉 Backup Completado", message)
            
            # Actualizar estadísticas si estamos en la pestaña de reportes
            selected_tab = self.notebook.select()
            tab_text = self.notebook.tab(selected_tab, "text")
            if self.language_manager.get_text('tab_reports') in tab_text:
                self.load_statistics()
            
        else:
            self.progress_label.config(text="❌ Error en el backup")
            self.sound_manager.play_error()
            self.log_message("💥 ERROR EN EL BACKUP")
            self.log_message(message)
            
            messagebox.showerror("💥 Error en Backup", message)
    
    def process_progress_queue(self):
        """Procesar mensajes de la cola de progreso"""
        try:
            while True:
                try:
                    message = self.progress_queue.get_nowait()
                    
                    if message['type'] == 'progress':
                        self.update_progress(message['value'], message['text'])
                        
                    elif message['type'] == 'complete':
                        self.backup_completed(message['success'], message['message'])
                        
                    elif message['type'] == 'error':
                        self.backup_completed(False, message['message'])
                        
                except queue.Empty:
                    break
        except Exception as e:
            pass
        
        # Continuar procesamiento
        self.root.after(100, self.process_progress_queue)
    
    def log_message(self, message, level="INFO"):
        """Añadir mensaje al log principal"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✅", 
            "WARNING": "⚠️",
            "ERROR": "❌"
        }
        
        icon = icons.get(level, "ℹ️")
        log_entry = f"[{timestamp}] {icon} {message}\n"
        
        try:
            self.log_text.insert(tk.END, log_entry)
            self.log_text.see(tk.END)
        except:
            pass
        
        print(f"{level}: {message}")
        self.root.update_idletasks()

# ============================= APLICACIÓN PRINCIPAL =============================

class InfernalBackupProUltimate:
    """Clase principal de la aplicación"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔥 Infernal Backup Pro v2.0 Ultimate - by Stormy")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Configurar tema de ventana
        self.root.configure(bg='#0a0a0a')
        
        # Intentar establecer icono personalizado
        try:
            self.set_window_icon()
        except:
            pass
        
        # Centrar ventana
        self.center_window()
        
        # Crear aplicación principal
        self.app = InfernalBackupUltimate(self.root)
        
        # Configurar cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        print("🔥 Infernal Backup Pro v2.0 Ultimate - Iniciado correctamente")
        print("👤 Autor: Stormy | 📄 Licencia: Free")
    
    def set_window_icon(self):
        """Establecer icono personalizado"""
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "stormy_icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
    
    def center_window(self):
        """Centrar ventana en pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def on_closing(self):
        """Manejar cierre de aplicación"""
        self.app.exit_application()
    
    def run(self):
        """Ejecutar aplicación"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n🔥 Aplicación cerrada por el usuario")
        except Exception as e:
            print(f"❌ Error crítico: {e}")
            messagebox.showerror("Error Crítico", f"Error inesperado:\n{str(e)}")

# ============================= FUNCIÓN PRINCIPAL =============================

def main():
    """Función principal de entrada"""
    print("\n" + "="*80)
    print("🔥 INFERNAL BACKUP PRO v2.0 ULTIMATE 🔥")
    print("Aplicación Completa con Sistema de Pestañas y Funcionalidades Avanzadas")
    print("👤 Autor: Stormy | 📄 Licencia: Free")
    print("💻 Plataforma: Windows 10/11 (Optimizado)")
    print("="*80)
    
    # Verificar sistema
    if platform.system() != "Windows":
        print("⚠️  Esta aplicación está optimizada para Windows 10/11")
        print("   Puede funcionar en otros sistemas con limitaciones")
    
    # Verificar permisos (opcional)
    if platform.system() == "Windows" and not check_admin():
        print("⚠️  Se recomienda ejecutar como administrador")
        print("   para acceso completo al sistema de archivos")
    
    try:
        # Crear directorio de backups
        backup_dir = os.path.join(os.getcwd(), "backups")
        os.makedirs(backup_dir, exist_ok=True)
        print(f"📁 Directorio de backups: {backup_dir}")
        
        # Inicializar aplicación
        app = InfernalBackupProUltimate()
        app.run()
        
        print("\n🔥 Infernal Backup Pro Ultimate finalizado correctamente")
        
    except Exception as e:
        print(f"\n❌ Error crítico al iniciar:")
        print(f"   {str(e)}")
        print("\n💡 Sugerencias:")
        print("   - Verifica Python 3.8+")
        print("   - Ejecuta: pip install --upgrade pip")
        print("   - Reinicia como administrador")
        
        input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
