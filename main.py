import urwid
from prj_conf import PRJ_DIR
from models.taskmodel import TaskModel


class TaskFrame(object):
    palette = [
        ('body', 'black', 'dark cyan', 'standout'),
        ('foot', 'light gray', 'black'),
        ('key', 'light cyan', 'black', 'underline'),
        ('title', 'yellow', 'black',),
        ('message', 'yellow', 'black',),
        ('dlg_body', 'black', 'light gray', 'standout'),
        ('dlg_border', 'black', 'dark blue'),
        ('dlg_shadow', 'white', 'black'),
        ('dlg_selectable', 'black', 'dark cyan'),
        ('dlg_focus', 'white', 'dark blue', 'bold'),
        ('dlg_focustext', 'light gray', 'dark blue'),
    ]

    header_text = [
        ('title', "U Task"),
    ]
    footer_text = [
        ('key', "UP"), ", ", ('key', "DOWN"), ", ",
        ('key', "PAGE UP"), " and ", ('key', "PAGE DOWN"),
        " move view  ",
        ('key', "H"), " helps",
        "  ",
        ('key', "Q"), " exits",
    ]

    def __init__(self):
        self.overed_w = None
        self.task_model = TaskModel()
        self.task_model.load_tasks()
        self.list_walker = None
        self.list_walker_header_row_count = 0
        self.listbox = self.rebuild_listbox()
        self.body = urwid.AttrMap(urwid.Filler(self.listbox, valign="middle",
                                               height=('relative', 100),
                                               top=2, min_height=10), 'body')
        footer = urwid.AttrMap(urwid.Text(self.footer_text), 'foot')
        header = urwid.AttrMap(urwid.Text(self.header_text), 'foot')
        self.view = urwid.Frame(self.body, header, footer)
        self.loop = urwid.MainLoop(self.view,
                                   self.palette,
                                   unhandled_input=self.handle_input)
        self.loop.run()

    def update_header(self, text):
        self.view.header = urwid.AttrMap(urwid.Text(text), 'foot')

    def task_create(self):
        buttons = [
            ('OK', 'create_ok'),
            ('CANCEL', 'create_cancel')
        ]
        title = 'Create New Task'
        text = 'Task:'
        d = AddTaskDialog(self, title, text, buttons)
        d.show()

    def tasks_save(self):
        self.task_model.save_tasks()
        header_text = [
            ('title', "U Task"),
            "  saved",
        ]
        self.update_header(header_text)

    def task_switch_mark_done(self, w, index):
        label = w.label
        mark_postion = 5
        new_mark = 'X' if label[mark_postion] == ' ' else ' '
        w.set_label(label[:mark_postion] + new_mark + label[mark_postion + 1:])
        _, focus = self.list_walker.get_focus()
        index = focus - self.list_walker_header_row_count
        self.task_model.task_switch_mark_done(index)

    def encode_label_txt(self, txt, index):
        label_txt = format(str(index), ' <3') + txt[1:]
        return label_txt

    def decode_label_txt(self, label_txt):
        txt = f"- {label_txt[3:]}"
        return txt

    def show_help(self):
        buttons = [
            ('OK', 'help_ok'),
        ]
        title = 'Help'
        text = 'A Task build with Urwid.'
        d = Dialog(self, title, text, buttons)
        d.show()

    def dlg_buttons_press(self, dlg_data):
        header_text = [
            ('title', "U Task"),
            f"{dlg_data['key_code']}",
        ]
        self.update_header(header_text)

        if dlg_data['key_code'] == 'create_ok':
            model_txt = f"- [ ] {dlg_data['edit_txt']}"
            index = len(self.task_model.all())
            button_label = self.encode_label_txt(model_txt, index)
            self.task_model.create(model_txt)
            but = urwid.Button(button_label,
                               self.task_switch_mark_done,
                               index)
            self.list_walker.append(
                urwid.AttrMap(but, None, focus_map='reversed')
            )
            self.list_walker.set_focus(
                index + self.list_walker_header_row_count
            )

    def handle_input(self, input_char):
        if input_char in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        if input_char in ('h', 'H'):
            self.show_help()
        if input_char in ('a', 'A'):
            self.task_create()
        if input_char in ('s', 'S'):
            self.tasks_save()

    def rebuild_listbox(self):
        contents = [
            urwid.Columns(
                [
                    (4, urwid.Text('No.')),
                    (5, urwid.Text('Done')),
                    urwid.Text('Contents')
                ], 1
            ),
            urwid.Divider("="),
        ]
        self.list_walker_header_row_count = len(contents)
        for index, task in enumerate(self.task_model.all()):
            but_label = self.encode_label_txt(task, index)
            but = urwid.Button(but_label, self.task_switch_mark_done, index)
            contents.append(urwid.AttrMap(but, None, focus_map='reversed'))
        self.list_walker = urwid.SimpleFocusListWalker(contents)
        listbox = urwid.ListBox(self.list_walker)
        return listbox


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

if __name__ == "__main__":
    TaskFrame()
