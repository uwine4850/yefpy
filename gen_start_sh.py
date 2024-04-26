import os
import cfg


def generate_start_sh(projects_path: list[str], gen_path: str, cgo_ldflags=cfg.CGO_LDFLAGS, cgo_cflags=cfg.CGO_CFLAGS):
    if not os.path.exists(gen_path):
        os.makedirs(gen_path)
    with open(os.path.join(gen_path, 'start.sh'), "w") as script:
        script.write(f'export CGO_LDFLAGS="{cgo_ldflags}"\n')
        script.write(f'export CGO_CFLAGS="{cgo_cflags}"\n')
        for project in projects_path:
            script.write(f'export PYTHONPATH={os.path.abspath(project)}:$PYTHONPATH\n')
