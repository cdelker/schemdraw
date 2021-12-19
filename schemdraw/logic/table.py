''' Markdown table.

    Put in the logic module since logic truth tables were the first
    use case for tables.
'''
from __future__ import annotations

import re

from ..segments import Segment, SegmentText
from ..elements import Element
from ..backends import svg


def parse_colfmt(colfmt: str) -> tuple[str, str]:
    ''' Parse the column formatter string, using LaTeX style table formatter
        (e.g. "cc|c")

        Args:
            colfmt: column format string

        Returns:
            justifications: string of all justification characters, length = n
            bars: string of all separator characters, |, ǁ, or ., length = n+1
    '''
    colfmt = re.sub(r'\|\|', 'ǁ', colfmt)
    while True:
        out = re.sub(r'([lcr])([lcr])', r'\1.\2', colfmt)
        if out == colfmt:
            break
        colfmt = out

    if not colfmt.startswith('|') or colfmt.startswith('ǁ'):
        colfmt = '.' + colfmt
    if not colfmt.endswith('|') or colfmt.endswith('ǁ'):
        colfmt += '.'

    bars = colfmt[::2]
    justs = colfmt[1::2]
    return justs, bars


class Table(Element):
    r''' Table Element for drawing rudimentary Markdown formatted tables, such
        as logic truth tables.

        Args:
            table: Table definition, as markdown string. Columns separated by \|.
                Separator rows contain --- or === between column separators.
            colfmt: Justification and vertical separators to draw for each column,
                similar to LaTeX tabular environment parameter. Justification
                characters include 'c', 'r', and 'l' for center, left, and right
                justification. Separator characters may be '\|' for a single
                vertical bar, or '\|\|' or 'ǁ' for a double vertical bar, or omitted
                for no bar. Example: 'cc|c'.
            fontsize: Point size of table font
            font: Name of table font

        Example Table:
            \| A \| B \| Y \|
            \|---\|---\|---\|
            \| 0 \| 0 \| 1 \|
            \| 0 \| 1 \| 0 \|
            \| 1 \| 0 \| 0 \|
            \| 1 \| 1 \| 0 \|
    '''
    def __init__(self, table:str, colfmt:str=None, fontsize:float=12, font:str='sans', **kwargs):
        super().__init__(**kwargs)
        self.table = table

        doublebarsep = .03
        rowpad = .3
        colpad = .4
        kwargs.setdefault('lw', 1)

        rows = self.table.strip().splitlines()
        rowfmt = ''
        for row in rows:
            if '---' in row:
                rowfmt += '|'
            elif '===' in row:
                rowfmt += 'ǁ'
            else:
                rowfmt += 'l'
        rowjusts, rowbars = parse_colfmt(rowfmt)

        if colfmt in [None, '']:
            colfmt = 'c' * len(rows[0].strip('| ').split('|'))
        coljusts, colbars = parse_colfmt(colfmt)  # type: ignore

        ncols = len(coljusts)
        nrows = len(rowjusts)
        rows = [r for r in rows if '---' not in r and '===' not in r]
        if len(rows[0].strip('| ').split('|')) != ncols:
            raise ValueError('Number of columns in table does not match number of columns in colfmt string.')

        colwidths = [0.] * ncols
        rowheights = [0.] * nrows
        for k, row in enumerate(rows):
            cells = [c.strip() for c in row.strip('| ').split('|')]
            for i, cell in enumerate(cells):
                txtw, txth, _ = svg.text_size(cell, font=font, size=fontsize)
                colwidths[i] = max(colwidths[i], txtw/72*2+colpad)
                rowheights[k] = max(rowheights[k], txth/72*2+rowpad)

        totheight = sum(rowheights)
        totwidth = sum(colwidths)

        # Frame
        for i, colbar in enumerate(colbars):
            colx = sum(colwidths[:i])
            if colbar == '|':
                self.segments.append(Segment([(colx, 0), (colx, -totheight)], **kwargs))
            elif colbar == 'ǁ':
                self.segments.append(Segment([(colx-doublebarsep, 0), (colx-doublebarsep, -totheight)], **kwargs))
                self.segments.append(Segment([(colx+doublebarsep, 0), (colx+doublebarsep, -totheight)], **kwargs))
        for i, rowbar in enumerate(rowbars):
            rowy = -sum(rowheights[:i])
            if rowbar == '|':
                self.segments.append(Segment([(0, rowy), (totwidth, rowy)], **kwargs))
            elif rowbar == 'ǁ':
                self.segments.append(Segment([(0, rowy-doublebarsep), (totwidth, rowy-doublebarsep)], **kwargs))
                self.segments.append(Segment([(0, rowy+doublebarsep), (totwidth, rowy+doublebarsep)], **kwargs))

        # Text
        for r, row in enumerate(rows):
            cells = [c.strip() for c in row.strip('| ').split('|')]
            for c, cell in enumerate(cells):
                cellx = sum(colwidths[:c])
                celly = -sum(rowheights[:r]) - rowheights[r]
                halign = {'c': 'center', 'l': 'left', 'r': 'right'}.get(coljusts[c])
                if halign == 'center':
                    cellx += colwidths[c]/2
                elif halign == 'right':
                    cellx += colwidths[c] - colpad/2
                else:
                    cellx += colpad/2
                self.segments.append(
                    SegmentText((cellx, celly), cell, font=font, fontsize=fontsize,
                                align=(halign, 'bottom')))    # type: ignore
