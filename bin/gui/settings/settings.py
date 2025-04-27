# coding:utf-8
import os
from imports.MCmain import *
from qfluentwidgets import isDarkTheme, FluentTranslator
from qfluentwidgets import FluentIcon as FIF
from module.moduleLoader import load_module
from qfluentwidgets import __version__
from enum import Enum

class SongQuality(Enum):
    """ Online song quality enumeration class """

    STANDARD = "Standard quality"
    HIGH = "High quality"
    SUPER = "Super quality"
    LOSSLESS = "Lossless quality"


class MvQuality(Enum):
    """ MV quality enumeration class """

    FULL_HD = "Full HD"
    HD = "HD"
    SD = "SD"
    LD = "LD"


class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = QLocale(QLocale.Language.Chinese, QLocale.Country.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Language.Chinese, QLocale.Country.HongKong)
    ENGLISH = QLocale(QLocale.Language.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """ Language serializer """

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


class Config(QConfig):
    """ Config of application """

    # folders
    musicFolders = ConfigItem(
        "Folders", "LocalMusic", [], FolderListValidator())
    downloadFolder = ConfigItem(
        "Folders", "Download", "download", FolderValidator())

    # online
    onlineSongQuality = OptionsConfigItem(
        "Online", "SongQuality", SongQuality.STANDARD, OptionsValidator(SongQuality), EnumSerializer(SongQuality))
    onlinePageSize = RangeConfigItem(
        "Online", "PageSize", 30, RangeValidator(0, 50))
    onlineMvQuality = OptionsConfigItem(
        "Online", "MvQuality", MvQuality.FULL_HD, OptionsValidator(MvQuality), EnumSerializer(MvQuality))

    # main window
    enableAcrylicBackground = ConfigItem(
        "MainWindow", "EnableAcrylicBackground", False, BoolValidator())
    minimizeToTray = ConfigItem(
        "MainWindow", "MinimizeToTray", True, BoolValidator())
    playBarColor = ColorConfigItem("MainWindow", "PlayBarColor", "#225C7F")
    recentPlaysNumber = RangeConfigItem(
        "MainWindow", "RecentPlayNumbers", 300, RangeValidator(10, 300))
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem(
        "MainWindow", "Language", Language.AUTO, OptionsValidator(Language), LanguageSerializer(), restart=True)

    # desktop lyric
    deskLyricHighlightColor = ColorConfigItem(
        "DesktopLyric", "HighlightColor", "#0099BC")
    deskLyricFontSize = RangeConfigItem(
        "DesktopLyric", "FontSize", 50, RangeValidator(15, 50))
    deskLyricStrokeSize = RangeConfigItem(
        "DesktopLyric", "StrokeSize", 5, RangeValidator(0, 20))
    deskLyricStrokeColor = ColorConfigItem(
        "DesktopLyric", "StrokeColor", Qt.GlobalColor.black)
    deskLyricFontFamily = ConfigItem(
        "DesktopLyric", "FontFamily", "Microsoft YaHei")
    deskLyricAlignment = OptionsConfigItem(
        "DesktopLyric", "Alignment", "Center", OptionsValidator(["Center", "Left", "Right"]))

    # software update
    checkUpdateAtStartUp = ConfigItem(
        "Update", "CheckUpdateAtStartUp", True, BoolValidator())

    @property
    def desktopLyricFont(self):
        """ get the desktop lyric font """
        font = QFont(self.deskLyricFontFamily.value)
        font.setPixelSize(self.deskLyricFontSize.value)
        return font

    @desktopLyricFont.setter
    def desktopLyricFont(self, font: QFont):
        dpi = QGuiApplication.primaryScreen().logicalDotsPerInch()
        self.deskLyricFontFamily.value = font.family()
        self.deskLyricFontSize.value = max(15, int(font.pointSize()*dpi/72))
        self.save()

YEAR = 2025
AUTHOR = "Folk.Skill"
VERSION = __version__
HELP_URL = "https://pyqt-fluent-widgets.readthedocs.io"
FEEDBACK_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues"
RELEASE_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets/releases/latest"

cfg = Config()
qconfig.load('config/config.json', cfg)


class SettingInterface(ScrollArea):
    """ Setting interface """

    checkUpdateSig = pyqtSignal()
    musicFoldersChanged = pyqtSignal(list)
    acrylicEnableChanged = pyqtSignal(bool)
    downloadFolderChanged = pyqtSignal(str)
    minimizeToTrayChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel(self.tr("设置"), self)

        # personalization
        self.personalGroup = SettingCardGroup(self.tr('个性化'), self.scrollWidget)
        self.enableAcrylicCard = SwitchSettingCard(
            FIF.TRANSPARENT,
            self.tr("使用亚克力效果"),
            self.tr("启用亚克力效果以获得更平滑的窗口效果，但可能会降低性能。"),
            configItem=cfg.enableAcrylicBackground,
            parent=self.personalGroup
        )
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            self.tr('程序外观'),
            self.tr("更改应用程序的外观"),
            texts=[
                self.tr('亮色'), self.tr('暗色'),
                self.tr('跟随系统')
            ],
            parent=self.personalGroup
        )
        self.themeColorCard=CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            self.tr('主题颜色'),
            self.tr('更改应用程序的主题颜色'),
            self.personalGroup
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            FIF.ZOOM,
            self.tr("界面缩放"),
            self.tr("更改应用程序的界面缩放比例"),
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                self.tr("使用系统设置")
            ],
            parent=self.personalGroup
        )
        self.languageCard = ComboBoxSettingCard(
            cfg.language,
            FIF.LANGUAGE,
            self.tr('语言'),
            self.tr('选择应用程序的语言'),
            texts=['简体中文', '繁體中文', 'English', self.tr('跟随系统')],
            parent=self.personalGroup
        )

        # online music
        self.onlineMusicGroup = SettingCardGroup(self.tr('音视频界面'), self.scrollWidget)
        self.onlinePageSizeCard = RangeSettingCard(
            cfg.onlinePageSize,
            FIF.SEARCH,
            self.tr("每页显示的音乐数量"),
            parent=self.onlineMusicGroup
        )
        self.onlineMusicQualityCard = OptionsSettingCard(
            cfg.onlineSongQuality,
            FIF.MUSIC,
            self.tr('音频品质'),
            texts=[
                self.tr('标准品质'), self.tr('高品质'),
                self.tr('极高品质'), self.tr('无损品质')
            ],
            parent=self.onlineMusicGroup
        )
        self.onlineMvQualityCard = OptionsSettingCard(
            cfg.onlineMvQuality,
            FIF.VIDEO,
            self.tr('MV 品质'),
            texts=[
                self.tr('Full HD'), self.tr('HD'),
                self.tr('SD'), self.tr('LD')
            ],
            parent=self.onlineMusicGroup
        )

        # desktop lyric
        self.deskLyricGroup = SettingCardGroup(self.tr('样式'), self.scrollWidget)
        self.deskLyricFontCard = PushSettingCard(
            self.tr('选择字体'),
            FIF.FONT,
            self.tr('字体'),
            parent=self.deskLyricGroup
        )
        self.deskLyricHighlightColorCard = ColorSettingCard(
            cfg.deskLyricHighlightColor,
            FIF.PALETTE,
            self.tr('前景色'),
            parent=self.deskLyricGroup
        )
        self.deskLyricStrokeColorCard = ColorSettingCard(
            cfg.deskLyricStrokeColor,
            FIF.PENCIL_INK,
            self.tr('描边颜色'),
            parent=self.deskLyricGroup
        )
        self.deskLyricStrokeSizeCard = RangeSettingCard(
            cfg.deskLyricStrokeSize,
            FIF.HIGHTLIGHT,
            self.tr('笔画大小'),
            parent=self.deskLyricGroup
        )
        self.deskLyricAlignmentCard = OptionsSettingCard(
            cfg.deskLyricAlignment,
            FIF.ALIGNMENT,
            self.tr('布局'),
            texts=[
                self.tr('居中'), self.tr('居左'),
                self.tr('居右')
            ],
            parent=self.deskLyricGroup
        )

        # main panel
        self.mainPanelGroup = SettingCardGroup(self.tr('主面板'), self.scrollWidget)
        self.minimizeToTrayCard = SwitchSettingCard(
            FIF.MINIMIZE,
            self.tr('关闭后最小化到托盘'),
            self.tr('关闭后最小化到托盘 MirrorChat 将继续在后台运行'),
            configItem=cfg.minimizeToTray,
            parent=self.mainPanelGroup
        )

        # update software
        self.updateSoftwareGroup = SettingCardGroup(self.tr("软件更新"), self.scrollWidget)
        self.updateOnStartUpCard = SwitchSettingCard(
            FIF.UPDATE,
            self.tr('在应用程序启动时检查更新'),
            self.tr('应用程序启动时检查更新新版本会更稳定，功能更多'),
            configItem=cfg.checkUpdateAtStartUp,
            parent=self.updateSoftwareGroup
        )

        # application
        self.aboutGroup = SettingCardGroup(self.tr('关于'), self.scrollWidget)
        self.helpCard = HyperlinkCard(
            HELP_URL,
            self.tr('打开帮助页面'),
            FIF.HELP,
            self.tr('帮助'),
            self.tr('发现新功能并了解有关 MirrorChat 的有用提示'),
            self.aboutGroup
        )
        self.feedbackCard = PrimaryPushSettingCard(
            self.tr('打开 feedback'),
            FIF.FEEDBACK,
            self.tr('打开 feedback'),
            self.tr('帮助我们改进 MirrorChat 以提供更好的用户体验'),
            self.aboutGroup
        )
        self.aboutCard = PrimaryPushSettingCard(
            self.tr('检测更新'),
            FIF.INFO,
            self.tr('关于'),
            '© ' + self.tr('版权') + f" {YEAR}, {AUTHOR}. " +
            self.tr('版本') + f" {VERSION}",
            self.aboutGroup
        )

        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        # initialize style sheet
        self.__setQss()

        # initialize layout
        load_module(self, [], "bin\gui\settings\interface\settings.mirc")
        self.__connectSignalToSlot()

    def __setQss(self):
        """ set style sheet """
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')

        theme = 'dark' if isDarkTheme() else 'light'
        with open(f'bin/gui/settings/resource/qss/{theme}/setting_interface.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def __showRestartTooltip(self):
        """ show restart tooltip """
        InfoBar.warning(
            '',
            self.tr('配置项将在下次启动时生效'),
            parent=self.window()
        )

    def __onDeskLyricFontCardClicked(self):
        """ desktop lyric font button clicked slot """
        font, isOk = QFontDialog.getFont(
            cfg.desktopLyricFont, self.window(), self.tr("选择字体"))
        if isOk:
            cfg.desktopLyricFont = font

    def __onDownloadFolderCardClicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("选择目录"), "./")
        if not folder or cfg.get(cfg.downloadFolder) == folder:
            return

        cfg.set(cfg.downloadFolder, folder)
        self.downloadFolderCard.setContent(folder)

    def __onThemeChanged(self, theme: Theme):
        """ theme changed slot """
        # change the theme of qfluentwidgets
        setTheme(theme)

        # chang the theme of setting interface
        self.__setQss()

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.appRestartSig.connect(self.__showRestartTooltip)
        cfg.themeChanged.connect(self.__onThemeChanged)

        # personalization
        self.enableAcrylicCard.checkedChanged.connect(
            self.acrylicEnableChanged)
        self.themeColorCard.colorChanged.connect(setThemeColor)

        # playing interface
        self.deskLyricFontCard.clicked.connect(self.__onDeskLyricFontCardClicked)

        # main panel
        self.minimizeToTrayCard.checkedChanged.connect(
            self.minimizeToTrayChanged)

        # about
        self.aboutCard.clicked.connect(self.checkUpdateSig)
        self.feedbackCard.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))


class SettingsFrame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("SettingsFrame")

        self.hBoxLayout = QHBoxLayout(self)
        self.settingInterface = SettingInterface(self)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.settingInterface)

        self.setWindowIcon(QIcon(":/qfluentwidgets/images/logo.png"))
        self.setWindowTitle("PyQt-Fluent-Widgets")

        self.setQss()
        cfg.themeChanged.connect(self.setQss)

    def setQss(self):
        theme = 'dark' if isDarkTheme() else 'light'
        with open(f'bin/gui/settings/resource/qss/{theme}/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())


if __name__ == '__main__':
    # enable dpi scale
    if cfg.get(cfg.dpiScale) != "Auto":
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

    # create application
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

    # internationalization
    locale = cfg.get(cfg.language).value
    fluentTranslator = FluentTranslator(locale)
    settingTranslator = QTranslator()
    settingTranslator.load(locale, "settings", ".", "resource/i18n")

    app.installTranslator(fluentTranslator)
    app.installTranslator(settingTranslator)

    # create main window
    w = SettingsFrame()
    w.show()
    app.exec()