import urwid


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
        self.tasks = self.load_tasks()
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

    def load_tasks(self):

        tasks = [
            '+1st buy milk',
            '-2rd clean body',
            '-3rd go to school',
            '-测试一下很长很长的内容，这个内容真的很长。' * 3,
            '-3rd go to school',
            '-3rd go to school',
            '-3rd go to school',
            '-3rd go to school',
            '-3rd go to school',
            '-3rd go to school',
            '-3rd go to school',
        ]
        return TaskModel(tasks)

    def update_header(self, text):
        self.view.header = urwid.AttrMap(urwid.Text(text), 'foot')

    def task_switch_mark_done(self, w, index):
        label = w.label
        mark_postion = 7
        new_mark = 'X' if label[mark_postion] == ' ' else ' '
        w.set_label(label[:mark_postion] + new_mark + label[mark_postion + 1:])

    def show_help(self):
        buttons = [
            ('OK', 'help_ok'),
        ]
        title = 'Help'
        text = 'A Task build with Urwid.'
        d = Dialog(self, title, text, buttons)
        d.show()

    def dlg_buttons_press(self, code):
        # self.body.original_widget = self.overed_w
        header_text = [
            ('title', "U Task"),
            (f"{code}"),
        ]
        self.update_header(header_text)

    def dia_but_clicked(self, button):
        self.body.original_widget = self.overed_w

    def handle_input(self, input_char):
        if input_char in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        if input_char in ('h', 'H'):
            self.show_help()

    def rebuild_listbox(self):
        contents = [
            urwid.Columns(
                [
                    (6, urwid.Text('No.')),
                    (5, urwid.Text('Done')),
                    urwid.Text('Contents')
                ], 1
            ),
            urwid.Divider("="),
        ]
        for index, task in enumerate(self.tasks.all()):
            index_txt = format(str(index), ' <3')
            is_done_txt = '[X]' if task[0] == '+' else '[ ]'
            but_txt = '   '.join([index_txt, is_done_txt, task[1:]])
            but = urwid.Button(but_txt, self.task_switch_mark_done, index)
            contents.append(urwid.AttrMap(but, None, focus_map='reversed'))
        listbox = urwid.ListBox(urwid.SimpleFocusListWalker(contents))
        return listbox


class Dialog(object):
    def __init__(self, parent, title, text, buttons, width=None, height=None):
        self.parent = parent
        self.code = None
        contents = [
            urwid.Text(text), urwid.Divider(),
        ]
        # add buttons
        l = []
        for name, exitcode in buttons:
            b = urwid.Button(name, self.key_press, exitcode)
            b = urwid.AttrWrap(b, 'dlg_selectable', 'dlg_focus')
            l.append(b)
        but_box = urwid.GridFlow(l, 10, 3, 1, 'center')
        contents.append(but_box)
        w = urwid.ListBox(urwid.SimpleFocusListWalker(contents))
        w = urwid.LineBox(w, title=title)
        self.w = w

    def show(self):
        self.old_widget = self.parent.body.original_widget
        self.parent.body.original_widget = urwid.Overlay(
            self.w, self.parent.body.original_widget,
            align='center', width=('relative', 50),
            valign='middle', height=('relative', 50),
        )

    def key_press(self, button, code):
        self.parent.body.original_widget = self.old_widget
        self.parent.dlg_buttons_press(code)


class TaskModel(object):
    def __init__(self, tasks):
        self.tasks = tasks

    def all(self):
        return self.tasks


if __name__ == "__main__":
    TaskFrame()
