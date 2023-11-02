from dataclasses import dataclass

from mermaid import text_to_snake_case


@dataclass
class NodeShape:
    start: str
    end: str


NODE_SHAPES: dict[str, NodeShape] = {
    'normal': NodeShape('[', ']'),
    'round-edge': NodeShape('(', ')'),
    'stadium-shape': NodeShape('([', '])'),
    'subroutine-shape': NodeShape('[[', ']]'),
    'cylindrical': NodeShape('[(', ')]'),
    'circle': NodeShape('((', '))'),
    'label-shape': NodeShape('>', ']'),
    'rhombus': NodeShape('{', '}'),
    'hexagon': NodeShape('{{', '}}'),
    'parallelogram': NodeShape('[/', '/]'),
    'parallelogram-alt': NodeShape('[\\', '\\]'),
    'trapezoid': NodeShape('[/', '\\]'),
    'trapezoid-alt': NodeShape('[\\', '/]'),
    'double-circle': NodeShape('(((', ')))'),
}

HREF_TYPES: dict[str, str] = {
    'blank': '_blank',
    'self': '_self',
    'parent': '_parent',
    'top': '_top'
}


class Node:
    def __init__(self,
                 id_: str,
                 content: str = '',
                 shape: str = 'normal',
                 sub_nodes: list['Node'] = None,
                 href: str = None,
                 href_type: str = 'blank') -> None:

        self.id_: str = text_to_snake_case(id_)
        self.content: str = content if content else id_
        self.shape: NodeShape = NODE_SHAPES[shape]
        self.href: str = href if href is not None else '#'
        self.href_type: str = HREF_TYPES[href_type]
        self.sub_nodes: list[
            'Node'] = sub_nodes if sub_nodes is not None else []

    def __str__(self) -> str:
        string: str = ''
        if len(self.sub_nodes):
            string = '\n'.join([
                f'subgraph {self.id_} ["{self.content}"]',
                '\n'.join([str(f'\t{node}') for node in self.sub_nodes]), 'end'
            ])
        else:
            string = ''.join([
                self.id_, self.shape.start, f'"{self.content}"', self.shape.end
            ])
            if self.href != '#':
                string = ''.join([
                    string, '\n',
                    f'click {self.id_} "{self.href}" {self.href_type}'
                ])
        return string
