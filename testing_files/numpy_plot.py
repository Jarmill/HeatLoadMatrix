
def display_chart(inputfile):
    return

    try:
        from mpl_toolkits.mplot3d import axes3d
        import matplotlib.pyplot as plt
        from matplotlib import cm
        import numpy as np
    except Exception:
        return

    x = []
    y = []
    z = []
    i = 0

    with open(inputfile) as csvfile:
        inreader = csv.reader(csvfile, delimiter=',')
        for row in inreader:
            i += 1
            if i == 1:
                xSave = [float(xVal) for xVal in row[1:]]  # skip first value, is depth
            else:
                x.extend(xSave) # Another copy of X
                yPos = float(row[0])
                y.extend([yPos for t in range(1,len(row[1:])+1)]) # Y position is first
                z.extend([float(zVal) for zVal in row[1:]]) # Z is remainder of rows 2 through end

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_wireframe(x, y, z)
        #print (x, y, z)
        #ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=cm.jet, linewidth=0, antialiased=False, shade=False)
        plt.show()
        
    
