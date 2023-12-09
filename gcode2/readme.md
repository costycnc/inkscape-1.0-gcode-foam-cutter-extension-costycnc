Inkscape extension multiple path to one line path for cnc foam cutters (for costycnc foam cutter)

in gcode2.py at line 47 bezier.cspsubdiv(csp_list,.1)  ... change .1 to 1 if your computer is not fast

put gcode2.inx and gcode2.py in C:\Users\YOUR_NAME_ADMIN\AppData\Roaming\inkscape\extensions(after need to restart Inkscape)

in same folder will autosave file gcode ... the gcode will be rewrite automatically

If your path have Translate ... you need remove translate or another other commands for result real values gcode.

If your path is inside group or another ... not found path!

Nee to use Menu > Path > Combine to combine all separate path in one .. and need to be first child of root parent!

If is child of another child ... not function! Give error "Path not found!"

Not need to select paths ... will be procesate also if is not select! Will process all path !
