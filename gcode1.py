import inkex
from inkex import bezier
from inkex.elements import Group, Line,Circle


class hello(inkex.EffectExtension):

    def effect(self):
        '''
        L = [1, 2, 3]
        L.pop() # returns 3, L is now [1, 2]
        L.append(4) # returns None, L is now [1, 2, 4]
        L.insert(0, 5) # returns None, L is now [5, 1, 2, 4]
        L.remove(2) # return None, L is now [5, 1, 4]
        del(L[0]) # return None, L is now [1, 4]
        L.pop(0) # return 1, L is now [4]
        '''
        a=[]
        b=[]
        c=[]
        a1=0
        g="G21 F500 G90\nG92 X0 Y0\n"
        current_layer = self.svg.get_current_layer()
        path_list = current_layer.xpath('./svg:path')
        first = True
        if len(path_list) < 1:
            self.msg('No path found !')
            return
        for path in path_list:
            csp_list = path.path.to_superpath()
            bezier.cspsubdiv(csp_list, 32)           
            for csp in csp_list:                
                first=True
                for cord in csp:
                    a1 +=1
                    g +="G01 X"+"{:.2f}".format(cord[0][0])+" Y"+"{:.2f}".format( cord[0][1])+"\n" 
                    #self.msg(str(int(cord[0][0]))+","+str(int(cord[0][1])))
                    a.append(int(cord[0][0]))
                    a.append(int(cord[0][1]))
                    b.append(a)
                    a=[]
                    if first:
                        first=False
                        g +="G01 Z5\n"
                g +="G01 Z0\n"
                c.append(b)
                b=[]
        #self.msg(len(c))
        self.msg(str(a1)+"points")
        
        layer = self.svg.add(Group.new('my_label', is_layer=True))
        for csp in c:
            for cord in csp:   
                circle = current_layer.add(Circle(cx=str(cord[0]), cy= str(cord[1]), r="5"))
                circle.style = {'fill': 'red'} 
                
        
        g +="G01 Y0\nG01 X0" 
        with open("gcode.nc", "w") as f:
            f.write(g)
		
if __name__ == '__main__':
    hello().run()
