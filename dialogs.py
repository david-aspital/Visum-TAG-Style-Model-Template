import wx
import wx.grid
import wx.lib.sized_controls as sized_controls

class user_data_input(sized_controls.SizedDialog):
    def __init__(self, parent, title, columns, table=None):
        super(user_data_input, self).__init__(parent, title=title)
        if table is None:
            table = []
        pane = self.GetContentsPane()

        self.grid = wx.grid.Grid(pane, -1)
        self.grid.SetMaxSize(wx.Size(800, 300))
        self.grid.CreateGrid(len(table), 2)
        self.grid.HideRowLabels()
        for i, col in enumerate(columns):
            self.grid.SetColLabelValue(i, columns[i])
        self.grid.AutoSizeColumns()
        for i, col in enumerate(columns):
            self.grid.SetColFormatNumber(i)
        self.grid.SetColFormatNumber(1)
        self.grid.Fit()

        pane_btns = sized_controls.SizedPanel(pane)
        pane_btns.SetSizerType('horizontal')

        button_ok = wx.Button(pane_btns, wx.ID_OK, label='OK')
        button_cancel = wx.Button(pane_btns, wx.ID_CANCEL, label='Cancel')

        self.Fit()

    def get_value(self, columns):
        result = []
        for i in range(self.grid.GetNumberRows()):
            result.append(tuple(self.grid.GetCellValue(i, j) for j in range(len(columns))))
        return result


def text_entry_dlg(message, caption, parent=None, default_value=''):
    with wx.TextEntryDialog(parent, message, caption, value=default_value) as dlg:
        if dlg.ShowModal() == wx.ID_CANCEL:
            exit(0)
        result = dlg.GetValue()
    return result


def file_select_dlg(message,wildcard):
    with wx.FileDialog(parent=None, message=message, wildcard=wildcard,
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dlg:

        if dlg.ShowModal() == wx.ID_CANCEL:
            exit(0)
        pathname = dlg.GetPath()
    return pathname

def folder_select_dlg(message,path):
    with wx.DirDialog(parent=None, message=message, defaultPath=path,
                       style=wx.DD_DEFAULT_STYLE) as dlg:

        if dlg.ShowModal() == wx.ID_CANCEL:
            exit(0)
        path = dlg.GetPath()
    return path

def num_entry_dlg(message, caption, l_bound, u_bound, parent=None):
    with wx.SingleChoiceDialog( parent, message=message, caption=caption,choices=[str(x) for x in range(l_bound,u_bound+1)]) as dlg:
        if dlg.ShowModal() == wx.ID_CANCEL:
            exit(0)
        result = int(dlg.GetStringSelection())
    return result

