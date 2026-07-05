import gradio as gr
from gradio.blocks import Block

all_components = []

# Guard Block init to track all components (used by dump_default_english_config)
if not hasattr(Block, 'original_init'):
    Block.original_init = Block.__init__

def blk_ini(self, *args, **kwargs):
    all_components.append(self)
    return Block.original_init(self, *args, **kwargs)

Block.__init__ = blk_ini


class ImageWrapper:
    """Wrapper to translate Gradio 3 Image arguments to standard Gradio 5 Image."""
    def __new__(cls, *args, **kwargs):
        # Translate source to sources
        if 'source' in kwargs:
            src = kwargs.pop('source')
            if src == 'upload':
                kwargs['sources'] = ['upload', 'clipboard']
            elif src == 'webcam':
                kwargs['sources'] = ['webcam']
            else:
                kwargs['sources'] = [src]
                
        # Clean up parameters not supported by Gradio 5 Image
        kwargs.pop('tool', None)
        kwargs.pop('brush_color', None)
        kwargs.pop('mask_opacity', None)
        kwargs.pop('invert_colors', None)
        kwargs.pop('mirror_webcam', None)
        kwargs.pop('brush_radius', None)
        kwargs.pop('show_share_button', None)
        kwargs.pop('streaming', None)
        
        return gr.Image(*args, **kwargs)

# Expose as Image to match modules.gradio_hijack.Image
Image = ImageWrapper
