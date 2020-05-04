import urwid


def main():
    palette = [
        ('body', 'black', 'dark cyan', 'standout'),
        ('foot', 'light gray', 'black'),
        ('key', 'light cyan', 'black', 'underline'),
        ('title', 'white', 'black',),
    ]

    footer_text = [
        ('title', "U Todo"), "    ",
        ('key', "UP"), ", ", ('key', "DOWN"), ", ",
        ('key', "PAGE UP"), " and ", ('key', "PAGE DOWN"),
        " move view  ",
        ('key', "Q"), " exits",
    ]
    listbox_content = gen_view_contents()

    def exit_on_q(input_char):
        if input_char in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
    footer = urwid.AttrMap(urwid.Text(footer_text), 'foot')
    view = urwid.Frame(urwid.AttrWrap(listbox, 'body'), footer=footer)
    loop = urwid.MainLoop(view, palette, unhandled_input=exit_on_q)
    loop.run()


def gen_view_contents():
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
                (8, urwid.Text('Done')),
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

        contents.append(
            urwid.Columns(
                [
                    (5, urwid.Text(str(index))),
                    (8, urwid.Text(is_done_txt)),
                    urwid.Text(item[1:])
                ], 1
            )
        )

    return contents


if __name__ == "__main__":
    main()
