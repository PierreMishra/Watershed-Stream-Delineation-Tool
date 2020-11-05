@set the_env=env859-py3
call "C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\activate.bat" "%the_env%"
call "%localappdata%\ESRI\conda\envs\%the_env%\scripts\spyder.exe" -p %cd% 
call "C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\deactivate.bat"