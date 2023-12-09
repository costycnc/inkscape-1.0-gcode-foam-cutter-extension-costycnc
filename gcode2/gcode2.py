import inkex,sys,math
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

        for node in self.svg.selection.filter(inkex.PathElement):
            path = node.path.to_superpath()
            bezier.cspsubdiv(path, self.options.flatness)
            newpath = []
            for subpath in path:
                first = True
                for csp in subpath:
                    cmd = "L"
                    if first:
                        cmd = "M"
                    first = False
                    newpath.append([cmd, [csp[1][0], csp[1][1]]])
            node.path = newpath

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
            self.msg("pathlist="+str(len(path_list)))
            csp_list = path.path.to_superpath()
            bezier.cspsubdiv(csp_list,.1)           
            for csp in csp_list:                
                first=True
                for cord in csp:
                    a1 +=1
                    g +="G01 X"+"{:.2f}".format(cord[0][0])+" Y"+"{:.2f}".format( cord[0][1])+"\n" 
                    #self.msg(str(int(cord[0][0]))+","+str(int(cord[0][1])))
                    a.append(cord[0][0])
                    a.append(cord[0][1])
                    b.append(a)
                    a=[]
                    if first:
                        first=False
                        g +="G01 Z5\n"
                g +="G01 Z0\n"
                c.append(b)
                self.msg("len(b)")
                self.msg(len(b))
                b=[]
        #self.msg(str(a1)+"points")
        
        pathx=[[0,0]]
        minDiff = sys.maxsize
        curdiff=0
        num0=0
        num1=0
        num2=0
        currDiff=0
        x=0
        y=0
        x1=0
        y1=0
        x2=0
        y2=0
        
        self.msg("len c="+str(len(c)))
        self.msg(c)
        while(len(c)):
            minDiff = sys.maxsize
            self.msg("mindiff="+str(minDiff))
            for i, d in enumerate(pathx):
                for m,csp in enumerate(c): 
                    for n,cord in enumerate(csp): 
                        #self.msg("len="+str(len(pathx))+" i="+str(i)+">"+str(d[0])+","+str(d[1])+" len m="+str(len(c))+" m="+str(m)+" n="+str(n)+">"+str(cord[0])+","+str(cord[1]))
                        currDiff=math.dist(d,cord)
                        #self.msg("currdiff="+str(currDiff)+" mindiff="+str(minDiff))
                        if (currDiff < minDiff):
                            minDiff = currDiff
                            pos0 = i
                            pat1 = m
                            pos1 = n
                            #self.msg("gasit traseu mic pos0="+str(pos0)+"pat1="+str(pat1)+"pos1="+str(pos1))
                
            p=c.pop(pat1)
            self.msg("pat1")
            self.msg(pat1)
            self.msg("c.pop(pat1)")
            self.msg(p)
            p=p[pos1:]+p[:pos1]
            if (p[0]!=p[-1]):
                p.append(p[0])
            self.msg("p[pos1:]+p[:pos1]")
            self.msg(p)
            self.msg("pathx[pos0]")            
            self.msg(pathx[pos0])
            self.msg("pos0")            
            self.msg(pos0)
            pathx=pathx[:pos0]+[pathx[pos0]]+p+pathx[pos0:]  
            self.msg("pathx=pathx[pos0:]+p+pathx[:pos0]")
            self.msg(pathx)
        #self.msg(p)
        
        g="G21 F500 G90\nG92 X0 Y0\n"
        for gc in pathx:
            g +="G01 X"+"{:.2f}".format(gc[0])+" Y"+"{:.2f}".format(gc[1])+"\n"
            
                
                
        '''        
                https://www.costycnc.it/cm8/extract.js
        function extract(costyx){
//console.log("entrata");
//console.log(costyx[0][0]);
	pathx=[[0,0]];
	let minDiff = Number.MAX_VALUE;
	let num0=0,num1=0,num2=0,currDiff=0;
	
	//pathx contain all paths finded and joined ... at begin is empty
	//costyx contain all paths remained ... if a path is find ... is added to patx and canceled from costyx
	// x,y is coordonate point from pathx( one path with all path finded and joined)
	// x1,y1 is coordonate of points of all points of paths remained ( that is compared with points of path finded x,y)
	
	
	
	while(costyx.length){	
		minDiff = Number.MAX_VALUE;
		for(let i = 0; i < pathx.length; i=i+10){
			for(let m =0; m< costyx.length; m++){
				for(let n = 0; n < costyx[m].length; n++){
					x=pathx[i][0];
					y=pathx[i][1];
					x1=costyx[m][n][0];
					y1=costyx[m][n][1];						
					x2=x-x1;
					y2=y-y1;
					currDiff = x2*x2+y2*y2;  					
					if(currDiff < minDiff){
						minDiff = currDiff;
						pos0 = i;
						pat1 = m;
						pos1 = n;
					} 
				}   		
			}	
		}
	
	p=costyx.splice(pat1,1)[0];     //extract
	//p=p[0];                      //extract because need
	p = p.splice(pos1).concat(p);//rotate
		p.push(p[0]);                //close path
	pathx=pathx.slice(0,pos0).concat(p, pathx.slice(pos0-1));
	}
	
//console.log("uscita");   
//console.log(pathx[0]);
return pathx;	
  }
  '''
        g +="G01 X0 Y0" 
        with open("gcode.nc", "w") as f:
            f.write(g)
		
if __name__ == '__main__':
    hello().run()
