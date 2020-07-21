# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['ytmusiclibtracker.py'],
             pathex=['E:\\workspace_ll\\ytmusic-lib-tracker'],
             binaries=[],
             datas=[ ('config.ini', '.') ],
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ytmusiclibtracker',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )


# copy additional files to ./dist folder together with exe
import shutil
shutil.copyfile('config.ini', '{0}/config.ini'.format(DISTPATH))