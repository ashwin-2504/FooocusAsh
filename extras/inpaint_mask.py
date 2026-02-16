import modules.config
import numpy as np
from rembg import remove, new_session

def generate_mask_from_image(image: np.ndarray, mask_model: str = 'u2net', extras=None,
                             sam_options=None) -> tuple[np.ndarray | None, int | None, int | None, int | None]:
    dino_detection_count = 0
    sam_detection_count = 0
    sam_detection_on_mask_count = 0

    if image is None:
        return None, dino_detection_count, sam_detection_count, sam_detection_on_mask_count

    if extras is None:
        extras = {}

    if 'image' in image:
        image = image['image']

    # We only support u2net/rembg now. SAM/GroundingDINO is removed.
    try:
        result = remove(
            image,
            session=new_session(mask_model, **extras),
            only_mask=True,
            **extras
        )
    except Exception as e:
        print(f"Error in rembg: {e}")
        return None, 0, 0, 0

    return result, dino_detection_count, sam_detection_count, sam_detection_on_mask_count
