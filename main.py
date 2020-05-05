import urwid

class Todo_Frame(object):
    palette = [
        ('body', 'black', 'dark cyan', 'standout'),
        ('foot', 'light gray', 'black'),
        ('key', 'light cyan', 'black', 'underline'),
        ('title', 'yellow', 'black',),
    ]

    footer_text = [
        ('title', "U Todo"), "    ",
        ('key', "UP"), ", ", ('key', "DOWN"), ", ",
        ('key', "PAGE UP"), " and ", ('key', "PAGE DOWN"),
        " move view  ",
        ('key', "Q"), " exits",
    ]

    def __init__(self):
        listbox_content = self.gen_view_contents()
        self.listbox = urwid.ListBox(urwid.SimpleFocusListWalker(listbox_content))
        footer = urwid.AttrMap(urwid.Text(self.footer_text), 'foot')
        self.view = urwid.Frame(urwid.AttrWrap(self.listbox, 'body'), footer=footer)
        self.loop = urwid.MainLoop(self.view, self.palette, unhandled_input=exit_on_q)
        self.loop.run()


    def item_chosen(self, w, index):
        response = urwid.Text([u'You chose ', str(index), u'\n'])
        done = urwid.Button(u'Ok')
        urwid.connect_signal(done, 'click', self.dia_but_clicked)
        # main.original_widget = urwid.Filler(urwid.Pile([response,
        self.view.body = urwid.Filler(urwid.Pile([response,
            urwid.AttrMap(done, None, focus_map='reversed')]))

    def gen_view_contents(self):
        todo_items = [
            '+1st buy milk',
            '-2rd clean body',
            '-3rd go to school',
            '-测试一下很长很长的内容，这个内容真的很长。'*3
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

            but_txt = '   '.join([str(index) ,is_done_txt, item[1:]])
            but = urwid.Button(but_txt)
            urwid.connect_signal(but, 'click', self.item_chosen, index)
            contents.append(urwid.AttrMap(but, None, focus_map='reversed'))

        return contents

    def dia_but_clicked(self, button):
        self.view.body = self.listbox


def exit_program(button):
    raise urwid.ExitMainLoop()


def exit_on_q(input_char):
    if input_char in ('q', 'Q'):
        raise urwid.ExitMainLoop()




if __name__ == "__main__":
    Todo_Frame()

