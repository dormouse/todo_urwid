import urwid
from prj_conf import PRJ_DIR
from models.taskmodel import TaskModel
from widgets.dialogs import Dialog, AddTaskDialog, DialogExit, DialogM
from dialog import DialogDisplay

PALETTE = [
    ('body', 'black', 'dark cyan', 'standout'),
    ('header', 'white', 'black'),
    ('footer', 'light gray', 'black'),
    ('key', 'light cyan', 'black', 'underline'),
    ('title', 'yellow', 'black',),
    ('message', 'yellow', 'black',),
    ('dlg_body', 'black', 'light gray', 'standout'),
    ('dlg_border', 'black', 'dark blue'),
    ('dlg_shadow', 'white', 'black'),
    ('dlg_selectable', 'black', 'dark cyan'),
    ('dlg_focus', 'white', 'dark blue', 'bold'),
    ('dlg_focustext', 'light gray', 'dark blue'),
    ('reversed', 'black', 'dark cyan', 'standout'),
]


class SelectableRow(urwid.WidgetWrap):
    def __init__(self, contents, on_select=None):
        self.on_select = on_select
        self.contents = contents
        self._columns = urwid.Columns([urwid.Text(c) for c in contents])
        self._focusable_columns = urwid.AttrMap(self._columns, '', 'reversed')
        super(SelectableRow, self).__init__(self._focusable_columns)

    def selectable(self):
        return True

    def update_contents(self, contents):
        # update the list record inplace...
        self.contents[:] = contents

        # ... and update the displayed items
        for t, (w, _) in zip(contents, self._columns.contents):
            w.set_text(t)

    def keypress(self, size, key):
        if self.on_select and key in ('enter',):
            self.on_select(self)
        return key

    def __repr__(self):
        return '%s(contents=%r)' % (self.__class__.__name__, self.contents)


class Table(urwid.WidgetWrap):
    def __init__(self, on_select=None):
        self.on_select = on_select
        self.task_model = TaskModel()
        self.task_model.load_tasks()

        self.widgets = [
            urwid.Columns(
                [
                    (4, urwid.Text('No.')),
                    (5, urwid.Text('Done')),
                    urwid.Text('Contents')
                ], 1
            ),
            urwid.Divider("="),
        ]
        self.body = self.build_body()
        # self.widgets.append(self.body)
        self.view = urwid.Pile(self.widgets)
        super(Table, self).__init__(self.view)

    def build_body(self):
        contents = []
        for index, task in enumerate(self.task_model.all()):
            but_label = (task, 'test')
            but = SelectableRow(but_label, self.on_select)
            contents.append(urwid.AttrMap(but, None, focus_map='reversed'))
        self.list_walker = urwid.SimpleFocusListWalker(contents)
        listbox = urwid.ListBox(self.list_walker)
        return listbox

    def selectable(self):
        return True


class App(object):
    def __init__(self):
        self.header = None
        header_texts = [
            ('title', "U Task"),
        ]
        self.header = urwid.AttrMap(urwid.Text(header_texts), 'header')
        footer_texts = [
            ('key', "UP"), ", ", ('key', "DOWN"), ", ",
            ('key', "PAGE UP"), " and ", ('key', "PAGE DOWN"),
            " move view  ",
            ('key', "H"), " helps",
            "  ",
            ('key', "Q"), " exits",
        ]
        self.footer = urwid.AttrMap(urwid.Text(footer_texts), 'footer')
        self.table = Table(self.task_switch_mark_done)
        # self.body = urwid.AttrMap(urwid.Filler(self.table, valign="middle",
        #                                        height=('relative', 100),
        #                                        top=2, min_height=10), 'body')
        self.body = urwid.AttrMap(self.table, 'body')
        self.view = urwid.Frame(self.body, self.header, self.footer)
        self.loop = urwid.MainLoop(self.view,
                                   PALETTE,
                                   unhandled_input=self.handle_input)

    def update_header(self, texts):
        self.header = urwid.AttrMap(urwid.Text(texts), 'header')

    def update_footer(self, texts):
        self.footer = urwid.AttrMap(urwid.Text(texts), 'footer')

    def task_switch_mark_done(self, w, index):
        label = w.label
        mark_postion = 5
        new_mark = 'X' if label[mark_postion] == ' ' else ' '
        # w.set_label(label[:mark_postion] + new_mark + label[mark_postion + 1:])
        # _, focus = self.list_walker.get_focus()
        # index = focus - self.list_walker_header_row_count
        # self.task_model.task_switch_mark_done(index)

    def handle_input(self, input_char):
        if input_char in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        # if input_char in ('h', 'H'):
        #     self.show_help()
        # if input_char in ('a', 'A'):
        #     self.task_create()
        # if input_char in ('s', 'S'):
        #     self.tasks_save()

    def main(self):
        self.loop.run()


class TaskFrame(object):
    header_text = [
        ('title', "U Task"),
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
        text = 'test'
        height = 20
        width = 20
        d = DialogDisplay(text, height, width, self.body)
        d.add_buttons([("OK", 0)])
        exitcode, exitstring = d.main()

        header_text = [
            ('title', "U Task"),
            f"{exitcode}",
        ]
        self.loop.draw_screen()
        self.body.re

        """
        
        self.overed_w = self.body
        buttons = [
            ('OK', 'help_ok'),
        ]
        title = 'Help'
        text = 'A Task build with Urwid.'
        d = Dialog(self, title, text, buttons)
        d.show()
        """

    def dlg_buttons_press(self, exitcode):
        header_text = [
            ('title', "U Task"),
            f"{exitcode}",
        ]
        self.update_header(header_text)
        self.body.original_widget = self.overed_w

        """
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
        """



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


if __name__ == "__main__":
    app = App()
    app.main()
