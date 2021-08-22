from OpenGL.GL import *
from glfw.GLFW import *
import glm
import math

class Navigation:
    def __init__(self, glfw_window, camera_translate):
        self.glfw_window = glfw_window
        self.camera_translate = camera_translate
        self.drag_start = glm.vec2(0)
        self.drag_vec = glm.vec2(0)
        self.rotate_vec = glm.vec2(0)
        self.drag = False
        self.vp_size = glfwGetFramebufferSize(self.glfw_window)
        self.start_time_s = glfwGetTime()
        glfwSetWindowSizeCallback(self.glfw_window, self.window_size_callback)
        glfwSetMouseButtonCallback(self.glfw_window, self.mouse_button_callback)
        glfwSetCursorPosCallback(self.glfw_window, self.cursor_position_callback)
        
    @property
    def drag_vector(self):
        v = self.drag_vec + self.rotate_vec
        v.x, _ = math.modf(v.x)
        v.y = glm.clamp(v.y, -1, 1)
        return v

    @property
    def rotation_matrix(self):
        v = self.drag_vector
        return glm.rotate(glm.rotate(glm.mat4(1), v.y * -math.pi/2, glm.vec3(1, 0, 0)), v.x * math.pi*2, glm.vec3(0, 1, 0))

    @property
    def view_matrix(self):
        m1 = glm.translate(glm.mat4(1), glm.vec3(self.camera_translate) * glm.vec3(0, 0, 1))
        m2 = glm.translate(glm.mat4(1), glm.vec3(self.camera_translate) * glm.vec3(1, 1, 0))
        return m1 * self.rotation_matrix * m2

    @property
    def projection_matrix(self):
        return glm.perspective(glm.radians(45), self.vp_size[0]/self.vp_size[1], 0.01, 10.0)

    @property
    def delta_time_s(self):
        current_time_s = glfwGetTime()
        return current_time_s - self.start_time_s

    def start(self):
        self.start_time_s = glfwGetTime()

    def window_size_callback(self, window, width, height):
        self.vp_size = width, height
        glViewport(0, 0, *self.vp_size)

    def mouse_button_callback(self, window, button, action, mods):
        if button != GLFW_MOUSE_BUTTON_LEFT:
            return
        if action == GLFW_PRESS:
            self.drag = True
            xpos, ypos = glfwGetCursorPos(self.glfw_window)
            self.drag_start = glm.vec2(xpos, ypos)
        elif action == GLFW_RELEASE:
            self.drag = False
            self.rotate_vec = self.drag_vector
            self.drag_vec = glm.vec2(0)

    def cursor_position_callback(self, window, xpos, ypos):
        if self.drag:
            self.drag_vec = glm.vec2(xpos - self.drag_start.x, self.drag_start.y - ypos) / glm.vec2(self.vp_size[0], self.vp_size[1]/2)