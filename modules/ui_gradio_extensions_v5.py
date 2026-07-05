import os
import gradio as gr
import args_manager

from modules.localization import localization_js

modules_path = os.path.dirname(os.path.realpath(__file__))
script_path = os.path.dirname(modules_path)


def webpath(fn):
    if fn.startswith(script_path):
        web_path = os.path.relpath(fn, script_path).replace('\\', '/')
    else:
        web_path = os.path.abspath(fn)

    # In Gradio 5, we mount static files or reference relative paths.
    # We will use /file= prefix which is standard for local file serving.
    return f'file/{web_path}' if not web_path.startswith('file/') else web_path


def javascript_html():
    script_js_path = "/file=javascript/script.js"
    context_menus_js_path = "/file=javascript/contextMenus.js"
    localization_js_path = "/file=javascript/localization.js"
    zoom_js_path = "/file=javascript/zoom.js"
    edit_attention_js_path = "/file=javascript/edit-attention.js"
    viewer_js_path = "/file=javascript/viewer.js"
    image_viewer_js_path = "/file=javascript/imageviewer.js"
    samples_path = "/file=sdxl_styles/samples/fooocus_v2.jpg"

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
    style_css_path = "/file=css/style.css"
    head = f'<link rel="stylesheet" property="stylesheet" href="{style_css_path}">'
    return head


def get_head_html():
    return javascript_html() + css_html()


def reload_javascript():
    # Deprecated in Gradio 5 as we pass head directly to gr.Blocks(head=...)
    pass
