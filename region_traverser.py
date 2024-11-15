from PIL import Image, ImageDraw

class RegionTraverser:
    def __init__(self, image):
        self.original_image = image
        self.current_image = image.copy()
        self.image_width, self.image_height = image.size
        self.x1, self.y1 = 0, 0
        self.x2, self.y2 = self.image_width, self.image_height
        self.highlighted_image = None
        self.cropped_image = None

        self.is_mobile = self.image_width < self.image_height

    def _convert_coordinate_relative_to_region(self, coord):
        x, y = coord
        region_width = self.x2 - self.x1
        region_height = self.y2 - self.y1

        scaled_x = self.x1 + (x / 999) * region_width
        scaled_y = self.y1 + (y / 999) * region_height

        return int(scaled_x), int(scaled_y)

    def consume_coordinate(self, x, y, new_width=None, new_height=None):
        x, y = self._convert_coordinate_relative_to_region((x, y))

        width = self.x2 - self.x1
        height = self.y2 - self.y1

        if self.is_mobile:
            if new_width is None: new_width = width / 1.2
            if new_height is None: new_height = height / 2
        else:
            if new_width is None: new_width = width / 2
            if new_height is None: new_height = height / 2

        new_x1 = x - new_width / 2
        new_y1 = y - new_height / 2
        new_x2 = x + new_width / 2
        new_y2 = y + new_height / 2

        if new_x1 < self.x1:
            new_x1 = self.x1
            new_x2 = new_x1 + new_width
        if new_x2 > self.x2:
            new_x2 = self.x2
            new_x1 = new_x2 - new_width

        if new_y1 < self.y1:
            new_y1 = self.y1
            new_y2 = new_y1 + new_height
        if new_y2 > self.y2:
            new_y2 = self.y2
            new_y1 = new_y2 - new_height

        new_x1 = max(self.x1, new_x1)
        new_x2 = min(self.x2, new_x2)
        new_y1 = max(self.y1, new_y1)
        new_y2 = min(self.y2, new_y2)

        self.x1, self.y1, self.x2, self.y2 = map(int, (new_x1, new_y1, new_x2, new_y2))

        self.highlighted_image = self.original_image.copy()
        draw = ImageDraw.Draw(self.highlighted_image)

        draw.rectangle([self.x1, self.y1, self.x2, self.y2], outline="red", width=2)

        mid_x = (self.x1 + self.x2) // 2
        mid_y = (self.y1 + self.y2) // 2

        draw.line([(mid_x, self.y1), (mid_x, self.y2)], fill="blue", width=1)  # Vertical line
        draw.line([(self.x1, mid_y), (self.x2, mid_y)], fill="blue", width=1)  # Horizontal line

        self.cropped_image = self.original_image.crop((self.x1, self.y1, self.x2, self.y2))

    def get_bounding_box(self):
        return self.x1, self.y1, self.x2, self.y2

    def get_highlighted_image(self):
        return self.highlighted_image

    def get_cropped_image(self):
        # bb = self.get_bounding_box()
        return self.cropped_image

    def reset_region(self):
        self.x1, self.y1 = 0, 0
        self.x2, self.y2 = self.image_width, self.image_height
        self.highlighted_image = None
        self.cropped_image = None