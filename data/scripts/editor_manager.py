from data.scripts.file_manager import write_json, read_json

class EditorManager:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
        self.shift_x = None
        self.shift_y = None
        self.editor_layers = ['background', 'platform', 'foreground']
        self.editor_map = {}
        self.export_data = {}
        self.current_layer = 0
        self.click = False
        self.erase_click = False
        self.level = 1
        self.set_layers()

    def set_layers(self):
        for layer in self.editor_layers:
            self.editor_map[layer] = {}

    def change_layer(self, number):
        self.current_layer += number
        if self.current_layer < 0:
            self.current_layer = len(self.editor_layers) - 1
        if self.current_layer > len(self.editor_layers) - 1:
            self.current_layer = 0

    def change_offset(self, shift):
        if self.shift_x == "right":
            self.offset_x -= shift
        if self.shift_x == "left":
            self.offset_x += shift
        if self.shift_y == "top":
            self.offset_y -= shift
        if self.shift_y == "bottom":
            self.offset_y += shift

    def show_layer(self, display, text):
        text.display_fonts(display, self.editor_layers[self.current_layer], [10, 8], 2)

    def add_tile(self, tile_data, pos):
        self.editor_map[self.editor_layers[self.current_layer]][tuple([pos[0] + self.offset_x,
                                                                       pos[1] + self.offset_y])] = [tile_data[0],
                                                                                                    tile_data[1]]

    def remove_tile(self, pos):
        if tuple([pos[0] + self.offset_x, pos[1] + self.offset_y]) in self.editor_map[self.editor_layers[
            self.current_layer]]:
            del self.editor_map[self.editor_layers[self.current_layer]][tuple([pos[0] + self.offset_x,
                                                                       pos[1] + self.offset_y])]

    def show_map(self, display):
        for layer in self.editor_map:
            layer_data = self.editor_map[layer]
            for tile in layer_data:
                display.blit(layer_data[tile][1], (tile[0] - self.offset_x, tile[1] - self.offset_y))

    def save_map(self, tileset_data):
        for layer in self.editor_map:
            layer_data = self.editor_map[layer]
            self.export_data[layer] = {}
            for tile in layer_data:
                tile_data = layer_data[tile]
                tileset = tileset_data[tile_data[0]]
                tile_index = tileset.index(tile_data[1])
                # Convert tuple keys to strings
                self.export_data[layer][f"{tile}"] = [tile_data[0], tile_index]

        write_json(f'maps/level_{self.level}.json', self.export_data, is_json=True)

    def load_map(self, tileset_data):
        map_data = read_json(f'maps/level_{self.level}.json', is_json=True)
        self.editor_map = {}

        for layer, layer_data in map_data.items():
            self.editor_map[layer] = {}
            for tile_key, tile_value in layer_data.items():
                tile = eval(tile_key)
                tileset = tileset_data[tile_value[0]]
                tile_image = tileset[tile_value[1]]
                self.editor_map[layer][tile] = [tile_value[0], tile_image]
