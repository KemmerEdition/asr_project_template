import torch
from torch import Tensor
import librosa
import numpy as np
from hw_asr.augmentations.base import AugmentationBase
# based on the 3d seminar of DLA Course
# также добавляем параметр вероятности


class Noise(AugmentationBase):
    def __init__(self, p, noise_name, noise_level):
        filename = librosa.ex(noise_name)
        y, sr = librosa.load(filename)
        assert 0 <= p <= 1
        self.p = p
        self.y = torch.from_numpy(y).unsqueeze(0)
        self.noise_level = torch.Tensor([noise_level])
        self.audio_energy = torch.norm(self.y)

    def __call__(self, data: Tensor):
        aug_noise = np.random.binomial(1, self.p)
        if aug_noise:
            alpha = ((torch.norm(data)) / self.audio_energy) * torch.pow(10, -self.noise_level / 20)
            clipped_wav = data[..., :self.y.size(1)]
            clip_noise = self.y[:, :clipped_wav.size(1)]
            augmented_wav = clipped_wav + alpha * clip_noise
            result = torch.clamp(augmented_wav, -1, 1)
            return result
        else:
            return data
