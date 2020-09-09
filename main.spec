# -*- mode: python ; coding: utf-8 -*-
import os, sys
from os import path

bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname("__file__")))

assets = path.join(bundle_dir, 'assets')
audio = path.join(bundle_dir, 'audio')
fonts = path.join(bundle_dir, 'fonts')
background = path.join(bundle_dir, 'background')
characters = path.join(bundle_dir, 'characters')
items = path.join(bundle_dir, 'items')
introduction = path.join(bundle_dir, 'introduction')
difficulty = path.join(bundle_dir, 'difficulty')

block_cipher = None

a = Analysis(['main.py'],
             pathex=['/Users/ludovicnoble/pygame9/partywithdist'],
             binaries=[],
             datas=[(audio, 'audio'), (fonts, 'fonts'), (background, 'background'), (characters, 'characters'), (items, 'items'), (introduction, 'introduction'), (difficulty, 'difficulty')],
             hiddenimports=["pygame", "simpleaudio", "wavinfo", "game"],
             hookspath=None,
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += [('main.py', '/Users/ludovicnoble/pygame9/partywithdist/main.py', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='The Four Temperaments Party Game',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )

app = BUNDLE(exe,
         name='Four Temperaments Party Game.app',
         icon='icon.icns',
         bundle_identifier='com.ldovic.fourtemperamentspartygame.mac',
         info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSAppleScriptEnabled': False,
            'CFBundleDocumentTypes': [
                {
                    'CFBundleTypeName': 'My File Format',
                    'CFBundleTypeIconFile': 'MyFileIcon.icns',
                    'LSItemContentTypes': ['com.example.myformat'],
                    'LSHandlerRank': 'Owner'
                    }
                ]
            },
         )
