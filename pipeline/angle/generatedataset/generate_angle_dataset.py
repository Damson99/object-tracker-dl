import pandas as pd

width_percentage = list(range(1, 101))

angle = []

for wp in width_percentage:
    if wp < 50:
        angle.append(int((wp / 49) * 30 - 30))
    elif wp >= 50:
        angle.append(int(((wp - 50) / 50) * 30))

data = pd.DataFrame({
    'width_percentage': width_percentage,
    'angle': angle,
})

data.to_csv('width_angle_dataset.csv', index=False)
