import os
import gradio as gr
import args_manager

from modules.localization import localization_js

modules_path = os.path.dirname(os.path.realpath(__file__))
script_path = os.path.dirname(modules_path)


def webpath(fn):
    # Resolve the absolute path of the resource
    abs_path = os.path.abspath(os.path.join(script_path, fn) if not os.path.isabs(fn) else fn)
    # Convert backslashes to forward slashes for URLs
    abs_path = abs_path.replace('\\', '/')
    # Cache busting query parameter using modification time
    try:
        mtime = int(os.path.getmtime(abs_path))
    except Exception:
        mtime = 0
    return f'/file={abs_path}?{mtime}'


def javascript_html():
    script_js_path = webpath("javascript/script.js")
    context_menus_js_path = webpath("javascript/contextMenus.js")
    localization_js_path = webpath("javascript/localization.js")
    zoom_js_path = webpath("javascript/zoom.js")
    edit_attention_js_path = webpath("javascript/edit-attention.js")
    viewer_js_path = webpath("javascript/viewer.js")
    image_viewer_js_path = webpath("javascript/imageviewer.js")
    samples_path = webpath("sdxl_styles/samples/fooocus_v2.jpg")

    head = f'<script type="text/javascript">{localization_js(args_manager.args.language)}</script>\n'
    head += f'<script type="text/javascript" src="{script_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{context_menus_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{localization_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{zoom_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{edit_attention_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{viewer_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{image_viewer_js_path}"></script>\n'
    head += f'<meta name="samples-path" content="{samples_path}">\n'

    if args_manager.args.theme:
        head += f'<script type="text/javascript">set_theme(\"{args_manager.args.theme}\");</script>\n'

    return head


def css_html():
    style_css_path = webpath("css/style.css")
    head = f'<link rel="stylesheet" property="stylesheet" href="{style_css_path}">'
    return head


def get_head_html():
    return javascript_html() + css_html()

