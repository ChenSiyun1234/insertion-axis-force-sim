"""Render saved joint-position replays."""
import argparse
from pathlib import Path
import imageio.v2 as imageio
import mujoco as mj
import numpy as np
from PIL import Image, ImageDraw
from .scene import build


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("out_dir", type=Path)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    name = "can_arm_1ms"
    trace = np.genfromtxt(args.run_dir/f"{name}.csv", delimiter=",", skip_header=1)
    with np.load(args.run_dir/f"{name}_qpos.npz", allow_pickle=False) as replay:
        times, positions = replay["time"].copy(), replay["qpos"].copy()
    model, _ = build("arm", jam=True)
    model.vis.headlight.ambient[:] = [.45, .45, .45]
    model.vis.headlight.diffuse[:] = [.8, .8, .8]
    data = mj.MjData(model)
    camera = mj.MjvCamera()
    camera.lookat[:] = [.15, 0, .48]
    camera.distance, camera.azimuth, camera.elevation = .95, -140, -35
    frames = []
    with mj.Renderer(model, height=360, width=640) as renderer:
        for t in np.linspace(.1, times[-1], 90):
            i = min(np.searchsorted(times, t), len(times)-1)
            data.qpos[:] = positions[i]
            mj.mj_forward(model, data)
            renderer.update_scene(data, camera=camera)
            picture = Image.fromarray(renderer.render().copy())
            draw = ImageDraw.Draw(picture)
            row = trace[min(np.searchsorted(trace[:, 0], t), len(trace)-1)]
            draw.rectangle((0, 0, 640, 44), fill=(17, 25, 35))
            draw.text((12, 7), "Generic linear insertion | force limit and backoff", fill="white")
            draw.text((12, 24), f"t = {t:.2f} s   force = {row[3]:.2f} N   carriage = {row[1]:.2f} mm", fill="white")
            frames.append(np.asarray(picture))
    imageio.mimsave(args.out_dir/"insertion.gif", frames, duration=70, loop=0)
    trip_time = trace[np.flatnonzero(trace[:, 5] == 5)[0], 0]
    trip_frame = int(np.argmin(np.abs(np.linspace(.1, times[-1], 90)-trip_time)))
    Image.fromarray(frames[trip_frame]).save(args.out_dir/"fixture.png")
    print(f"Rendered {len(frames)} replay frames and one screenshot.")


if __name__ == "__main__":
    main()
