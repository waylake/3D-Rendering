import numpy as np


class RotatingCube:
    def __init__(
        self,
        cube_width,
        screen_width,
        screen_height,
        background_ascii,
        distance_from_camera,
        horizontal_offset,
        k1,
        increment_speed,
    ):
        self.cube_width = cube_width
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background_ascii = ord(background_ascii)
        self.distance_from_camera = distance_from_camera
        self.horizontal_offset = horizontal_offset
        self.k1 = k1
        self.increment_speed = increment_speed
        self.center_x = screen_width // 2 + horizontal_offset
        self.center_y = screen_height // 2
        self.rotation_angle_x = 0
        self.rotation_angle_y = 0
        self.rotation_angle_z = 0
        self.z_buffer = np.zeros(screen_width * screen_height)
        self.buffer = np.full(
            screen_width * screen_height, self.background_ascii)

    def calculate_rotated_coordinates(self, i, j, k):
        rotation_matrix_x = np.array(
            [
                [1, 0, 0],
                [0, np.cos(self.rotation_angle_x), -
                 np.sin(self.rotation_angle_x)],
                [0, np.sin(self.rotation_angle_x),
                 np.cos(self.rotation_angle_x)],
            ]
        )

        rotation_matrix_y = np.array(
            [
                [np.cos(self.rotation_angle_y), 0,
                 np.sin(self.rotation_angle_y)],
                [0, 1, 0],
                [-np.sin(self.rotation_angle_y), 0,
                 np.cos(self.rotation_angle_y)],
            ]
        )

        rotation_matrix_z = np.array(
            [
                [np.cos(self.rotation_angle_z), -
                 np.sin(self.rotation_angle_z), 0],
                [np.sin(self.rotation_angle_z), np.cos(
                    self.rotation_angle_z), 0],
                [0, 0, 1],
            ]
        )

        rotated_vector = np.dot(
            rotation_matrix_x,
            np.dot(rotation_matrix_y, np.dot(
                rotation_matrix_z, np.array([i, j, k]))),
        )
        return rotated_vector

    def calculate_for_surface(self, cube_x, cube_y, cube_z, ch):
        x, y, z = self.calculate_rotated_coordinates(cube_x, cube_y, cube_z)
        z += self.distance_from_camera

        ooz = 1 / z

        xp = int(self.center_x + self.k1 * ooz * x * 2)
        yp = int(self.center_y + self.k1 * ooz * y)

        idx = xp + yp * self.screen_width
        if 0 <= idx < self.screen_width * self.screen_height:
            if ooz > self.z_buffer[idx]:
                self.z_buffer[idx] = ooz
                self.buffer[idx] = ch

    def draw_cube(self):
        for cube_x in np.arange(
            -self.cube_width, self.cube_width, self.increment_speed
        ):
            for cube_y in np.arange(
                -self.cube_width, self.cube_width, self.increment_speed
            ):
                self.calculate_for_surface(
                    cube_x, cube_y, -self.cube_width, ord("@"))
                self.calculate_for_surface(
                    self.cube_width, cube_y, cube_x, ord("$"))
                self.calculate_for_surface(-self.cube_width,
                                           cube_y, -cube_x, ord("~"))
                self.calculate_for_surface(-cube_x,
                                           cube_y, self.cube_width, ord("#"))
                self.calculate_for_surface(
                    cube_x, -self.cube_width, -cube_y, ord(";"))
                self.calculate_for_surface(
                    cube_x, self.cube_width, cube_y, ord("+"))

    def update_rotation_angles(self):
        self.rotation_angle_x += 0.05
        self.rotation_angle_y += 0.05
        self.rotation_angle_z += 0.01

    def clear_screen(self):
        print("\033[H", end="")

    def render(self):
        self.buffer.fill(self.background_ascii)
        self.z_buffer.fill(0)

        self.draw_cube()
        self.update_rotation_angles()

        self.clear_screen()
        print(
            "".join(
                chr(self.buffer[k])
                if k % self.screen_width
                else "\n" + chr(self.buffer[k])
                for k in range(self.screen_width * self.screen_height)
            )
        )


try:
    cube = RotatingCube(10, 40, 20, ".", 100, 0, 40, 1)
    while True:
        cube.render()
except KeyboardInterrupt:
    pass  # Exiting the loop on keyboard interrupt (Ctrl+C)

