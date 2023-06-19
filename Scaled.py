



class Quiver:
    def __init__(self, v, scale=1, show=False, xlabel='x', ylabel='y', title='title', xlim=[-20, 20], ylim=[-20, 20]):
        import matplotlib.pyplot as plt
        self.plt=plt
        self.v=v
        self.scale=scale
        self.show=show
        self.xlabel=xlabel
        self.ylabel=ylabel
        self.title=title
        self.xlim=xlim
        self.ylim=ylim
        

    def plt_quiver(self):
        plt = self.plt
        fig, ax = plt.subplots()
        if self.v.ndim == 2:
            for a in self.v:
                ax.scatter(a[0], a[1], color='red')
                # ax.quiver(0, 0, a[0], a[1], scale=self.scale, scale_units='xy', angles='xy', color='blue')
        # # ax 折现
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.title)
        plt.xlim(self.xlim)
        plt.ylim(self.ylim)

        if self.show == True:
          plt.grid()
        return plt
