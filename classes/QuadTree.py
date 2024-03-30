class QuadTreeNode:
    def __init__(self, x, y, width, height, max_entities, max_depth, depth=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_entities = max_entities
        self.max_depth = max_depth
        self.depth = depth
        self.entities = []
        self.children: list[QuadTreeNode] = []

    def draw(self, arcade):
        arcade.draw_rectangle_outline(
            center_x=self.x + self.width / 2,
            center_y=self.y + self.height / 2,
            width=self.width,
            height=self.height,
            color=arcade.color.RED,
            border_width=2,
        )
        for child in self.children:
            child.draw(arcade)

    def is_leaf(self):
        return len(self.children) == 0

    def subdivide(self):
        if self.depth >= self.max_depth:
            return

        child_width = self.width / 2
        child_height = self.height / 2

        self.children.append(
            QuadTreeNode(
                self.x,
                self.y,
                child_width,
                child_height,
                self.max_entities,
                self.max_depth,
                self.depth + 1,
            )
        )
        self.children.append(
            QuadTreeNode(
                self.x + child_width,
                self.y,
                child_width,
                child_height,
                self.max_entities,
                self.max_depth,
                self.depth + 1,
            )
        )
        self.children.append(
            QuadTreeNode(
                self.x,
                self.y + child_height,
                child_width,
                child_height,
                self.max_entities,
                self.max_depth,
                self.depth + 1,
            )
        )
        self.children.append(
            QuadTreeNode(
                self.x + child_width,
                self.y + child_height,
                child_width,
                child_height,
                self.max_entities,
                self.max_depth,
                self.depth + 1,
            )
        )

    def insert(self, entity):
        if not self.is_leaf():
            child = self.get_child(entity)
            if child:
                child.insert(entity)
                return

        self.entities.append(entity)

        if (
            len(self.entities) > self.max_entities
            and self.depth < self.max_depth
        ):
            self.subdivide()
            for e in self.entities:
                child = self.get_child(e)
                if child:
                    child.insert(e)
            self.entities = []

    def get_child(self, entity):
        for child in self.children:
            if child.contains(entity):
                return child
        return None

    def contains(self, entity):
        return (
            entity.left >= self.x
            and entity.right <= self.x + self.width
            and entity.bottom >= self.y
            and entity.top <= self.y + self.height
        )

    def retrieve(self, entity):
        if self.is_leaf():
            return self.entities

        child = self.get_child(entity)
        if child:
            return child.retrieve(entity)

        return self.entities

    def clear(self):
        self.entities = []
        self.children = []


class QuadTree:
    def __init__(self, width, height, max_entities=4, max_depth=6):
        self.root = QuadTreeNode(0, 0, width, height, max_entities, max_depth)

    def insert(self, entity):
        self.root.insert(entity)

    def retrieve(self, entity):
        return self.root.retrieve(entity)

    def clear(self):
        self.root.clear()
