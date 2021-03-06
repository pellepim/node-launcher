from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout

from node_launcher.constants import LNCLI_COMMANDS
from node_launcher.gui.components.console_dialog import ConsoleWidget
from node_launcher.gui.components.tabs_dialog import TabsDialog
from node_launcher.gui.menu.manage_lnd.lnd_configuration_tab import \
    LndConfigurationTab
from .lnd_output_tab import LndOutputTab


class LndManagerTabsDialog(TabsDialog):
    def __init__(self, lnd, system_tray):
        super().__init__()

        self.lnd = lnd
        self.system_tray = system_tray

        # lnd console
        self.console_tab = ConsoleWidget(
            title='lncli',
            program=self.lnd.software.lncli,
            args=self.lnd.lncli_arguments(),
            commands=LNCLI_COMMANDS
        )
        self.tab_widget.addTab(self.console_tab, 'lncli')

        # lnd output
        self.output_tab = LndOutputTab(
            lnd=self.lnd,
            system_tray=self.system_tray
        )
        self.tab_widget.addTab(self.output_tab, 'Logs')

        self.configuration_tab = LndConfigurationTab(self.lnd)
        self.tab_widget.addTab(self.configuration_tab, 'Configuration')

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.tab_widget)
        self.setLayout(self.main_layout)

        self.setWindowTitle('Manage LND')

        self.has_run_help = False

    def show(self):
        if self.lnd.file['alias'] is not None:
            self.configuration_tab.alias_layout.set_alias(self.lnd.file['alias'])

        super().showMaximized()
        self.raise_()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()

        if not self.has_run_help:
            self.console_tab.run_command('help')
