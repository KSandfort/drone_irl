import tkinter as tk
import numpy as np
from droneworld import DroneWorld

if __name__ == '__main__':
    """
    This main function needs to be executed to start a new drone world simulation including GUI
    """

    # Edit these variables to change the generation of the world:
    size = 500
    n_people = 5  # Number of people
    n_obstacles = 5  # Number of obstacles

    # Create new instance of the drone world
    dw = DroneWorld(size, n_people, n_obstacles)

    # Set up GUI
    root = tk.Tk()
    root.geometry('{}x{}'.format(size + 200, size + 200))
    canvas = tk.Canvas(root, bg='green', height=size, width=size)
    canvas.pack(side=tk.LEFT)

    # --- Set up elements ---
    p = dw.starting_pos

    # People
    for person in dw.people:
        canvas.create_oval(
            person[0] - dw.p_radius,
            person[1] - dw.p_radius,
            person[0] + dw.p_radius,
            person[1] + dw.p_radius,
            fill='purple'
        )

    # Obstacles
    for obst in dw.obst:
        canvas.create_rectangle(
            obst[0],
            obst[1],
            obst[2],
            obst[3],
            fill='grey'
        )

    # Sensors
    sensor_lines_people = []
    for i in range(dw.n_sensors):
        new_sensor = canvas.create_line(
            p[0],
            p[1],
            dw.people_sensors[i][0],
            dw.people_sensors[i][1],
            fill='purple',
            width=5
        )
        sensor_lines_people.append(new_sensor)
    sensor_lines_obst = []
    for i in range(dw.n_sensors):
        angle_offset = (i - (dw.n_sensors // 2)) * dw.sensor_spread
        new_sensor = canvas.create_line(
            p[0],
            p[1],
            dw.obst_sensors[i][0],
            dw.obst_sensors[i][1],
            fill='blue')
        sensor_lines_obst.append(new_sensor)

    # Drone
    dr = 10  # Drone radius
    drone_sphere = canvas.create_oval(
        p[0] - dr,
        p[1] - dr,
        p[0] + dr,
        p[1] + dr,
        fill='red')

    # --- Text Area (for state features) ---
    text_area = tk.Text(root, bg='white', height=16)
    text_area.pack(side=tk.RIGHT, padx=10, pady=10)

    def output_state():
        """
        # Prints the current simulation state onto the right text field as individual features
        """
        feature_count = 1
        for state_feature in dw.state_features:
            text_area.insert(tk.INSERT, 's_{}:\t {}\n'.format(feature_count, round(state_feature, 4)))
            feature_count += 1

    output_state()

    def keypress(event):
        """
        Moves the drone (red circle) on the field when a button is pressed.
        :param event:
        :return:
        """
        dw.update_drone_location(event.char)
        new_pos = dw.current_pos
        canvas.moveto(
            drone_sphere,
            new_pos[0] - dr,
            new_pos[1] - dr,)
        for i in range(dw.n_sensors):
            canvas.coords(
                sensor_lines_people[i],
                new_pos[0],
                new_pos[1],
                dw.people_sensors[i][0],
                dw.people_sensors[i][1]
            )
            canvas.coords(
                sensor_lines_obst[i],
                new_pos[0],
                new_pos[1],
                dw.obst_sensors[i][0],
                dw.obst_sensors[i][1]
            )
        text_area.delete('1.0', tk.END)
        output_state()

    root.bind("<Key>", keypress)

    root.mainloop()
