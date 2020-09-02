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

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.spec'],
             pathex=['/Users/ludovicnoble/pygame6/partywithdist'],
             binaries=[],
             datas=[(audio, 'audio'), (fonts, 'fonts'), (background, 'background'), (characters, 'characters'), (items, 'items'), (introduction, 'introduction'), (difficulty, 'difficulty')],
             hiddenimports=["pygame", "simpleaudio", "wavinfo", "game"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
