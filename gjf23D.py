import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
import logging
DEBUG=True

def decide_position1(init_pos, distance):
    init_pos[0] += distance
    return init_pos


def decide_position2(init_pos, p_angle_pos, distance, angle):
    p_angle_vec = (distance)/np.linalg.norm(p_angle_pos -
                                            init_pos) * (p_angle_pos-init_pos)
    rad_angle = math.radians(angle)
    rotation_matrix = np.array([[np.cos(rad_angle), np.sin(rad_angle), 0],
                                [-np.sin(rad_angle), np.cos(rad_angle), 0],
                                [0, 0, 1]])
    new_vec = np.dot(rotation_matrix, p_angle_vec)
    result_pos = init_pos+new_vec
    return result_pos


def decide_position3(init_pos, p_angle_pos, d_angle_pos, distance, p_angle, d_angle):
    standard_p_angle_vec = (p_angle_pos-init_pos) / \
        np.linalg.norm(p_angle_pos-init_pos)
    standard_d_angle_vec = (d_angle_pos-init_pos) / \
        np.linalg.norm(d_angle_pos-init_pos)
    to_a = np.copy(standard_p_angle_vec)
    to_b = (standard_d_angle_vec-np.dot(to_a, standard_d_angle_vec)*to_a)
    to_b /= np.linalg.norm(to_b)
    to_c = np.cross(to_a, to_b)
    to_c /= np.linalg.norm(to_c)
    p_radian = math.radians(p_angle)
    d_radian = math.radians(d_angle)
    O = np.array([0.0, 0.0, 0.0])
    bias = np.array([0.0, 0.0, 0.0])

    from_a = np.array([1, 0, 0])
    from_b = np.array([0, 1, 0])
    from_c = np.array([0, 0, 1])
    tmp_a = np.array([distance, 0, 0])
    from_ans = np.array([np.cos(p_radian), np.sin(
        p_radian)*np.cos(d_radian), np.sin(p_radian)*np.sin(d_radian)])
    to_vec = np.array([to_a, to_b, to_c]).T
    from_vec = np.array([from_a, from_b, from_c]).T
    from_vec_inv = np.linalg.inv(from_vec)
    U = np.dot(to_vec, from_vec_inv)
    result_vec = np.dot(U, from_ans)
    result = result_vec+init_pos
    return result

def gjf23D(file):
    l = None
    with open(file) as f:
        l = f.readlines()
    O = np.array([0.00, 0.00, 0.00])


    class Atom:
        def __init__(self, atom, pos) -> None:
            self.atom = atom
            self.pos = np.copy(pos)


    atom_infos = []
    atom_bonds = []
    for i in range(5, len(l)):
        cmd_list = l[i].split()
        if not cmd_list:
            continue
        print(cmd_list)
        if i == 5:
            if len(cmd_list) != 1:
                logging.error('Syntax error')
            atom_c = cmd_list[0][0]
            atom_info = Atom(atom_c, O)
            atom_infos.append(atom_info)
        elif i == 6:
            if len(cmd_list) != 3:
                logging.error('Syntax error')
            atom_c = cmd_list[0][0]
            atom_pos = decide_position1(O, float(cmd_list[2]))
            atom_info = Atom(atom_c, atom_pos)
            atom_infos.append(atom_info)
            atom_bonds.append([0, 1])
        elif i == 7:
            if len(cmd_list) != 5:
                logging.error('Syntax error')
            atom_c = cmd_list[0][0]
            init_atom_num = int(cmd_list[1])-1
            p_atom_num = int(cmd_list[3])-1
            init_atom_pos = atom_infos[init_atom_num].pos
            p_atom_pos = atom_infos[p_atom_num].pos
            atom_pos = decide_position2(
                init_atom_pos, p_atom_pos, float(cmd_list[2]), float(cmd_list[4]))
            atom_info = Atom(atom_c, atom_pos)
            atom_infos.append(atom_info)
            atom_bonds.append([init_atom_num, i-5])
        else:
            if len(cmd_list) != 7:
                logging.error('Syntax error')
            atom_c = cmd_list[0][0]
            init_atom_num = int(cmd_list[1])-1
            p_atom_num = int(cmd_list[3])-1
            d_atom_num = int(cmd_list[5])-1
            init_atom_pos = atom_infos[init_atom_num].pos
            p_atom_pos = atom_infos[p_atom_num].pos
            d_atom_pos = atom_infos[d_atom_num].pos
            atom_pos = decide_position3(
                init_atom_pos, p_atom_pos, d_atom_pos, float(cmd_list[2]), float(cmd_list[4]), float(cmd_list[6]))
            atom_info = Atom(atom_c, atom_pos)
            atom_infos.append(atom_info)
            atom_bonds.append([init_atom_num, i-5])
    for i in atom_infos:
        i.pos = np.round(i.pos, decimals=10)
    np.set_printoptions(suppress=True)
    if DEBUG:
        for i in atom_infos:
            for k, v in i.__dict__.items():
                print(k, ":", v, end=' , ')
            print()
        print(atom_bonds)

    # Figureを追加
    fig = plt.figure(figsize=(8, 8), facecolor="gray")

    # 3DAxesを追加
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor("gray")
    # Axesのタイトルを設定
    ax.set_title("", size=20)

    # 軸ラベルを設定
    ax.set_xlabel("x", size=14, color="r")
    ax.set_ylabel("y", size=14, color="r")
    ax.set_zlabel("z", size=14, color="r")


    x_list = []
    y_list = []
    z_list = []
    color_list = []
    index = 1
    for i in atom_infos:
        color = 'green'
        if i.atom == 'C':
            color = 'black'
        if i.atom == 'O':
            color = 'red'
        if i.atom == 'H':
            color = 'white'
        if i.atom=='N':
            color='blue'
        if i.atom=='S':
            color='yellow'
        if i.atom=='P':
            color='purple'
        x_list.append(i.pos[0])
        y_list.append(i.pos[1])
        z_list.append(i.pos[2])
        ax.text(i.pos[0], i.pos[1], i.pos[2], i.atom+str(index))
        color_list.append(color)
        print(i.pos)
        index += 1
    ax.scatter(x_list, y_list, z_list, c=color_list, s=100)
    for i in atom_bonds:
        ax.plot([atom_infos[i[0]].pos[0], atom_infos[i[1]].pos[0]],
                [atom_infos[i[0]].pos[1], atom_infos[i[1]].pos[1]],
                [atom_infos[i[0]].pos[2], atom_infos[i[1]].pos[2]],
                color='black')

    # 曲線を描画
    ax.view_init(elev=60, azim=30)
    ax.tick_params(bottom=False,
                   left=False,
                   right=False,
                   top=False)
    plt.grid()
    plt.show()
