import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Card Game",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["Images","Handlers","GameObjects","Colors.py","Game.py","Timer.py","cardData.json"]}},
    executables = executables

    )