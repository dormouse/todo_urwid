import urwid


class TodoFrame(object):
    palette = [
        ('body', 'black', 'dark cyan', 'standout'),
        ('foot', 'light gray', 'black'),
        ('key', 'light cyan', 'black', 'underline'),
        ('title', 'yellow', 'black',),
        ('message', 'yellow', 'black',),
    ]

    footer_text = [
        ('title', "U Todo"), "    ",
        ('key', "UP"), ", ", ('key', "DOWN"), ", ",
        ('key', "PAGE UP"), " and ", ('key', "PAGE DOWN"),
        " move view  ",
        ('key', "H"), " helps",
        ('key', "Q"), " exits",
    ]

    def __init__(self):
        listbox_content = self.gen_view_contents()
        self.listbox = urwid.ListBox(urwid.SimpleFocusListWalker(listbox_content))
        self.body = urwid.AttrMap(urwid.Filler(self.listbox, valign="middle",
                                               height=('relative', 100),
                                               top=2, min_height=10), 'body')
        footer = urwid.AttrMap(urwid.Text(self.footer_text), 'foot')
        self.view = urwid.Frame(self.body, footer=footer)
        self.loop = urwid.MainLoop(self.view,
                                   self.palette,
                                   unhandled_input=self.handle_input)
        self.loop.run()

    def show_help(self):
        done = urwid.Button(u'Ok')
        urwid.connect_signal(done, 'click', self.dia_but_clicked)

        help_body = [urwid.Text('help'), urwid.Divider(),
                     urwid.Text('help content'), urwid.Divider(),
                     done]
        help_box = urwid.AttrMap(
            urwid.ListBox(urwid.SimpleFocusListWalker(help_body)),
            'message'
        )
        self.body.original_widget = urwid.Overlay(
            help_box,
            self.body.original_widget,
            align='center', width=('relative', 50),
            valign='middle', height=('relative', 50),
        )

    def item_chosen(self, w, index):
        pass

    def gen_view_contents(self):
        todo_items = [
            '+1st buy milk',
            '-2rd clean body',
            '-3rd go to school',
            '-测试一下很长很长的内容，这个内容真的很长。' * 3
        ]
        contents = [
            urwid.Columns(
                [
                    (5, urwid.Text('No.')),
                    (5, urwid.Text('Done')),
                    urwid.Text('Contents')
                ], 1
            ),
            urwid.Divider("="),
        ]
        for index, item in enumerate(todo_items):
            if item[0] == '+':
                is_done_txt = '[X]'
            else:
                is_done_txt = '[ ]'

            but_txt = '   '.join([str(index), is_done_txt, item[1:]])
            but = urwid.Button(but_txt)
            urwid.connect_signal(but, 'click', self.item_chosen, index)
            contents.append(urwid.AttrMap(but, None, focus_map='reversed'))

        return contents

    def dia_but_clicked(self, button):
        self.body.original_widget = self.listbox

    def handle_input(self, input_char):
        if input_char in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        if input_char in ('h', 'H'):
            self.show_help()


if __name__ == "__main__":
    TodoFrame()
