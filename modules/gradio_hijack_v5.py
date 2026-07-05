import gradio as gr
import numpy as np
from PIL import Image as PILImage

all_components = []

# Guard Block init to track all components (used by dump_default_english_config)
if not hasattr(gr.Block, 'original_init'):
    gr.Block.original_init = gr.Block.__init__

def blk_ini(self, *args, **kwargs):
    all_components.append(self)
    return gr.Block.original_init(self, *args, **kwargs)

gr.Block.__init__ = blk_ini


class ImageWrapper:
    """Wrapper to translate Gradio 3 Image arguments to Gradio 5 Image or ImageEditor."""
    def __new__(cls, *args, **kwargs):
        is_editor = kwargs.get('tool') == 'sketch'
        
        # Translate source to sources
        if 'source' in kwargs:
            src = kwargs.pop('source')
            if src == 'upload':
                kwargs['sources'] = ['upload', 'clipboard']
            elif src == 'webcam':
                kwargs['sources'] = ['webcam']
            else:
                kwargs['sources'] = [src]
                
        # Clean up parameters not supported by Gradio 5 Image or ImageEditor
        kwargs.pop('tool', None)
        kwargs.pop('brush_color', None)
        kwargs.pop('mask_opacity', None)
        kwargs.pop('invert_colors', None)
        kwargs.pop('mirror_webcam', None)
        kwargs.pop('brush_radius', None)
        kwargs.pop('show_share_button', None)
        kwargs.pop('streaming', None)
        
        if is_editor:
            # gr.ImageEditor in Gradio 5
            return gr.ImageEditor(*args, **kwargs)
        else:
            # gr.Image in Gradio 5
            return gr.Image(*args, **kwargs)

# Expose as Image to match modules.gradio_hijack.Image
Image = ImageWrapper
