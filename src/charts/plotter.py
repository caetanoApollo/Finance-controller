import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class Plotter:
    def __init__(self):
        pass

    def criar_grafico_pizza(self, dados, titulo='Gráfico de Pizza', rotulos=None, figsize=(5, 5)):
        figura = Figure(figsize=figsize, dpi=100)
        ax = figura.add_subplot(111)
        cores = plt.get_cmap('tab20').colors  # Paleta de cores mais bonita
        wedges, texts, autotexts = ax.pie(dados, labels=rotulos, autopct='%1.1f%%', startangle=140, colors=cores)
        ax.set_title(titulo)
        figura.patch.set_alpha(0.0)  # Fundo transparente

        # Ajustar cor do texto para ser mais visível
        for text in texts + autotexts:
            text.set_color('black')

        return figura