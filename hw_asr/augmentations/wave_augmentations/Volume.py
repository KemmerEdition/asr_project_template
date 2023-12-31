from hw_asr.augmentations.base import AugmentationBase
import torchaudio
from torch import Tensor
import numpy as np


class Volume(AugmentationBase):
    def __init__(self, p, *args, **kwargs):
        assert 0 <= p <= 1
        self.p = p
        self.aug_vol = torchaudio.transforms.Vol(*args, **kwargs)

    def __call__(self, data: Tensor):
        p_ = np.random.binomial(1, self.p)
        x = data.unsqueeze(1)
        if p_:
            return self.aug_vol(x).squeeze(1)
        else:
            return data
