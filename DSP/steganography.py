from bit_manipulation import lsb_deinterleave_bytes, lsb_interleave_bytes
import wave
from time import time
import os

def encode(sound_path, file_path, output_path, num_lsb):
    if sound_path is None:
        raise ValueError("WavSteg hiding requires an input sound file path")
    if file_path is None:
        raise ValueError("WavSteg hiding requires a secret file path")
    if output_path is None:
        raise ValueError("WavSteg hiding requires an output sound file path")

    sound = wave.open(sound_path, "r")

    params = sound.getparams()
    num_channels = sound.getnchannels()
    sample_width = sound.getsampwidth()
    num_frames = sound.getnframes()
    num_samples = num_frames * num_channels

    max_bytes_to_hide = (num_samples * num_lsb) // 8
    file_size = os.stat(file_path).st_size

    print(f"Using {num_lsb} LSBs, we can hide {max_bytes_to_hide} bytes")

    start = time()
    sound_frames = sound.readframes(num_frames)
    with open(file_path, "rb") as file:
        data = file.read()
    print("Files read".ljust(30) + f" in {time() - start:.2f}s")

    if file_size > max_bytes_to_hide:
        status = 'fail'
        required_lsb = math.ceil(file_size * 8 / num_samples)
        raise ValueError(
            "Input file too large to hide, "
            f"requires {required_lsb} LSBs, using {num_lsb}"
        )
    else:
        status = 'success'

    if sample_width != 1 and sample_width != 2:
        # Python's wave module doesn't support higher sample widths
        raise ValueError("File has an unsupported bit-depth")

    start = time()
    sound_frames = lsb_interleave_bytes(
        sound_frames, data, num_lsb, byte_depth=sample_width
    )
    hide_time = f" in {time() - start:.2f}s"
    print(f"{file_size} bytes hidden".ljust(30) + hide_time)

    
    start = time()
    sound_steg = wave.open(output_path, "w")
    sound_steg.setparams(params)
    sound_steg.writeframes(sound_frames)
    sound_steg.close()
    print("Output wav written".ljust(30) + f" in {time() - start:.2f}s")

    return status, num_lsb, max_bytes_to_hide, file_size, hide_time
def decode(sound_path, output_path, num_lsb, bytes_to_recover):
    if sound_path is None:
        raise ValueError("WavSteg recovery requires an input sound file path")
    if output_path is None:
        raise ValueError("WavSteg recovery requires an output file path")
    if bytes_to_recover is None:
        raise ValueError("WavSteg recovery requires the number of bytes to recover")

    start = time()
    sound = wave.open(sound_path, "r")

    sample_width = sound.getsampwidth()
    num_frames = sound.getnframes()
    sound_frames = sound.readframes(num_frames)
    print("Files read".ljust(30) + f" in {time() - start:.2f}s")

    if sample_width != 1 and sample_width != 2:
        status = 'fail'
        # Python's wave module doesn't support higher sample widths
        raise ValueError("File has an unsupported bit-depth")
    else:
        status = 'success'

    start = time()
    data = lsb_deinterleave_bytes(
        sound_frames, 8 * bytes_to_recover, num_lsb, byte_depth=sample_width
    )
    rec_time = f" in {time() - start:.2f}s"
    print(
        f"Recovered {bytes_to_recover} bytes".ljust(30) + rec_time
    )

    start = time()
    output_file = open(output_path, "wb+")
    output_file.write(bytes(data))
    output_file.close()
    print("Written output file".ljust(30) + f" in {time() - start:.2f}s")	

    return status, bytes_to_recover, rec_time