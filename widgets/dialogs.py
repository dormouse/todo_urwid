import urwid


class Dialog(object):
    def __init__(self, parent, title, text, buttons, width=None, height=None):
        self.parent = parent
        self.code = None
        self.text = text
        self.buttons = buttons
        self.old_widget = None
        contents = self.init_contents()
        w = urwid.ListBox(urwid.SimpleFocusListWalker(contents))
        w = urwid.LineBox(w, title=title)
        self.w = w

    def init_contents(self):
        contents = [
            urwid.Text(self.text),
            urwid.Divider(),
            self.init_buttons()
        ]
        return contents

    def init_buttons(self):
        # add buttons
        widgets = []
        for name, exitcode in self.buttons:
            b = urwid.Button(name, self.key_press, exitcode)
            b = urwid.AttrWrap(b, 'dlg_selectable', 'dlg_focus')
            widgets.append(b)
        but_box = urwid.GridFlow(widgets, 10, 3, 1, 'center')
        return but_box

    def show(self):
        self.old_widget = self.parent.body.original_widget
        self.parent.body.original_widget = urwid.Overlay(
            self.w, self.parent.body.original_widget,
            align='center', width=('relative', 50),
            valign='middle', height=('relative', 50),
        )

    def key_press(self, button, code):
        self.parent.body.original_widget = self.old_widget
        dlg_data = dict(
            key_code=code,
        )
        self.parent.dlg_buttons_press(dlg_data)


class AddTaskDialog(Dialog):
    class DiaEdit(urwid.Edit):
        def keypress(self, size, key):
            if key != 'enter':
                return super(AddTaskDialog.DiaEdit, self).keypress(size, key)

    def __init__(self, parent, title, text, buttons, width=None, height=None):
        super(AddTaskDialog, self).__init__(parent, title, text, buttons, width,
                                            height)

    def init_contents(self):
        self.edit = urwid.Edit()
        contents = [
            urwid.Text(self.text),
            # AddTaskDialog.DiaEdit(),
            urwid.LineBox(self.edit),
            urwid.Divider(),
            self.init_buttons()
        ]
        return contents

    def key_press(self, button, code):
        self.parent.body.original_widget = self.old_widget
        dlg_data = dict(
            key_code=code,
            edit_txt=self.edit.edit_text
        )
        self.parent.dlg_buttons_press(dlg_data)
