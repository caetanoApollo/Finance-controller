from PyQt5 import QtWidgets, QtGui, QtCore
from database.db_manager import DBManager
from utils.helpers import formatar_data, calcular_total
from charts.plotter import Plotter
from datetime import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import sys

class Interface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DBManager()
        self.plotter = Plotter()
        self.categorias_entrada = ["Salário", "Investimentos", "Outras Entradas"]
        self.categorias_saida = ["Alimentação", "Transporte", "Lazer", "Saúde", "Educação", "Outras Saídas"]
        self.meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.anos = [str(ano) for ano in range(2020, datetime.now().year + 1)]
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Gestão Financeira")
        self.setWindowIcon(QtGui.QIcon('C:/Users/Caeta/Desktop/Bot controle financeiro/finance-bot/src/icons/icon.ico'))
        self.setMinimumSize(1920, 1080)
        self.showMaximized()  # Abre a aplicação em tela cheia

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.frame_controles = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.frame_controles)

        self.frame_transacoes = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.frame_transacoes)

        self.frame_graficos = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.frame_graficos)

        self.adicionar_controles()
        self.criar_tabelas()
        self.exibir_transacoes()
        self.atualizar_total()
        self.exibir_graficos()

        self.set_dark_mode()

    def adicionar_controles(self):
        grid_layout = QtWidgets.QGridLayout()
        self.frame_controles.addLayout(grid_layout)

        btn_adicionar_transacao = QtWidgets.QPushButton("Adicionar Transação")
        btn_adicionar_transacao.clicked.connect(self.adicionar_transacao)
        btn_adicionar_transacao.setShortcut("Ctrl++")
        grid_layout.addWidget(btn_adicionar_transacao, 0, 0)

        btn_excluir_transacao = QtWidgets.QPushButton("Excluir Transação")
        btn_excluir_transacao.clicked.connect(self.excluir_transacao)
        btn_excluir_transacao.setShortcut("del")
        grid_layout.addWidget(btn_excluir_transacao, 0, 1)

        btn_exportar = QtWidgets.QPushButton("Exportar Dados")
        btn_exportar.clicked.connect(self.exportar_dados)
        grid_layout.addWidget(btn_exportar, 0, 2)

        self.label_total = QtWidgets.QLabel("Total: R$ 0,00")
        self.label_total.setFont(QtGui.QFont("Helvetica", 20))
        self.label_total.setAlignment(QtCore.Qt.AlignRight)
        grid_layout.addWidget(self.label_total, 0, 3, 1, 2)

        self.tipo_transacao_var = QtWidgets.QComboBox()
        self.tipo_transacao_var.addItems(["Todas", "Entradas", "Saídas"])
        self.tipo_transacao_var.currentIndexChanged.connect(self.atualizar_categorias)
        grid_layout.addWidget(QtWidgets.QLabel("Tipo:"), 1, 0, QtCore.Qt.AlignRight)
        grid_layout.addWidget(self.tipo_transacao_var, 1, 1)

        self.categoria_var = QtWidgets.QComboBox()
        self.categoria_var.addItems(["Todas"] + self.categorias_entrada + self.categorias_saida)
        self.categoria_var.currentIndexChanged.connect(self.filtrar_transacoes)
        grid_layout.addWidget(QtWidgets.QLabel("Categoria:"), 1, 2, QtCore.Qt.AlignRight)
        grid_layout.addWidget(self.categoria_var, 1, 3)

        self.mes_var = QtWidgets.QComboBox()
        self.mes_var.addItems(self.meses)
        self.mes_var.setCurrentIndex(datetime.now().month - 1)
        self.mes_var.currentIndexChanged.connect(self.filtrar_transacoes)
        grid_layout.addWidget(QtWidgets.QLabel("Mês:"), 1, 4, QtCore.Qt.AlignRight)
        grid_layout.addWidget(self.mes_var, 1, 5)

        self.ano_var = QtWidgets.QComboBox()
        self.ano_var.addItems(self.anos)
        self.ano_var.setCurrentText(str(datetime.now().year))
        self.ano_var.currentIndexChanged.connect(self.filtrar_transacoes)
        grid_layout.addWidget(QtWidgets.QLabel("Ano:"), 1, 6, QtCore.Qt.AlignRight)
        grid_layout.addWidget(self.ano_var, 1, 7)

    def exportar_dados(self):
        caminho, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Salvar Dados", "", "CSV Files (*.csv)")
        if caminho:
            transacoes = self.db_manager.get_transactions()
            with open(caminho, 'w') as arquivo:
                arquivo.write("Descricao,Valor,Data,Categoria\n")
                for transacao in transacoes:
                    descricao, valor, data, categoria = transacao[1:]
                    arquivo.write(f"{descricao},{valor},{data},{categoria}\n")
            self.exibir_mensagem("Dados exportados com sucesso!")

    def exibir_mensagem(self, mensagem):
        QtWidgets.QMessageBox.information(self, "Informação", mensagem)

    def adicionar_transacao(self):
        dialogo = QtWidgets.QDialog(self)
        dialogo.setWindowTitle("Adicionar Transação")
        layout = QtWidgets.QFormLayout(dialogo)

        descricao_entry = QtWidgets.QLineEdit()
        descricao_entry.setStyleSheet("color: black;")
        layout.addRow("Descrição:", descricao_entry)

        valor_entry = QtWidgets.QLineEdit()
        valor_entry.setStyleSheet("color: black;")
        layout.addRow("Valor:", valor_entry)

        tipo_combo = QtWidgets.QComboBox()
        tipo_combo.addItems(["Entrada", "Saída"])
        layout.addRow("Tipo:", tipo_combo)

        categoria_combo = QtWidgets.QComboBox()
        layout.addRow("Categoria:", categoria_combo)

        def atualizar_categorias():
            tipo = tipo_combo.currentText()
            categoria_combo.clear()
            if tipo == "Entrada":
                categoria_combo.addItems(self.categorias_entrada)
            else:
                categoria_combo.addItems(self.categorias_saida)

        tipo_combo.currentIndexChanged.connect(atualizar_categorias)
        atualizar_categorias()

        btn_salvar = QtWidgets.QPushButton("Salvar")
        layout.addRow(btn_salvar)

        def salvar_transacao():
            descricao = descricao_entry.text()
            valor = valor_entry.text()
            tipo = tipo_combo.currentText()
            categoria = categoria_combo.currentText()
            try:
                valor = float(valor.replace(',', '.'))
                if tipo == "Saída":
                    valor = -valor
                data = datetime.now()
                self.db_manager.add_transaction(descricao, valor, formatar_data(data), categoria)
                self.exibir_mensagem("Transação adicionada com sucesso!")
                dialogo.accept()
                self.exibir_transacoes()
                self.atualizar_total()
                self.exibir_graficos()
            except ValueError:
                self.exibir_mensagem("Por favor, insira um valor válido.")

        btn_salvar.clicked.connect(salvar_transacao)
        dialogo.setStyleSheet(self.styleSheet())
        dialogo.exec_()

    def editar_transacao(self, item):
        transacao_id = item.data(0, QtCore.Qt.UserRole)
        transacao = self.db_manager.get_transaction_by_id(transacao_id)

        dialogo = QtWidgets.QDialog(self)
        dialogo.setWindowTitle("Editar Transação")
        layout = QtWidgets.QFormLayout(dialogo)

        descricao_entry = QtWidgets.QLineEdit(transacao[1])
        descricao_entry.setStyleSheet("color: black;")
        layout.addRow("Descrição:", descricao_entry)

        valor_entry = QtWidgets.QLineEdit(str(abs(transacao[2])))
        valor_entry.setStyleSheet("color: black;")
        layout.addRow("Valor:", valor_entry)

        tipo_combo = QtWidgets.QComboBox()
        tipo_combo.addItems(["Entrada", "Saída"])
        tipo_combo.setCurrentText("Entrada" if transacao[2] > 0 else "Saída")
        layout.addRow("Tipo:", tipo_combo)

        categoria_combo = QtWidgets.QComboBox()
        layout.addRow("Categoria:", categoria_combo)

        def atualizar_categorias():
            tipo = tipo_combo.currentText()
            categoria_combo.clear()
            if tipo == "Entrada":
                categoria_combo.addItems(self.categorias_entrada)
            else:
                categoria_combo.addItems(self.categorias_saida)
            categoria_combo.setCurrentText(transacao[4])

        tipo_combo.currentIndexChanged.connect(atualizar_categorias)
        atualizar_categorias()

        btn_salvar = QtWidgets.QPushButton("Salvar")
        layout.addRow(btn_salvar)

        def salvar_transacao():
            descricao = descricao_entry.text()
            valor = valor_entry.text()
            tipo = tipo_combo.currentText()
            categoria = categoria_combo.currentText()
            try:
                valor = float(valor.replace(',', '.'))
                if tipo == "Saída":
                    valor = -valor
                self.db_manager.update_transaction(transacao_id, descricao, valor, categoria)
                self.exibir_mensagem("Transação editada com sucesso!")
                dialogo.accept()
                self.exibir_transacoes()
                self.atualizar_total()
                self.exibir_graficos()
            except ValueError:
                self.exibir_mensagem("Por favor, insira um valor válido.")

        btn_salvar.clicked.connect(salvar_transacao)
        dialogo.setStyleSheet(self.styleSheet())
        dialogo.exec_()

    def criar_tabelas(self):
        # Layout para as tabelas lado a lado
        layout_tabelas = QtWidgets.QHBoxLayout()

        # Tabela de Entradas
        frame_entradas = QtWidgets.QVBoxLayout()
        label_entradas = QtWidgets.QLabel("Entradas")
        label_entradas.setFont(QtGui.QFont("Helvetica", 14))
        frame_entradas.addWidget(label_entradas, alignment=QtCore.Qt.AlignCenter)
        frame_entradas.setSpacing(2)  # Ajusta o espaçamento entre o título e a tabela

        self.tree_entradas = QtWidgets.QTreeWidget()
        self.tree_entradas.setColumnCount(4)
        self.tree_entradas.setHeaderLabels(["Descrição", "Valor", "Data", "Categoria"])
        self.tree_entradas.setFixedSize(800, 300)
        self.tree_entradas.itemDoubleClicked.connect(self.editar_transacao)
        frame_entradas.addWidget(self.tree_entradas, alignment=QtCore.Qt.AlignCenter)

        # Tabela de Saídas
        frame_saidas = QtWidgets.QVBoxLayout()
        label_saidas = QtWidgets.QLabel("Saídas")
        label_saidas.setFont(QtGui.QFont("Helvetica", 14))
        frame_saidas.addWidget(label_saidas, alignment=QtCore.Qt.AlignCenter)
        frame_saidas.setSpacing(2)  # Ajusta o espaçamento entre o título e a tabela

        self.tree_saidas = QtWidgets.QTreeWidget()
        self.tree_saidas.setColumnCount(4)
        self.tree_saidas.setHeaderLabels(["Descrição", "Valor", "Data", "Categoria"])
        self.tree_saidas.setFixedSize(800, 300)
        self.tree_saidas.itemDoubleClicked.connect(self.editar_transacao)
        frame_saidas.addWidget(self.tree_saidas, alignment=QtCore.Qt.AlignCenter)

        layout_tabelas.addLayout(frame_entradas)
        layout_tabelas.addLayout(frame_saidas)
        self.frame_transacoes.addLayout(layout_tabelas)

    def exibir_transacoes(self):
        self.tree_entradas.clear()
        self.tree_saidas.clear()

        transacoes = self.db_manager.get_transactions()
        mes_selecionado = self.meses.index(self.mes_var.currentText()) + 1
        ano_selecionado = int(self.ano_var.currentText())
        transacoes = [t for t in transacoes if self._data_valida(t[3], mes_selecionado, ano_selecionado)]

        for transacao in transacoes:
            transacao_id, descricao, valor, data, categoria = transacao
            item = QtWidgets.QTreeWidgetItem([descricao, f"R$ {abs(valor):.2f}".replace('.', ','), data, categoria])
            item.setData(0, QtCore.Qt.UserRole, transacao_id)
            if valor > 0:
                self.tree_entradas.addTopLevelItem(item)
            else:
                self.tree_saidas.addTopLevelItem(item)

    def excluir_transacao(self):
        selected_item = self.tree_entradas.currentItem() or self.tree_saidas.currentItem()
        if selected_item:
            transacao_id = selected_item.data(0, QtCore.Qt.UserRole)
            descricao = selected_item.text(0)
            valor = selected_item.text(1)
            reply = QtWidgets.QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja excluir esta transação?\n\nDescrição: {descricao}\nValor: {valor}",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.db_manager.delete_transaction_by_id(transacao_id)
                self.exibir_mensagem("Transação excluída com sucesso!")
                self.exibir_transacoes()
                self.atualizar_total()
                self.exibir_graficos()
        else:
            self.exibir_mensagem("Por favor, selecione uma transação para excluir.")

    def atualizar_total(self):
        transacoes = self.db_manager.get_transactions()
        mes_selecionado = self.meses.index(self.mes_var.currentText()) + 1
        ano_selecionado = int(self.ano_var.currentText())
        transacoes = [t for t in transacoes if self._data_valida(t[3], mes_selecionado, ano_selecionado)]
        total = calcular_total([t[2] for t in transacoes])
        self.label_total.setText(f"Total: R$ {total:.2f}".replace('.', ','))

    def exibir_graficos(self):
        for i in reversed(range(self.frame_graficos.count())):
            widget = self.frame_graficos.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        transacoes = self.db_manager.get_transactions()
        mes_selecionado = self.meses.index(self.mes_var.currentText()) + 1
        ano_selecionado = int(self.ano_var.currentText())
        transacoes = [t for t in transacoes if self._data_valida(t[3], mes_selecionado, ano_selecionado)]

        valores = [t[2] for t in transacoes]
        rotulos = [t[1] for t in transacoes]
        cores = ['#66c2a5' if v > 0 else '#fc8d62' for v in valores]

        fig, ax = plt.subplots(figsize=(6, 6))
        fig.patch.set_facecolor('#1e1e1e')
        ax.set_facecolor('#1e1e1e')
        ax.pie([abs(v) for v in valores], labels=rotulos, colors=cores, startangle=90, autopct='%1.1f%%', textprops={'color': 'white'})
        ax.set_title('Entradas e Saídas', color='white')

        canvas = FigureCanvas(fig)
        self.frame_graficos.addWidget(canvas)

    def filtrar_transacoes(self):
        self.exibir_transacoes()
        self.atualizar_total()
        self.exibir_graficos()

    def atualizar_categorias(self):
        tipo = self.tipo_transacao_var.currentText()
        self.categoria_var.clear()
        if tipo == "Entradas":
            self.categoria_var.addItems(["Todas"] + self.categorias_entrada)
        elif tipo == "Saídas":
            self.categoria_var.addItems(["Todas"] + self.categorias_saida)
        else:
            self.categoria_var.addItems(["Todas"] + self.categorias_entrada + self.categorias_saida)
        self.filtrar_transacoes()

    def _data_valida(self, data_str, mes, ano):
        try:
            data = datetime.strptime(data_str, "%Y-%m-%d")
        except ValueError:
            try:
                data = datetime.strptime(data_str, "%d-%m-%Y")
            except ValueError:
                return False
        return data.month == mes and data.year == ano

    def set_dark_mode(self):
        dark_stylesheet = """
        QMainWindow {
            background-color: #1e1e1e;
        }
        QLabel, QComboBox, QPushButton {
            color: #ffffff;
            font-size: 14px;
        }
        QPushButton {
            background-color: #3c3c3c;
            border: 1px solid #5a5a5a;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #5a5a5a;
        }
        QComboBox {
            background-color: #3c3c3c;
            border: 1px solid #5a5a5a;
        }
        QComboBox QAbstractItemView {
            background-color: #3c3c3c;
            color: #ffffff;
            selection-background-color: #5a5a5a;
        }
        QTreeWidget {
            background-color: #3c3c3c;
            color: #ffffff;
            border: 1px solid #5a5a5a;
        }
        QHeaderView::section {
            background-color: #3c3c3c;
            color: #ffffff;
            padding: 4px;
            border: 1px solid #5a5a5a;
        }
        QDialog {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        """
        self.setStyleSheet(dark_stylesheet)

    def aplicar_tema(self, widget):
        widget.setStyleSheet("""
        QDialog {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        QLabel, QLineEdit, QComboBox, QPushButton {
            color: #ffffff;
            font-size: 14px;
        }
        QPushButton {
            background-color: #3c3c3c;
            border: 1px solid #5a5a5a;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #5a5a5a;
        }
        QComboBox {
            background-color: #3c3c3c;
            border: 1px solid #5a5a5a;
        }
        QComboBox QAbstractItemView {
            background-color: #3c3c3c;
            color: #ffffff;
            selection-background-color: #5a5a5a;
        }
        QLineEdit {
            background-color: #ffffff;
            color: #000000;
        }
        """)

    def iniciar(self):
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    interface = Interface()
    interface.iniciar()
    sys.exit(app.exec_())