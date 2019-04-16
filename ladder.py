from tkinter import *
import numpy as np

args = sys.argv

print(args)

dataname_weight = '1b1w.txt'
dataname_node = '1b1n.txt'

def init_weight_data(dataname):
    f = open(dataname)
    lines = f.readlines()
    datalen = len(lines)
    f.close()
    data = np.zeros((datalen, datalen))
    for j in range (datalen):
        for i in range (datalen):
            sp = lines[i].split()
            data[i,j] = sp[j+1]
    return data

def init_node_data(dataname):
    f = open(dataname)
    lines = f.readlines()
    datalen = len(lines)
    f.close()
    data = np.zeros((datalen, 2))
    for j in range (2):
        for i in range (datalen):
            sp = lines[i].split()
            data[i,j] = sp[j+1]
    return data

weight_list = init_weight_data(dataname_weight)
node_list = init_node_data(dataname_node)

master = Tk()

count = 1

# Scale factor for viewing
scale = 4
margin_x = 16 * scale
margin_y = 16 * scale

# Ladder properties
ladder_aria_width = 128
ladder_aria_height = 96
leg_width = [16, 20, 28]

# base properties
base_margin = 7
ladder_margin = 8
ladder_width = 16

# Ladder dimensions
ladder_x = ladder_aria_width * scale
ladder_y = ladder_aria_height * scale
leg_16 = leg_width[0] * scale
leg_20 = leg_width[1] * scale
leg_28 = leg_width[2] * scale

# roadway dimensions in studs
roadway_x = (ladder_aria_width + ladder_margin * 2) * scale
roadway_y = (ladder_aria_height + ladder_margin * 2) * scale

# base dimensions in studs
base_x = (ladder_aria_width + (ladder_margin + base_margin) * 2) * scale
base_y = (ladder_aria_height + (ladder_margin + base_margin) * 2) * scale

# base-of-shelf dimensions in studs
shelfBase_x = ladder_x - (ladder_width + ladder_margin) * 2 * scale
shelfBase_y = ladder_y - (ladder_width + ladder_margin) * 2 * scale

# shelf dimensions in studs
shelf_x = 20 * scale
shelf_y = 10 * scale
unit_x = 3
unit_y = 2

w = Canvas(master, width=base_x + margin_x * 2, height=base_y + margin_y * 2)
w.pack()

# base coodinates upper left 0 and lower_right 1
base_x0, base_y0 = margin_x, margin_y
base_x1, base_y1 = base_x0 + base_x, base_y0 + base_y
# base in green
w.create_rectangle(base_x0, base_y0, base_x1, base_y1, outline="#323232", fill="#6ed76e")

# roadway coodinates upper left 0 and lower_right 1
roadway_x0, roadway_y0 = base_x0 + base_margin * scale, base_y0 + base_margin * scale
roadway_x1, roadway_y1 = base_x1 - base_margin * scale, base_y1 - base_margin * scale
# roadway in gray
w.create_rectangle(roadway_x0, roadway_y0, roadway_x1, roadway_y1, outline="#323232", fill="#B2B2B2")

# shelf base coodinates upper left 0 and lower_right 1
shelfBase_x0, shelfBase_y0 = (base_x - shelfBase_x)/2 + margin_x, (base_y - shelfBase_y)/2 + margin_y
shelfBase_x1, shelfBase_y1 = shelfBase_x0 + shelfBase_x, shelfBase_y0 + shelfBase_y
# shelf base in green
w.create_rectangle(shelfBase_x0, shelfBase_y0, shelfBase_x1, shelfBase_y1, outline="#323232", fill="#6ed76e")

# shelf 3x2 layout
total_shelf_x, total_shelf_y = shelf_x * 3, shelf_y * 2
shelf_x0, shelf_y0 = (base_x - total_shelf_x)/2 + margin_x, (base_y - total_shelf_y)/2 + margin_y
shelf_x1, shelf_y1 = shelf_x0 + shelf_x, shelf_y0 + shelf_y
# shelf in blue
num_of_x = 0
shelf_x00 = shelf_x0
shelf_x11 = shelf_x1
while(num_of_x < unit_x):
    num_of_y = 0
    shelf_y00 = shelf_y0
    shelf_y11 = shelf_y1
    while (num_of_y < unit_y):
        w.create_rectangle(shelf_x00, shelf_y00, shelf_x11, shelf_y11, outline="#323232", fill="#00ffff")
        shelf_y00 = shelf_y00 + shelf_y
        shelf_y11 = shelf_y11 + shelf_y
        num_of_y = num_of_y + 1
    shelf_x00 = shelf_x00 + shelf_x
    shelf_x11 = shelf_x11 + shelf_x
    num_of_x = num_of_x + 1

node_circle_radius = 8
display_offset_x = margin_x + (base_margin + ladder_margin) * scale
display_offset_y = margin_y + (base_margin + ladder_margin) * scale

node_list_d = []
for i in range(len(node_list)):
    node_list_d.append([node_list[i,0] * scale + display_offset_x, node_list[i,1] * scale + display_offset_y])

for j in range(len(weight_list)):
    for i in range(len(weight_list)):
        if weight_list[i,j] != 0:
            w.create_line(node_list_d[i], node_list_d[j], fill="yellow", width=3)
            if i < j:
                w.create_text((node_list_d[i][0] + node_list_d[j][0]) / 2,
                          (node_list_d[i][1] + node_list_d[j][1]) / 2 - node_circle_radius,
                          text="(%s,%s)" %(weight_list[i,j], weight_list[j,i]))
# nodes in yellow

for i in range(len(node_list_d)):
    w.create_oval(node_list_d[i][0] - node_circle_radius, node_list_d[i][1] - node_circle_radius, node_list_d[i][0] + node_circle_radius,node_list_d[i][1] + node_circle_radius, outline="#323232", fill="yellow")
    w.create_text(node_list_d[i][0], node_list_d[i][1], text=str(i+1))


# for debugging
#count = 1
def callback(event):
    print("(%s,%s)" %(event.x, event.y))

    #global count
    #print ("leg %s" %count)
    #w.create_line(node_list_d[count - 1], node_list_d[count], fill="blue", width=3)
    # w.create_text((node_list_d[count - 1][0] + node_list_d[count][0])/2 - node_circle_radius, (node_list_d[count - 1][1] + node_list_d[count][1])/2 - node_circle_radius, text="leg%s (16,16)" %count)
    # count = count + 1
w.bind("<Button-1>", callback)

mainloop()
